# Kokoro audition candidate

This is an isolated, local-only evaluation path for Kokoro-ONNX. It does not
replace the existing Qwen audition service, expose an HTTP endpoint, or publish
audio automatically. The candidate uses the English Kokoro v1.0 model and the
Chinese-capable v1.1-zh model, both int8, with one female and one male voice per
language. The short pilot script is used, with FDEBOK normalized to
“eff-dee-bok” before phonemization.

Build from the repository root:

```sh
docker build -f services/tts/kokoro-candidate/Dockerfile -t fdebok-kokoro-audition .
```

Generate the four review-only WAVs:

```sh
docker run --rm --cpus=2 \
  -v "$PWD:/workspace" \
  -v "$HOME/.cache/fdebok-kokoro:/root/.cache/fdebok-kokoro" \
  fdebok-kokoro-audition
```

The first run downloads pinned model weights and voice data. WAVs are written
under `audio/pilot/audition/kokoro/`, separate from existing auditions and
excluded from publication. Listen for pronunciation, prosody, clarity, voice
character, and whether the Chinese voice handles mixed English naturally.
Kokoro has no natural-language style instruction, so these clips evaluate its
actual preset delivery rather than applying the Qwen voice instructions.

Model weights are Apache-2.0. Kokoro-ONNX is MIT-licensed. The separately
published voice packs and dependencies should be checked against their
upstream license notices again before any generated audio or bundled model
assets are redistributed.
