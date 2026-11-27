FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OMP_NUM_THREADS=2 \
    HF_HOME=/root/.cache/huggingface

RUN apt-get update \
    && apt-get install -y --no-install-recommends libsndfile1 sox libsox-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY services/tts/requirements.txt /workspace/requirements.txt
# Gradio is only needed by the upstream demo UI, not this offline CLI tool.
RUN pip install --no-cache-dir torch==2.9.0+cpu torchaudio==2.9.0+cpu \
      --extra-index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir --no-deps qwen-tts==0.1.1 \
    && pip install --no-cache-dir -r /workspace/requirements.txt

COPY services/tts/generate_audition.py /workspace/generate_audition.py
COPY services/tts/voice-profiles.json /workspace/voice-profiles.json

ENTRYPOINT ["python", "/workspace/generate_audition.py"]
