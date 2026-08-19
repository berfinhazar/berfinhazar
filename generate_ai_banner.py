"""
Animasyonlu bir "neural network forward-pass" SVG banner'ı üretir.
Katmanlar arasında sinyal akışını simüle eder (stroke-dashoffset animasyonu ile).
Harici kütüphane gerektirmez, saf SVG + SMIL animasyonu üretir.
"""

import random

WIDTH = 900
HEIGHT = 220
LAYERS = [4, 6, 6, 3]  # input, hidden, hidden, output
NODE_R = 10
COLORS = ["#7C3AED", "#8B5CF6", "#A78BFA", "#22D3EE", "#38BDF8"]

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

    # arka plan
    svg_parts.append(
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="14" fill="#0B0B14"/>'
    )

    # gradient tanımları
    svg_parts.append("<defs>")
    svg_parts.append(
        '<radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">'
        '<stop offset="0%" stop-color="#C4B5FD"/>'
        '<stop offset="100%" stop-color="#7C3AED"/>'
        "</radialGradient>"
    )
    svg_parts.append("</defs>")

    # kenarlar (edges) - katmanlar arasında, "BERFİN" harfleri akıyor
    edge_id = 0
    signal_word = "BERFIN"
    for li in range(len(LAYERS) - 1):
        for (x1, y1) in positions[li]:
            for (x2, y2) in positions[li + 1]:
                edge_id += 1
                color = random.choice(COLORS)
                dur = round(random.uniform(2.2, 4.0), 2)
                delay = round(random.uniform(0, 3.0), 2)
                svg_parts.append(
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{color}" stroke-opacity="0.18" stroke-width="1.2"/>'
                )
                # hareketli "sinyal": BERFIN kelimesinin bir harfi, path boyunca akıyor
                letter = signal_word[edge_id % len(signal_word)]
                svg_parts.append(
                    f'<text font-family="monospace" font-size="11" font-weight="bold" '
                    f'fill="{color}" text-anchor="middle">{letter}'
                    f'<animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite" '
                    f'path="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>'
                    f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" '
                    f'begin="{delay}s" repeatCount="indefinite"/>'
                    f"</text>"
                )

    # düğümler (nodes) - hafif nabız animasyonu ile
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

    # başlık yazısı
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
