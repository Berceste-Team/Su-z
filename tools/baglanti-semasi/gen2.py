#!/usr/bin/env python3
"""Suİz iki yataklı tam sistem: Elektrik + Yerleşim görünümü, web sayfası ve PDF."""
import os, html as H_
here = os.path.dirname(os.path.abspath(__file__))
src = open(f"{here}/gen.py", encoding="utf-8").read()
src = src[:src.index("ALL = []")]
src = src.replace("UX, UY, UW, UH = 40, 110, 343, 266.7", "UX, UY, UW, UH = 40, 170, 343, 266.7")
src = src.replace("BX, BY, BW, BH = 440, 110, 412, 248", "BX, BY, BW, BH = 440, 170, 412, 248")
src = src.replace("    y = 440\n", "    y = 520\n")
src = src.replace('o.append(t(BX+78, BY-5, f"üst hatlar {rails[0]} · alt hatlar {rails[1]}", 8.5, fill="#66716d"))',
                  'o.append(t(BX-4, ROWY["T+"]+9, "5 V", 8, "bold", "#c8372d", "end")); o.append(t(BX+BW+5, ROWY["B+"]+9, "3,3 V", 8, "bold", "#e07b00"))')
exec(src)

W, H = 1200, 650
STEPS = {1: "Güç hatları ve nem sensörleri", 2: "Pompalar, MOSFET kartları, adaptör", 3: "Şamandıralar", 4: "Akış sensörleri ve bölücüler", 5: "DHT22"}
TP, TM, BP, BM = ROWY["T+"], ROWY["T-"], ROWY["B+"], ROWY["B-"]
ma, mb = (960, 156), (960, 312)          # MOSFET A ve B kutuları (116 x 88)
MW = 116

WIRES, ROWS = [], []
_n = [0]
def K(step, col, pts, a, b, note="", d=(17, 17), g="guc", e=("pin", "pin")):
    _n[0] += 1
    k = f"K{_n[0]}"
    WIRES.append((k, step, col, pts, d, g, e)); ROWS.append((k, step, col, a, b, note, g))
    return k
def X(name, step, what, a, b, note="", g="guc"):
    ROWS.append((name, step, what, a, b, note, g))

# ---- Adım 1: güç hatları ve nem sensörleri ----
K(1, "v33", [U("3V3"), (U("3V3")[0], 466), (RX(3), 466), B("B+", 3)], "UNO Q 3V3", "alt + hattı, 3. sıra", "alt + hattı artık 3,3 V", (17, 60))
K(1, "gnd", [(UX+1600*0.127, YB), (UX+1600*0.127, 456), (RX(2), 456), B("B-", 2)], "UNO Q GND (5V'un yanındaki)", "alt − hattı, 2. sıra", "", (17, 38))
K(1, "gnd", [B("B-", 23), B("T-", 23)], "alt − hattı, 23. sıra", "üst − hattı, 23. sıra", "iki GND hattını birleştirir", (40, 40))
SENS = [("A1", 7, "A0", 415, 304, 446), ("A2", 13, "A1", 407, 297, 441), ("B1", 19, "A2", 399, 290, 436), ("B2", 25, "A3", 391, 283, 431)]
for i, (nm, r, pin, lane, gy, yb) in enumerate(SENS):
    g = "nem" + nm; px = U(pin)[0]
    K(1, "v33", [(RX(r+1), 520), B("B+", r+1)], f"Nem {nm} VCC (kırmızı tel)", f"alt + hattı, {r+1}. sıra", "", (32, None), g)
    K(1, "gnd", [(RX(r+2), 520), B("B-", r+2)], f"Nem {nm} GND (siyah tel)", f"alt − hattı, {r+2}. sıra", "", (50, None), g)
    K(1, "sari", [(RX(r), 520), B("a", r)], f"Nem {nm} AOUT (sarı tel)", f"Breadboard a{r} deliği", "", (14, None), g)
    K(1, "sari", [B("e", r), (RX(r), gy), (lane, gy), (lane, yb), (px, yb), (px, YB)], f"Breadboard e{r} deliği", f"UNO Q {pin}",
      f"Yatak {nm[0]}, {'5' if nm[1]=='1' else '10'} cm sensörü", (44 + i*4, (yb-YB) + (lane-px) + 26 + i*17), g)

