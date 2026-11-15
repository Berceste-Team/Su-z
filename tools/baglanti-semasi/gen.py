#!/usr/bin/env python3
"""Suİz bağlantı şeması: her adım için bir SVG sayfası üretir."""
import os, html

W, H = 1100, 780
UX, UY, UW, UH = 40, 110, 343, 266.7          # UNO Q, 5 birim = 1 mm
BX, BY, BW, BH = 440, 110, 412, 248           # 400 delikli breadboard
FONT = "DejaVu Sans, Arial, sans-serif"
C = dict(v33="#e07b00", v5="#c8372d", gnd="#20262a", sari="#c9a100", mavi="#1f6fd1",
         yesil="#2b8a3e", mor="#7a3fb5", gri="#5b6b7a")
RENK = dict(v33="turuncu", v5="kırmızı", gnd="siyah", sari="sarı", mavi="mavi", yesil="yeşil", mor="mor", gri="gri")

# ---- UNO pinleri (klasik UNO delik yerleşimi, mil cinsinden) ----
TOP = [("SCL",740),("SDA",840),("AREF",940),("GND",1040),("D13",1140),("D12",1240),("D11",1340),("D10",1440),
       ("D9",1540),("D8",1640),("D7",1800),("D6",1900),("D5",2000),("D4",2100),("D3",2200),("D2",2300),("D1",2400),("D0",2500)]
BOT = [("",1100),("IOREF",1200),("RESET",1300),("3V3",1400),("5V",1500),("GND",1600),("GND",1700),("VIN",1800),
       ("A0",2000),("A1",2100),("A2",2200),("A3",2300),("A4",2400),("A5",2500)]
YT, YB = UY + 12.7, UY + 254
def U(name):
    for n, x in TOP:
        if n == name: return (UX + x * 0.127, YT)
    for n, x in BOT:
        if n == name: return (UX + x * 0.127, YB)
    raise KeyError(name)

ROWY = {"T+": BY+16, "T-": BY+28.7, "B+": BY+219, "B-": BY+231.7}
for i, c in enumerate("jihgf"): ROWY[c] = BY + 54 + i * 12.7
for i, c in enumerate("edcba"): ROWY[c] = BY + 143 + i * 12.7
def RX(r): return BX + 22 + (r - 1) * 12.7
def B(col, r): return (RX(r), ROWY[col])
RAILROWS = [r for r in range(1, 31) if r % 6 != 1]

