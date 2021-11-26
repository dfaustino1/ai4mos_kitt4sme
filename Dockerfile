FROM python:3.8

RUN pip install pipenv
RUN mkdir /src
COPY Pipfile /src/Pipfile
COPY Pipfile.lock /src/Pipfile.lock
RUN cd /src && { pipenv lock -r > /requirements.txt; }
RUN pip install -r /requirements.txt

COPY main.py /src/main.py
COPY mlp.sav /src/mlp.sav
COPY roughnator /src/roughnator
WORKDIR /src
ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
