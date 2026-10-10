
(function () {
  /* Forms. The contact form needs a form service (e.g. Formspree) on the live site. */
  function store(k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  function recall(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  var sf = document.getElementById('search-form');
  if (sf) sf.addEventListener('submit', function (e) {
    e.preventDefault();
    store('tm-search', JSON.stringify({ q: sf.q.value, price: sf.price.value, beds: sf.beds.value, baths: sf.baths.value }));
    location.href = sf.getAttribute('data-target');
  });
  var cf = document.getElementById('contact-form');
  if (cf) cf.addEventListener('submit', function (e) { e.preventDefault(); document.getElementById('sent').hidden = false; });

  /* Rentals filter */
  var rf = document.getElementById('rent-filter');
  if (rf) {
    var saved = recall('tm-search');
    if (saved) { try { var v = JSON.parse(saved); ['q', 'price', 'beds', 'baths'].forEach(function (k) { if (v[k] && rf[k]) rf[k].value = v[k]; }); } catch (e) {} store('tm-search', ''); }
    var cards = Array.prototype.slice.call(document.querySelectorAll('.listing'));
    var count = document.getElementById('rent-count');
    function applyFilter() {
      var q = rf.q.value.trim().toLowerCase(), price = parseInt((rf.price.value || '').replace(/[^0-9]/g, ''), 10) || Infinity;
      var beds = parseInt(rf.beds.value, 10) || 0, baths = parseInt(rf.baths.value, 10) || 0, shown = 0;
      cards.forEach(function (c) {
        var ok = (!q || c.textContent.toLowerCase().indexOf(q) > -1) && +c.dataset.price <= price && +c.dataset.beds >= beds && +c.dataset.baths >= baths;
        c.hidden = !ok; if (ok) shown++;
      });
      count.textContent = shown === 1 ? '1 home' : shown + ' homes';
      document.getElementById('rent-empty').hidden = shown > 0;
    }
    rf.addEventListener('submit', function (e) { e.preventDefault(); applyFilter(); });
    rf.addEventListener('change', applyFilter);
    applyFilter();
  }

  /* Carousel arrows */
  Array.prototype.forEach.call(document.querySelectorAll('.car-nav'), function (nav) {
    var track = document.getElementById(nav.querySelector('.car-btn').getAttribute('aria-controls'));
    if (!track) return;
    var btns = nav.querySelectorAll('.car-btn');
    function step() { var c = track.children[0]; return c ? c.getBoundingClientRect().width + 20 : 300; }
    function sync() {
      btns[0].disabled = track.scrollLeft <= 2;
      btns[1].disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
    }
    Array.prototype.forEach.call(btns, function (b) {
      b.addEventListener('click', function () { track.scrollBy({ left: step() * +b.dataset.dir, behavior: 'smooth' }); });
    });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* Painted desert scenes. Any element with data-src shows that photo instead. */
  var PAL = {
    morning: { sky: ['#8fc0e2', '#cfe4ee', '#f6dfc0'], sun: '#fff4d6', sunY: .2, far: '#a9a3c4', mid: '#b98b77', ground: '#dcb68e', fg: '#9a7656', plant: '#5f7a4f', wall: '#e2b48c', shade: '#c48f68', mwall: '#f1ece4', glass: '#9fc6dc', glow: false },
    golden:  { sky: ['#e39a63', '#f3c487', '#f8e2b8'], sun: '#fff3c4', sunY: .46, far: '#b27a77', mid: '#a5644e', ground: '#d49a66', fg: '#7a4e33', plant: '#4f6b3f', wall: '#e7a96f', shade: '#c07d4c', mwall: '#f6e6d2', glass: '#ffd18a', glow: true },
    dusk:    { sky: ['#26325f', '#8a4f74', '#ef9a6a'], sun: '#ffcf86', sunY: .6, far: '#5b4a78', mid: '#6e4256', ground: '#9a6249', fg: '#4a2f2c', plant: '#3c4a35', wall: '#b9785e', shade: '#8e5643', mwall: '#c8b3ad', glass: '#ffc978', glow: true },
    day:     { sky: ['#5c9fd1', '#9fcbe6', '#eef0ec'], sun: '#ffffff', sunY: .16, far: '#8fa3bf', mid: '#a7826b', ground: '#dfbe97', fg: '#9b7656', plant: '#5b7a46', wall: '#e8c39c', shade: '#c9996f', mwall: '#f7f4ef', glass: '#a9cfe2', glow: false }
  };
  var VIGA = '#5a3a26';
  function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function f(n) { return Math.round(n * 10) / 10; }
  function R(x, y, w, h, fill, rx) { return '<rect x="' + f(x) + '" y="' + f(y) + '" width="' + f(w) + '" height="' + f(h) + '" rx="' + (rx || 0) + '" fill="' + fill + '"/>'; }
  function ridge(r, W, H, base, amp, n, fill, smooth) {
    var pts = [];
    for (var i = 0; i <= n; i++) pts.push([W * i / n, base - amp * (.3 + .7 * r()) * (i % 2 ? 1 : .6)]);
    var d = 'M0 ' + H + ' L0 ' + f(pts[0][1]);
    if (smooth) {
      for (var j = 0; j < pts.length - 1; j++) {
        var mx = (pts[j][0] + pts[j + 1][0]) / 2, my = (pts[j][1] + pts[j + 1][1]) / 2;
        d += ' Q' + f(pts[j][0]) + ' ' + f(pts[j][1]) + ' ' + f(mx) + ' ' + f(my);
      }
      d += ' L' + W + ' ' + f(pts[n][1]);
    } else {
      for (var k = 1; k < pts.length; k++) d += ' L' + f(pts[k][0]) + ' ' + f(pts[k][1]);
    }
    return '<path d="' + d + ' L' + W + ' ' + H + ' Z" fill="' + fill + '"/>';
  }
  function saguaro(x, y, s, c) {
    return '<g stroke="' + c + '" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke-width="' + f(9 * s) + '">' +
      '<path d="M' + f(x) + ' ' + f(y) + ' V' + f(y - 64 * s) + '"/>' +
      '<path d="M' + f(x) + ' ' + f(y - 24 * s) + ' h' + f(-15 * s) + ' v' + f(-22 * s) + '"/>' +
      '<path d="M' + f(x) + ' ' + f(y - 34 * s) + ' h' + f(13 * s) + ' v' + f(-17 * s) + '"/></g>';
  }
  function shrub(x, y, s, c) {
    return '<g fill="' + c + '"><ellipse cx="' + f(x) + '" cy="' + f(y) + '" rx="' + f(14 * s) + '" ry="' + f(7 * s) + '"/><ellipse cx="' + f(x + 10 * s) + '" cy="' + f(y - 3 * s) + '" rx="' + f(9 * s) + '" ry="' + f(6 * s) + '"/></g>';
  }
  function windowAt(x, y, w, h, p) {
    return R(x - 2, y - 2, w + 4, h + 4, VIGA, 2) + R(x, y, w, h, p.glow ? '#ffd58a' : '#6f8599', 1) + R(x + w / 2 - .8, y, 1.6, h, VIGA);
  }
  function adobe(x, y, w, h, p) {
    var o = '';
    var bw = w * .44, bh = h * 1.3, bx = x + w * .06;
    o += '<ellipse cx="' + f(x + w * .55) + '" cy="' + f(y + 2) + '" rx="' + f(w * .75) + '" ry="' + f(h * .07) + '" fill="#000" opacity=".12"/>';
    o += R(bx, y - bh, bw, bh, p.wall, 5) + R(bx + bw * .72, y - bh, bw * .28, bh, p.shade, 5);
    o += windowAt(bx + bw * .25, y - bh + bh * .14, bw * .22, bh * .14, p);
    o += R(x, y - h, w, h, p.wall, 5) + R(x + w * .86, y - h, w * .14, h, p.shade, 5);
    for (var i = 0; i < 6; i++) o += R(x + w * .08 + i * w * .14, y - h + h * .1, w * .035, h * .08, VIGA, 1);
    o += windowAt(x + w * .1, y - h * .6, w * .14, h * .3, p) + windowAt(x + w * .64, y - h * .6, w * .14, h * .3, p);
    var dw = w * .13, dx = x + w * .4, dh = h * .58;
    o += '<path d="M' + f(dx) + ' ' + f(y) + ' V' + f(y - dh + dw / 2) + ' A' + f(dw / 2) + ' ' + f(dw / 2) + ' 0 0 1 ' + f(dx + dw) + ' ' + f(y - dh + dw / 2) + ' V' + f(y) + ' Z" fill="' + VIGA + '"/>';
    o += R(x + w, y - h * .34, w * .34, h * .34, p.shade, 3);
    o += '<path d="M' + f(x + w * 1.12) + ' ' + f(y) + ' V' + f(y - h * .2) + ' A' + f(w * .05) + ' ' + f(w * .05) + ' 0 0 1 ' + f(x + w * 1.22) + ' ' + f(y - h * .2) + ' V' + f(y) + ' Z" fill="' + VIGA + '" opacity=".85"/>';
    return o;
  }
  function modern(x, y, w, h, p) {
    var o = '';
    o += '<ellipse cx="' + f(x + w * .5) + '" cy="' + f(y + 2) + '" rx="' + f(w * .7) + '" ry="' + f(h * .07) + '" fill="#000" opacity=".12"/>';
    var uh = h * .62;
    o += R(x + w * .12, y - h - uh, w * .52, uh, p.mwall) + R(x + w * .42, y - h - uh + uh * .18, w * .2, uh * .64, p.glass);
    o += R(x + w * .06, y - h - uh - 6, w * .66, 6, '#3b3633');
    o += R(x, y - h, w * .5, h, p.mwall);
    for (var i = 0; i < 9; i++) o += R(x + w * .05 + i * w * .045, y - h * .82, w * .014, h * .62, '#8a5a3a');
    o += R(x + w * .5, y - h, w * .46, h, p.glass);
    for (var j = 1; j < 4; j++) o += R(x + w * .5 + j * w * .115, y - h, 1.6, h, '#3b3633');
    o += R(x - w * .06, y - h - 6, w * 1.14, 6, '#3b3633');
    o += R(x + w * .6, y + 4, w * .5, Math.max(4, h * .08), '#5fb3c9', 2);
    return o;
  }

  function txt(x, y, size, fill, str, weight) { return '<text x="' + f(x) + '" y="' + f(y) + '" font-family="Barlow Condensed, Arial Narrow, sans-serif" font-weight="' + (weight || 700) + '" font-size="' + f(size) + '" fill="' + fill + '" text-anchor="middle">' + str + '</text>'; }
  function sign(x, y, k, big, small) {
    var bw = 86 * k, bh = 46 * k, top = y - 92 * k;
    return '<g>' + R(x - 2.5 * k, top, 5 * k, 92 * k, '#6b4a33') + R(x, top + 4 * k, bw * .62, 4 * k, '#6b4a33') +
      R(x + 4 * k, top + 8 * k, 1.2 * k, 7 * k, '#3b3633') + R(x + bw * .5, top + 8 * k, 1.2 * k, 7 * k, '#3b3633') +
      R(x - bw * .2, top + 15 * k, bw, bh, '#ffffff', 3) + R(x - bw * .2, top + 15 * k, bw, 6 * k, '#c9413b', 0) +
      txt(x + bw * .3, top + 15 * k + bh * .62, 20 * k, '#c9413b', big) + txt(x + bw * .3, top + 15 * k + bh * .88, 9 * k, '#12305a', small, 600) + '</g>';
  }
  function boxes(x, y, k, big) {
    var w = (big ? 30 : 18) * k, o = '';
    [[0, 0], [w * 1.05, 0], [w * .5, -w * .8]].forEach(function (b) {
      o += R(x + b[0], y + b[1] - w * .8, w, w * .8, '#c9955c', 1) + R(x + b[0], y + b[1] - w * .8, w, w * .12, '#b07c45') + R(x + b[0] + w * .44, y + b[1] - w * .8, w * .12, w * .8, '#e8d2a6');
    });
    return o;
  }
  function aframe(x, y, k) {
    var w = 74 * k, h = 70 * k;
    return '<g><path d="M' + f(x - w / 2 - 6 * k) + ' ' + f(y) + ' L' + f(x - w / 2) + ' ' + f(y - h) + ' L' + f(x + w / 2) + ' ' + f(y - h) + ' L' + f(x + w / 2 + 6 * k) + ' ' + f(y) + '" fill="none" stroke="#3b3633" stroke-width="' + f(3 * k) + '"/>' +
      R(x - w / 2, y - h, w, h * .78, '#ffffff', 3) + R(x - w / 2, y - h, w, h * .3, '#c9413b', 3) +
      txt(x, y - h + h * .23, 15 * k, '#ffffff', 'OPEN') + txt(x, y - h + h * .52, 15 * k, '#12305a', 'HOUSE') +
      '<path d="M' + f(x - 16 * k) + ' ' + f(y - h * .32) + ' h' + f(26 * k) + ' l' + f(-7 * k) + ' ' + f(-6 * k) + ' M' + f(x + 10 * k) + ' ' + f(y - h * .32) + ' l' + f(-7 * k) + ' ' + f(6 * k) + '" stroke="#c9413b" stroke-width="' + f(3 * k) + '" fill="none" stroke-linecap="round"/></g>';
  }
  function scene(spec, seed, W, H, mode) {
    var parts = spec.split(':'), p = PAL[parts[0]] || PAL.golden, kind = parts[1] || 'adobe';
    var r = rng(seed), id = 'sky' + seed + (mode || ''), k = H / 300;
    var o = '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">';
    o += '<defs><linearGradient id="' + id + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + p.sky[0] + '"/><stop offset=".55" stop-color="' + p.sky[1] + '"/><stop offset="1" stop-color="' + p.sky[2] + '"/></linearGradient></defs>';
    o += '<rect width="' + W + '" height="' + H + '" fill="url(#' + id + ')"/>';
    var sx = W * (.15 + .7 * r()), sy = H * p.sunY, gid = id + "s";
    o += '<radialGradient id="' + gid + '"><stop offset="0" stop-color="' + p.sun + '" stop-opacity=".6"/><stop offset="1" stop-color="' + p.sun + '" stop-opacity="0"/></radialGradient><circle cx="' + f(sx) + '" cy="' + f(sy) + '" r="' + f(H * .26) + '" fill="url(#' + gid + ')"/><circle cx="' + f(sx) + '" cy="' + f(sy) + '" r="' + f(H * .085) + '" fill="' + p.sun + '"/>';
    o += ridge(r, W, H, H * .56, H * .2, Math.round(W / 45), p.far, false);
    o += ridge(r, W, H, H * .68, H * .1, Math.round(W / 70), p.mid, true);
    var gy = H * .78;
    o += ridge(r, W, H, gy, H * .025, 6, p.ground, true);
    o += saguaro(W * (.06 + .1 * r()), gy - 4 * k, .55 * k, p.plant);
    var hw = (kind === 'band' ? W * .3 : W * .4), hh = H * (kind === 'band' ? .16 : .19), hx = kind === 'band' ? W * .52 : W * (.22 + .12 * r());
    if (kind === 'portfolio') {
      o += adobe(W * .06, gy + 4 * k, W * .2, H * .13, p) + modern(W * .4, gy + 2 * k, W * .2, H * .12, p) + adobe(W * .7, gy + 4 * k, W * .17, H * .11, p);
    } else if (kind === 'adobe' || kind === 'rent' || kind === 'movein') {
      if (kind === 'rent') hx = W * .4;
      o += adobe(hx, gy + 4 * k, hw, hh, p);
    } else {
      if (kind === 'openhouse') hx = W * .42;
      o += modern(hx, gy + 4 * k, hw, hh, p);
    }
    o += saguaro(W * .9, H * .93, 1.15 * k, p.plant) + shrub(W * .12, H * .92, 1.4 * k, p.plant) + shrub(W * .7, H * .95, k, p.plant);
    o += ridge(r, W, H, H * .93, H * .02, 5, p.fg, true);
    if (kind === 'rent') o += sign(W * .2, H * .96, k, 'FOR RENT', '(520) 440-6342');
    if (kind === 'movein') o += boxes(hx + hw * .62, gy + 4 * k, k) + boxes(W * .16, H * .95, 1.3 * k, true);
    if (kind === 'portfolio') o += sign(W * .5, H * .97, k * .85, 'RENTED', 'Help-U-Manage');
    if (kind === 'openhouse') o += aframe(W * .2, H * .97, k);
    return o + '</svg>';
  }
  function fill(el, W, H, mode) {
    var inner = el.dataset.src ? '<img src="' + el.dataset.src + '" alt="">' : scene(el.dataset.scene, +el.dataset.seed || 1, W, H, mode);
    if (mode === 'band') { el.innerHTML = inner; } else { el.innerHTML = '<div class="ph-in">' + inner + '</div>'; }
  }
  document.querySelectorAll('.ph[data-scene]').forEach(function (el) { fill(el, 400, 340); });
  document.querySelectorAll('[data-band]').forEach(function (el) { fill(el, 1440, 760, 'band'); });

  /* Hero: separate layers so each can drift at its own speed */
  Array.prototype.forEach.call(document.querySelectorAll('.hero-scene'), function (hs) {
    var W = 1440, H = 470, r = rng(+hs.dataset.seed || 11), p = PAL.dusk, k = H / 300;
    function layer(depth, body) { return '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="xMidYMax slice" data-depth="' + depth + '">' + body + '</svg>'; }
    var houses = '';
    houses += adobe(W * .14, H * .8, W * .17, H * .15, p);
    houses += modern(W * .46, H * .81, W * .19, H * .13, p);
    houses += adobe(W * .74, H * .8, W * .13, H * .12, p);
    houses += saguaro(W * .09, H * .8, .9 * k, '#2f3a2c') + saguaro(W * .41, H * .8, .7 * k, '#2f3a2c') + saguaro(W * .69, H * .8, .8 * k, '#2f3a2c');
    hs.innerHTML =
      layer(.36, '<defs><radialGradient id="hsun"><stop offset="0" stop-color="#ffd890" stop-opacity=".55"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient></defs><circle cx="' + W * .72 + '" cy="' + H * .5 + '" r="' + H * .34 + '" fill="url(#hsun)"/><circle cx="' + W * .72 + '" cy="' + H * .5 + '" r="' + H * .085 + '" fill="#ffd27e"/>') +
      layer(.24, ridge(r, W, H, H * .58, H * .28, 26, '#4b3f6e', false)) +
      layer(.15, ridge(r, W, H, H * .7, H * .14, 14, '#6a3f57', true)) +
      layer(.07, ridge(r, W, H, H * .8, H * .03, 8, '#8c5644', true) + houses) +
      layer(0, '<path d="M0 ' + H + ' L0 ' + H * .9 + ' Q' + W * .25 + ' ' + H * .84 + ' ' + W * .5 + ' ' + H * .9 + ' T' + W + ' ' + H * .88 + ' L' + W + ' ' + H + ' Z" fill="var(--sand)"/>' +
        saguaro(W * .94, H * .97, 1.6 * k, '#3a4a33') + shrub(W * .05, H * .95, 1.6 * k, '#55684a') + shrub(W * .6, H * .97, 1.2 * k, '#55684a'));
  });

  /* Parallax: layers lag the scroll by their data-depth; photos drift inside their frames */
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var hero = document.querySelector('.hero');
  if (!hero) return;
  var heroLayers = Array.prototype.slice.call(document.querySelectorAll('.hero [data-depth]'));
  var frames = Array.prototype.slice.call(document.querySelectorAll('.ph > .ph-in > *, .band-bg > *'));
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight;
    var ht = hero.getBoundingClientRect().top;
    if (ht > -hero.offsetHeight) heroLayers.forEach(function (el) { el.style.transform = 'translate3d(0,' + f(-ht * el.dataset.depth) + 'px,0)'; });
    frames.forEach(function (el) {
      var box = el.parentNode.parentNode.getBoundingClientRect();
      if (box.bottom < -50 || box.top > vh + 50) return;
      var prog = (box.top + box.height / 2 - vh / 2) / (vh / 2 + box.height / 2);
      var range = el.parentNode.classList.contains('band-bg') ? .14 : .1;
      el.style.transform = 'translate3d(0,' + f(prog * range * box.height) + 'px,0)';
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();

