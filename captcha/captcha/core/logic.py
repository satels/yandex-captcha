# coding: utf-8
from captcha.core import conf
from captcha.letters.logic import make_letters, LettersError, get_word_image_for_letters
from captcha.nn.logic.prepare import to_bool
from captcha.nn.logic.core import (
    make_word_len_net,
    make_letter_net,
    load_net,
    get_value_from_net,
    get_values_lst_from_net,
)
from captcha.nn.logic.train import get_word_train_image, get_letter_train_image
from skimage.io import imsave
import numpy as np


def get_global_nets():
    word_len_net = make_word_len_net(5)
    load_net(word_len_net, conf.NN_WORD_LENS_FN)
    letter_net = make_letter_net()
    load_net(letter_net, conf.NN_LETTERS_FN)
    return {
        'word_len': word_len_net,
        'letter': letter_net,
    }


_nets = get_global_nets()


def get_word(image):
    nets = _nets
    test_word_image = get_word_train_image(image)
    word_len = get_value_from_net(nets['word_len'], test_word_image) + 3
    word_image = get_word_image_for_letters(image)
    try:
        letter_images = make_letters(word_image, word_len)
    except LettersError:
        return
    test_letter_images = [get_letter_train_image(im) for im in letter_images]
    letter_keys = get_values_lst_from_net(nets['letter'], test_letter_images)
    letters = [conf.RUS_LETTERS[key] for key in letter_keys]
    # imsave('/opt/data/log_test_letter_image' + conf.CAPTCHA_EXTENSION, test_letter_images[0])
    return u''.join(letters)
