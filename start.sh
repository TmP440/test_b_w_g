#!/bin/sh

sleep 5
alembic revision --autogenerate
alembic upgrade head
python main.py
#exec uvicorn main:app --host 127.0.0.1 --port 8080