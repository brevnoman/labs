FROM python:3.9

COPY requirements.txt /src/
COPY . /src/
WORKDIR src
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "rand_cat.py"]