# ---- Adım 2: pompalar ----
K(2, "v5", [(RX(27), 150), B("T+", 27)], "Adaptör jakı + klemensi", "üst + hattı, 27. sıra", "üst + hattı artık 5 V", (9, None), e=('vida', 'pin'))
K(2, "gnd", [(RX(26), 150), B("T-", 26)], "Adaptör jakı − klemensi", "üst − hattı, 26. sıra", "", (30, None), e=('vida', 'pin'))
# LR7843 kartı üç klemenslidir (−, LOAD, +): + ve − adaptörden gelir, pompa + ile LOAD arasına bağlanır;
# kart pompanın eksi tarafını anahtarlar. Çizimde klemens sırası +, −, LOAD (kablolar kesişmesin diye).
K(2, "v5", [B("T+", 30), (ma[0], TP)], "üst + hattı, 30. sıra", "MOSFET A + klemensi", "", (40, None), "pompaA", e=('pin', 'vida'))
K(2, "gnd", [B("T-", 30), (ma[0], TM)], "üst − hattı, 30. sıra", "MOSFET A − klemensi", "", (66, None), "pompaA", e=('pin', 'vida'))
K(2, "v5", [B("T+", 29), (RX(29), 166), (884, 166), (884, mb[1]+30), (mb[0], mb[1]+30)], "üst + hattı, 29. sıra", "MOSFET B + klemensi", "", (44, 24), "pompaB", e=('pin', 'vida'))
K(2, "gnd", [B("B-", 30), (RX(30), 436), (900, 436), (900, mb[1]+42.7), (mb[0], mb[1]+42.7)], "alt − hattı, 30. sıra", "MOSFET B − klemensi", "K3 üzerinden adaptöre döner", (52, 24), "pompaB", e=('pin', 'vida'))
for _nm, _m, _py in (("A", ma, 264), ("B", mb, 420)):
    K(2, "v5", [(960, _py+27), (936, _py+27), (936, _m[1]+30), (_m[0], _m[1]+30)], f"Pompa {_nm} kırmızı teli", f"MOSFET {_nm} + klemensi", "ya da doğrudan üst + hattına", (40, None), "pompa"+_nm, e=('ek', 'vida'))
    K(2, "gnd", [(960, _py+13), (948, _py+13), (948, _m[1]+68), (_m[0], _m[1]+68)], f"Pompa {_nm} siyah teli", f"MOSFET {_nm} LOAD klemensi", "", (36, None), "pompa"+_nm, e=('ek', 'vida'))
K(2, "mavi", [U("D10"), (U("D10")[0], 28), (1100, 28), (1100, ma[1]+40), (ma[0]+MW, ma[1]+40)], "UNO Q D10", "MOSFET A PWM", "Pompa A sinyali", (17, 40), "pompaA")
K(2, "mavi", [U("D11"), (U("D11")[0], 16), (1190, 16), (1190, mb[1]+70), (mb[0]+MW, mb[1]+70)], "UNO Q D11", "MOSFET B PWM", "Pompa B sinyali", (36, 60), "pompaB")
K(2, "gnd", [(ma[0]+MW, ma[1]+70), (1136, ma[1]+70), (1136, 486), (RX(28), 486), B("B-", 28)], "MOSFET A GND (PWM'in yanındaki)", "alt − hattı, 28. sıra", "", (36, 17), "pompaA")
K(2, "gnd", [(mb[0]+MW, mb[1]+40), (1124, mb[1]+40), (1124, 474), (RX(29), 474), B("B-", 29)], "MOSFET B GND (PWM'in yanındaki)", "alt − hattı, 29. sıra", "", (30, 40), "pompaB")
X("D1", 2, "1N5819", "MOSFET A + klemensi (çizgili uç)", "MOSFET A LOAD klemensi", "pompa telleriyle aynı klemenslere", "pompaA")
X("D2", 2, "1N5819", "MOSFET B + klemensi (çizgili uç)", "MOSFET B LOAD klemensi", "pompa telleriyle aynı klemenslere", "pompaB")
X("C1", 2, "1000 µF", "üst + hattı, 12. sıra (uzun bacak)", "üst − hattı, 12. sıra", "ters takılmaz")
X("C2", 2, "1000 µF", "üst + hattı, 21. sıra (uzun bacak)", "üst − hattı, 21. sıra", "ters takılmaz")

# ---- Adım 3: şamandıralar ----
K(3, "mor", [(940, 72), (U("D4")[0], 72), U("D4")], "Şamandıra A teli 1", "UNO Q D4", "kodda INPUT_PULLUP", (17, 17), "samA", e=('ek', 'pin'))
K(3, "gnd", [(940, 84), (RX(24), 84), B("T-", 24)], "Şamandıra A teli 2", "üst − hattı, 24. sıra", "", (48, 30), "samA", e=('ek', 'pin'))
K(3, "mor", [(940, 44), (U("D5")[0], 44), U("D5")], "Şamandıra B teli 1", "UNO Q D5", "kodda INPUT_PULLUP", (17, 36), "samB", e=('ek', 'pin'))
K(3, "gnd", [(940, 56), (RX(22), 56), B("T-", 22)], "Şamandıra B teli 2", "üst − hattı, 22. sıra", "", (48, 52), "samB", e=('ek', 'pin'))

# ---- Adım 4: akış sensörleri ----
for nm, r0, rt, pin, cy, dd in (("A", 8, 13, "D2", 110, 17), ("B", 15, 19, "D3", 98, 36)):
    g = "akis" + nm
    K(4, "v5", [(RX(r0), 150), B("T+", r0)], f"Akış {nm} kırmızı tel", f"üst + hattı (5 V), {r0}. sıra", "JST konnektöre erkek jumper", (8, None), g)
    K(4, "gnd", [(RX(r0+1), 150), B("T-", r0+1)], f"Akış {nm} siyah tel", f"üst − hattı, {r0+1}. sıra", "", (30, None), g)
    K(4, "sari", [(RX(r0+2), 150), B("j", r0+2)], f"Akış {nm} sarı tel (sinyal)", f"Breadboard j{r0+2} deliği", "doğrudan UNO Q'ya takılmaz", (56, None), g)
    X(f"R1{nm}", 4, "10 kΩ", f"Breadboard h{r0+2}", f"Breadboard h{rt}", f"{r0+2}. sıradan {rt}. sıraya", g)
    X(f"R2{nm}", 4, "20 kΩ", f"Breadboard i{rt}", f"üst − hattı, {rt+1}. sıra", f"{rt}. sıradan GND'ye", g)
    K(4, "yesil", [B("j", rt), (RX(rt), cy), (U(pin)[0], cy), U(pin)], f"Breadboard j{rt} (orta nokta)", f"UNO Q {pin}", "darbe burada 3,3 V'a inmiş olur", (40, dd + 18), g)

