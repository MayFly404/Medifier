// check if login works on login.html
document.getElementById('loginForm').addEventListener('submit', function(event) {
	event.preventDefault();
	var formData = new FormData(this);
	fetch('/login', {
		method: 'POST',
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			window.location.href = '/dashboard'; // Redirect to dashboard upon successful login
		} else {
			alert(data.message); // Display error message in a popup
		}
	})
	.catch(error => console.error('Error:', error));
});
