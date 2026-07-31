window.addEventListener("load", function () {

    const loader = document.getElementById("preloader");

    if (loader) {

        loader.style.opacity = "0";

        setTimeout(function () {

            loader.style.display = "none";

        }, 500);

    }

});