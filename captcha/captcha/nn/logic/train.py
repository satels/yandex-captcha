# coding: utf-8
from captcha.core import conf
from skimage.io import imsave
from captcha.nn.logic.prepare import (
    get_fn_lst,
    get_word_from_fn,
    get_image,
    clean_image,
    to_black,
    to_bool,
    get_strip_captcha_coords,
    strip_captcha,
    framing_image,
)
from skimage.transform import resize
import logging
import numpy as np
import os
import random


logger = logging.getLogger('captcha')


def train_to_numpy(func):

    def wrapped(*args, **kwargs):
        X_train, Y_train = func(*args, **kwargs)
        items = zip(X_train, Y_train)
        random.shuffle(items)

        _X_train = []
        _Y_train = []

        for x, y in items:
            _X_train.append(x)
            _Y_train.append(y)

        X_train = np.array(_X_train)
        Y_train = np.array(_Y_train).astype(np.uint8)
        return X_train, Y_train

    return wrapped


def get_word_train_image(image):
    clean_image(image)

    black_image = to_black(image)

    min_x, max_x, min_y, max_y = get_strip_captcha_coords(black_image)

    striped_image = strip_captcha(to_bool(image), min_x, max_x, min_y, max_y)

    striped_image = framing_image(striped_image, frame_size=(60, 200))

    ret = resize(striped_image, (30, 100))

    return ret


def get_letter_train_image(image):

    striped_image = framing_image(to_bool(image), frame_size=(70, 70), orientation='center')

    ret = resize(striped_image, (55, 55))

    return ret


@train_to_numpy
def get_train_word_lens_data(count):

    logger.info('Start get train word lens')

    X_train = []
    Y_train = []

    fn_lst = get_fn_lst(conf.CAPTCHA_SRC_DIR)

    num = 0
    for fn in fn_lst[:count]:

        word = get_word_from_fn(fn)

        image = get_image(fn)

        train_image = get_word_train_image(image)

        X_train.append([train_image])

        Y_train.append(len(word))

        num += 1
        if num % 1000 == 0:
            logger.info('Get train word lens: complete %s', num)

    imsave('/opt/data/log_train_word_lens_data' + conf.CAPTCHA_EXTENSION, X_train[0][0])

    return X_train, Y_train


@train_to_numpy
def get_train_letters_data(count):
    X_train = []
    Y_train = []

    logger.info('Start get train letters')

    sorted_letters_folders_lst = filter(
        lambda l: len(l.decode('utf-8')) == 1,
        sorted(os.listdir(conf.CAPTCHA_TRAIN_DIR))
    )

    letters_folders_lst = list(enumerate(sorted_letters_folders_lst))

    random.shuffle(letters_folders_lst)

    for num, letter in letters_folders_lst:

        letter_folder = conf.CAPTCHA_TRAIN_DIR + letter + '/'

        letters_fn_lst = os.listdir(letter_folder)

        random.shuffle(letters_fn_lst)

        for fn in letters_fn_lst[:count]:
            letter_fn = letter_folder + fn

            image = get_image(letter_fn)

            train_image = get_letter_train_image(image)

            X_train.append([train_image])

            Y_train.append(num)

        imsave('/opt/data/log_train_letter_image' + conf.CAPTCHA_EXTENSION, train_image)

        logger.info('Get train letters %s: complete %s', letter, num)

    return X_train, Y_train
