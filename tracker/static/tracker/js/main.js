window.onload = function() {
    let loginBtn = document.querySelector("#login-btn");
    loginBtn.addEventListener("click", function (e) {
        let formAction = e.target.form.action;
        let email = document.querySelector("#email").value;
        let password = document.querySelector("#password").value;
        let remember = document.querySelector("#remember").checked;
        const headers = {
            "X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]").value,
            "Content-Type": "application/json"
        };
        let data = {
            email: email,
            password: password,
            remember: remember
        };
        axios.post(formAction, data, {headers: headers}).then((response) => {
            location.reload();
        }, (error) => {
            if (error.response) {
                if (error.response.data.message === "Login failed") {
                    let errorMessage = document.querySelector("#login-failed");
                    errorMessage.classList.remove("hidden")
                }

            }
        });
        e.preventDefault();
        return false;
    });

    let registerBtn = document.querySelector("#reg-btn");
    registerBtn.addEventListener("click", function(e) {
        let formAction = e.target.form.action;
        let email = document.querySelector("#reg-email").value;
        let username = document.querySelector("#reg-username").value;
        let password1 = document.querySelector("#reg-password1").value;
        let password2 = document.querySelector("#reg-password2").value;

        const headers = {
            "X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]").value,
            "Content-Type": "application/json"
        };
        let data = {
            email: email,
            username: username,
            password1: password1,
            password2: password2
        };
        //make this portion a function and use it for login and register events?
        axios.post(formAction, data, {headers: headers}).then((response) => {
            if (response.data === "registration-success") {
                window.location = "/"
            }
        }, (error) => {
            if (error.response) {
                if (error.response.data.message === "Registration failed") {
                    let errorMessage = document.querySelector("#reg-failed");
                    errorMessage.classList.remove("hidden")
                }

            }
        });
        e.preventDefault();
        return false;
    });


    let showsTable = document.querySelector("#shows_table");
    if (showsTable) {
        showsTable.addEventListener("click", function(e){
            let value = e.target.value;
            let formAction = e.target.form.action;
            const headers = {
                "X-CSRFToken": document.querySelector("input[name=csrfmiddlewaretoken]").value,
                "Content-Type": "application/json"
            };
            let data = {
                alter_show_list: value
            };
            axios.post(formAction, data, {headers: headers});

            if (value === "add") {
                e.target.classList.remove("btn-success");
                e.target.classList.add("btn-danger");
                e.target.value = "remove";
                e.target.innerHTML = "Remove";
            } else if (value === "remove") {
                e.target.classList.remove("btn-danger");
                e.target.classList.add("btn-success");
                e.target.value = "add";
                e.target.innerHTML = "Add";
            }
            e.preventDefault();
            return false;
        });
    }
};