def t(x, y, s, size=10, weight="normal", fill="#1a211f", anchor="start", extra=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{html.escape(s)}</text>'

def uno(used=()):
    o = [f'<rect x="{UX}" y="{UY}" width="{UW}" height="{UH}" rx="8" fill="#dfe9e6" stroke="#7d8a86"/>']
    o.append(f'<rect x="{UX-10}" y="{UY+70}" width="34" height="46" rx="4" fill="#f4f6f5" stroke="#7d8a86"/>')
    o.append(t(UX+30, UY+97, "USB-C", 8, fill="#66716d"))
    o.append(f'<rect x="{UX+150}" y="{UY+95}" width="120" height="70" rx="3" fill="none" stroke="#9aa6a2" stroke-dasharray="3 3"/>')
    o.append(t(UX+210, UY+134, "LED matrisi", 8, fill="#66716d", anchor="middle"))
    o.append(t(UX+18, UY+150, "Arduino UNO Q", 13, "bold"))
    o.append(t(UX+18, UY+165, "üstten, USB-C solda", 8.5, fill="#66716d"))
    for n, x in TOP:
        px = UX + x * 0.127; u = n in used and n != "GND"
        o.append(f'<rect x="{px-4:.1f}" y="{YT-4:.1f}" width="8" height="8" fill="#fff" stroke="{"#1a211f" if u else "#8a9692"}" stroke-width="{1.6 if u else 0.8}"/>')
        o.append(f'<text transform="translate({px-2.6:.1f},{YT+9:.1f}) rotate(90)" font-family="{FONT}" font-size="7.5" font-weight="{"bold" if u else "normal"}" fill="{"#1a211f" if u else "#66716d"}">{n}</text>')
    seen_gnd = 0
    for n, x in BOT:
        px = UX + x * 0.127
        u = n in used and not (n == "GND" and seen_gnd)
        if n == "GND": seen_gnd += 1
        o.append(f'<rect x="{px-4:.1f}" y="{YB-4:.1f}" width="8" height="8" fill="#fff" stroke="{"#1a211f" if u else "#8a9692"}" stroke-width="{1.6 if u else 0.8}"/>')
        if n:
            o.append(f'<text transform="translate({px+2.6:.1f},{YB-9:.1f}) rotate(-90)" font-family="{FONT}" font-size="7.5" font-weight="{"bold" if u else "normal"}" fill="{"#1a211f" if u else "#66716d"}">{n}</text>')
    return "\n".join(o)

def bread(rails=("5 V", "3,3 V")):
    o = [f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="6" fill="#f7f5ee" stroke="#9c9a8f"/>']
    for key, col in (("T+", "#c8372d"), ("T-", "#2a56b0"), ("B+", "#c8372d"), ("B-", "#2a56b0")):
        y = ROWY[key]
        o.append(f'<line x1="{BX+14}" y1="{y-6.3:.1f}" x2="{BX+BW-14}" y2="{y-6.3:.1f}" stroke="{col}" stroke-width="0.7" opacity=".55"/>')
        for r in RAILROWS:
            o.append(f'<circle cx="{RX(r):.1f}" cy="{y:.1f}" r="2.3" fill="#fff" stroke="#8d8b80" stroke-width=".7"/>')
        o.append(t(BX+6, y+3, "+" if key[1] == "+" else "−", 9, "bold", col))
    for c in "jihgfedcba":
        y = ROWY[c]
        o.append(t(BX+7, y+2.6, c, 7, fill="#77756b"))
        for r in range(1, 31):
            o.append(f'<circle cx="{RX(r):.1f}" cy="{y:.1f}" r="2.3" fill="#fff" stroke="#8d8b80" stroke-width=".7"/>')
    for r in (1, 5, 10, 15, 20, 25, 30):
        o.append(t(RX(r), BY+45, str(r), 6.5, fill="#77756b", anchor="middle"))
        o.append(t(RX(r), ROWY["a"]+11.5, str(r), 6.5, fill="#77756b", anchor="middle"))
    o.append(t(BX+78, BY-5, f"üst hatlar {rails[0]} · alt hatlar {rails[1]}", 8.5, fill="#66716d"))
    o.append(t(BX+4, BY-5, "Breadboard", 10, "bold"))
    return "\n".join(o)

def path(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def along(pts, d):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = abs(x1-x0) + abs(y1-y0)
        if d <= L and L > 0:
            k = d / L
            return x0 + (x1-x0)*k, y0 + (y1-y0)*k
        d -= L
    return pts[-1]

def total(pts):
    return sum(abs(x1-x0) + abs(y1-y0) for (x0, y0), (x1, y1) in zip(pts, pts[1:]))

def wire(k, col, pts, d=(17, 17)):
    c = C[col]
    o = [f'<path d="{path(pts)}" fill="none" stroke="#fff" stroke-width="6.5" stroke-linejoin="round"/>',
         f'<path d="{path(pts)}" fill="none" stroke="{c}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>']
    for p in (pts[0], pts[-1]):
        o.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="3.4" fill="{c}" stroke="#fff" stroke-width="1"/>')
    return "\n".join(o)

def wlabels(k, col, pts, d=(17, 17)):
    T_ = total(pts)
    spots = [along(pts, T_/2)] if T_ < 100 else [along(seq, dd) for seq, dd in ((pts, d[0]), (pts[::-1], d[1])) if dd is not None]
    o = []
    for x, y in spots:
        w = 6.2 * len(k) + 5
        o.append(f'<rect x="{x-w/2:.1f}" y="{y-6:.1f}" width="{w:.1f}" height="12" rx="3" fill="#fff" stroke="{C[col]}" stroke-width="1"/>')
        o.append(t(x, y+3.2, k, 8, "bold", anchor="middle"))
    return "\n".join(o)

def box(x, y, w, h, title, sub=None, fill="#dfe9e6"):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="#7d8a86"/>',
         t(x + w/2, y + h/2 + (0 if sub is None else -3), title, 10, "bold", anchor="middle")]
    if sub: o.append(t(x + w/2, y + h/2 + 10, sub, 8, fill="#66716d", anchor="middle"))
    return "\n".join(o)

def pinmark(x, y, label, side):
    o = [f'<rect x="{x-4:.1f}" y="{y-4:.1f}" width="8" height="8" fill="#fff" stroke="#1a211f" stroke-width="1.4"/>']
    if side == "r":   o.append(t(x+8, y+3, label, 8, "bold"))
    elif side == "l": o.append(t(x-8, y+3, label, 8, "bold", anchor="end"))
    elif side == "d": o.append(t(x, y+15, label, 8, "bold", anchor="middle"))
    return "\n".join(o)

def sensor(xa, label):
    """Kapasitif sensör, pinleri üstte: AOUT, VCC, GND (soldan sağa)."""
    y = 440
    o = [f'<rect x="{xa-13:.1f}" y="{y-6}" width="{25.4+26:.1f}" height="50" rx="4" fill="#dfe9e6" stroke="#7d8a86"/>',
         f'<path d="M{xa-5:.1f},{y+44} V{y+92} L{xa+12.7:.1f},{y+104} L{xa+30.4:.1f},{y+92} V{y+44}" fill="#dfe9e6" stroke="#7d8a86"/>',
         f'<line x1="{xa-5:.1f}" y1="{y+56}" x2="{xa+30.4:.1f}" y2="{y+56}" stroke="#1a211f" stroke-dasharray="3 2" stroke-width=".8"/>']
    for i, n in enumerate(("A", "V", "G")):
        o.append(pinmark(xa + i*12.7, y, n, "d"))
    o.append(t(xa+12.7, y+37, label, 8, "bold", anchor="middle"))
    return "\n".join(o)

def table(rows, notes, y0=566):
    cols = (40, 82, 168, 470, 760)
    o = [f'<line x1="40" y1="{y0+5}" x2="{W-40}" y2="{y0+5}" stroke="#1a211f" stroke-width="1.2"/>']
    for x, h in zip(cols, ("Kablo", "Renk", "Nereden", "Nereye", "Not")):
        o.append(t(x, y0, h, 8.5, "bold", "#66716d"))
    y = y0 + 19
    for k, col, a, b, n in rows:
        if col in C:
            o.append(f'<rect x="{cols[1]}" y="{y-7:.1f}" width="18" height="5" rx="2" fill="{C[col]}"/>')
            o.append(t(cols[1]+23, y, RENK[col], 9.5))
        else:
            o.append(t(cols[1], y, col, 9.5))
        o.append(t(cols[0], y, k, 9.5, "bold"))
        o.append(t(cols[2], y, a, 9.5)); o.append(t(cols[3], y, b, 9.5)); o.append(t(cols[4], y, n, 9, fill="#66716d"))
        o.append(f'<line x1="40" y1="{y+4.5:.1f}" x2="{W-40}" y2="{y+4.5:.1f}" stroke="#d6dcd9" stroke-width=".7"/>')
        y += 14.5
    y += 6
    for n in notes:
        o.append(t(40, y, n, 9.5)); y += 13.5
    return "\n".join(o)

def page(no, total, title, sub, body, used=(), draw=True):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         t(40, 34, title, 18, "bold"), t(40, 52, sub, 10, fill="#66716d"),
         t(W-40, 34, f"Suİz bağlantı şeması · {no}/{total}", 9, fill="#66716d", anchor="end"),
         t(W-40, 48, "15 Kasım 2026 · taslak, parçalarla doğrulanmadı", 8.5, fill="#96560a", anchor="end")]
    if draw: o += [uno(used), bread()]
    o += [body, "</svg>"]
    return "\n".join(o)

def render(wires):
    return "\n".join(wire(*w) for w in wires) + "\n" + "\n".join(wlabels(*w) for w in wires)

ALL = []   # tüm kablo satırları (son sayfa için)
PAGES = []
T = 7

# ---------- Sayfa 2: güç hatları + nem sensörleri ----------
s1, s2 = RX(7), RX(13)
w2 = [
 ("K1", "v33", [U("3V3"), (U("3V3")[0], 402), (RX(3), 402), B("B+", 3)], (17, 52)),
 ("K2", "gnd", [(UX+1600*0.127, YB), (UX+1600*0.127, 390), (RX(2), 390), B("B-", 2)]),
 ("K3", "gnd", [B("B-", 26), B("T-", 26)]),
 ("K4", "v33", [(s1+12.7, 440), B("B+", 8)]),
 ("K5", "gnd", [(s1+25.4, 440), B("B-", 9)], (36, 36)),
 ("K6", "sari", [(s1, 440), (s1, 414), (U("A0")[0], 414), U("A0")], (60, 17)),
 ("K7", "v33", [(s2+12.7, 440), B("B+", 14)]),
 ("K8", "gnd", [(s2+25.4, 440), B("B-", 15)], (36, 36)),
 ("K9", "sari", [(s2, 440), (s2, 426), (U("A1")[0], 426), U("A1")], (40, 36)),
]
r2 = [
 ("K1", "v33", "UNO Q 3V3", "Breadboard alt + hattı, 3. sıra", "alt + hattı artık 3,3 V"),
 ("K2", "gnd", "UNO Q GND (5V'un yanındaki)", "Breadboard alt − hattı, 2. sıra", ""),
 ("K3", "gnd", "Breadboard alt − hattı, 26. sıra", "Breadboard üst − hattı, 26. sıra", "iki GND hattını birleştirir"),
 ("K4", "v33", "Sensör 1 VCC (kırmızı tel)", "alt + hattı, 8. sıra", ""),
 ("K5", "gnd", "Sensör 1 GND (siyah tel)", "alt − hattı, 9. sıra", ""),
 ("K6", "sari", "Sensör 1 AOUT (sarı tel)", "UNO Q A0", "5 cm sensörü"),
 ("K7", "v33", "Sensör 2 VCC (kırmızı tel)", "alt + hattı, 14. sıra", ""),
 ("K8", "gnd", "Sensör 2 GND (siyah tel)", "alt − hattı, 15. sıra", ""),
 ("K9", "sari", "Sensör 2 AOUT (sarı tel)", "UNO Q A1", "ikinci sensör"),
]
n2 = ["Sensör pinleri çizimde A = AOUT, V = VCC, G = GND. Sıra sensörün üstündeki yazıdan okunur; kesik çizginin üstü ıslanmaz.",
      "Kontrol: USB-C takılıyken multimetreyle alt + ile alt − arası 3,3 V; her sensörün AOUT–GND arası havada 1,5–3 V."]
body2 = sensor(s1, "Nem 1") + sensor(s2, "Nem 2") + render(w2) + table(r2, n2)
PAGES.append(page(2, T, "Adım 1 · Güç hatları ve nem sensörleri", "Önce K1–K3 ile hatları kur, sonra sensörleri tak. Kabloları takarken USB-C çekili olsun.", body2, used=("3V3", "GND", "A0", "A1")))
ALL += r2

# ---------- Sayfa 3: pompa, MOSFET kartı, adaptör ----------
jx, jy = 910, 112
mx, my = 922, 180
w3 = [
 ("K10", "v5", [(jx, 126), B("T+", 30)]),
 ("K11", "gnd", [(jx, 138.7), B("T-", 30)]),
 ("K12", "v5", [B("T+", 29), (RX(29), 98), (1078, 98), (1078, 205), (mx+136, 205)], (60, 45)),
 ("K13", "gnd", [B("T-", 28), (RX(28), 86), (1090, 86), (1090, 222), (mx+136, 222)], (30, 130)),
 ("K14", "v5", [(mx+136, 255), (1072, 255), (1072, 340)], (None, 17)),
 ("K15", "gnd", [(mx+136, 272), (1064, 272), (1064, 340)], (None, 40)),
 ("K16", "mavi", [U("D10"), (U("D10")[0], 84), (407, 84), (407, 380), (908, 380), (908, 230), (mx, 230)], (17, 60)),
 ("K17", "gnd", [(mx, 250), (896, 250), (896, 370), (RX(30), 370), B("B-", 30)], (70, 17)),
]
r3 = [
 ("K10", "v5", "Adaptör jakı + klemensi", "Breadboard üst + hattı, 30. sıra", "üst + hattı artık 5 V"),
 ("K11", "gnd", "Adaptör jakı − klemensi", "Breadboard üst − hattı, 30. sıra", ""),
 ("K12", "v5", "üst + hattı, 29. sıra", "MOSFET kartı POWER +", ""),
 ("K13", "gnd", "üst − hattı, 28. sıra", "MOSFET kartı POWER −", ""),
 ("K14", "v5", "MOSFET kartı LOAD +", "Pompa kırmızı teli", ""),
 ("K15", "gnd", "MOSFET kartı LOAD −", "Pompa siyah teli", ""),
 ("K16", "mavi", "UNO Q D10", "MOSFET kartı PWM (tetik) pini", "pompayı açıp kapatan sinyal"),
 ("K17", "gnd", "MOSFET kartı sinyal GND pini", "Breadboard alt − hattı, 30. sıra", ""),
 ("D1", "1N5819", "LOAD + klemensi (diyodun çizgili ucu)", "LOAD − klemensi", "pompa telleriyle aynı klemense"),
 ("C1", "1000 µF", "POWER + klemensi (uzun bacak)", "POWER − klemensi (gri çizgili taraf)", "ters takılmaz"),
]
n3 = ["Önkoşul: Adım 1'deki K2 ve K3 takılı. Adaptörü prize en son tak; önce bağlantıları ikinci bir kişi kontrol etsin.",
      "Pompa yalnızca suyun içindeyken çalıştırılır. Klemens yazıları kartta farklıysa (DC+/DC−, OUT+/OUT−, TRIG) karttaki yazıya uy."]
body3 = (box(jx, jy, 90, 40, "5 V jak", "adaptör girişi") + pinmark(jx, 126, "+", "r") + pinmark(jx, 138.7, "−", "r")
         + f'<rect x="{mx}" y="{my}" width="136" height="110" rx="5" fill="#dfe9e6" stroke="#7d8a86"/>'
         + t(mx+10, my+17, "LR7843 MOSFET kartı", 9.5, "bold")
         + pinmark(mx+136, 205, "POWER +", "l") + pinmark(mx+136, 222, "POWER −", "l")
         + pinmark(mx+136, 255, "LOAD +", "l") + pinmark(mx+136, 272, "LOAD −", "l")
         + pinmark(mx, 230, "PWM", "r") + pinmark(mx, 250, "GND", "r")
         + box(1010, 340, 80, 50, "Pompa", "kovada") + render(w3) + table(r3, n3))
PAGES.append(page(3, T, "Adım 2 · Pompa, MOSFET kartı ve 5 V adaptör", "Pompa akımı UNO Q'dan değil adaptörden gelir; UNO Q yalnızca aç/kapa sinyali verir.", body3, used=("D10",)))
ALL += r3

# ---------- Sayfa 4: şamandıra ----------
w4 = [
 ("K18", "mor", [(930, 235), (896, 235), (896, 380), (407, 380), (407, 84), (U("D4")[0], 84), U("D4")]),
 ("K19", "gnd", [(930, 215), (912, 215), (912, 90), (RX(22), 90), B("T-", 22)]),
]
r4 = [
 ("K18", "mor", "Şamandıra teli 1", "UNO Q D4", "kodda INPUT_PULLUP açılır, direnç gerekmez"),
 ("K19", "gnd", "Şamandıra teli 2", "Breadboard üst − hattı, 22. sıra", "tellerin yönü fark etmez"),
]
n4 = ["Önkoşul: K2 ve K3 takılı. Kontrol: multimetre süreklilik (bip) kademesinde, şamandırayı oynatınca bir konumda bip, diğerinde sessiz."]
body4 = box(930, 195, 90, 60, "Şamandıra", "ZP7510") + pinmark(930, 215, "", "r") + pinmark(930, 235, "", "r") + render(w4) + table(r4, n4)
PAGES.append(page(4, T, "Adım 3 · Şamandıra", "İki tel. Depoda su bitince pompayı kilitleyen anahtar.", body4, used=("D4",)))
ALL += r4

# ---------- Sayfa 5: akış sensörü + bölücü ----------
w5 = [
 ("K20", "v5", [(930, 205), (872, 205), (872, 96), (RX(24), 96), B("T+", 24)]),
 ("K21", "gnd", [(930, 220), (884, 220), (884, 84), (RX(23), 84), B("T-", 23)]),
 ("K22", "sari", [(930, 235), (896, 235), (896, 380), (RX(24), 380), B("a", 24)]),
 ("K23", "yesil", [B("e", 28), (RX(28), 234), (427, 234), (427, 84), (U("D2")[0], 84), U("D2")]),
]
r5 = [
 ("K20", "v5", "YF-S401 kırmızı tel", "Breadboard üst + hattı (5 V), 24. sıra", ""),
 ("K21", "gnd", "YF-S401 siyah tel", "Breadboard üst − hattı, 23. sıra", ""),
 ("K22", "sari", "YF-S401 sarı tel (sinyal)", "Breadboard a24 deliği", "doğrudan UNO Q'ya takılmaz"),
 ("R1", "10 kΩ", "Breadboard c24", "Breadboard c28", "24. sıradan 28. sıraya"),
 ("R2", "20 kΩ", "Breadboard b28", "alt − hattı, 28. sıra", "28. sıradan GND'ye"),
 ("K23", "yesil", "Breadboard e28 (orta nokta)", "UNO Q D2", "5 V darbe burada 3,3 V'a inmiş olur"),
]
n5 = ["Önkoşul: Adım 2'deki K10 ve K11 (5 V hattı) ile K2, K3 takılı. Aynı sıradaki a–e delikleri kendi içinde bağlıdır; bölücü buna dayanır.",
      "Kontrol: K23'ü takmadan önce e28 ile GND arasını ölç. Pervane dönerken 0 V ile yaklaşık 3,3 V arasında gidip gelmeli, 3,4 V'u geçmemeli."]
def resistor(p, q, name):
    (x0, y0), (x1, y1) = p, q
    mxx, myy = (x0+x1)/2, (y0+y1)/2
    horiz = abs(x1-x0) > abs(y1-y0)
    bw, bh = (22, 7) if horiz else (7, 18)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#7a6a4a" stroke-width="1.6"/>'
            f'<rect x="{mxx-bw/2:.1f}" y="{myy-bh/2:.1f}" width="{bw}" height="{bh}" rx="2.5" fill="#d9c08a" stroke="#7a6a4a"/>'
            f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="2.6" fill="#7a6a4a"/><circle cx="{x1:.1f}" cy="{y1:.1f}" r="2.6" fill="#7a6a4a"/>'
            + t(mxx + (0 if horiz else 9), myy + (-7 if horiz else 3), name, 8, "bold", anchor="middle" if horiz else "start"))
