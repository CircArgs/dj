FROM python:3.10
WORKDIR /code
COPY . /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements/docker.txt
RUN pip install -e .
RUN pip install https://github.com/rogerbinns/apsw/releases/download/3.38.1-r1/apsw-3.38.1-r1.zip \
  --global-option=fetch --global-option=--version --global-option=3.38.1 --global-option=--all \
  --global-option=build --global-option=--enable-all-extensions
RUN pip install jupyter
CMD ["/code/start.sh"]
EXPOSE 8000
EXPOSE 8001
