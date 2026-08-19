(function () {
  var API_DEFAULT = 'https://salesup.recruitee.com/api/offers/';

  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function employmentLabel(code) {
    var map = {
      full_time: 'Voltijds',
      part_time: 'Deeltijds',
      fulltime_permanent: 'Voltijds (vast)',
      contract: 'Contract',
      temporary: 'Tijdelijk',
      internship: 'Stage',
      volunteer: 'Vrijwillig'
    };
    return map[code] || prettifyCode(code) || '';
  }

  function categoryLabel(code) {
    var map = {
      customer_service: 'Customer service',
      sales: 'Sales',
      marketing: 'Marketing'
    };
    return map[code] || prettifyCode(code) || '';
  }

  function prettifyCode(code) {
    if (!code) return '';
    return String(code)
      .replace(/_/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function slugFromLocation() {
    var params = new URLSearchParams(window.location.search);
    if (params.get('slug')) return params.get('slug');
    var parts = window.location.pathname.replace(/\/+$/, '').split('/');
    var last = parts[parts.length - 1];
    if (last && last !== 'vacature') return last;
    return '';
  }

  function cardHtml(offer, detailBase) {
    var loc = offer.city || offer.location || '';
    var dept = (offer.department && (offer.department.name || offer.department)) || '';
    var href = detailBase + '?slug=' + encodeURIComponent(offer.slug);
    var apply = offer.careers_apply_url || '#';
    return (
      '<article class="vac-job">' +
        (dept ? '<span class="vac-role-tag">' + escapeHtml(dept) + '</span>' : '') +
        '<h3>' + escapeHtml(offer.title || '') + '</h3>' +
        (loc ? '<span class="vac-loc">' + escapeHtml(loc) + '</span>' : '') +
        '<ul class="vac-meta">' +
          (offer.employment_type_code ? '<li>' + escapeHtml(employmentLabel(offer.employment_type_code)) + '</li>' : '') +
          (offer.category_code ? '<li>' + escapeHtml(categoryLabel(offer.category_code)) + '</li>' : '') +
        '</ul>' +
        '<a class="btn" href="' + href + '">Bekijk vacature <span class="arrow" aria-hidden="true">&rarr;</span></a>' +
        '<a class="vacd-recruitee" href="' + apply + '" target="_blank" rel="noopener">Solliciteer extern ↗</a>' +
      '</article>'
    );
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }

  function deptName(offer) {
    if (!offer.department) return '';
    return typeof offer.department === 'string' ? offer.department : (offer.department.name || '');
  }

  function loadList(section) {
    var api = section.getAttribute('data-api') || API_DEFAULT;
    var dept = (section.getAttribute('data-department') || '').toLowerCase();
    var detailBase = section.getAttribute('data-detail-base') || '/werken-bij/vacature';
    var grid = qs('[data-recruitee-grid]', section) || qs('.vac-job-grid', section);
    if (!grid) return;
    fetch(api, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var offers = (data.offers || data || []).filter(function (o) {
          if (!dept) return true;
          return deptName(o).toLowerCase().indexOf(dept) !== -1;
        });
        if (!offers.length) {
          grid.innerHTML = '<p class="vac-note" role="status">Geen open vacatures in deze afdeling. Solliciteer gerust spontaan.</p>';
          return;
        }
        grid.innerHTML = offers.map(function (o) { return cardHtml(o, detailBase); }).join('');
      })
      .catch(function () {
        grid.innerHTML = '<p class="vac-note" role="status">Vacatures konden niet geladen worden. Bekijk ze op Recruitee.</p>';
      });
  }

  function loadDetail() {
    var hero = qs('[data-recruitee-hero]');
    var body = qs('[data-recruitee-body]');
    if (!hero && !body) return;
    var slug = slugFromLocation();
    if (!slug) return;
    var api = 'https://salesup.recruitee.com/api/offers/' + encodeURIComponent(slug);
    fetch(api, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var offer = data.offer || data;
        if (!offer) return;
        var titleEl = qs('[data-vac-title]');
        if (titleEl) titleEl.textContent = offer.title || '';
        var chips = qs('[data-vac-chips]');
        if (chips) {
          var items = [offer.city, employmentLabel(offer.employment_type_code), deptName(offer)].filter(Boolean);
          chips.innerHTML = items.map(function (t) { return '<li><span class="chip">' + escapeHtml(t) + '</span></li>'; }).join('');
        }
        qsa('[data-vac-apply]').forEach(function (a) {
          if (offer.careers_apply_url) a.setAttribute('href', offer.careers_apply_url);
        });
        qsa('[data-vac-careers]').forEach(function (a) {
          if (offer.careers_url) a.setAttribute('href', offer.careers_url);
        });
        var meta = qs('[data-vac-meta]');
        if (meta) {
          meta.innerHTML =
            row('Locatie', offer.city) +
            row('Contract', employmentLabel(offer.employment_type_code)) +
            row('Afdeling', deptName(offer)) +
            row('Categorie', categoryLabel(offer.category_code));
        }
        if (body) {
          var html = '';
          if (offer.description) html += offer.description;
          if (offer.requirements) html += '<h2>Wat we zoeken</h2>' + offer.requirements;
          if (html) body.innerHTML = html;
        }
        injectJobPosting(offer);
      })
      .catch(function () { /* fallback HTML blijft staan */ });
  }

  function row(k, v) {
    if (!v) return '';
    return '<li><span><span class="k">' + escapeHtml(k) + '</span><span class="v">' + escapeHtml(v) + '</span></span></li>';
  }

  function injectJobPosting(offer) {
    var old = document.getElementById('recruitee-jobposting');
    if (old) old.remove();
    var s = document.createElement('script');
    s.type = 'application/ld+json';
    s.id = 'recruitee-jobposting';
    var emp = (offer.employment_type_code || 'OTHER').toUpperCase();
    s.text = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'JobPosting',
      title: offer.title,
      description: (offer.description || '').replace(/<[^>]+>/g, ' '),
      datePosted: offer.created_at,
      employmentType: emp,
      hiringOrganization: { '@type': 'Organization', name: 'salesUp', sameAs: 'https://www.salesup.be' },
      jobLocation: { '@type': 'Place', address: { '@type': 'PostalAddress', addressLocality: offer.city || '', addressCountry: 'BE' } },
      directApply: true,
      url: offer.careers_apply_url
    });
    document.head.appendChild(s);
  }

  qsa('[data-recruitee-list]').forEach(loadList);
  loadDetail();
})();
