# coding: utf-8
from captcha.core import conf
from captcha.core.logic import get_word
from captcha.nn.logic.prepare import get_image
import cgi
import falcon
import os
import re
import ujson
import uuid


class GetAnswerResource(object):

    def on_post(self, req, resp):

        image_key = str(uuid.uuid4())

        fn = os.path.join(conf.UNSET_FILES, image_key) + conf.CAPTCHA_EXTENSION

        image_text = req.stream.read()

        if not image_text:
            resp_data = {
                'status': 400,
                'error': 'Image is empty',
                'data': None,
            }
        else:

            open(fn, 'w').write(image_text)

            image = get_image(fn)

            word = get_word(image)

            for from_val, to_val in conf.RUS_REPLACE:
                word = re.sub(from_val, to_val, word)

            if word is None:
                resp_data = {
                    'status': 400,
                    'error': 'Word dnot determinate',
                    'data': None,
                }
            else:
                resp_data = {
                    'status': 200,
                    'error': None,
                    'data': {
                        'word': word,
                        'word_len': len(word),
                        'id': image_key,
                    },
                }

        resp.status = falcon.HTTP_200
        resp.body = ujson.dumps(resp_data, ensure_ascii=False)
