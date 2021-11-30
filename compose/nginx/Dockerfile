FROM openresty/openresty:latest

COPY ./compose/nginx/nginx.conf /etc/openresty/nginx.conf
COPY ./compose/nginx/foxwall.conf /etc/nginx/conf.d/foxwall.conf

ENV TZ=Europe/Moscow