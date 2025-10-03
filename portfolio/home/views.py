from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView
from .models import Profile
from educations.models import Skill,Tool,Education
from projects.models import Project,Resume
from contact.models import ContactInfo
from contact.forms import ContactForm


from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from .tokens import account_activation_token


from django.core.mail import send_mail
from .forms import ContactForm


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from google import genai 
from google.genai.errors import APIError as GeminiAPIError 


# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["profile"] = Profile.objects.prefetch_related("socials").first()
        ctx["skills"] = Skill.objects.all()
        ctx["tools"] = Tool.objects.all()
        ctx["education_list"] = Education.objects.all()
        ctx["projects"] = Project.objects.all()
        ctx["resume"] = Resume.objects.last()  
        ctx["contact_info"] = ContactInfo.objects.first()
        ctx["form"] = ContactForm()
        return ctx
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        success = False
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()  # Reset form after submission

        # Re-render the same template with updated context
        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form
        ctx["success"] = success
        return self.render_to_response(ctx)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        success = False
        if form.is_valid():
            contact = form.save()
            success = True
            form = ContactForm()  # reset form

            #send email here
            subject = "Thanks for contacting me"
            message = (
                f"Hi {contact.name},\n\n"
                "Thanks for reaching out! I received your message and will reply soon.\n\n"
                "Your message:\n"
                f"{contact.message}\n\n"
                "— Best regards"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email, settings.DEFAULT_FROM_EMAIL], 
                fail_silently=False,
            )

        ctx = self.get_context_data(**kwargs)
        ctx["form"] = form
        ctx["success"] = success
        return self.render_to_response(ctx)



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False 
            user.save()

            # Send activation email
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': settings.DOMAIN,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(
                subject="Activate your account",
                body=message,
                to=[user.email]
            )
            email.content_subtype = "html"
            email.send()

            messages.success(request, "Account created! Please check your email to activate.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})



def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and account_activation_token.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.is_staff = True 
            user.save()
            messages.success(request, "Your account has been activated. You can now login.")
        else:
            messages.info(request, "Your account is already activated. Please login.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or expired.")
        return redirect('register')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# for chatbot integration
client = genai.Client(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def chatbot_reply(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            if not user_message:
                return JsonResponse({'reply': 'Please enter a message.'}, status=400)

            system_instruction = (
                "You are Rito, a helpful and friendly assistant for Ritesh Chandra's portfolio website. "
                "You must answer questions about Ritesh's skills (Python, Django, JavaScript, APIs) and general knowledge questions."
            )
            
        
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[user_message],
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
            
            bot_response = response.text
            
            return JsonResponse({'reply': bot_response})
            
        except GeminiAPIError as e:
            print(f"Gemini API Error: {e}")
            user_facing_message = (
                "🤖 AI Service Error: I'm sorry, Rito's AI service is temporarily unavailable. "
                "The error suggests a **quota or configuration issue** with the backend."
            )
            return JsonResponse({'reply': user_facing_message}, status=503) 
            
        except Exception as e:
            print(f"Internal Error: {e}")
            return JsonResponse({'reply': 'An internal server error occurred.'}, status=500)
    
    return JsonResponse({'reply': 'Error: Method not allowed.'}, status=405)