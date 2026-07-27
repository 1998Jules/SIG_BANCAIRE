
document.addEventListener("DOMContentLoaded", function () {

    // =========================================
    // AFFICHER / MASQUER LE MOT DE PASSE
    // =========================================

    const passwordInput =
        document.getElementById("password");

    const togglePassword =
        document.getElementById("togglePassword");


    if (togglePassword && passwordInput) {

        togglePassword.addEventListener(
            "click",
            function () {

                if (
                    passwordInput.type === "password"
                ) {

                    passwordInput.type = "text";

                    togglePassword.textContent = "🙈";

                    togglePassword.setAttribute(
                        "aria-label",
                        "Masquer le mot de passe"
                    );

                } else {

                    passwordInput.type = "password";

                    togglePassword.textContent = "👁";

                    togglePassword.setAttribute(
                        "aria-label",
                        "Afficher le mot de passe"
                    );

                }

            }
        );

    }


    // =========================================
    // GESTION DU FORMULAIRE
    // =========================================

    const loginForm =
        document.getElementById("loginForm");

    const loginButton =
        document.getElementById("loginButton");

    const buttonText =
        document.getElementById("buttonText");

    const loader =
        document.getElementById("loader");


    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            function () {

                // Désactiver le bouton
                loginButton.disabled = true;

                // Afficher le chargement
                buttonText.style.display = "none";

                loader.style.display = "inline-block";

            }
        );

    }


    // =========================================
    // SAUVEGARDER LE NOM UTILISATEUR
    // =========================================

    const usernameInput =
        document.getElementById("username");

    const rememberMe =
        document.getElementById("rememberMe");


    // Restaurer le nom d'utilisateur
    const savedUsername =
        localStorage.getItem(
            "hypotheque_username"
        );


    if (
        savedUsername &&
        usernameInput
    ) {

        usernameInput.value =
            savedUsername;

        if (rememberMe) {
            rememberMe.checked = true;
        }

    }


    // Sauvegarder le nom utilisateur
    if (loginForm) {

        loginForm.addEventListener(
            "submit",
            function () {

                if (
                    rememberMe &&
                    rememberMe.checked
                ) {

                    localStorage.setItem(
                        "hypotheque_username",
                        usernameInput.value
                    );

                } else {

                    localStorage.removeItem(
                        "hypotheque_username"
                    );

                }

            }
        );

    }

})