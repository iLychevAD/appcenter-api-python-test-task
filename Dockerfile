# Dont forget to set env variables:
# APPCENTER_OWNER APPCENTER_APP APPCENTER_TOKEN

FROM python:alpine

COPY files /
RUN chmod +x /build.py
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT /build.py
