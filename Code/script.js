window.addEventListener('scroll', function() {
    var introSection = document.querySelector('.intro-section');
    var introContent = document.querySelector('.intro-content');
    var introTextItems = document.querySelectorAll('.rolling-text ul li');
    var aboutSection = document.querySelector('.about-section');
    var resourcesSection = document.querySelector('.resources-section');
    var introSectionHeight = introSection.offsetHeight;
    var scrollPosition = window.scrollY;

    // Fade out intro section
    introSection.style.opacity = 1 - (scrollPosition / introSectionHeight);

    // Activate rolling text items
    introTextItems.forEach(function(item, index) {
        if (item.getBoundingClientRect().top < introSectionHeight / 2) {
            item.classList.add('active');
        }
    });

    // Fade in about section
    if (aboutSection.getBoundingClientRect().top < window.innerHeight / 2) {
        aboutSection.style.opacity = 1;
    }

    // Fade in resources section
    if (resourcesSection.getBoundingClientRect().top < window.innerHeight / 2) {
        resourcesSection.style.opacity = 1;
    }
});
