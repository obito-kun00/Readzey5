document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".hero");
    hero.style.opacity = 0;
    hero.style.transform = "translateY(50px)";
    setTimeout(() => {
      hero.style.transition = "all 1s ease";
      hero.style.opacity = 1;
      hero.style.transform = "translateY(0)";
    }, 300);
  });

  document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.getElementById("menu-icon");
    const navLinks = document.getElementById("nav-links");

    menuIcon.addEventListener("click", function () {
        navLinks.style.display = navLinks.style.display === "flex" ? "none" : "flex";
    });
});

