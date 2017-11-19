/*var hoverElements = document.querySelectorAll('.hover');

for (var i = 0, len = hoverElements.length; i < len; i++) {
    var hoverElement = hoverElements[i];

    hoverElement.addEventListener('mouseenter', function() {
        image = this.querySelector('img');
        text = this.querySelector('.photo-font');

        image.classList.add('fade-photo');
        text.classList.add('show-text');
    });

    hoverElement.addEventListener('mouseleave', function() {
        image = this.querySelector('img');
        text = this.querySelector('.photo-font');

        image.classList.remove('fade-photo');
        text.classList.remove('show-text');
    });
}*/

var lightboxes = document.querySelectorAll('.lightbox');

for (var i = 0, len = lightboxes.length; i < len; i++) {
    var lightbox = lightboxes[i];

    var trigger = lightbox.querySelector('.lightbox-trigger');
    if (trigger) {
        trigger.addEventListener('click', function() {
            var trigger = this;
            var lightbox = trigger.parentElement;

            if (lightbox.classList.contains('active')) {
                lightbox.classList.add('inactive');
                lightbox.classList.remove('active');
                trigger.classList.add('non-fullscreen');
                trigger.classList.remove('fullscreen');
                lightbox.classList.remove('flex-content');
            }
            else if (lightbox.classList.contains('inactive')) {
                lightbox.classList.remove('inactive');
                lightbox.classList.add('active');
                trigger.classList.remove('non-fullscreen');
                trigger.classList.add('fullscreen');
                lightbox.classList.add('flex-content');
            }
        });
    }
}