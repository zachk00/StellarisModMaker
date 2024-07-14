document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-20px)';
            setTimeout(function() {
                flash.remove();
            }, 500); // Matches the transition duration for fade out
        }, 3000); // Time in milliseconds before the message starts to fade out
    });
});
