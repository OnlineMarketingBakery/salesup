(function () {
  var grid = document.getElementById('cases-grid');
  if (!grid) return;
  var buttons = document.querySelectorAll('.filter-knop');
  var empty = document.getElementById('filter-leeg');
  var status = document.getElementById('filter-teller');
  function apply(filter) {
    var n = 0;
    grid.querySelectorAll('.case-kaart').forEach(function (card) {
      var diensten = (card.getAttribute('data-diensten') || '').split(/\s+/);
      var show = filter === 'all' || diensten.indexOf(filter) !== -1;
      card.hidden = !show;
      if (show) n += 1;
    });
    if (status) status.textContent = n + (n === 1 ? ' case' : ' cases');
    if (empty) empty.hidden = n !== 0;
  }
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      btn.setAttribute('aria-pressed', 'true');
      apply(btn.getAttribute('data-filter') || 'all');
    });
  });
  apply('all');
})();
