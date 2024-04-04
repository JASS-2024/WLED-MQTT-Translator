FROM python:3.11.9-alpine3.19
COPY ./ ./
RUN python -m pip install -r requirements.txt
CMD python translator.py
