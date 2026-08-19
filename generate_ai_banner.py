"""
Animasyonlu bir "neural network forward-pass" SVG banner'ı üretir.
- Arka planda sürekli küçük "sinyal" noktaları katmanlar arasında akar.
- Periyodik olarak (her CYCLE saniyede bir) "BERFIN" kelimesinin harfleri
  sırayla katmanlar boyunca yürür, sonra kaybolup normal akışa döner.
Harici kütüphane gerektirmez, saf SVG + SMIL animasyonu üretir.
"""

import random

WIDTH = 900
HEIGHT = 220
LAYERS = [4, 6, 6, 3]  # input, hidden, hidden, output
NODE_R = 10
COLORS = ["#7C3AED", "#8B5CF6", "#A78BFA", "#22D3EE", "#38BDF8"]

SIGNAL_WORD = "BERFIN"
CYCLE = 12.0          # toplam döngü süresi (saniye)
LETTER_TRAVEL = 3.0    # bir harfin baştan sona yürüme süresi
LETTER_STAGGER = 0.35  # harfler arası başlama gecikmesi

random.seed(7)  # her çalışmada aynı düzen, sadece animasyon zamanlaması değişsin


def layer_x_positions(n_layers, width, margin=80):
    if n_layers == 1:
        return [width / 2]
    step = (width - 2 * margin) / (n_layers - 1)
    return [margin + i * step for i in range(n_layers)]


def node_y_positions(n_nodes, height, margin=30):
    if n_nodes == 1:
        return [height / 2]
    step = (height - 2 * margin) / (n_nodes - 1)
    return [margin + i * step for i in range(n_nodes)]


def build_svg():
    xs = layer_x_positions(len(LAYERS), WIDTH)
    positions = []  # positions[layer_idx] = list of (x, y)
    for li, n in enumerate(LAYERS):
        ys = node_y_positions(n, HEIGHT)
        positions.append([(xs[li], y) for y in ys])

    svg_parts = []
    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}">'
    )

    svg_parts.append(
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="14" fill="#0B0B14"/>'
    )

    svg_parts.append("<defs>")
    svg_parts.append(
        '<radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#C4B5FD"/>'
        '<stop offset="100%" stop-color="#7C3AED"/>'
        "</radialGradient>"
    )
    svg_parts.append("</defs>")

    # ---- kenarlar (edges) - sabit çizgiler ----
    for li in range(len(LAYERS) - 1):
        for (x1, y1) in positions[li]:
            for (x2, y2) in positions[li + 1]:
                color = random.choice(COLORS)
                svg_parts.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{color}" stroke-opacity="0.16" stroke-width="1.2"/>'
                )

    # ---- arka plan trafiği: sürekli akan küçük noktalar ----
    for li in range(len(LAYERS) - 1):
        for (x1, y1) in positions[li]:
            for (x2, y2) in positions[li + 1]:
                if random.random() > 0.35:
                    continue
                color = random.choice(COLORS)
                dur = round(random.uniform(2.0, 3.6), 2)
                delay = round(random.uniform(0, 3.0), 2)
                svg_parts.append(
                    f'<circle r="2" fill="{color}" opacity="0.8">'
                    f'<animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite" '
                    f'path="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>'
                    f'<animate attributeName="opacity" values="0;0.8;0.8;0" dur="{dur}s" '
                    f'begin="{delay}s" repeatCount="indefinite"/>'
                    f"</circle>"
                )

    # ---- düğümler (nodes) - hafif nabız animasyonu ----
    for li, layer in enumerate(positions):
        for (x, y) in layer:
            pulse_dur = round(random.uniform(2.0, 3.5), 2)
            svg_parts.append(
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{NODE_R}" fill="url(#nodeGlow)" '
                f'stroke="#1E1B2E" stroke-width="2">'
                f'<animate attributeName="r" values="{NODE_R};{NODE_R+2};{NODE_R}" '
                f'dur="{pulse_dur}s" repeatCount="indefinite"/>'
                f"</circle>"
            )

    # ---- periyodik "BERFIN" yazısı: harfler sırayla tüm katmanlardan geçiyor ----
    for i, letter in enumerate(SIGNAL_WORD):
        row = i % min(LAYERS)
        pts = []
        for li in range(len(LAYERS)):
            x, y = positions[li][row % len(positions[li])]
            pts.append((x, y))
        path_d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

        start_t = i * LETTER_STAGGER
        end_t = start_t + LETTER_TRAVEL
        start_frac = round(start_t / CYCLE, 4)
        end_frac = round(end_t / CYCLE, 4)

        opacity_key_times = f"0;{start_frac};{min(start_frac+0.01,1)};{end_frac};{min(end_frac+0.01,1)};1"
        opacity_values = "0;0;1;1;0;0"

        motion_key_times = f"0;{start_frac};{end_frac};1"
        motion_key_points = "0;0;1;1"

        svg_parts.append(
            f'<text font-family="monospace" font-size="13" font-weight="bold" '
            f'fill="#F5F3FF" text-anchor="middle" opacity="0">{letter}'
            f'<animateMotion dur="{CYCLE}s" repeatCount="indefinite" '
            f'keyPoints="{motion_key_points}" keyTimes="{motion_key_times}" '
            f'calcMode="linear" path="{path_d}"/>'
            f'<animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite" '
            f'keyTimes="{opacity_key_times}" values="{opacity_values}"/>'
            f"</text>"
        )

    svg_parts.append(
        f'<text x="20" y="24" font-family="monospace" font-size="13" fill="#A78BFA">'
        f"forward_pass() // training in progress</text>"
    )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


if __name__ == "__main__":
    svg = build_svg()
    with open("neural-network.svg", "w") as f:
        f.write(svg)
    print("neural-network.svg oluşturuldu.")
