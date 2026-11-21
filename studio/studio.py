#!/usr/bin/env python3
"""Studio Andamare : boite a outils de la chaine video (tache automatique 3).
Usage : python3 studio.py <commande> --help
Commandes : polyhaven, police, pixabay, openverse, rendre, vertical, mixer, planche, mesures
Tout est gratuit et sous licence libre (Poly Haven CC0, Google Fonts OFL, Pixabay, Openverse CC0)."""
import argparse, json, os, re, subprocess, sys, urllib.parse, urllib.request

UA = {'User-Agent': 'andamare-studio/1.0'}
def get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
def jget(url): return json.loads(get(url))
def save(url, path):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'wb').write(get(url)); return path
def sh(cmd): subprocess.run(cmd, check=True)

# ---------- Poly Haven : modeles 3D, textures, eclairages (CC0) ----------
def polyhaven(a):
    if a.action == 'chercher':
        t = {'modele': 'models', 'texture': 'textures', 'eclairage': 'hdris'}[a.type]
        d = jget(f'https://api.polyhaven.com/assets?t={t}')
        mots = [m.lower() for m in a.mots]
        for k, v in d.items():
            txt = (k + ' ' + ' '.join(v.get('tags', []) + v.get('categories', []))).lower()
            if all(m in txt for m in mots): print(k, '|', ', '.join(v.get('categories', [])[:4]))
        return
    f = jget(f'https://api.polyhaven.com/files/{a.nom}'); d = os.path.join(a.dossier, a.nom)
    if 'hdri' in f:                       # eclairage
        print(save(f['hdri'][a.res]['hdr']['url'], f'{a.dossier}/{a.nom}_{a.res}.hdr'))
    elif 'gltf' in f and a.type != 'texture':   # modele 3D
        g = f['gltf'][a.res]['gltf']; save(g['url'], f'{d}/{a.nom}.gltf')
        for rel, inc in g.get('include', {}).items(): save(inc['url'], f'{d}/{rel}')
        print(f'{d}/{a.nom}.gltf')
    else:                                 # texture : couleur, relief, rugosite
        for carte in ('Diffuse', 'nor_gl', 'Rough', 'AO', 'Displacement'):
            if carte in f and a.res in f[carte]:
                fmt = f[carte][a.res].get('jpg') or f[carte][a.res].get('png')
                print(save(fmt['url'], f"{d}/{a.nom}_{carte}.{fmt['url'].rsplit('.', 1)[-1]}"))

# ---------- Google Fonts : vraies polices (licence libre) ----------
def police(a):
    fam = a.famille.replace(' ', '+')
    css = get(f'https://fonts.googleapis.com/css2?family={fam}:wght@{a.graisse}').decode()
    url = re.findall(r'url\((https[^)]+)\)', css)[0]
    print(save(url, os.path.join(a.dossier, f"{a.famille.replace(' ', '')}-{a.graisse}.ttf")))

# ---------- Pixabay : vraies videos et photos ----------
def pixabay(a):
    cle = open(a.cle).read().strip(); q = urllib.parse.quote(' '.join(a.mots))
    if a.type == 'video':
        d = jget(f'https://pixabay.com/api/videos/?key={cle}&q={q}&per_page={a.n}')
        for h in d['hits']:
            v = h['videos'].get(a.taille) or h['videos']['medium']
            print(json.dumps({'id': h['id'], 'duree': h['duration'], 'l': v['width'], 'h': v['height'],
                              'tags': h['tags'], 'page': h['pageURL'], 'url': v['url'], 'vignette': v.get('thumbnail')}, ensure_ascii=False))
    else:
        d = jget(f'https://pixabay.com/api/?key={cle}&q={q}&image_type=photo&per_page={a.n}')
        for h in d['hits']:
            print(json.dumps({'id': h['id'], 'l': h['imageWidth'], 'h': h['imageHeight'], 'tags': h['tags'],
                              'page': h['pageURL'], 'url': h['largeImageURL'], 'vignette': h['previewURL']}, ensure_ascii=False))

# ---------- Openverse : sons et musiques CC0 heberges sur Wikimedia Commons ----------
def openverse(a):
    q = urllib.parse.quote(' '.join(a.mots))
    d = jget(f'https://api.openverse.org/v1/audio/?q={q}&license=cc0&page_size={a.n}&source=wikimedia_audio')
    for h in d['results']:
        print(json.dumps({'titre': h['title'], 'duree_s': round((h.get('duration') or 0) / 1000, 1),
                          'page': h['foreign_landing_url'], 'url': h['url']}, ensure_ascii=False))

