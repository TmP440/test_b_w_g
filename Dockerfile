FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

EXPOSE 5051

WORKDIR app
ENV PYTHONPATH=.
COPY ./ ./
CMD ["bash", "on_start/start.sh"]
#CMD python start.sh