    const loginTab = document.getElementById("loginTab");
    const registerTab = document.getElementById("registerTab");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");

    loginTab.addEventListener("click", () => {
      loginForm.classList.remove("hidden");
      registerForm.classList.add("hidden");
      loginTab.classList.add("border-indigo-600");
      registerTab.classList.remove("border-indigo-600");
    });

    registerTab.addEventListener("click", () => {
      registerForm.classList.remove("hidden");
      loginForm.classList.add("hidden");
      registerTab.classList.add("border-indigo-600");
      loginTab.classList.remove("border-indigo-600");
    });

    // Dummy form submission with validation
    registerForm.addEventListener("submit", e => {
      e.preventDefault();
      if (password.value !== confirmPassword.value) {
        alert("Passwords do not match!");
        return;
      }
      alert("Registration successful! (Connect to backend here)");
    });

    loginForm.addEventListener("submit", e => {
      e.preventDefault();
      alert("Login successful! (Connect to backend here)");
    });