body5 = (f'<rect x="930" y="185" width="150" height="65" rx="5" fill="#dfe9e6" stroke="#7d8a86"/>' + t(1072, 213, "YF-S401", 10, "bold", anchor="end") + t(1072, 226, "akış sensörü", 8, fill="#66716d", anchor="end") + pinmark(930, 205, "kırmızı", "r") + pinmark(930, 220, "siyah", "r") + pinmark(930, 235, "sarı", "r")
         + resistor(B("c", 24), B("c", 28), "R1 10k") + resistor(B("b", 28), B("B-", 28), "R2 20k")
         + render(w5) + table(r5, n5))
PAGES.append(page(5, T, "Adım 4 · Akış sensörü ve gerilim bölücü", "Sensör 5 V ile çalışır; sinyali iki dirençle 3,3 V'a indirilir.", body5, used=("D2",)))
ALL += r5

# ---------- Sayfa 6: DHT22 ----------
dx = RX(19)
w6 = [
 ("K24", "v33", [(dx+12.7, 440), B("B+", 20)]),
 ("K25", "gnd", [(dx+25.4, 440), B("B-", 21)], (36, 36)),
 ("K26", "gri", [(dx, 440), (dx, 414), (397, 414), (397, 84), (U("D12")[0], 84), U("D12")], (60, 17)),
]
r6 = [
 ("K24", "v33", "DHT22 modülü + pini", "Breadboard alt + hattı (3,3 V), 20. sıra", ""),
 ("K25", "gnd", "DHT22 modülü − pini", "Breadboard alt − hattı, 21. sıra", ""),
 ("K26", "gri", "DHT22 modülü out pini", "UNO Q D12", "pull-up direnci modülün üzerinde"),
]
n6 = ["Önkoşul: Adım 1'deki K1 ve K2 takılı. Pin sırası modülden modüle değişir; +, out, − yazılarını modülün üzerinden oku."]
body6 = (f'<rect x="{dx-13:.1f}" y="434" width="51.4" height="70" rx="4" fill="#dfe9e6" stroke="#7d8a86"/>'
         + pinmark(dx, 440, "out", "d") + pinmark(dx+12.7, 440, "+", "d") + pinmark(dx+25.4, 440, "−", "d")
         + t(dx+12.7, 484, "DHT22", 9, "bold", anchor="middle") + render(w6) + table(r6, n6))
