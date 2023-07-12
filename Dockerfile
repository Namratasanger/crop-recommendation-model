FROM tensorflow/tensorflow

ADD . .

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["gunicorn", "wsgi", "-b", "0.0.0.0:8000"]
