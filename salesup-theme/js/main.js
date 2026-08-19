(function () {
  var btn = document.getElementById('hamburger');
  var menu = document.getElementById('navlinks');
  if (btn && menu) {
    btn.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Menu sluiten' : 'Menu openen');
      document.body.classList.toggle('nav-open', open);
      if (!open) {
        menu.querySelectorAll('.nav-item.open').forEach(function (item) {
          item.classList.remove('open');
          var top = item.querySelector('.nav-top');
          if (top) top.setAttribute('aria-expanded', 'false');
        });
      }
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        if (a.classList.contains('nav-top')) return;
        menu.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
        btn.setAttribute('aria-label', 'Menu openen');
        document.body.classList.remove('nav-open');
        menu.querySelectorAll('.nav-item.open').forEach(function (item) {
          item.classList.remove('open');
          var top = item.querySelector('.nav-top');
          if (top) top.setAttribute('aria-expanded', 'false');
        });
      });
    });
  }
  var mobileNav = window.matchMedia('(max-width: 820px)');
  function closeMobileNav() {
    if (!menu || !btn) return;
    menu.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-label', 'Menu openen');
    document.body.classList.remove('nav-open');
    menu.querySelectorAll('.nav-item.open').forEach(function (item) {
      item.classList.remove('open');
      var top = item.querySelector('.nav-top');
      if (top) top.setAttribute('aria-expanded', 'false');
    });
  }
  if (mobileNav.addEventListener) {
    mobileNav.addEventListener('change', function () {
      if (!mobileNav.matches) closeMobileNav();
    });
  }
  document.querySelectorAll('.nav-top[aria-haspopup]').forEach(function (top) {
    top.addEventListener('click', function (event) {
      if (!mobileNav.matches) return;
      event.preventDefault();
      var item = top.closest('.nav-item');
      var willOpen = !item.classList.contains('open');
      document.querySelectorAll('.nav-item.open').forEach(function (other) {
        if (other === item) return;
        other.classList.remove('open');
        var otherTop = other.querySelector('.nav-top');
        if (otherTop) otherTop.setAttribute('aria-expanded', 'false');
      });
      item.classList.toggle('open', willOpen);
      top.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    });
  });
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    document.querySelectorAll('.nav-item.open').forEach(function (item) {
      item.classList.remove('open');
      var top = item.querySelector('.nav-top');
      if (top) top.setAttribute('aria-expanded', 'false');
    });
    if (menu && btn) {
      menu.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'Menu openen');
      document.body.classList.remove('nav-open');
    }
  });
  var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  function apply() {
    document.documentElement.classList.toggle('reduced-motion', mq.matches);
  }
  apply();
  if (mq.addEventListener) mq.addEventListener('change', apply);

  var track = document.getElementById('testiTrack');
  if (track) {
    function step() {
      var c = track.querySelector('.testi-card');
      return c ? c.getBoundingClientRect().width + 22 : 340;
    }
    document.querySelectorAll('.testi-nav').forEach(function (b) {
      b.addEventListener('click', function () {
        track.scrollBy({ left: (b.classList.contains('next') ? 1 : -1) * step(), behavior: 'smooth' });
      });
    });
  }
})();