PAGES.append(page(6, T, "Adım 5 · DHT22 sıcaklık ve nem modülü", "Üç tel. Kütüphane UNO Q'da çalışmazsa bu adım atlanır.", body6, used=("D12",)))
ALL += r6

# ---------- Sayfa 1: genel bakış ----------
chk = [
 ("UNO Q", "USB-C solda. Üst kenar soldan: SCL, SDA, AREF, GND, D13…D8, boşluk, D7…D0. Alt kenar: IOREF, RESET, 3V3, 5V, GND, GND, VIN, boşluk, A0…A5."),
 ("Breadboard", "30 sıralı, a–e ve f–j delikli. Kenardaki + ve − hatları boydan boya tek parça (uzun breadboard'larda ortadan bölünür)."),
 ("Nem sensörü", "Üç telli kablo: siyah GND, kırmızı VCC, sarı AOUT."),
 ("MOSFET kartı", "Dört vidalı klemens: POWER +, POWER −, LOAD +, LOAD −. İki pin: PWM ve GND."),
 ("Adaptör jakı", "İki vidalı klemens, + ve − işaretli. Adaptör fişinin iç ucu +."),
 ("YF-S401", "Üç tel: kırmızı 5 V, siyah GND, sarı sinyal. Gövdede akış yönünü gösteren ok."),
 ("Şamandıra", "İki tel, yönü yok."),
 ("DHT22 modülü", "Üç pin: +, out, −."),
]
b1 = [t(880, 126, "Renk kuralı", 11, "bold")]
yy = 146
for key, txt in (("v33", "3,3 V (UNO Q'dan)"), ("v5", "5 V (adaptörden)"), ("gnd", "GND"), ("sari", "sensör sinyali"), ("mavi", "pompa tetiği"), ("mor", "şamandıra"), ("yesil", "akış darbesi"), ("gri", "DHT22 verisi")):
    b1.append(f'<rect x="880" y="{yy-7}" width="26" height="5" rx="2" fill="{C[key]}"/>'); b1.append(t(914, yy, txt, 9.5)); yy += 16
