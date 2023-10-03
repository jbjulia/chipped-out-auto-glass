document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        const flashMessagesContainer = document.querySelector('.flash-messages');
        if (flashMessagesContainer) {
            flashMessagesContainer.style.display = 'none';
        }
    }, 5000); // The entire banner will be hidden after 5 seconds
});
