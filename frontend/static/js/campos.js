document.querySelectorAll('.stars').forEach(function(el) {
    var links = el.querySelectorAll('a');
    el.addEventListener('mouseover', function(e) {
        var target = e.target.closest('a');
        if (!target) return;
        var idx = Array.prototype.indexOf.call(links, target);
        links.forEach(function(a, i) {
            if (i <= idx) {
                a.classList.add('active');
            } else {
                a.classList.remove('active');
            }
        });
    });
    el.addEventListener('mouseleave', function() {
        links.forEach(function(a) { a.classList.remove('active'); });
    });
});