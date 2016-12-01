# coding: utf-8
from captcha.core import conf
from skimage.io import imsave
from captcha.nn.logic.prepare import (
    get_image,
    get_word_from_fn,
    get_fn_lst,
    clean_image,
    to_black,
    to_bool,
    get_strip_captcha_coords,
    strip_captcha,
)
import logging
import numpy as np
import os


logger = logging.getLogger('captcha')


class LettersError(Exception):
    pass


def get_word_image_for_letters(image):

    clean_image(image)

    black_image = to_black(image)

    min_x, max_x, min_y, max_y = get_strip_captcha_coords(black_image)

    striped_image = strip_captcha(image, min_x, max_x, min_y, max_y)

    return striped_image


def make_letters_from_all():
    for index, fn in enumerate(get_fn_lst(conf.CAPTCHA_SRC_DIR)):

        word = get_word_from_fn(fn)

        word_len = len(word)

        image = get_image(fn)

        word_image = get_word_image_for_letters(image)

        try:
            letter_images = make_letters(word_image, word_len)
        except LettersError:
            continue

        for p in range(word_len):

            letter = word[p]
            letter_folder = conf.CAPTCHA_TRAIN_DIR + letter.encode('utf-8') + '/'

            try:
                os.mkdir(letter_folder)
            except OSError:
                pass

            letter_image = letter_images[p]

            letter_fn = letter_folder + str(p) + '-' + word.encode('utf-8') + conf.CAPTCHA_EXTENSION

            imsave(letter_fn, letter_image)

        if index % 100 == 0:
            logger.info('Process on image: %s', index)


def make_letters(image, word_len):

    width = image.shape[1]

    step = 1.0*width/word_len

    ret = []
    for p in range(word_len):

        x1 = step*p - int(step/3)

        if x1 < 0:
            x1 = 0

        x2 = step*(p + 1) + int(step/3.1)

        if x2 >= width:
            x2 = width

        if int(x2) - int(x1) >= 70:
            logger.warn('Bad letter length p:%s, step:%s, word_len:%s, x1:%s, x2:%s', p, step, word_len, x1, x2)
            raise LettersError('Bad letter length')

        letter_image = image[:, int(x1):int(x2)]

        ret.append(letter_image)

    return ret
