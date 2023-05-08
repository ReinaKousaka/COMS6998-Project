try {
    var apigClient = apigClientFactory.newClient();
} catch (err) {}

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

    try {
        let params = {
            'email': username
        };
        let body = {};
        let additionalParams = {};
    
        let response = await apigClient.userGet(params, body, additionalParams);
        console.log(response);

        if (response.data == password) {
            user = username;
            sessionStorage.setItem('user', username);
            window.location = 'index.html';
        } else {
            alert('Invalid username or password');
        }
    } catch (err) {
        alert('Warning: failed to fetch user!');
        console.log(`failed to fetch user: ${err}`);
    }
};

const handleRegister = async () => {
    try {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        
        
        let params = {};
        let body = {
            'email': username,
            'password': password
        };
        let additionalParams = {};
    
        try {
            let response = await apigClient.userPost(params, body, additionalParams);
            alert('User added successfully!');
            console.log(`User added successfully: ${response}`);
        } catch (err) {
            alert('Warning: failed to add user!');
            console.log(`failed to add user: ${err}`);
        }
    } catch (err) {
        console.log(`failed to register: ${err}`);
    }
};

const handleLogoff = async() => {
    console.log(`log off called`)
    sessionStorage.clear();
    location.reload();
};
