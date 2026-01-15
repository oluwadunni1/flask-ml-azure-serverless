FROM python:3.10-slim
ARG VERSION
LABEL org.label-schema.version=$VERSION

COPY ./requirements.txt /webapp/requirements.txt
WORKDIR /webapp
RUN pip install --no-cache-dir -r requirements.txt
COPY webapp/* /webapp
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
