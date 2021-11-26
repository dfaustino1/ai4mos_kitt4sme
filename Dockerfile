FROM python:3.8.5-alpine3.12 as base
FROM base as builder
RUN apk --no-cache --update-cache add gcc python3 python3-dev py-pip build-base wget
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN pip install pipenv
RUN mkdir /src
COPY Pipfile /src/Pipfile
COPY Pipfile.lock /src/Pipfile.lock
RUN cd /src && { pipenv lock -r > /requirements.txt; }
RUN pip install -r /requirements.txt

FROM base
RUN apk --no-cache add curl
COPY --from=builder /usr/local /usr/local
COPY main.py /src/main.py
COPY roughnator /src/roughnator
WORKDIR /src
ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
