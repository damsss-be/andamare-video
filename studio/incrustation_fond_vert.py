# Incrustation fond vert (studio, issu de la video 25). Reglages PLANS = exemples a reecrire.
# Visiteur v2 : vraie video Pixabay (fond vert) -> calque plein ecran RGBA par image de la video finale.
# Detourage plein (interieur opaque a 100 %), suppression du debord vert, vraies couleurs eclairees chaud
# (balance des spots + liseré de lumiere cote spot), flou de profondeur calcule a l'echelle de l'ecran
# (premultiplie : le bord est doux, le corps reste opaque). Le grain et le vignettage sont ajoutes ensuite
# par la meme passe que la 3D (musee.html).
# python3 outils/visiteur2.py clip.mp4 sortie_dossier --plan p2 --largeur 540
import argparse, os, json, numpy as np, cv2

PLANS = {
  # P2 (1,80-3,30 s) : de dos, au premier plan, il marche et sort a droite (parallaxe du travelling) ;
  # la balle se decouvre vers 2,4 s.
  'p2': dict(n=45, s0=0.10, X=(.25, 1.75), dx=1.0, Y=(.12, .15), sc=(1.75, 1.65), flou=9.0, rim=(.4, -1)),
  # P7 (9,40-11,00 s) : plan large ; tete et epaules au premier plan en bas a droite, devant le cordon,
  # il s'eloigne vers la gauche ; le cadre coupe le corps (pieds hors champ).
  'p7': dict(n=48, s0=2.20, X=(.92, -.30), dx=1.55, Y=(.66, .61), sc=(1.60, 1.45), flou=6.0, rim=(-.4, -1), miroir=True),
}
p = argparse.ArgumentParser(); p.add_argument('clip'); p.add_argument('sortie'); p.add_argument('--plan', required=True)
p.add_argument('--largeur', type=int, default=540); p.add_argument('--seules', default='')
a = p.parse_args(); P = PLANS[a.plan]; L = a.largeur; H = L * 16 // 9; k1080 = L / 1080
os.makedirs(a.sortie, exist_ok=True)
cap = cv2.VideoCapture(a.clip); fps = cap.get(cv2.CAP_PROP_FPS)
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
doux = lambda x: (lambda y: y * y * (3 - 2 * y))(min(1, max(0, x)))
lin = lambda ab, k: ab[0] + (ab[1] - ab[0]) * k
s2l = lambda c: np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)
l2s = lambda c: np.where(c <= .0031308, c * 12.92, 1.055 * np.power(np.maximum(c, 0), 1 / 2.4) - .055)

def detoure(f):
    f = f.astype(np.float32) / 255; b, g, r = f[..., 0], f[..., 1], f[..., 2]
    d = g - np.maximum(r, b)
    al = 1 - np.clip((d - .10) / .22, 0, 1)
    # interieur plein : plus grande forme, trous bouches -> opaque a 100 %
    m = (al > .5).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); m = (lab == big).astype(np.uint8)
        cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE); m = np.zeros_like(m); cv2.drawContours(m, cs, -1, 1, -1)
        al = al * cv2.dilate(m, np.ones((5, 5), np.uint8)).astype(np.float32)
        al = np.maximum(al, cv2.erode(m, np.ones((5, 5), np.uint8)).astype(np.float32))
    al = cv2.GaussianBlur(al, (3, 3), .7)
    g2 = np.minimum(g, np.maximum(r, b) * 1.02)                     # plus de debord vert
    return np.dstack([b, g2, r]), al

def eclaire(c, al, rim):
    # vraies couleurs, exposees comme la salle : balance chaude des spots, liseré cote spot
    lc = s2l(c) * 2.2 * np.array([.86, .97, 1.10], np.float32)       # BGR : un peu plus chaud
    dx, dy = rim; M = np.float32([[1, 0, -dx * 6], [0, 1, -dy * 6]])
    sh = cv2.warpAffine(al, M, (al.shape[1], al.shape[0]))
    bord = np.clip(al - sh, 0, 1); bord = cv2.GaussianBlur(bord, (0, 0), 2.5) * al
    lc = lc + bord[..., None] * np.array([.30, .52, .78], np.float32) * .4   # halo chaud (BGR)
    return l2s(np.clip(lc, 0, 1)).astype(np.float32)

sel = set(int(x) for x in a.seules.split(',') if x)
meta = []
for k in range(P['n']):
    if sel and k not in sel: continue
    u = k / (P['n'] - 1); kk = doux(u)
    i = min(len(frames) - 1, round((P['s0'] + k / 30) * fps))
    c, al = detoure(frames[i][:, ::-1].copy() if P.get('miroir') else frames[i]); c = eclaire(c, al, P['rim'])
    ys, xs = np.where(al > .01); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    sc = lin(P['sc'], kk) * H / 1080                                 # pixels ecran par pixel source
    X, Y = lin(P['X'], doux(k / 30 / P['dx']) if 'dx' in P else kk) * L, lin(P['Y'], kk) * H                   # ou tombe le haut de la tete (centre)
    tete = al[y0:y0 + max(4, (y1 - y0) // 7)] > .5
    hx = np.where(tete)[1].mean() if tete.any() else (x0 + x1) / 2
    w, h = int((x1 - x0) * sc), int((y1 - y0) * sc)
    ox, oy = int(X + (x0 - hx) * sc), int(Y)
    cc = cv2.resize(c[y0:y1, x0:x1], (w, h), interpolation=cv2.INTER_CUBIC)
    aa = np.clip(cv2.resize(al[y0:y1, x0:x1], (w, h), interpolation=cv2.INTER_CUBIC), 0, 1)
    pad = int(P['flou'] * k1080 * 4) + 2
    can = np.zeros((H + 2 * pad, L + 2 * pad, 4), np.float32)
    cx0, cy0 = max(0, ox + pad), max(0, oy + pad); cx1, cy1 = min(L + 2 * pad, ox + pad + w), min(H + 2 * pad, oy + pad + h)
    if cx1 > cx0 and cy1 > cy0:
        sx, sy = cx0 - (ox + pad), cy0 - (oy + pad)
        can[cy0:cy1, cx0:cx1, :3] = cc[sy:sy + cy1 - cy0, sx:sx + cx1 - cx0] * aa[sy:sy + cy1 - cy0, sx:sx + cx1 - cx0, None]
        can[cy0:cy1, cx0:cx1, 3] = aa[sy:sy + cy1 - cy0, sx:sx + cx1 - cx0]
    s = P['flou'] * k1080
    if s > .3: can = cv2.GaussianBlur(can, (0, 0), s)
    can = can[pad:pad + H, pad:pad + L]
    A = can[..., 3:]; C = np.where(A > 1e-3, can[..., :3] / np.maximum(A, 1e-3), 0)
    out = np.dstack([C, A]); cv2.imwrite(f'{a.sortie}/{k:03d}.png', (np.clip(out, 0, 1) * 255 + .5).astype(np.uint8))
    meta.append(dict(k=k, clip=i, interieur_opaque=float((aa > .999).mean())))
print(a.sortie, len(meta), 'calques', L, 'x', H)