def telecharger(a):
    try: print(save(a.url, a.sortie))
    except Exception as e:
        sys.exit(f'ECHEC du telechargement ({e}). Le site refuse : prendre un autre resultat, ou composer le son par code.')

# ---------- Rendre une scene HTML image par image ----------
# Contrat de la page : window.ready === true quand tout est charge ; window.frame(t) dessine l'instant t (secondes).
def rendre(a):
    import asyncio, functools, http.server, shutil, socket, tempfile, threading
    from playwright.async_api import async_playwright
    racine, page = os.path.split(os.path.abspath(a.page))
    s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
    class Muet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *x): pass
    h = functools.partial(Muet, directory=racine)
    srv = http.server.ThreadingHTTPServer(('127.0.0.1', port), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    L, H = (540, 960) if a.brouillon else (1080, 1920)
    tmp = tempfile.mkdtemp(); n = round((a.fin - a.debut) * a.ips)
    async def go():
        async with async_playwright() as p:
            b = await p.chromium.launch(args=['--use-gl=angle', '--use-angle=swiftshader',
                                              '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
            pg = await b.new_page(viewport={'width': L, 'height': H})
            pg.on('pageerror', lambda e: print('ERREUR PAGE :', e, file=sys.stderr))
            await pg.goto(f'http://127.0.0.1:{port}/{page}')
            await pg.wait_for_function('window.ready===true', timeout=180000)
            for i in range(n):
                await pg.evaluate(f'window.frame({a.debut + i / a.ips})')
                await pg.screenshot(path=f'{tmp}/{i:05d}.png')
            await b.close()
    asyncio.run(go())
    cmd = ['ffmpeg', '-v', 'error', '-y', '-framerate', str(a.ips), '-i', f'{tmp}/%05d.png']
    if a.son: cmd += ['-i', a.son, '-c:a', 'aac', '-b:a', '192k', '-shortest']
    cmd += ['-c:v', 'libx264', '-crf', '21', '-maxrate', '9M', '-bufsize', '18M', '-pix_fmt', 'yuv420p',
            '-movflags', '+faststart', a.sortie]
    sh(cmd); shutil.rmtree(tmp); print(a.sortie, f'{n} images {L}x{H}')

# ---------- Preparer une vraie video : decoupe, cadrage vertical, etalonnage ----------
ETALONNAGES = {
    'aucun': 'null',
    'chaud': 'eq=contrast=1.08:saturation=1.15,colorbalance=rs=.06:gs=.02:bs=-.05:rh=.04:bh=-.04',
    'froid': 'eq=contrast=1.1:saturation=.95,colorbalance=rs=-.05:bs=.07:bh=.05',
    'cinema': 'eq=contrast=1.15:saturation=1.05:gamma=.96,colorbalance=rs=-.03:bs=.05:rh=.06:bh=-.05,vignette=PI/5',
    'vif': 'eq=contrast=1.12:saturation=1.35:brightness=.02',
    'noir_blanc': 'hue=s=0,eq=contrast=1.25',
}
def vertical(a):
    L, H = (540, 960) if a.brouillon else (1080, 1920)
    vf = (f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)':'(iw-ow)*{a.x}':'(ih-oh)*{a.y}',"
          f"scale={L}:{H}:flags=lanczos,fps={a.ips},{ETALONNAGES[a.etalonnage]}")
    if a.vitesse != 1: vf += f',setpts=PTS/{a.vitesse}'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', str(a.debut), '-i', a.entree]
    if a.duree: cmd += ['-t', str(a.duree * a.vitesse)]
    sh(cmd + ['-vf', vf, '-an', '-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p', a.sortie]); print(a.sortie)

# ---------- Mixer le son : musique + bruitages cales, volume normalise ----------
# --piste fichier:debut_s:volume  (repetable). La premiere piste est la musique.
def mixer(a):
    cmd = ['ffmpeg', '-v', 'error', '-y']; filtres = []; noms = []
    for i, p in enumerate(a.piste):
        f, debut, vol = (p.split(':') + ['0', '1'])[:3]
        cmd += ['-i', f]
        filtres.append(f'[{i}:a]aresample=48000,volume={vol},adelay={int(float(debut) * 1000)}:all=1[a{i}]'); noms.append(f'[a{i}]')
    fin = max(a.duree - a.fondu, 0)
    filtres.append(''.join(noms) + f'amix=inputs={len(noms)}:normalize=0:duration=longest,atrim=0:{a.duree},'
                   f'afade=t=out:st={fin}:d={a.fondu},loudnorm=I=-14:TP=-1.5:LRA=11[m]')
    sh(cmd + ['-filter_complex', ';'.join(filtres), '-map', '[m]', '-ar', '48000', a.sortie]); print(a.sortie)

# ---------- Planche d'images horodatees (pour juger sans tout regarder en grand) ----------
def planche(a):
    vf = (f"fps={a.par_seconde},scale=270:480,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=20:"
          f"fontcolor=white:box=1:boxcolor=black@0.6,tile=6x2")
    sh(['ffmpeg', '-v', 'error', '-y', '-i', a.entree, '-vf', vf, f'{a.prefixe}_%02d.jpg']); print(a.prefixe + '_NN.jpg')

# ---------- Mesures de rythme ----------
def mesures(a):
    duree = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                           '-of', 'csv=p=0', a.entree]).decode())
    r = subprocess.run(['ffmpeg', '-i', a.entree, '-vf', f"select='gt(scene,{a.seuil})',showinfo", '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    coupes = [float(x) for x in re.findall(r'pts_time:([0-9.]+)', r)]
    print(json.dumps({'duree_s': round(duree, 2), 'plans': len(coupes) + 1,
                      'duree_moyenne_plan_s': round(duree / (len(coupes) + 1), 2),
                      'premier_changement_s': coupes[0] if coupes else None,
                      'poids_Mo': round(os.path.getsize(a.entree) / 1e6, 1)}))

def main():
    P = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    S = P.add_subparsers(dest='cmd', required=True)
    p = S.add_parser('polyhaven'); p.add_argument('action', choices=['chercher', 'prendre'])
    p.add_argument('--type', choices=['modele', 'texture', 'eclairage'], default='modele'); p.add_argument('--mots', nargs='*', default=[])
    p.add_argument('--nom'); p.add_argument('--res', default='1k'); p.add_argument('--dossier', default='assets'); p.set_defaults(f=polyhaven)
    p = S.add_parser('police'); p.add_argument('famille'); p.add_argument('--graisse', default='700'); p.add_argument('--dossier', default='assets'); p.set_defaults(f=police)
    p = S.add_parser('pixabay'); p.add_argument('type', choices=['video', 'photo']); p.add_argument('mots', nargs='+')
    p.add_argument('--cle', required=True); p.add_argument('--n', type=int, default=12); p.add_argument('--taille', default='medium'); p.set_defaults(f=pixabay)
    p = S.add_parser('openverse'); p.add_argument('mots', nargs='+'); p.add_argument('--n', type=int, default=12); p.set_defaults(f=openverse)
    p = S.add_parser('telecharger'); p.add_argument('url'); p.add_argument('sortie'); p.set_defaults(f=telecharger)
    p = S.add_parser('rendre'); p.add_argument('page'); p.add_argument('sortie'); p.add_argument('--debut', type=float, default=0)
    p.add_argument('--fin', type=float, required=True); p.add_argument('--ips', type=int, default=30)
    p.add_argument('--brouillon', action='store_true'); p.add_argument('--son'); p.set_defaults(f=rendre)
    p = S.add_parser('vertical'); p.add_argument('entree'); p.add_argument('sortie'); p.add_argument('--debut', type=float, default=0)
    p.add_argument('--duree', type=float); p.add_argument('--x', type=float, default=.5); p.add_argument('--y', type=float, default=.5)
    p.add_argument('--etalonnage', choices=list(ETALONNAGES), default='aucun'); p.add_argument('--vitesse', type=float, default=1)
    p.add_argument('--ips', type=int, default=30); p.add_argument('--brouillon', action='store_true'); p.set_defaults(f=vertical)
    p = S.add_parser('mixer'); p.add_argument('sortie'); p.add_argument('--piste', action='append', required=True)
    p.add_argument('--duree', type=float, required=True); p.add_argument('--fondu', type=float, default=.8); p.set_defaults(f=mixer)
    p = S.add_parser('planche'); p.add_argument('entree'); p.add_argument('prefixe'); p.add_argument('--par_seconde', type=float, default=1); p.set_defaults(f=planche)
    p = S.add_parser('mesures'); p.add_argument('entree'); p.add_argument('--seuil', type=float, default=.3); p.set_defaults(f=mesures)
    a = P.parse_args(); a.f(a)
if __name__ == '__main__': main()
