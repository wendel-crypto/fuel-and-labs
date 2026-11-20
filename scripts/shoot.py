"""Headless Chrome screenshots of the apps into docs/. Serves app/ on a local port."""
import asyncio, http.server, threading, functools, pathlib, sys
from playwright.async_api import async_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(ROOT / 'app'))
    h.log_message = lambda *a: None
    s = http.server.ThreadingHTTPServer(('127.0.0.1', 8765), h); threading.Thread(target=s.serve_forever, daemon=True).start()
SHOTS = [
  # name, path, viewport, full_page, scroll_to selector
  ('fuel-desktop', 'fuel/?date=2026-11-24&theme=light', (1440, 900), False, None),
  ('fuel-desktop-full', 'fuel/?date=2026-11-24&theme=light', (1440, 900), True, None),
  ('fuel-meals', 'fuel/?date=2026-11-24&theme=light', (1440, 1000), False, '#meals'),
  ('fuel-build', 'fuel/?date=2026-11-24&theme=light', (1440, 1000), False, '#build'),
  ('fuel-juices', 'fuel/?date=2026-11-24&theme=light', (1440, 900), False, '#juices'),
  ('fuel-shop', 'fuel/?date=2026-11-24&theme=light', (1440, 1000), False, '#shop'),
  ('fuel-dark', 'fuel/?date=2026-12-06&theme=dark', (1440, 900), False, None),
  ('fuel-mobile', 'fuel/?date=2026-11-24&theme=light', (390, 844), False, None),
  ('fuel-mobile-meals', 'fuel/?date=2026-11-24&theme=light', (390, 844), False, '#meals'),
  ('labs-desktop', 'labs/?theme=light', (1440, 900), False, None),
  ('labs-desktop-full', 'labs/?theme=light', (1440, 900), True, None),
  ('labs-heatmap', 'labs/?theme=light', (1440, 1000), False, '#heatmap'),
  ('labs-systems', 'labs/?theme=light', (1440, 1000), False, '#systems'),
  ('labs-explore', 'labs/?theme=light', (1440, 900), False, '#explore'),
  ('labs-dark', 'labs/?theme=dark', (1440, 900), False, None),
  ('labs-mobile', 'labs/?theme=light', (390, 844), False, None),
  ('launcher', '', (1440, 900), False, None),
]
async def main(only):
    serve(); out = ROOT / 'docs' / 'raw'; out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
        for name, path, vp, full, sel in SHOTS:
            if only and name not in only: continue
            pg = await b.new_page(viewport={'width': vp[0], 'height': vp[1]}, device_scale_factor=2 if vp[0] < 500 else 1)
            errs = []; pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
            await pg.goto(f'http://127.0.0.1:8765/{path}', wait_until='networkidle')
            await pg.wait_for_timeout(900)
            if sel:
                await pg.evaluate(f"(()=>{{const e=document.querySelector('{sel}');window.scrollTo(0,e.getBoundingClientRect().top+scrollY-70)}})()")
                await pg.wait_for_timeout(500)
            await pg.screenshot(path=str(out / f'{name}.png'), full_page=full)
            print(name, 'errors:', errs[:3])
            await pg.close()
        await b.close()
asyncio.run(main(sys.argv[1:]))
