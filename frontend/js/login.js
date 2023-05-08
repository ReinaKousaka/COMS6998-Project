
var user = sessionStorage.getItem('user');

console.log(`user is ${user}`)
try {
    if (user) {
        document.getElementById('login-button').setAttribute("hidden", true);
        document.getElementById('logoff-button').removeAttribute("hidden");
        // document.getElementById('login-indicator').innerText = user;
    } else {
        document.getElementById('login-button').removeAttribute("hidden");
        document.getElementById('logoff-button').setAttribute("hidden", true);
        // document.getElementById('login-indicator').innerText = 'Please Login';
    }
} catch {}



const handleLogin = async () => {
    console.log(`handlelogin called`);

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // search by username
    if (username === 'yinsongheng@gmail.com' && password === '12345678') {
        user = username;
        sessionStorage.setItem('user', username);
        window.location = 'index.html';
     } else {
       alert('Invalid username or password');
     }
};

const handleLogoff = async() => {
    console.log(`log off called`)
    sessionStorage.clear();
    location.reload();
};
