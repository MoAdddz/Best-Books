document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    const tests = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    }
    for (const [key, passed] of Object.entries(tests)) {
        const element = document.getElementById(key);
        element.style.color = passed ? 'green' : 'red';
    }
});

function updateMatchStatus() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const matchElement = document.getElementById('match');
    if (password === confirmPassword) {
        matchElement.style.color =" green";
    } else {
        matchElement.style.color = "red";
    }
}

document.getElementById("confirm_password").addEventListener("input", updateMatchStatus);