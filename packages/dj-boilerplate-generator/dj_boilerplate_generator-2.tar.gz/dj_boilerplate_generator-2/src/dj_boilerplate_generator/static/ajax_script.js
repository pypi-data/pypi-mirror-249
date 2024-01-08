document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('userInfoForm').addEventListener('submit', function (event) {
        event.preventDefault();
        getUserInfo();
    });

    function getUserInfo() {
        const name = document.getElementById('nameInput').value;
        const birthDate = document.getElementById('birthdateInput').value;

        console.log('Name:', name);
        console.log('bd:', birthDate);

        const csrfToken = getCSRFToken(); // Set CSRF token in headers

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.setRequestHeader('X-CSRFToken', csrfToken);

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    const messagesDiv = document.getElementById('messages');
                    messagesDiv.innerHTML = "";
                    const response = JSON.parse(xhr.responseText);
                    messagesDiv.innerHTML += `<p>${response.time_greeting}, ${response.name}!</p>`;
                    messagesDiv.innerHTML += `<p>Your age is ${response.age}.</p>`;
                    messagesDiv.innerHTML += `<p>The current time is ${response.current_time}.</p>`;
                } else {
                    console.error('Error:', xhr.statusText);
                }
            }
        };

        const formData = `name=${name}&birth_date=${birthDate}`;
        xhr.send(formData);
    }

    // Function to get the CSRF token from the cookie
    function getCSRFToken() {
        const cookieString = document.cookie || '';  // Default to an empty string if document.cookie is undefined
        const cookieArray = cookieString.split('; ');
    
        for (const cookie of cookieArray) {
            const [name, value] = cookie.split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
    
        console.error('CSRF token not found in cookies');
        return null;  // Or handle the absence of the CSRF token according to your needs
    }
    
});
