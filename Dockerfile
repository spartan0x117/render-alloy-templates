FROM python:3.10-slim

WORKDIR /app

COPY ./render_templates.py .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "render_templates.py"]