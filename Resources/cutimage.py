try:
    from PIL import Image
except ModuleNotFoundError:
    import pip._internal as pip
    pip.main(['install', "PIL"])
    from PIL import Imagezz
import os
resources_dir = os.path.join(os.path.dirname(__file__))
image = Image.open(os.path.join(resources_dir, 'A4kr.png'))
width, height = image.size
w = 5 # number of columns
h = 4 # number of rows
names = list(range(1, 21))
os.makedirs(os.path.join(resources_dir, 'images'), exist_ok=True)
for j in range(h):
    for i in range(w):
        cropped = image.crop((i * width / w, j * height / h, (i + 1) * width / w, (j + 1) * height / h))
        cropped.save(os.path.join(resources_dir, 'images',str(names.pop(0)).zfill(3) + '.png'))
