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

            # ✅ send email here
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
                [contact.email, settings.DEFAULT_FROM_EMAIL],  # send to user + you
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
            user.is_active = False  # deactivate until email verification
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
            user.is_staff = True  # give staff access automatically
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


# ✅ Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# views.py
import openai
from django.conf import settings
from django.http import JsonResponse
import json

# Set OpenAI API key
openai.api_key = settings.OPENAI_API_KEY

def chatbot_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        msg = data.get("message", "")

        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful chatbot."},
                    {"role": "user", "content": msg}
                ]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "Invalid request."}, status=400)


