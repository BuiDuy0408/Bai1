FROM alpine:3.16

EXPOSE 4898
WORKDIR /Company
ADD  ./company ./Company
RUN apk update
RUN apk add chromium=102.0.5005.61-r0 \
    && apk add chromium-chromedriver=102.0.5005.61-r0 \
    && apk add --no-cache python3 \
    && apk add py3-pip
RUN pip3 install -U selenium \
    && pip3 install requests

# CMD [ "python3","./down_load_file_test.py" ]

