FROM python:3.10.15-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# CMD ["fastapi", "run", "app/main.py", "--reload", "--host", "0.0.0.0", "--port", "8000"]

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
# CMD ["sh", "-c", ". venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]