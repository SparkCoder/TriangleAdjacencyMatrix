import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
w, h = 1024, 2048
thickness = 30
font = ImageFont.truetype(os.path.join(
    dir_path, 'fonts', 'Poppins-Bold.ttf'), 80)
color = '#020202'

items = [
    'Parking',
    'Entry gate',
    'lobby & reception',
    'Admin. office',
    'R&D block',
    'Multi-purpose hall',
    'Gallery block',
    'Library',
    'Conference hall',
    'Amphitheatre',
    'Meeting area'
]
n_items = len(items)

if __name__ == '__main__':
    matrix = np.array([[0] * n_items] * n_items)
    for rel in range(n_items):
        for entry in range(rel + 1):
            con = (rel + entry) % 2
            matrix[rel][entry] = 1 if rel == entry else (0 if con == 0 else 2)
            matrix[entry][rel] = 1 if rel == entry else (0 if con == 0 else 2)

    img = Image.new("RGBA", (w * 2, h + 100))
    canvas = ImageDraw.Draw(img)

    s = h / n_items
    m = s / 4
    for i in range(n_items):
        x_pos = w - s
        y_pos = 50
        canvas.line([(x_pos, (i * s) + y_pos), (w - (s / 2) - (s * 0.5 * i) + (s / 2) +
                    x_pos, (h / 2) + (s * 0.5 * i) + y_pos)], fill=color, width=thickness)
        canvas.line([(x_pos, h - (i * s) + y_pos), (w - (s / 2) - (s * 0.5 * i) +
                    (s / 2) + x_pos, (h / 2) - (s * 0.5 * i) + y_pos)], fill=color, width=thickness)

        if i < (n_items - 1):
            for j in range(n_items - i - 1):
                p = i * (s / 2)
                c = j * s

                x_index = j
                y_index = i

                canvas.ellipse([(p + m + x_pos, p - (s / 2) + s + m + c + y_pos), (p + s - m + x_pos, p + (
                    s / 2) + s - m + c + y_pos)], fill=(255, 0, 0) if matrix[y_index][x_index] == 0 else (0, 255, 0))

            for i in range(n_items + 1):
                canvas.line([(0, (i * s) + y_pos), (x_pos, (i * s) +
                            y_pos)], fill=color, width=thickness)

            for i in range(n_items):
                canvas.text((30, (i * s) + font.size),
                            items[i], font=font, align="left", fill=color)

    img = img.resize(img.size, Image.ANTIALIAS)
    plt.imshow(np.asarray(img))
    plt.show()