# ---- Adım 5: DHT22 ----
K(5, "v33", [(RX(4), 520), B("B+", 4)], "DHT22 + pini", "alt + hattı (3,3 V), 4. sıra", "", (32, None), "dht")
K(5, "gnd", [(RX(5), 520), B("B-", 5)], "DHT22 − pini", "alt − hattı, 5. sıra", "", (50, None), "dht")
K(5, "gri", [(RX(3), 520), (RX(3), 512), (16, 512), (16, 140), (U("D12")[0], 140), U("D12")], "DHT22 out pini", "UNO Q D12", "", (60, 17), "dht")

NOTES = {
 1: ["Her nem sensörünün üç teli breadboard'a girer: VCC ve GND alt hatlara, AOUT a sırasına. Aynı sıranın e deliğinden çıkan kablo sinyali UNO Q'ya taşır.",
     "Kontrol: USB-C takılıyken alt + ile alt − arası 3,3 V; her sensörün AOUT–GND arası havada 1,5–3 V. A0–A5'e 3,3 V'tan fazlası verilmez.",
     "Oje: sensör toprağa girmeden önce kartın kesik kenarlarına şeffaf oje sür, kurumasını bekle; üstteki elektronik kısmı oje ya da makaronla koru. Ojesiz kenar nem çeker ve okuma kayar."],
 2: ["Önkoşul: güç hatları kurulu. Adaptörü prize en son tak; pompalar yalnızca suyun içindeyken çalıştırılır.",
     "MOSFET kartı üç klemenslidir (+, LOAD, −): pompa + ile LOAD arasına bağlanır. Yazılar kartın arka yüzündedir; çizimdeki klemens sırası temsilidir, yazıya uy.",
     "Pompadan önce test: yalnızca adaptör bağlıyken + ile LOAD arası 0 V; PWM'e 3,3 V verince yaklaşık 5 V ve kart LED'i yanar."],
 3: ["Kontrol: multimetre süreklilik kademesinde, şamandırayı oynatınca bir konumda bip, diğerinde sessiz. Tellerin yönü fark etmez."],
 4: ["Akış sensörünün telleri 3'lü dişi JST konnektörle biter (sıra: sarı, siyah, kırmızı). Erkek jumper konnektöre doğrudan girer; lehim gerekmez, bantla sabitle.",
     "Aynı sıradaki f–j delikleri kendi içinde bağlıdır; bölücü buna dayanır. Sarı tel hiçbir zaman doğrudan UNO Q'ya takılmaz.",
     "Kontrol: yeşil kabloyu takmadan önce orta nokta ile GND arasını ölç; pervane dönerken 0 V ile yaklaşık 3,3 V arası, 3,4 V'u geçmemeli."],
 5: ["Pin sırası modülden modüle değişir; +, out, − yazılarını modülün üzerinden oku."],
}

def resistor(p, q, name):
    (x0, y0), (x1, y1) = p, q
    mxx, myy = (x0+x1)/2, (y0+y1)/2
    horiz = abs(x1-x0) > abs(y1-y0)
    bw, bh = (20, 7) if horiz else (7, 14)
    return (f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#7a6a4a" stroke-width="1.6"/>'
            f'<rect x="{mxx-bw/2:.1f}" y="{myy-bh/2:.1f}" width="{bw}" height="{bh}" rx="2.5" fill="#d9c08a" stroke="#7a6a4a"/>'
            f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="2.6" fill="#7a6a4a"/><circle cx="{x1:.1f}" cy="{y1:.1f}" r="2.6" fill="#7a6a4a"/>'
            + t(mxx + (0 if horiz else 8), myy + (11.5 if horiz else 3), name, 7, "bold", anchor="middle" if horiz else "start"))

def cap(r, name):
    x = RX(r)
    return (f'<line x1="{x:.1f}" y1="{TP}" x2="{x:.1f}" y2="{TM}" stroke="#44506a" stroke-width="1.6"/>'
            f'<circle cx="{x:.1f}" cy="{(TP+TM)/2:.1f}" r="5" fill="#5d6f96" stroke="#2c3550"/>'
            f'<circle cx="{x:.1f}" cy="{TP}" r="2.6" fill="#2c3550"/><circle cx="{x:.1f}" cy="{TM}" r="2.6" fill="#2c3550"/>'
            + t(x, TM+12.5, name, 7, "bold", anchor="middle"))

