  // Footer year
    document.getElementById('year').textContent = new Date().getFullYear();

    // Contact form demo: validate & store locally
    (function(){
      const form = document.getElementById('contactForm');
      const success = document.getElementById('formSuccess');
      form?.addEventListener('submit', function(e){
        e.preventDefault();
        if (!form.checkValidity()){ form.classList.add('was-validated'); return; }
        const data = Object.fromEntries(new FormData(form).entries());
        const stored = JSON.parse(localStorage.getItem('contactMessages') || '[]');
        stored.push({ ...data, at: new Date().toISOString() });
        localStorage.setItem('contactMessages', JSON.stringify(stored));
        form.reset(); form.classList.remove('was-validated');
        success.classList.remove('d-none');
        setTimeout(()=> success.classList.add('d-none'), 3500);
      });
    })();

    // Simple reveal-on-scroll for fade-in elements
    (function(){
      const els = document.querySelectorAll('.fade-in');
      const io = new IntersectionObserver((entries)=>{
        entries.forEach(ent => { if (ent.isIntersecting) ent.target.style.animationPlayState = 'running'; });
      }, { threshold: .12 });
      els.forEach(el => io.observe(el));
    })();

    /* -----------------------------
       Rule-based client-side Chatbot
       -----------------------------
       - Auto-greets once per session
       - Keyword routing: hello, skills, projects, resume, contact, name, thanks
       - Stores visitor name in sessionStorage
    */
    (function(){
      const botName = 'Rito';
      const el = {
        toggle: document.getElementById('chatbotToggle'),
        box: document.getElementById('chatbot'),
        close: document.getElementById('chatbotClose'),
        log: document.getElementById('chatLog'),
        form: document.getElementById('chatForm'),
        input: document.getElementById('chatMessage')
      };

      const state = { username: sessionStorage.getItem('cb_username') || null };

      function showBox(){ el.box.style.display = 'flex'; el.input.focus(); }
      function hideBox(){ el.box.style.display = 'none'; }

      el.toggle.addEventListener('click', ()=> { getComputedStyle(el.box).display === 'none' ? showBox() : hideBox(); });
      el.close.addEventListener('click', hideBox);

      function addMsg(text, who='bot'){
        const d = document.createElement('div'); d.className = 'msg ' + (who==='bot' ? 'bot' : 'user');
        d.innerHTML = text;
        el.log.appendChild(d);
        el.log.scrollTop = el.log.scrollHeight;
      }
      function botSay(t){ addMsg(t, 'bot'); }
      function userSay(t){ addMsg(t, 'user'); }

      // greet once per tab session
      if (!sessionStorage.getItem('cb_greeted')){
        setTimeout(()=>{
          showBox();
          botSay(`<strong>Hi${state.username ? ' ' + state.username : ''}!</strong> I'm ${botName}. Try: <span class="small text-muted">skills • projects • resume • contact</span>`);
          sessionStorage.setItem('cb_greeted', '1');
        }, 1100);
      }

      // simple handlers
      const handlers = {
        help(){ botSay('Try asking about <em>skills</em>, <em>projects</em>, <em>resume</em>, or <em>contact</em>.'); },
        hello(){ botSay(`Hello${state.username ? ' ' + state.username : ''}! How can I help?`); },
        name(msg){
          const m = msg.match(/my name is (.+)/i) || msg.match(/i am (.+)/i) || msg.match(/i'm (.+)/i);
          if (m && m[1]) {
            state.username = m[1].split(/[,.!?]/)[0].trim();
            sessionStorage.setItem('cb_username', state.username);
            botSay(`Nice to meet you, <strong>${state.username}</strong>!`);
          } else botSay(`I'm ${botName}. What's your name? e.g. say: <em>my name is Rahul</em>`);
        },
        skills(){ botSay('I work with <strong>Python, Django, HTML/CSS, Bootstrap, JavaScript</strong>. See <a href="#skills">Skills</a>.'); },
        projects(){ botSay('Check <a href="#projects">Projects</a>. Need details about Django auth or REST APIs?'); },
        resume(){ botSay('Download my resume: <a href="assets/resume.pdf" download>Download</a> or preview at <a href="#resume">Resume</a>.'); },
        contact(){ botSay('Please use the <a href="#contact">contact</a> form — I will respond soon.'); },
        thanks(){ botSay(`You\'re welcome${state.username ? ', ' + state.username : ''}!`); },
        unknown(){ botSay('Sorry, I did not understand. Try: <em>skills</em>, <em>projects</em>, <em>resume</em>, or say <em>help</em>.'); }
      };

      function route(msg){
        const m = msg.toLowerCase();
        if (/\b(help|options|menu)\b/.test(m)) return handlers.help();
        if (/\b(hi|hello|hey)\b/.test(m)) return handlers.hello();
        if (/\bname\b/.test(m) || /my name is|i am|i'm/i.test(msg)) return handlers.name(msg);
        if (/\bskill|skills\b/.test(m)) return handlers.skills();
        if (/\bproject|projects\b/.test(m)) return handlers.projects();
        if (/\bresume|cv\b/.test(m)) return handlers.resume();
        if (/\bcontact|email|reach\b/.test(m)) return handlers.contact();
        if (/\bthank(s)?\b/.test(m)) return handlers.thanks();
        return handlers.unknown();
      }

      el.form.addEventListener('submit', function(e){
        e.preventDefault();
        const txt = el.input.value.trim();
        if (!txt) return;
        userSay(txt);
        el.input.value = '';
        setTimeout(()=> route(txt), 350);
      });
    })();




    // for skills section animation on refresh

window.addEventListener("load", function () {
let bars = document.querySelectorAll(".skill-bar");
bars.forEach(bar => {
    let target = bar.getAttribute("data-skill");
    let count = 0;
    let fill = setInterval(() => {
    if (count >= target) {
        clearInterval(fill);
    } else {
        count++;
        bar.style.width = count + "%";
        bar.textContent = count + "%";
    }
    }, 20); // adjust speed here
});
});



// tools and techlogies section 


function animateTools() {
  const tools = document.querySelectorAll(".tool");
  tools.forEach(tool => {
    const rect = tool.getBoundingClientRect();
    if(rect.top < window.innerHeight - 50) {
      const delay = tool.getAttribute("data-delay") || 0;
      setTimeout(() => {
        tool.classList.add("show");
      }, delay * 1000);
    }
  });
}

// Trigger on scroll and on load
window.addEventListener("scroll", animateTools);
window.addEventListener("load", animateTools);



// about me section

function animateAbout() {
  const elements = document.querySelectorAll('.fade-left, .fade-right');
  elements.forEach(el => {
    const rect = el.getBoundingClientRect();
    if(rect.top < window.innerHeight - 50) {
      el.classList.add('show');
    }
  });
}

window.addEventListener('scroll', animateAbout);
window.addEventListener('load', animateAbout);



