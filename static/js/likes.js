function prepareLink(link) {
    link.addEventListener('click', function(e) {
        e.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.open('GET', link.href);
        xhr.send();

        var countSpan = link.getElementsByClassName('count')[0];
        countSpan.textContent = parseInt(countSpan.textContent) + 1;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var likes = document.getElementsByClassName('like-link');

    for (var i = 0; i < likes.length; i++) {
        prepareLink(likes[i]);
    }
});
