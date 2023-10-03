/**
 * Adds 'scrolled-over' class to '.service-cards' elements on scroll.
 * The function is triggered each time the user scrolls.
 * It is intended to run only on mobile view or single-column layout.
 * When a '.service-cards' element has been scrolled over, it adds the 'scrolled-over' class to it.
 */
window.addEventListener('scroll', function () {
    // Only run this for mobile view or single-column layout
    if (window.innerWidth <= 768) {
        const cards = document.querySelectorAll('.service-cards');
        const windowBottom = window.scrollY + window.innerHeight;

        cards.forEach(function (card) {
            const cardBottom = card.offsetTop + card.offsetHeight;

            if (windowBottom > cardBottom) {
                card.classList.add('scrolled-over');
            } else {
                card.classList.remove('scrolled-over');
            }
        });
    }
});