b1 += [t(880, yy+14, "Okuma kuralı", 11, "bold"),
       t(880, yy+32, "Her kablonun iki ucunda aynı", 9.5), t(880, yy+46, "etiket var (K1, K2…). Tabloda", 9.5),
       t(880, yy+60, "aynı etiketle bulunur.", 9.5),
       t(880, yy+82, "Breadboard deliği: harf + sıra", 9.5), t(880, yy+96, "numarası, örneğin a24.", 9.5)]
b1 += [t(40, 420, "Çizimde varsayılanlar: elindeki parçada farklıysa bildir", 12, "bold"),
       f'<line x1="40" y1="428" x2="{W-40}" y2="428" stroke="#1a211f" stroke-width="1.2"/>']
yy = 446
for a, bb_ in chk:
    b1.append(t(40, yy, a, 9.5, "bold")); b1.append(t(168, yy, bb_, 9.5))
    b1.append(f'<line x1="40" y1="{yy+5}" x2="{W-40}" y2="{yy+5}" stroke="#d6dcd9" stroke-width=".7"/>'); yy += 17
b1 += [t(40, yy+14, "Kullanılan UNO Q pinleri: 3V3, GND, A0, A1 (nem), D2 (akış), D4 (şamandıra), D10 (pompa), D12 (DHT22). Test kılavuzundaki kodlarla aynı pinler.", 9.5),
       t(40, yy+30, "Güç: üst hatlar 5 V adaptörden, alt hatlar UNO Q'nun 3,3 V'undan. İki − hattı K3 ile birleşir; bu olmadan pompa ve akış sensörü çalışmaz.", 9.5),
       t(40, yy+46, "A0–A5 pinlerine 3,3 V'tan fazlası verilmez. Her adımda kabloları güç yokken tak, güç vermeden önce tabloyla karşılaştır.", 9.5)]
