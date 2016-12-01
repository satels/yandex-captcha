# coding: utf-8
from captcha.core import conf
from captcha.nn.logic.core import make_letter_net, save_net
from captcha.nn.logic.train import get_train_letters_data
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
    net_fn = conf.NN_LETTERS_FN


if __name__ == '__main__':
    net = make_letter_net()

    X_train, Y_train = get_train_letters_data(count)

    net.fit(X_train, Y_train)

    save_net(net, net_fn)