def diode(x, y0, y1, name):
    my_ = (y0+y1)/2
    return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="#333" stroke-width="1.4"/>'
            f'<path d="M{x-4},{my_+4} L{x+4},{my_+4} L{x},{my_-3} Z" fill="#333"/><line x1="{x-4}" y1="{my_-3}" x2="{x+4}" y2="{my_-3}" stroke="#333" stroke-width="1.8"/>'
            + t(x, y1+11, name, 7, "bold", anchor="middle"))

def mosfet(x, y, nm, dname, pwm_top):
    # Sol kenar: +, −, LOAD klemensleri. Sağ kenar: PWM ve GND. Diyot + ile LOAD arasında, çizgili ucu +'da.
    sig = [pinmark(x+MW, y+40, "PWM" if pwm_top else "GND", "l"), pinmark(x+MW, y+70, "GND" if pwm_top else "PWM", "l")]
    o = [f'<rect x="{x}" y="{y}" width="{MW}" height="88" rx="5" fill="#dfe9e6" stroke="#7d8a86"/>',
         t(x+MW/2, y+11, f"MOSFET {nm} · LR7843", 8, "bold", anchor="middle"),
         pinmark(x, y+30, "+", "r"), pinmark(x, y+42.7, "−", "r"), pinmark(x, y+68, "LOAD", "r"),
         *sig, diode(x+MW//2, y+32, y+66, dname)]
    return "\n".join(o)

def parts():
    o = [uno(("3V3", "GND", "A0", "A1", "A2", "A3", "D2", "D3", "D4", "D5", "D10", "D11", "D12")), bread()]
    for nm, r, *_ in SENS: o.append(sensor(RX(r), "Nem " + nm))
    dx = RX(3)
    o += [f'<rect x="{dx-13:.1f}" y="514" width="51.4" height="70" rx="4" fill="#dfe9e6" stroke="#7d8a86"/>',
          pinmark(dx, 520, "out", "d"), pinmark(dx+12.7, 520, "+", "d"), pinmark(dx+25.4, 520, "−", "d"), t(dx+12.7, 564, "DHT22", 9, "bold", anchor="middle"),
          f'<rect x="{RX(26)-14:.1f}" y="112" width="36" height="44" rx="4" fill="#dfe9e6" stroke="#7d8a86"/>',
          t(RX(26)+4, 126, "5 V jak", 7.5, "bold", anchor="middle"), pinmark(RX(26), 150, "", "d"), pinmark(RX(27), 150, "", "d"),
          t(RX(26), 142, "−", 9, "bold", anchor="middle"), t(RX(27), 142, "+", 9, "bold", anchor="middle")]
    for nm, r0 in (("A", 8), ("B", 15)):
        o += [f'<rect x="{RX(r0)-14:.1f}" y="122" width="53.4" height="34" rx="4" fill="#dfe9e6" stroke="#7d8a86"/>',
              t(RX(r0+1), 135, f"Akış {nm}", 8, "bold", anchor="middle"), pinmark(RX(r0), 150, "", "d"), pinmark(RX(r0+1), 150, "", "d"), pinmark(RX(r0+2), 150, "", "d")]
    o += [mosfet(*ma, "A", "D1", True), mosfet(*mb, "B", "D2", False),
          box(960, 264, 90, 40, "Pompa A"), pinmark(960, 277, "", "r"), pinmark(960, 291, "", "r"),
          box(960, 420, 90, 40, "Pompa B"), pinmark(960, 433, "", "r"), pinmark(960, 447, "", "r"),
          box(940, 64, 96, 30, "Şamandıra A"), pinmark(940, 72, "", "r"), pinmark(940, 84, "", "r"),
          box(940, 32, 96, 30, "Şamandıra B"), pinmark(940, 44, "", "r"), pinmark(940, 56, "", "r"),
          resistor(B("h", 10), B("h", 13), "R1A"), resistor(B("i", 13), B("T-", 14), "R2A"),
          resistor(B("h", 17), B("h", 19), "R1B"), resistor(B("i", 19), B("T-", 20), "R2B"),
          cap(12, "C1"), cap(21, "C2"), legend_marks()]
    return "\n".join(o)

import math
def marker(x, y, kind, c):
    if kind == "vida":
        return f'<rect x="{x-4.2:.1f}" y="{y-4.2:.1f}" width="8.4" height="8.4" fill="{c}" stroke="#fff" stroke-width="1.2"/>'
    if kind == "ek":
        p = []
        for i in range(10):
            r = 7.2 if i % 2 == 0 else 3.1
            a = -math.pi/2 + i * math.pi/5
            p.append(f"{x + r*math.cos(a):.1f},{y + r*math.sin(a):.1f}")
        return f'<polygon points="{" ".join(p)}" fill="{c}" stroke="#fff" stroke-width="1.1"/>'
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{c}" stroke="#fff" stroke-width="1"/>'

def wire2(col, pts, e):
    c = C[col]
    return (f'<path d="{path(pts)}" fill="none" stroke="#fff" stroke-width="6.5" stroke-linejoin="round"/>'
            f'<path d="{path(pts)}" fill="none" stroke="{c}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>'
            + marker(*pts[0], e[0], c) + marker(*pts[-1], e[1], c))

def legend_marks():
    x, y = 44, 566
    o = [f'<rect x="{x-12}" y="{y-22}" width="392" height="88" rx="4" fill="#fff" stroke="#d6dcd9"/>', t(x, y-6, "Uçtaki işaret bağlantı biçimini gösterir", 9.5, "bold")]
    for i, (kind, txt) in enumerate((("pin", "Yuvarlak: takılır. Jumper ucu deliğe ya da pine girer, alet gerekmez."),
                                     ("vida", "Kare: vidalı klemens. Telin ucu soyulur, tornavidayla sıkılır."),
                                     ("ek", "Yıldız: ek yeri. Parçanın kendi teli uzatılır: lehim ya da geçmeli klemens, üstüne makaron."))):
        yy = y + 12 + i*18
        o.append(marker(x+4, yy-3, kind, "#1a211f")); o.append(t(x+18, yy, txt, 8.5))
    return "\n".join(o)

def wlab(k, col, pts, d):
    if d[1] is None: spots = [along(pts, d[0])]
    elif d[0] is None: spots = [along(pts[::-1], d[1])]
    else: spots = [along(pts, d[0]), along(pts[::-1], d[1])]
    o = []
    for x, y in spots:
        w = 6.2 * len(k) + 5
        o.append(f'<rect x="{x-w/2:.1f}" y="{y-6:.1f}" width="{w:.1f}" height="12" rx="3" fill="#fff" stroke="{C[col]}" stroke-width="1"/>')
        o.append(t(x, y+3.2, k, 8, "bold", anchor="middle"))
    return "\n".join(o)

def wires_svg(only=None, web=False):
    a, b = [], []
    for k, s, col, pts, d, g, e in WIRES:
        if only and s != only: continue
        at = f' data-k="{k}" data-s="{s}" data-g="{g}"' if web else ""
        a.append(f'<g class="w"{at}>' + wire2(col, pts, e) + "</g>")
        b.append(f'<g class="wl"{at}>' + wlab(k, col, pts, d) + "</g>")
    return "\n".join(a + b)

# ================= Yerleşim görünümü =================
LW, LH = 1200, 560
LY0 = 160
def layout(web=False):
    def nm_of(g):
        if g.startswith("nem"): return f"Nem sensörü {g[3:]}"
        if g.startswith("pompa"): return f"Pompa {g[5:]}"
        if g.startswith("sam"): return f"Şamandıra {g[3:]}"
        if g.startswith("akis"): return f"Akış sensörü {g[4:]} (YF-S401)"
        return {"dht": "DHT22 sıcaklık ve nem modülü", "buat": "Buat: UNO Q ve breadboard"}[g]
    def grp(g, body):
        return f'<g class="ph" data-g="{g}" data-n="{nm_of(g)}" data-h="{"Tıkla: Elektrik görünümünü aç" if g == "buat" else "Tıkla: kablolarını göster"}">{body}</g>' if web else body
    def tip(n, body): return f'<g class="tp" data-n="{n}">{body}</g>' if web else body
    def num(x, y, n):
        return f'<circle cx="{x}" cy="{y}" r="8" fill="#1a211f"/>' + t(x, y+3.2, str(n), 8.5, "bold", "#fff", "middle")
    o = [f'<rect y="{LY0}" width="{LW}" height="{LH-LY0}" fill="#fff"/>',
         # sifon çizgisi
         f'<line x1="14" y1="303" x2="{LW-14}" y2="303" stroke="#1f6fd1" stroke-width="1" stroke-dasharray="6 4" opacity=".7"/>',
         t(600, 178, "Kesik mavi çizgi hortumun çıkış seviyesidir: kovalardaki su hep bu çizginin altında kalmalı.", 9.5, fill="#1f6fd1", anchor="middle"),
         # masa
         f'<rect x="150" y="404" width="900" height="12" fill="#c9b79a" stroke="#8f7f63"/>',
         f'<rect x="170" y="416" width="12" height="130" fill="#c9b79a" stroke="#8f7f63"/><rect x="1018" y="416" width="12" height="130" fill="#c9b79a" stroke="#8f7f63"/>',
         t(600, 448, "balkon masası (duvar tarafı arkada)", 9, fill="#66716d", anchor="middle")]
    for nm, x0, kx, side in (("A", 210, 30, 1), ("B", 710, 1090, -1)):
        # saksı
        o += [f'<rect x="{x0-10}" y="398" width="300" height="6" fill="#b9c4c0" stroke="#7d8a86"/>',
              f'<path d="M{x0},290 H{x0+280} L{x0+270},398 H{x0+10} Z" fill="#eef2f0" stroke="#7d8a86"/>',
              f'<path d="M{x0+1.5},306 H{x0+278.5} L{x0+270},398 H{x0+10} Z" fill="#b89b7a" opacity=".75"/>',
              t(x0+140, 384, f"Yatak {nm} · {'zamanlayıcı (kontrol)' if nm == 'A' else 'Suİz'}", 10, "bold", "#fff", "middle")]
        for sx in range(x0+30, x0+260, 22):
            o.append(f'<path d="M{sx},305 q-5,-12 -9,-12 M{sx},305 q4,-14 9,-13" fill="none" stroke="#2b8a3e" stroke-width="1.6" stroke-linecap="round"/>')
        # nem sensörleri
        for j, sx in enumerate((x0+70, x0+210), 1):
            body = (f'<path d="M{sx-8},258 H{sx+8} V352 L{sx},364 L{sx-8},352 Z" fill="#2f3a36" stroke="#111"/>'
                    f'<rect x="{sx-10}" y="246" width="20" height="26" rx="2" fill="#dfe9e6" stroke="#7d8a86"/>'
                    f'<line x1="{sx-12}" y1="300" x2="{sx+12}" y2="300" stroke="#fff" stroke-width="1.2"/>'
                    + t(sx, 240, f"Nem {nm}{j}", 8.5, "bold", anchor="middle"))
            o.append(grp(f"nem{nm}{j}", body))
        # kova + sandalye
        bx = kx
        o += [f'<rect x="{bx-12}" y="500" width="104" height="8" fill="#c9b79a" stroke="#8f7f63"/><rect x="{bx-6}" y="508" width="8" height="40" fill="#c9b79a" stroke="#8f7f63"/><rect x="{bx+78}" y="508" width="8" height="40" fill="#c9b79a" stroke="#8f7f63"/>',
              tip(f"Kova {nm} (su deposu)", f'<path d="M{bx},372 H{bx+80} L{bx+74},500 H{bx+6} Z" fill="#f4f6f5" stroke="#7d8a86"/><path d="M{bx+1.6},404 H{bx+78.4} L{bx+74},500 H{bx+6} Z" fill="#9cc4ee" opacity=".65"/>'),
              t(bx+40 + side*14, 394, f"Kova {nm}", 8.5, "bold", anchor="middle")]
        ppx = bx + (14 if side == 1 else 36); fpx = bx + (54 if side == 1 else 14)
        o.append(grp(f"pompa{nm}", f'<rect x="{ppx}" y="474" width="30" height="22" rx="3" fill="#44506a" stroke="#222"/>' + t(ppx+15, 488, "P", 9, "bold", "#fff", "middle")))
        o.append(grp(f"sam{nm}", f'<rect x="{fpx}" y="464" width="12" height="20" rx="3" fill="#fff" stroke="#7a3fb5" stroke-width="1.6"/><line x1="{fpx+6}" y1="484" x2="{fpx+6}" y2="496" stroke="#7a3fb5" stroke-width="1.6"/>' + t(fpx+6, 458, "Ş", 8, "bold", "#7a3fb5", "middle")))
        # hortum hattı: pompa → yukarı → yatay → saksı ortası
        hx = ppx + 15; tx = x0 + 140; hy = 200
        xs = sorted((hx, tx)); d = 1 if tx > hx else -1
        o += [f'<path d="M{hx},474 V{hy} H{tx} V300" fill="none" stroke="#3a7fc4" stroke-width="5" stroke-linejoin="round"/>',
              f'<path d="M{hx},474 V{hy} H{tx} V300" fill="none" stroke="#cfe3f7" stroke-width="2" stroke-linejoin="round"/>',
              tip(f"Delikli hortum {nm}", f'<path d="M{x0+40},302 H{x0+240}" fill="none" stroke="#3a7fc4" stroke-width="4" stroke-dasharray="2 9" stroke-linecap="round"/><path d="M{x0+40},302 H{x0+240}" fill="none" stroke="#3a7fc4" stroke-width="1.5"/><path d="M{x0+40},302 H{x0+240}" fill="none" stroke="#000" stroke-opacity="0" stroke-width="12"/>')]
        fx = hx + d*70; rx_ = hx + d*122; cx = hx + d*160
        o.append(grp(f"akis{nm}", f'<rect x="{fx-22}" y="{hy-12}" width="44" height="24" rx="4" fill="#dfe9e6" stroke="#1a211f"/><path d="M{fx-d*10},{hy} H{fx+d*10} m{-d*5},-4 l{d*5},4 l{-d*5},4" fill="none" stroke="#1a211f" stroke-width="1.6"/>'))
        o += [tip(f"Çekvalf {nm}", f'<rect x="{cx-13}" y="{hy-8}" width="26" height="16" rx="3" fill="#fff" stroke="#1a211f"/><path d="M{cx-d*7},{hy} H{cx+d*7} m{-d*4},-3.5 l{d*4},3.5 l{-d*4},3.5" fill="none" stroke="#1a211f" stroke-width="1.4"/>'),
              tip(f"T-parça {nm}", f'<circle cx="{tx}" cy="300" r="6" fill="#fff" stroke="#1a211f"/>'),
              num(hx - d*22, 470, 1), num(hx - d*18, 300, 2), num(fx, hy-24, 3), num(cx, hy-22, 4), num(tx + 16, 284, 5), num(x0+250, 318, 6)]
        # kablo demetleri (kesik çizgi)
        bxc = 600
        ex = bxc - side*30
        o.append(f'<path d="M{x0+70},246 C{x0+70},226 {ex},250 {ex},352" fill="none" stroke="#66716d" stroke-width="1.2" stroke-dasharray="4 3"/>')
        o.append(f'<path d="M{x0+210},246 C{x0+210},226 {ex},270 {ex},352" fill="none" stroke="#66716d" stroke-width="1.2" stroke-dasharray="4 3"/>')
        o.append(f'<path d="M{bx+40},372 L{bx+40+side*46},426 H{bxc-side*14} V404" fill="none" stroke="#66716d" stroke-width="1.2" stroke-dasharray="4 3"/>')
    # buat ve DHT22
    o.append(grp("buat", f'<rect x="545" y="352" width="110" height="52" rx="4" fill="#f4f6f5" stroke="#1a211f" stroke-width="1.4"/>' + t(600, 374, "Buat", 10, "bold", anchor="middle") + t(600, 388, "UNO Q + breadboard", 8, fill="#66716d", anchor="middle")))
    o.append(grp("dht", f'<line x1="600" y1="352" x2="600" y2="334" stroke="#66716d" stroke-width="1.2"/><rect x="584" y="312" width="32" height="22" rx="3" fill="#fff" stroke="#1a211f"/>' + t(600, 327, "DHT22", 7.5, "bold", anchor="middle")))
    o += [f'<path d="M600,404 V470 H690" fill="none" stroke="#1a211f" stroke-width="1.4"/>', f'<rect x="690" y="458" width="46" height="24" rx="3" fill="#fff" stroke="#1a211f"/>',
          t(713, 474, "priz", 8.5, "bold", anchor="middle"), t(744, 474, "USB-C adaptör + 5 V adaptör; topraklı, sudan uzak ve kuru", 8.5, fill="#66716d")]
    return "\n".join(o)
LEGEND = ["Mini pompa: kovanın dibinde, tamamen suyun içinde.", "Hortum (4×6 mm silikon): pompa çıkışından akış sensörüne, oradan saksının üstüne kadar tek ölçü.",
          "Akış sensörü (YF-S401): üzerindeki ok pompadan saksıya doğru bakar.",
          "Çekvalf: oku pompadan saksıya doğru; pompa durunca hortumdaki su geri kaçmaz.",
          "T-parça: hattı saksının ortasında ikiye ayırır.", "Delikli hortum: toprağın üstünde, iki ucu kapalı, iğneyle delinmiş."]
LNOTES = ["Nem sensörleri beyaz çizgiye kadar toprağa girer; çizginin üstündeki elektronik kısım toprağın dışında ve kuru kalır. Toprağa girmeden önce kart kenarlarına şeffaf oje sürülür.",
          "Şamandıra kovanın dibine yakın durur: su onun altına inince pompa kilitlenir. Kovalar sandalyede, su seviyesi kesik mavi çizginin altında.",
          "İki saksı eşit ışık alacak şekilde yan yana; buat ve DHT22 gölgede. Kesik gri çizgiler kablo demetlerini gösterir, ayrıntısı Elektrik görünümünde."]

out = f"{here}/out"; os.makedirs(out, exist_ok=True)

# ================= PDF =================
PH = 1090
def pdfpage(no, tot, title, sub, body, h=PH):
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}">',
        f'<rect width="{W}" height="{h}" fill="#fff"/>', t(40, 30, title, 17, "bold"), t(40, 46, sub, 9.5, fill="#66716d"),
        t(W-40, 30, f"Suİz bağlantı şeması · {no}/{tot}", 9, fill="#66716d", anchor="end"),
        t(W-40, 44, "17 Kasım 2026 · taslak; parçalar 16 Kasım'da karşılaştırıldı, testler bekliyor", 8.5, fill="#96560a", anchor="end"), body, "</svg>"])
