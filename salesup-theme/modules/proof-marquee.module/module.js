(function () {
  function fill(scroller) {
    var track = scroller.querySelector('.marquee-track');
    if (!track || track.dataset.filled === 'true') return;
    var originals = Array.prototype.slice.call(track.children);
    if (!originals.length) return;
    var i = 0;
    while (track.scrollWidth < scroller.clientWidth * 2 && i < 8) {
      originals.forEach(function (node) { track.appendChild(node.cloneNode(true)); });
      i++;
    }
    track.dataset.filled = 'true';
  }
  function init() {
    document.querySelectorAll('.proof .marquee').forEach(fill);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
