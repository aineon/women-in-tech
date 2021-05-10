function navSlide() {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav-links");
    const navLinks = document.querySelectorAll(".nav-links li");

    burger.addEventListener("click", () => {
        //Toggle
        nav.classList.toggle("nav-active");

        //Animated menu 
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = "";
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
            }
        });
        //Burger
        burger.classList.toggle("toggle");
    });

}

navSlide();


// Hide flash messages after 2secs
setTimeout(()=> {
    flash_message = document.getElementsByClassName("flash");
    for (let i = 0; i < flash_message.length; i++) {
        flash_message[i].style.display="none";
    }
}, 2000);

