# coding: utf-8
from captcha.core import conf
from captcha.nn.logic.core import make_word_len_net, save_net
from captcha.nn.logic.train import get_train_word_lens_data
import numpy as np
import sys
import warnings


try:
    count = int(sys.argv[1])
except ValueError:
    raise ValueError('Bad type of first arg: must be int')
except IndexError:
    raise IndexError('Set param: "count": size of train data')


try:
    net_fn = sys.argv[2].strip()
except IndexError:
    net_fn = None

if not net_fn:
    warnings.warn('No set param: "nn filename", use default fn')
    net_fn = conf.NN_WORD_LENS_FN


if __name__ == '__main__':

    X_train, Y_train = get_train_word_lens_data(count)

    Y_train_set = set(Y_train)

    max_Y = max(Y_train_set)
    min_Y = min(Y_train_set)

    print 'min and max Y:', min_Y, max_Y, Y_train_set, len(Y_train_set)

    Y_train = np.array([y - min_Y for y in Y_train])

    net = make_word_len_net(5)

    net.fit(X_train, Y_train)

    save_net(net, net_fn)
