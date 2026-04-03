FROM docker.io/python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY generated/ generated/
COPY ui/ ui/
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=2s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/v1/health')"
CMD ["uvicorn", "generated.app:app", "--host", "0.0.0.0", "--port", "8080"]
