FROM tiangolo/meinheld-gunicorn-flask:python3.9

COPY ./requirements.txt /app/requirements.txt
COPY ./api /app/api
COPY ./migrations /app/migrations
COPY ./prestart.sh /app/prestart.sh

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ENV MODULE_NAME="api.__init__"