def rows_for(s): return [(k, col, a, b, n) for k, st, col, a, b, n, g in ROWS if st == s]
TOT = 8
fig_g = lambda only=None: '<g transform="translate(0,40)">' + parts() + wires_svg(only=only) + '</g>'
pages = [pdfpage(1, TOT, "Elektrik: tüm sistem", "İki yatak, 48 kablo. Sonraki sayfalarda adım adım; son sayfada tam liste.",
                 fig_g() + t(40, 716, "Renkler: turuncu 3,3 V · kırmızı 5 V · siyah GND · sarı sensör sinyali · mavi pompa tetiği · mor şamandıra · yeşil akış darbesi · gri DHT22 verisi", 9.5)
                 + t(40, 734, "Üst hatlar adaptörün 5 V'u, alt hatlar UNO Q'nun 3,3 V'u. İki − hattı K3 ile birleşir. A0–A5 pinlerine 3,3 V'tan fazlası verilmez.", 9.5)
                 + t(40, 752, "Her kablonun üzerinde etiketi var. Breadboard deliği: harf + sıra numarası (örneğin j10). Kabloları güç yokken tak.", 9.5), h=790)]
lay = '<g transform="translate(0,-90)">' + layout() + '</g>'
yy = 500; leg = []
for i, s in enumerate(LEGEND, 1):
    leg.append(f'<circle cx="48" cy="{yy-3}" r="8" fill="#1a211f"/>' + t(48, yy, str(i), 8.5, "bold", "#fff", "middle") + t(64, yy, s, 9.5)); yy += 19
