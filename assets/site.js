/* Tang & Co concept: menu, Scottish tax band tool, booking form, lazy map. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // menu
  const btn = $('.menu-btn');
  const menu = $('#menu');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open);
      menu.hidden = !open;
      document.documentElement.classList.toggle('menu-open', open);
    });
    $$('a', menu).forEach((a) => a.addEventListener('click', () => {
      btn.setAttribute('aria-expanded', 'false'); menu.hidden = true; document.documentElement.classList.remove('menu-open');
    }));
  }

  // Scottish income tax 2026/27 (non-savings, non-dividend income). Source: GOV.UK.
  const PA = 12570;
  const SCOT = { limits: [3967, 16956, 31092, 62430, 125140], rates: [0.19, 0.20, 0.21, 0.42, 0.45, 0.48] };
  const RUK = { limits: [37700, 125140], rates: [0.20, 0.40, 0.45] };
  const allowance = (inc) => (inc <= 100000 ? PA : Math.max(0, PA - Math.floor((inc - 100000) / 2)));
  const calc = (inc, sys) => {
    const taxable = Math.max(0, inc - allowance(inc));
    let tax = 0; let prev = 0; let top = -1;
    sys.rates.forEach((r, i) => {
      const lim = i < sys.limits.length ? sys.limits[i] : Infinity;
      const slice = Math.max(0, Math.min(taxable, lim) - prev);
      if (slice > 0) { tax += slice * r; top = i; }
      prev = lim;
    });
    return { tax, top };
  };
  const tool = $('#taxtool');
  if (tool) {
    const S = JSON.parse($('#tt-strings').textContent);
    const input = $('#tt-pay', tool);
    const segs = $$('.seg', tool);
    const gbp = (n) => '£' + Math.round(n).toLocaleString('en-GB');
    const run = () => {
      const inc = Math.min(10000000, Number(String(input.value).replace(/[^0-9.]/g, '')) || 0);
      const s = calc(inc, SCOT);
      const r = calc(inc, RUK);
      segs.forEach((el, i) => { el.classList.toggle('on', i === s.top); el.classList.toggle('off', s.top >= 0 && i > s.top); });
      if (s.top < 0) {
        $('#tt-band').textContent = inc > 0 ? S.none : '—';
        $('#tt-tax').textContent = gbp(0);
        $('#tt-vs').textContent = '—';
        return;
      }
      $('#tt-band').textContent = `${S.names[s.top]} ${Math.round(SCOT.rates[s.top] * 100)}%`;
      $('#tt-tax').textContent = gbp(s.tax);
      const d = s.tax - r.tax;
      $('#tt-vs').textContent = Math.abs(d) < 1 ? S.same : `${gbp(Math.abs(d))} ${d > 0 ? S.more : S.less}`;
    };
    input.addEventListener('input', run);
    input.addEventListener('blur', () => {
      const n = Number(String(input.value).replace(/[^0-9.]/g, ''));
      if (n) input.value = Math.round(n).toLocaleString('en-GB');
    });
    run();
  }

  // booking form -> WhatsApp or email
  const form = $('#book-form');
  if (form) {
    const T = JSON.parse($('#f-strings').textContent);
    let via = 'wa';
    $$('button[type=submit]', form).forEach((b) => b.addEventListener('click', () => { via = b.dataset.via; }));
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const v = (id) => $(id, form).value.trim();
      const err = $('#f-err', form);
      if (!v('#f-name') || !v('#f-phone')) { err.hidden = false; (v('#f-name') ? $('#f-phone', form) : $('#f-name', form)).focus(); return; }
      err.hidden = true;
      const lines = [`${T.name}: ${v('#f-name')}`, `${T.phone}: ${v('#f-phone')}`, `${T.topic}: ${v('#f-topic')}`, `${T.office}: ${v('#f-office')}`];
      if (v('#f-msg')) lines.push(`${T.msg}: ${v('#f-msg')}`);
      const body = `${T.subject}\n\n${lines.join('\n')}`;
      const url = via === 'wa'
        ? `https://wa.me/${T.wa}?text=${encodeURIComponent(body)}`
        : `mailto:${T.to}?subject=${encodeURIComponent(T.subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
      window.open(url, via === 'wa' ? '_blank' : '_self');
    });
  }

  // map: load MapLibre only when the map comes near the screen
  const box = $('[data-map]');
  if (box && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((ents) => {
      if (!ents.some((e) => e.isIntersecting)) return;
      io.disconnect();
      const s = document.createElement('script');
      const mj = document.querySelector('script[src*="map.js"]');
      if (!mj) return;
      s.src = mj.src.replace(/map\.js.*/, 'vendor/maplibre/maplibre-gl.js');
      s.onload = () => { if (window.tcMap) window.tcMap(box); };
      document.head.appendChild(s);
    }, { rootMargin: '400px' });
    io.observe(box);
  }
})();
