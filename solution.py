from PIL import Image
import numpy as np
import os
import argparse


def dhash(image, hash_size=16):
    image = image.convert('LA').resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    mat = np.array(
        list(map(lambda x: x[0], image.getdata()))
    ).reshape(hash_size, hash_size + 1)

    return ''.join(
        map(
            lambda x: hex(x)[2:].rjust(2, '0'),
            np.packbits(np.fliplr(np.diff(mat) < 0))
        )
    )


def hamming_distance(s1, s2):
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


parser = argparse.ArgumentParser(description='First test task on images similarity.')
parser.add_argument('--path', help='folder with images', required=True)
args = parser.parse_args()
files = os.listdir(args.path)
pairs = []
threshold = 0.2
for i in range(len(files)):
    img1 = Image.open(args.path + '/' + files[i])
    img_hash = dhash(img1)
    for j in range(len(files)):
        img2 = Image.open(args.path + '/' + files[j])
        img_hash2 = dhash(img2)
        dist = hamming_distance(img_hash, img_hash2) / len(img_hash)
        if dist < threshold and files[i] != files[j] and sorted([files[i], files[j]]) not in pairs:
            pairs.append(sorted([files[i], files[j]]))
            print(files[i], files[j])


