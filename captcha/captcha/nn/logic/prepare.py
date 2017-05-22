# coding: utf-8
from captcha.core import conf
from skimage import img_as_bool, img_as_int
from skimage.io import imread
from skimage.transform import probabilistic_hough_line
import numpy as np
import random
import os


def to_bool(image):
    return np.invert(img_as_bool(image))


def to_black(image):
    ret = image.copy()
    for row in ret:
        for i, v in enumerate(row):
            if v < 1:
                row[i] = 1
            else:
                row[i] = 0
    return ret


def get_image(fn):
    return imread(fn, as_grey=True)


def get_fn_lst(folder):
    ret = [
        os.path.join(folder, fn)
        for fn in os.listdir(folder)
        if '-' not in fn and ('.png' in fn or '.gif' in fn)
    ]
    random.shuffle(ret)
    return ret


def get_word_from_fn(fn):
    base_fn = os.path.basename(fn)

    word = base_fn.strip().decode('utf-8').replace(u'\u0438\u0306', u'й').replace('_', '').replace('.png', '').replace('.gif', '')

    return word


def framing_image(image, frame_size=(40, 40), zeros=True, orientation='center'):

    if zeros:
        new_image = np.zeros(frame_size)
    else:
        new_image = np.ones(frame_size)

    if orientation == 'center':
        shift_y, shift_x = new_image.shape[0] - image.shape[0], new_image.shape[1] - image.shape[1]
        if frame_size[1] == image.shape[1]:
            new_image[shift_y/2:-shift_y/2, :] = image
        else:
            new_image[shift_y/2:-shift_y/2, shift_x/2:-shift_x/2] = image
    elif orientation == 'left':
        shift_y, shift_x = image.shape[0], image.shape[1]
        new_image[:shift_y, :shift_x] = image

    return new_image


def draw_random_lines(image, count):

    for i in range(count):
        y1 = random.randint(0, image.shape[1] - 1)
        y2 = random.randint(0, image.shape[1] - 1)
        x1 = random.randint(0, image.shape[0] - 1)
        x2 = random.randint(0, image.shape[0] - 1)

        rr, cc = line(x1, y1, x2, y2)
        image[rr, cc] = 0
    return image


def get_clean_name(fn, prefix='clean'):
    word = get_word_from_fn(fn)
    return '/'.join(fn.split('/')[:-1]) + '/' + prefix + '-' + word + '.png'


def clean_image(image):
    image[:conf.BANNER_SIZE[0], conf.CAPTCHA_SIZE[1] - conf.BANNER_SIZE[1]:] = np.ones(conf.BANNER_SIZE)


def get_strip_captcha_coords(image):

    lines = probabilistic_hough_line(
        image,
        threshold=6,
        line_length=6,
        line_gap=18,
        theta=np.array([np.pi,]),
    )

    min_y = conf.CAPTCHA_SIZE[0]
    max_y = 0
    min_x = conf.CAPTCHA_SIZE[1]
    max_x = 0

    for line in lines:
        p0, p1 = line

        X = (p1[0], p0[0])
        Y = (p1[1], p0[1])

        min_x = min([min(X), min_x])
        max_x = max([max(X), max_x])
        min_y = min([min(Y), min_y])
        max_y = max([max(Y), max_y])

    max_x += 2  # boundary conditions

    if max_x > conf.CAPTCHA_SIZE[1]:
        max_x = conf.CAPTCHA_SIZE[1]

    return min_x, max_x, min_y, max_y


def strip_captcha(img, min_x, max_x, min_y, max_y):

    return img[min_y:max_y, min_x:max_x]
