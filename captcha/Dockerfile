FROM phusion/baseimage:0.9.19
MAINTAINER Ivan Petuhov <satels@gmail.com>

CMD ["/sbin/my_init"]

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -qq && apt-get upgrade -qq \
    && locale-gen en_US.UTF-8 ru_RU.UTF-8 \
    && apt-get install -qq \
        git \
        nginx-full \
        python \
        python-dev \
        python-pip \
        g++ \
        runit \
        ruby \
        rubygems-integration \
    && gem install --no-rdoc --no-ri --version=0.74.0 foreman \
    && rm -rf /etc/logrotate.d \
    && pip install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt /var/www/captcha/
RUN pip install -r /var/www/captcha/requirements.txt

COPY etc/ /etc/
RUN rm -f etc/nginx/sites-enabled/default \
    && nginx -t \
    && rm -r /root/.ssh

WORKDIR /var/www/captcha

COPY Procfile /var/www/captcha/
RUN foreman export \
        --app=web \
        --log=/var/log/captcha \
        --user=www-data \
        --root=/var/www/captcha \
        --concurrency="web=1" \
        runit /etc/service \
    && rm Procfile

EXPOSE 80

COPY . /var/www/captcha/

RUN mkdir -p /var/log/captcha \
    && rm -rf /var/log/captcha/* \
    && mkdir -p /var/log/krapi \
    && find . -name '*.pyc' -delete \
    && find . -name '*.swp' -delete \
    && python -c 'import compileall, os; compileall.compile_dir(os.curdir, force=1)' > /dev/null \
    && rm -rf /var/log/captcha/* \
    && rm -rf build/ \
    && rm requirements.txt \
    && rm Procfile \
    && rm Dockerfile