yy += 6
for s in LNOTES: leg.append(t(40, yy, s, 9.5)); yy += 15
pages.append(pdfpage(2, TOT, "Yerleşim: saksılar, kovalar ve su hattı", "Yandan görünüm. Numaralar suyun izlediği yolu gösterir.", lay + "\n".join(leg), h=740))
for s in range(1, 6):
    pages.append(pdfpage(s+2, TOT, f"Adım {s} · {STEPS[s]}", "Bu adımda takılacak kablolar. Diğer parçalar yerinde gösterilir, kabloları gizlidir.",
                         fig_g(s) + table(rows_for(s), NOTES[s], y0=712)))
cols = (40, 86, 168, 470, 760)
b7 = [f'<line x1="40" y1="75" x2="{W-40}" y2="75" stroke="#1a211f" stroke-width="1.2"/>']
for x, h in zip(cols, ("Kablo", "Renk", "Nereden", "Nereye", "Not")): b7.append(t(x, 70, h, 8.5, "bold", "#66716d"))
yy = 92
for k, st, col, a, b_, n, g in ROWS:
    if col in C:
        b7.append(f'<rect x="{cols[1]}" y="{yy-7}" width="18" height="5" rx="2" fill="{C[col]}"/>'); b7.append(t(cols[1]+23, yy, RENK[col], 9.5))
    else: b7.append(t(cols[1], yy, col, 9.5))
    b7 += [t(cols[0], yy, k, 9.5, "bold"), t(cols[2], yy, a, 9.5), t(cols[3], yy, b_, 9.5), t(cols[4], yy, n, 9, fill="#66716d"),
           f'<rect x="{W-58}" y="{yy-9}" width="11" height="11" fill="none" stroke="#66716d"/>',
           f'<line x1="40" y1="{yy+5.5}" x2="{W-40}" y2="{yy+5.5}" stroke="#d6dcd9" stroke-width=".7"/>']
    yy += 17.5
