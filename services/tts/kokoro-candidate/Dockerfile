FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=2 \
    KOKORO_MODEL_DIR=/root/.cache/fdebok-kokoro

RUN apt-get update \
    && apt-get install -y --no-install-recommends espeak-ng libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY services/tts/kokoro-candidate/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY services/tts/kokoro-candidate/generate_auditions.py /opt/fdebok-kokoro/generate_auditions.py

ENTRYPOINT ["python", "/opt/fdebok-kokoro/generate_auditions.py"]
