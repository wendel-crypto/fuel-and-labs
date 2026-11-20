/* Minimal runtime for the Fuel & Labs pages.
   Implements the small dashboard API the pages are written against:
   dash.data(name), dash.calc(name,{inputs,fn}), dash.draw(name[,fn]), dash.colors, dash.loader().
   Data is inlined in window.__DATA (name -> rows). */
(function () {
  var PAL = {
    light: ['#2f6fec', '#0ea5b7', '#0b1f3a', '#f59e0b', '#7c5cff', '#ef5b5b', '#94a3b8', '#bcd3ff'],
    dark: ['#6c9bff', '#2dd4bf', '#dbe7ff', '#fbbf24', '#a78bfa', '#f87171', '#94a3b8', '#33507f']
  };
  var calcs = [], draws = {}, state = {}, ready = false;
  function run(n) {
    var f = draws[n]; if (!f) return;
    document.querySelectorAll('[data-draw="' + n + '"]').forEach(function (el) {
      try { f(el); } catch (e) { console.error('draw ' + n, e); }
    });
  }
  function theme() {
    var t = document.documentElement.getAttribute('data-theme');
    if (!t) t = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    return t;
  }
  window.dash = {
    colors: PAL.light,
    loader: function () {},
    data: function (n) { return n in state ? { status: 'ok', data: state[n] } : { status: 'loading', data: null }; },
    calc: function (n, o) { calcs.push([n, o]); },
    draw: function (n, fn) { if (fn) { draws[n] = fn; if (ready) run(n); } else if (ready) run(n); }
  };
  function compute() {
    var raw = window.__DATA || {};
    Object.keys(raw).forEach(function (k) { state[k] = raw[k]; });
    var left = calcs.slice(), guard = 0;
    while (left.length && guard++ < 40) {
      left = left.filter(function (c) {
        var o = c[1];
        if (o.inputs.every(function (i) { return i in state; })) {
          try { state[c[0]] = o.fn.apply(null, o.inputs.map(function (i) { return state[i]; })); }
          catch (e) { console.error('calc ' + c[0], e); state[c[0]] = []; }
          return false;
        }
        return true;
      });
    }
  }
  function redrawAll() { dash.colors = PAL[theme()]; Object.keys(draws).forEach(run); }
  window.__wfRedraw = redrawAll;
  document.addEventListener('DOMContentLoaded', function () {
    dash.colors = PAL[theme()]; compute(); ready = true; redrawAll();
    var b = document.getElementById('wf-theme');
    if (b) b.addEventListener('click', function () {
      var t = theme() === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', t);
      try { localStorage.setItem('wf-theme', t); } catch (e) {}
      redrawAll();
    });
    if (window.matchMedia) matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function () {
      if (!document.documentElement.getAttribute('data-theme')) redrawAll();
    });
  });
  try { var s = localStorage.getItem('wf-theme'); if (s) document.documentElement.setAttribute('data-theme', s); } catch (e) {}
  var q = new URLSearchParams(location.search);
  if (q.get('theme')) document.documentElement.setAttribute('data-theme', q.get('theme'));
})();