pages.append(pdfpage(8, TOT, "Tüm bağlantılar", "Takılan her kabloyu sağdaki kutudan işaretle.", "\n".join(b7)))
for i, p in enumerate(pages, 1): open(f"{out}/b{i}.svg", "w", encoding="utf-8").write(p)

# ================= Web =================
fig = f'<svg id="fig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Suİz elektrik bağlantıları"><rect width="{W}" height="{H}" fill="#fff"/>{parts()}{wires_svg(web=True)}</svg>'
lfig = f'<svg id="lay" xmlns="http://www.w3.org/2000/svg" viewBox="0 {LY0} {LW} {LH-LY0}" role="img" aria-label="Suİz yerleşim: saksılar, kovalar ve su hattı">{layout(web=True)}</svg>'
trs = []
for s in range(1, 6):
    trs.append(f'<tr class="grp" data-s="{s}"><th colspan="6">Adım {s} · {STEPS[s]}</th></tr>')
    for k, st, col, a, b_, n, g in ROWS:
        if st != s: continue
        sw = f'<span class="sw" style="background:{C[col]}"></span>{RENK[col]}' if col in C else H_.escape(col)
        trs.append(f'<tr data-k="{k}" data-s="{s}" data-g="{g}" tabindex="0"><td><input type="checkbox" id="c-{k}" aria-label="{k} takıldı"></td><td class="m">{k}</td><td>{sw}</td><td>{H_.escape(a)}</td><td>{H_.escape(b_)}</td><td class="n">{H_.escape(n)}</td></tr>')
    for n in NOTES[s]: trs.append(f'<tr class="note" data-s="{s}"><td></td><td colspan="5">{H_.escape(n)}</td></tr>')
