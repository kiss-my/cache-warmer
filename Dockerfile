FROM bitnami/python:3.7.6-debian-10-r41-prod
LABEL maintainer="The DevOps team @kiss my <devops@kissmy.co>"

RUN pip install --upgrade pip && \
    pip install requests

COPY ./rootfs/ /

ENTRYPOINT [ "/bin/cache-warmer.py" ]
CMD ["--help"]
