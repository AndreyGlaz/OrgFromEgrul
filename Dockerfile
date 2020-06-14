FROM python:3.6
ENV PYTHONUNBUFFERED 1
#ENV VIRTUAL_ENV /root/.cache/pypoetry/virtualenvs/egisu-SlVxDKY_-py3.6/
#ENV PATH /root/.cache/pypoetry/virtualenvs/egisu-SlVxDKY_-py3.6/bin:$PATH
WORKDIR /usr/src/OrgFromEgrul

EXPOSE 8000

# Установка в контейнере таймзоны
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#RUN apt-get update && apt-get install -y curl && apt-get install -y python3-venv
#COPY pyproject.toml .
#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
#RUN /bin/bash -c 'source $HOME/.poetry/env; \
#poetry install'
COPY Pipfile* /usr/src/OrgFromEgrul/
RUN pip install pipenv && pipenv install --system


COPY . .
