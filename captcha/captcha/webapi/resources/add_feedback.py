# coding: utf-8
from captcha.core import conf
import falcon
import os
import ujson
import uuid


class AddFeedbackResource(object):

    def on_get(self, req, resp):

        image_key = req.get_param('key', required=True)

        valid = req.get_param_as_bool('valid', required=True)

        from_fn = os.path.join(conf.UNSET_FILES, image_key) + conf.CAPTCHA_EXTENSION

        to_folder = conf.VALID_FILES if valid else conf.INVALID_FILES

        to_fn = os.path.join(to_folder, image_key) + conf.CAPTCHA_EXTENSION

        os.rename(from_fn, to_fn)

        resp_data = {
            'status': 200,
            'error': None,
            'data': None,
        }

        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps(resp_data, ensure_ascii=False)
