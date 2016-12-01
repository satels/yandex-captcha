# coding: utf-8

_base_path = '/opt/data/'

CAPTCHA_EXTENSION = '.gif'
CAPTCHA_SRC_DIR = _base_path + 'captcha_source/'
CAPTCHA_TEST_DIR = _base_path + 'captcha_test/'
CAPTCHA_TRAIN_DIR = _base_path + 'captcha_train/'
CAPTCHA_SIZE = (60, 200)
BANNER_SIZE = (15, 36)

LETTER_SRC_DIR = _base_path + 'letter_source/'

NN_WORD_LENS_FN = _base_path + 'nn/word_lens.params'
NN_LETTERS_FN = _base_path + 'nn/letters.params'

UNSET_FILES = '/opt/data/upload/unset/'
VALID_FILES = '/opt/data/upload/valid/'
INVALID_FILES = '/opt/data/upload/invalid/'

RUS_LETTERS = u'абвгдежзиклмнопрстуфхцчшщъыьэюя'

RUS_REPLACE = [
    (ur'ьы', u'ы'),
    (ur'ыи$', u'ый'),
]

from logging import config as log_config


LOGGING_DIR = '/var/log/captcha/'

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
    },
    'handlers': {
        'console': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'captcha': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


log_config.dictConfig(LOGGING_CONF)
