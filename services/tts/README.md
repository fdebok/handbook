# Offline TTS audition service

This directory contains a local-only, one-segment voice audition tool. It does
not expose an HTTP endpoint and does not send narration text to a hosted TTS
provider. The first run downloads the pinned, Apache-2.0 Qwen3-TTS model into
the local Hugging Face cache.

Build the CPU-only image from the repository root:

```sh
docker build -f services/tts/Dockerfile -t fdebok-tts .
```

Generate one audition clip from the repository root:

```sh
docker run --rm --cpus=2 \
  -v "$PWD/audio:/workspace/audio" \
  -v "$HOME/.cache/huggingface:/root/.cache/huggingface" \
  fdebok-tts --locale all --voice both --segment c1-s1
```

This generates one Chinese and one English audition in each voice, loading the
model once. Use `--locale zh-CN` or `--locale en` to generate only one language,
and `--voice female` or `--voice male` to generate only one voice. The output is
written under `audio/pilot/audition/`; the static-site builder does not publish
that directory. Delete audition files after review if they are not approved
for publication.

The English female voice currently uses the model's Chinese-native `Serena`
timbre cross-lingually. Treat all four selected voices as audition candidates,
not approved production voices. In particular, verify English pronunciation,
accent, naturalness, and consistency by listening before generating the full
chapter. The voices are synthetic presets, not imitations of real people.
