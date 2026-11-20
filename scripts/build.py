"""Build the two standalone apps from the dashboard pages in src/.

app/fuel/index.html  Performance Nutrition Planner ("Fuel")
app/labs/index.html  Health & Lab Results ("Labs")
app/index.html       Launcher

Each app is one HTML file: page markup + src/shim.js + inlined data. d3 v7 loads from jsDelivr.
The public build uses sample data: a 70 kg demo athlete and lab values that are shifted from the
originals (pass --labs path/to/labs.csv to build from your own file instead of src/data/labs_demo.csv).
"""
import csv, json, pathlib, random, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, APP = ROOT / 'src', ROOT / 'app'

BLOB = {
    'acai': '3f42ef4f86001ce8d793a4749d33479c', 'bagel': '3f07b96ea1386948ae31e749b0cb5288',
    'beet_juice': '6b029acd01ab8bff3ca13af4beaf2e86', 'chicken_pasta': '4c464571d8e368543ae4883f719c0d85',
    'chicken_quinoa': '4b2b1bce4a31e5fafca95c9cc2de54a4', 'chicken_rice_beans': '5a5f24555949662c1a702b38062d10d0',
    'choc_milk': '3c4419bb5a2fa6313c45877cc3a15f24', 'fish_tacos': 'e24f731d0bea6da41ce65c7f3cefe6bd',
    'green_juice': '7e4eb454b53ac0ee2378bd886c2fcd00', 'lentil_soup': '41371e00a12583bd30732d766e6009fc',
    'oatmeal': 'a0751dbb176654fa7777a8137d8586b8', 'omelette': '466a532a5c01d1bfe3ce51b6358f9b24',
    'orange_juice': '39528639e63ea127772a56abfdfd9be4', 'poke': '7b6fb1a6889110bcc986203f510dca2c',
    'rice_cakes': '9fb07e09d06ad2a1efa7395df6e94781', 'salmon_sweetpotato': '58f6e5f7a24aeac23ac45f270ed6b888',
    'shake': '1303836c02f2c7b107d1a716cf829433', 'shrimp_pasta': 'ab7d1770b11eaee17e095519621285f0',
    'tapioca': '6276e31512d59062680ff27acf599f3b', 'tilapia': 'f1ac5e22f10ed6a90d424c5fd9aad1cd',
    'toast_avocado': 'f501ad9c395faaa34a957a0723e7f8b5', 'watermelon_juice': '0596cb15a14397ffa010e57447189874',
    'yogurt_granola': 'fc610539d882e42cb0f6628a950cd41d',
}
BLOB2FILE = {v: k for k, v in BLOB.items()}


def rows(name):
    return list(csv.DictReader(open(SRC / 'data' / name, encoding='utf-8')))


def unblob(text, prefix):
    def r(m):
        k = m.group(1)
        if k in BLOB2FILE: return prefix + 'img/' + BLOB2FILE[k] + '.jpg'
        if k == '9b99985f8741605a51ccaa207603ab87': return '../assets/hero_run.jpg'
        if k == 'f2add6853def95c1d7d05f46f6207e97': return '../assets/produce.jpg'
        raise SystemExit('unknown blob ' + k)
    return re.sub(r'/_blob/([0-9a-f]{32})', r, text)


def demo_labs(src):
    """Shift every value by a seeded 5–12% up or down and recompute the High/Low flag from the lab range."""
    rnd = random.Random(20261120)
    out = []
    for r in csv.DictReader(open(src, encoding='utf-8')):
        r = dict(r)
        v = r['value']
        dec = len(v.split('.')[1]) if '.' in v else 0
        f = rnd.uniform(0.05, 0.12)
        nv = float(v) * (1 + f if rnd.random() < .5 else 1 - f)
        r['value'] = f'{nv:.{dec}f}' if dec else str(int(round(nv)))
        hi = float(r['ref_high']) if r['ref_high'] else None
        lo = float(r['ref_low']) if r['ref_low'] else None
        x = float(r['value'])
        r['flag'] = 'H' if (hi is not None and x > hi and not r['qualifier']) else ('L' if (lo is not None and lo > 0 and x < lo) else '')
        out.append(r)
    return out


