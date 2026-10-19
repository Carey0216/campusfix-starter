FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/data/campusfix.db
WORKDIR /app
COPY requirements-runtime.txt .
RUN python -m pip install --no-cache-dir -r requirements-runtime.txt \
    && groupadd --gid 10001 campusfix \
    && useradd --uid 10001 --gid campusfix --no-create-home campusfix \
    && mkdir -p /app/data \
    && chown campusfix:campusfix /app/data
COPY --chown=campusfix:campusfix app.py init_db.py container_entrypoint.py schema.sql VERSION ./
COPY --chown=campusfix:campusfix templates ./templates
USER campusfix
EXPOSE 5000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=2)"
CMD ["python", "container_entrypoint.py"]
