document.addEventListener("DOMContentLoaded", function () {
	// listen for auth status changes
	auth.onAuthStateChanged(user => {
		if (user) {
			setupUI(user);
			console.log("user2", user)

		} else {
			console.log("user logged out");
			setupUI();
		}
	});

	// register
	const registerForm = document.querySelector('#register-form');
	registerForm.addEventListener('submit', (e) => {
		e.preventDefault();
		// get user info
		const email = registerForm['input-email'].value;
		const password = registerForm['input-password'].value;
		const confirmPassword = registerForm['input-confirm-password'].value;
		console.log('email: ', email)
		console.log('password: ', password)
		console.log('confirmPassword: ', confirmPassword)

		// Kiểm tra xác nhận mật khẩu
		if (password !== confirmPassword) {
			document.getElementById("error-message").innerHTML = "Mật khẩu xác nhận không khớp.";
			return;
		}

		// Tạo tài khoản người dùng mới
		auth.createUserWithEmailAndPassword(email, password)
			.then((cred) => {
				// Đóng form đăng ký & reset form
				registerForm.reset();
				window.location.href = 'index.html';
				console.log("Đăng ký thành công!");
			})
			.catch((error) => {
				const errorCode = error.code;
				const errorMessage = error.message;
				document.getElementById("error-message").innerHTML = errorMessage;
				console.log(errorMessage);
			});
	});

});  