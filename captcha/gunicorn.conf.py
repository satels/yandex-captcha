import multiprocessing

bind = '0.0.0.0:8009'
max_requests = 10000
timeout = 60
workers = 1
errorlog = '/var/log/captcha/gunicorn.error.log'
accesslog = '/var/log/captcha/gunicorn.access.log'
