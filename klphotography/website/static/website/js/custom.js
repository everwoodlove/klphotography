var hoverElements = document.querySelectorAll('.hover');

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
}