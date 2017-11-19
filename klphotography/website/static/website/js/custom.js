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

var expandableImages = document.querySelectorAll('.expandable');

for (var i = 0, len = expandableImages.length; i < len; i++) {
    var image = expandableImages[i];

    image.addEventListener('click', function() {
        if (this.classList.contains('expandable')) {
            this.classList.remove('expandable');
            this.classList.add('fullscreen');
            this.parent.classList.add('dimmed-background');
        }
        else if (this.classList.contains('fullscreen')) {
            this.classList.remove('fullscreen');
            this.classList.add('expandable');
            this.parent.classList.remove('dimmed-background');
        }
    });
}