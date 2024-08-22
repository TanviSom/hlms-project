function setActionForm(action) {
    let form = document.getElementById("auth-form");
    if (action === 'Register') {
        form.action = "/signup";
        form.method = "post";
        form.submit();
    }
}