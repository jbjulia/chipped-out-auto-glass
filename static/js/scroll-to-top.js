window.addEventListener('scroll', function () {
    /**
     * Handles scroll events to toggle the visibility of a "Scroll to Top" button.
     */

        // Get the 'scroll-to-top' button element
    const scrollBtn = document.getElementById('scroll-to-top');

    // Show the button if the scroll position is greater than 50 pixels
    if (window.scrollY > 50) {
        scrollBtn.classList.add('show');
    } else {
        // Hide the button otherwise
        scrollBtn.classList.remove('show');
    }
});