SHELL = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} · Wendel Freitas</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0b1f3a"><meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="{short}">
<link rel="icon" href="data:image/svg+xml,{icon}">
<link rel="apple-touch-icon" href="../assets/icon-{key}.png">
<link rel="manifest" href="manifest.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<style>
:root{{--font-anthropic-sans:Inter,system-ui,-apple-system,Segoe UI,sans-serif;--cds-font-weight-medium:600;--cds-font-size-caption:12px;
--color-bg:#f3f6fb;--color-panel:#fff;--color-fg:#0b1f3a;--color-fg-muted:#5a6b82;--color-border-line:#dde5f0;
--cds-surface-popover:#fff;--cds-border:#dde5f0;--cds-shadow-popover:0 8px 28px rgba(11,31,58,.14);--color-ok:#16a34a;--color-warn:#f59e0b;--color-bad:#e5484d;--cds-text-secondary:#5a6b82;--cds-chart-axis:#8a99ae;--cds-chart-grid:#e4eaf3;color-scheme:light}}
:root[data-theme=dark]{{--color-bg:#0a1222;--color-panel:#111c30;--color-fg:#eef3fb;--color-fg-muted:#93a3ba;--color-border-line:#22314a;--cds-surface-popover:#16233b;--cds-border:#2a3a56;--cds-shadow-popover:0 8px 28px rgba(0,0,0,.5);--color-ok:#34d399;--color-warn:#fbbf24;--color-bad:#f87171;--cds-text-secondary:#93a3ba;--cds-chart-axis:#6b7d98;--cds-chart-grid:#22314a;color-scheme:dark}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--color-bg:#0a1222;--color-panel:#111c30;--color-fg:#eef3fb;--color-fg-muted:#93a3ba;--color-border-line:#22314a;--cds-surface-popover:#16233b;--cds-border:#2a3a56;--cds-shadow-popover:0 8px 28px rgba(0,0,0,.5);--color-ok:#34d399;--color-warn:#fbbf24;--color-bad:#f87171;--cds-text-secondary:#93a3ba;--cds-chart-axis:#6b7d98;--cds-chart-grid:#22314a;color-scheme:dark}}}}
*{{box-sizing:border-box}}html,body{{margin:0;background:var(--color-bg);color:var(--color-fg);font-family:var(--font-anthropic-sans);-webkit-font-smoothing:antialiased}}
.wf-bar{{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--color-bg) 86%,transparent);backdrop-filter:blur(12px);border-bottom:1px solid var(--color-border-line);padding-top:env(safe-area-inset-top)}}
.wf-bar .in{{max-width:1180px;margin:0 auto;padding:10px 18px;display:flex;align-items:center;gap:10px}}
.wf-logo{{display:flex;align-items:center;gap:8px;text-decoration:none;color:inherit;font-weight:800;letter-spacing:-.02em;font-size:16px;margin-right:6px}}
.wf-logo i{{width:28px;height:28px;border-radius:9px;display:grid;place-items:center;background:linear-gradient(135deg,#1746a0,#0ea5b7);color:#fff;font-style:normal;font-size:12px;font-weight:800}}
.wf-tabs{{display:flex;gap:4px;background:var(--color-panel);border:1px solid var(--color-border-line);border-radius:999px;padding:3px}}
.wf-tabs a{{text-decoration:none;color:var(--color-fg-muted);font-size:13px;font-weight:650;padding:6px 14px;border-radius:999px}}
.wf-tabs a[aria-current]{{background:var(--color-fg);color:var(--color-bg)}}
.wf-sp{{flex:1}}
.wf-pill{{font-size:11px;font-weight:650;letter-spacing:.06em;text-transform:uppercase;color:#8a5300;background:#fef3c7;border-radius:999px;padding:4px 10px}}
:root[data-theme=dark] .wf-pill{{background:#3b2a07;color:#fbbf24}}
.wf-ib{{width:34px;height:34px;border-radius:10px;border:1px solid var(--color-border-line);background:var(--color-panel);color:var(--color-fg);display:grid;place-items:center;cursor:pointer}}
.wf-main{{max-width:1180px;margin:0 auto;padding:18px 18px calc(48px + env(safe-area-inset-bottom))}}
.wf-foot{{max-width:1180px;margin:0 auto;padding:0 18px 40px;font-size:12px;color:var(--color-fg-muted);display:flex;gap:12px;flex-wrap:wrap}}
.wf-foot a{{color:inherit}}
.dash-select{{font:inherit;font-size:14px;color:var(--color-fg);background:var(--color-panel);border:1px solid var(--color-border-line);border-radius:12px;padding:9px 12px;max-width:100%}}
@media(max-width:600px){{.wf-pill{{display:none}}.wf-logo b{{display:none}}}}
body.embed .wf-bar,body.embed .wf-foot{{display:none}}body.embed .wf-main{{padding:12px}}
</style>
<script>window.NX={{}};(function(){{var q=new URLSearchParams(location.search);if(q.get('date'))NX.date=q.get('date');}})();</script>
<script>{shim}</script>
<script>window.__DATA={data};</script>
</head><body>
<script>if(new URLSearchParams(location.search).has('embed'))document.body.classList.add('embed');</script>
<header class="wf-bar"><div class="in">
<a class="wf-logo" href="../"><i>WF</i><b>Performance</b></a>
<nav class="wf-tabs" aria-label="Apps"><a href="../fuel/"{fuel_cur}>Fuel</a><a href="../labs/"{labs_cur}>Labs</a></nav>
<span class="wf-sp"></span><span class="wf-pill">Sample data</span>
<button class="wf-ib" id="wf-theme" type="button" aria-label="Switch light or dark"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/></svg></button>
</div></header>
<main class="wf-main">
{page}
</main>
<footer class="wf-foot"><span>{foot}</span><span>·</span><a href="https://www.wendelfreitas.com/fuel-and-labs/">Case study</a><a href="https://github.com/wendel-crypto/fuel-and-labs">GitHub</a></footer>
</body></html>
'''


def icon(letter):
    svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%231746a0'/><stop offset='1' stop-color='%230ea5b7'/></linearGradient></defs><rect width='64' height='64' rx='16' fill='url(%23g)'/><text x='32' y='43' font-family='Arial' font-weight='700' font-size='30' fill='white' text-anchor='middle'>{letter}</text></svg>"
    return svg.replace('<', '%3C').replace('>', '%3E').replace('"', "'").replace(' ', '%20')


def manifest(key, name, short):
    return json.dumps({"name": name, "short_name": short, "start_url": "./", "display": "standalone",
                       "background_color": "#0b1f3a", "theme_color": "#0b1f3a",
                       "icons": [{"src": f"../assets/icon-{key}.png", "sizes": "512x512", "type": "image/png"}]}, indent=1)


def write(key, title, short, desc, foot, page, data):
    out = APP / key
    out.mkdir(parents=True, exist_ok=True)
    html = SHELL.format(title=title, short=short, desc=desc, foot=foot, key=key, icon=icon(short[0]),
                        shim=(SRC / 'shim.js').read_text(), data=json.dumps(data, ensure_ascii=False, separators=(',', ':')),
                        page=page, fuel_cur=' aria-current="page"' if key == 'fuel' else '',
                        labs_cur=' aria-current="page"' if key == 'labs' else '')
    (out / 'index.html').write_text(html, encoding='utf-8')
    (out / 'manifest.webmanifest').write_text(manifest(key, title, short))
    print(key, len(html) // 1024, 'KB')


def page_body(path):
    s = (SRC / path).read_text(encoding='utf-8')
    return s.replace('<meta name="dash-one-writer">', '').strip()


def main():
    labs_src = sys.argv[sys.argv.index('--labs') + 1] if '--labs' in sys.argv else None
    # ---- Fuel
    meals = rows('meal_templates.csv')
    for m in meals:
        m['image'] = unblob(m['image'], '') if m['image'] else ''
    juices = rows('juices.csv')
    for j in juices:
        j['image'] = unblob(j['image'], '') if j['image'] else ''
    fuel_data = {
        'plan': rows('plan_days.csv'), 'rules': rows('fuel_rules.csv'), 'meal_templates': meals,
        'juices': juices, 'shopping': rows('shopping.csv'), 'swaps': rows('swaps.csv'), 'weather': rows('weather.csv'),
        'g_weight': [{'date': '2026-11-15', 'weight_kg': 70}],
    }
    fuel = unblob(page_body('fuel.page.html'), '')
    fuel = fuel.replace('Targets use your Garmin weight', 'Targets use body weight')
    write('fuel', 'Fuel — Performance Nutrition Planner', 'Fuel',
          'Daily carbs, protein and fat for every session of a 22-week marathon build, with meals, recipes, juices, weather and a weekly grocery cart.',
          'Fuel · 70 kg sample athlete · weather is a saved Miami forecast', fuel, fuel_data)
    # ---- Labs
    if labs_src:
        labs = list(csv.DictReader(open(labs_src, encoding='utf-8')))
    else:
        labs = rows('labs_demo.csv')
    lp = page_body('labs.page.html').replace('Book Dr. Pimentel and bring all 7 reports', 'Book your physician and bring all 7 reports')
    write('labs', 'Labs — Health & Lab Results', 'Labs',
          'Seven blood panels from 2023–2026 in one view: focus markers, a heatmap of every result, body systems, trends and an action plan.',
          'Labs · sample values · educational only, not medical advice', lp, {'labs': labs})


if __name__ == '__main__':
    if '--make-demo' in sys.argv:
        d = demo_labs(sys.argv[sys.argv.index('--make-demo') + 1])
        with open(SRC / 'data' / 'labs_demo.csv', 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(d[0].keys())); w.writeheader(); w.writerows(d)
        print('labs_demo.csv', len(d))
    main()
