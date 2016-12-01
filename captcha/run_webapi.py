# coding: utf-8
from captcha.webapi.resources.add_feedback import AddFeedbackResource
from captcha.webapi.resources.get_answer import GetAnswerResource
import falcon


app = falcon.API()


add_feedback = AddFeedbackResource()
get_answer = GetAnswerResource()


app.add_route('/add/feedback/', add_feedback)
app.add_route('/get/answer/', get_answer)


if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 8009, app)
    httpd.serve_forever()

