function togglePassword() {
    var passwordField = document.getElementById("password");
    var toggleIcon = document.getElementById("toggle-password");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleIcon.className = "fa fa-eye-slash";
    } else {
        passwordField.type = "password";
        toggleIcon.className = "fa fa-eye";
    }
}

function confirmDelete() {
            if (confirm("Are you sure you want to delete your account?\nThis action cannot be undone.")) {
                window.location.href = "/perform-delete-account";
            }
}