PAGES.insert(0, page(1, T, "Genel bakış", "Tek otomatik yatak: 2 nem sensörü, pompa, şamandıra, akış sensörü, DHT22. Her adım kendi sayfasında.", "\n".join(b1),
                     used=("3V3", "GND", "A0", "A1", "D2", "D4", "D10", "D12")))

# ---------- Sayfa 7: tüm kablolar ----------
cols = (40, 82, 168, 470, 760)
b7 = [f'<line x1="40" y1="79" x2="{W-40}" y2="79" stroke="#1a211f" stroke-width="1.2"/>']
for x, h in zip(cols, ("Kablo", "Renk", "Nereden", "Nereye", "Not")): b7.append(t(x, 74, h, 8.5, "bold", "#66716d"))
yy = 94
for k, col, a, b_, n in ALL:
    if col in C:
        b7.append(f'<rect x="{cols[1]}" y="{yy-7}" width="18" height="5" rx="2" fill="{C[col]}"/>'); b7.append(t(cols[1]+23, yy, RENK[col], 9.5))
    else: b7.append(t(cols[1], yy, col, 9.5))
    b7 += [t(cols[0], yy, k, 9.5, "bold"), t(cols[2], yy, a, 9.5), t(cols[3], yy, b_, 9.5), t(cols[4], yy, n, 9, fill="#66716d"),
           f'<line x1="40" y1="{yy+5}" x2="{W-40}" y2="{yy+5}" stroke="#d6dcd9" stroke-width=".7"/>']
    yy += 20
PAGES.append(page(7, T, "Tüm bağlantılar", "Takılan her kabloyu bu listeden işaretle.", "\n".join(b7), draw=False))

out = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(out, exist_ok=True)
for i, p in enumerate(PAGES, 1):
    open(f"{out}/p{i}.svg", "w", encoding="utf-8").write(p)
print(len(PAGES), "sayfa,", len(ALL), "satır")
