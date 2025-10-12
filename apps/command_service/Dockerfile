# syntax=docker/dockerfile:1

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install runtime deps
RUN pip install --upgrade pip && \
    pip install \
      fastapi==0.118.3 \
      uvicorn[standard]==0.37.0 \
      pydantic==2.12.0

# Copy only necessary sources (avoid copying local venv)
COPY main.py /app/main.py
COPY models.py /app/models.py
COPY commands_db.py /app/commands_db.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


