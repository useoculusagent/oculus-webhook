FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir .
COPY oculus_webhook ./oculus_webhook
EXPOSE 8000
CMD ["uvicorn", "oculus_webhook.app:app", "--host", "0.0.0.0", "--port", "8000"]

<!-- rev 11 -->

<!-- rev 13 -->

<!-- rev 14 -->

<!-- rev 15 -->
# rev 7
