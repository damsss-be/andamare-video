# Rend une plage d'images d'une page (contrat studio.py) en PNG numerotes par leur indice global (t*ips),
# pour ne re-rendre que les plans modifies et assembler ensuite en un seul encodage.
# python3 outils/rendu_png.py musee.html dossier --debut 0 --fin 11 [--brouillon] [--ips 30]
import argparse, asyncio, functools, http.server, os, socket, sys, threading, time
from playwright.async_api import async_playwright
p = argparse.ArgumentParser(); p.add_argument('page'); p.add_argument('sortie'); p.add_argument('--debut', type=float, default=0)
p.add_argument('--fin', type=float, required=True); p.add_argument('--ips', type=int, default=30); p.add_argument('--brouillon', action='store_true')
a = p.parse_args(); os.makedirs(a.sortie, exist_ok=True)
L, H = (540, 960) if a.brouillon else (1080, 1920)
racine, nom = os.path.split(os.path.abspath(a.page))
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
class Muet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *x): pass
srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(Muet, directory=racine))
threading.Thread(target=srv.serve_forever, daemon=True).start()
i0, i1 = round(a.debut * a.ips), round(a.fin * a.ips)
async def go():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width': L, 'height': H})
        pg.on('pageerror', lambda e: print('ERREUR PAGE :', e, file=sys.stderr, flush=True))
        await pg.goto(f'http://127.0.0.1:{port}/{nom}')
        await pg.wait_for_function('window.ready===true', timeout=300000)
        t0 = time.time()
        for i in range(i0, i1):
            f = f'{a.sortie}/{i:05d}.png'
            if os.path.exists(f): continue          # reprise possible apres coupure
            await pg.evaluate(f'window.frame({i / a.ips})')
            await pg.screenshot(path=f + '.tmp.png'); os.replace(f + '.tmp.png', f)
            print(f'{i} {time.time() - t0:.0f}s', flush=True)
        await b.close()
asyncio.run(go())
print('FINI', i0, i1, flush=True)