tabs = '<button type="button" class="tab" data-s="0" aria-pressed="true">Hepsi</button>' + "".join(f'<button type="button" class="tab" data-s="{s}" aria-pressed="false">{s} · {STEPS[s].split(",")[0].split(" ve ")[0]}</button>' for s in range(1, 6))
legend_html = "".join(f"<li>{H_.escape(s)}</li>" for s in LEGEND)
lnotes_html = "".join(f"<p>{H_.escape(s)}</p>" for s in LNOTES)
tpl = open(f"{here}/page.tpl.html", encoding="utf-8").read()
page_html = (tpl.replace("__TABS__", tabs).replace("__FIG__", fig).replace("__LAY__", lfig).replace("__ROWS__", "\n".join(trs))
             .replace("__LEGEND__", legend_html).replace("__LNOTES__", lnotes_html).replace("__W__", str(W)).replace("__H__", str(H)))
open(f"{here}/index.html", "w", encoding="utf-8", newline="\n").write(page_html)
# Proje sitesi (GitHub Pages, docs/) aynı sayfayı docs/sema/ altında yayınlar.
site = os.path.normpath(f"{here}/../../docs/sema")
if os.path.isdir(site):
    open(f"{site}/index.html", "w", encoding="utf-8", newline="\n").write(page_html)
open(f"{out}/all2.svg", "w", encoding="utf-8").write(fig.replace('id="fig" ', f'width="{W}" height="{H}" '))
open(f"{out}/lay.svg", "w", encoding="utf-8").write(lfig.replace('id="lay" ', f'width="{LW}" height="{LH-LY0}" '))
print("ok", len(WIRES), "kablo,", len(ROWS), "satır,", len(page_html), "bayt")
