document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const menu = document.getElementById("menuToggle");

    if (!sidebar || !menu) return;

    menu.addEventListener("click", function () {

        if (window.innerWidth <= 768) {

            sidebar.classList.toggle("show");

        } else {

            sidebar.classList.toggle("closed");

        }

    });

});