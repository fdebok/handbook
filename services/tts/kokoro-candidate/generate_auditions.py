import argparse
import hashlib
import json
import os
import re
import tempfile
import time
import urllib.request
from pathlib import Path


WORKSPACE = Path("/workspace")
AUDIO_ROOT = Path(os.environ.get("AUDIO_ROOT", WORKSPACE / "audio"))
MODEL_DIR = Path(
    os.environ.get("KOKORO_MODEL_DIR", Path.home() / ".cache/fdebok-kokoro")
)
SEGMENT_ID = "c1-s1"
ASSETS = {
    "en": {
        "model": (
            "kokoro-v1.0.int8.onnx",
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
            "model-files-v1.1/kokoro-v1.0.int8.onnx",
            "ae315a79b623f244700e4afb9246c46a26066782e049ba174bf3ba433970ee9c",
        ),
        "voices": (
            "voices-v1.0.bin",
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
            "model-files-v1.1/voices-v1.0.bin",
            "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d",
        ),
    },
    "zh": {
        "model": (
            "kokoro-v1.1-zh.int8.onnx",
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
            "model-files-v1.1/kokoro-v1.1-zh.int8.onnx",
            "11751c087b4bbeed031e2b687b11dda698bd27ba0509472f960b57f835a999f7",
        ),
        "voices": (
            "voices-v1.1-zh.bin",
            "https://github.com/thewh1teagle/kokoro-onnx/releases/download/"
            "model-files-v1.1/voices-v1.1-zh.bin",
            "14cb6186c99e4f6016871405f62046c5df863ae27465cbdc4ee08be7dd703acd",
        ),
        "vocab": (
            "zh-config.json",
            "https://huggingface.co/hexgrad/Kokoro-82M-v1.1-zh/"
            "raw/main/config.json",
            "bc333efa5ce4ceff433c8c8e5d027a1eca0166001e4e4a62bea2d26ff7a46890",
        ),
    },
}
VOICE_CHOICES = {
    "zh-CN": {
        "female": ("知微", "zf_001"),
        "male": ("行远", "zm_010"),
    },
    "en": {
        "female": ("Mira", "af_heart"),
        "male": ("Miles", "am_michael"),
    },
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate review-only Kokoro voice audition clips."
    )
    parser.add_argument(
        "--locale", choices=("zh-CN", "en", "all"), default="all"
    )
    parser.add_argument(
        "--voice", choices=("female", "male", "both"), default="both"
    )
    return parser.parse_args()


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_asset(asset):
    filename, url, expected_sha256 = asset
    target = MODEL_DIR / filename
    if target.exists():
        if expected_sha256 is None or sha256_file(target) == expected_sha256:
            target.chmod(0o644)
            return target
        target.unlink()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=MODEL_DIR, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "fdebok-kokoro-audition/1.0"}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            with temporary_path.open("wb") as file:
                while chunk := response.read(1024 * 1024):
                    file.write(chunk)
        if expected_sha256 is not None:
            actual_sha256 = sha256_file(temporary_path)
            if actual_sha256 != expected_sha256:
                raise ValueError(
                    f"SHA-256 mismatch for {filename}: {actual_sha256}"
                )
        temporary_path.replace(target)
        target.chmod(0o644)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    return target


def load_segment(locale):
    script_locale = "zh" if locale == "zh-CN" else "en"
    script_path = AUDIO_ROOT / "scripts" / script_locale / "c01.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    if script.get("locale") != locale or script.get("chapterId") != "c1":
        raise ValueError(f"Unexpected pilot script metadata in {script_path}")
    segment = next(
        (item for item in script.get("segments", []) if item.get("id") == SEGMENT_ID),
        None,
    )
    if segment is None or not segment.get("auditionText", "").strip():
        raise ValueError(f"Pilot script {script_path} has no {SEGMENT_ID} audition")
    return segment


def speech_text(text, nickname):
    text = text.replace("{host_name}", nickname)
    return re.sub(r"\bFDEBOK\b", "eff-dee-bok", text, flags=re.IGNORECASE)


def generate_locale(locale, genders):
    import soundfile as sf
    from kokoro_onnx import Kokoro

    model_key = "zh" if locale == "zh-CN" else "en"
    assets = ASSETS[model_key]
    model_path = download_asset(assets["model"])
    voices_path = download_asset(assets["voices"])
    vocab_path = (
        download_asset(assets["vocab"]) if model_key == "zh" else None
    )

    started = time.perf_counter()
    model = Kokoro(
        str(model_path),
        str(voices_path),
        vocab_config=str(vocab_path) if vocab_path else None,
    )
    load_seconds = time.perf_counter() - started

    if model_key == "zh":
        from misaki import zh

        g2p = zh.ZHG2P(
            version="1.1",
            en_callable=lambda text: model.tokenizer.phonemize(text, lang="en-us"),
        )

    segment = load_segment(locale)
    output_dir = AUDIO_ROOT / "pilot" / "audition" / "kokoro"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"{locale}: model and voice data loaded in {load_seconds:.2f}s")
    for gender in genders:
        nickname, voice_id = VOICE_CHOICES[locale][gender]
        if voice_id not in model.get_voices():
            raise ValueError(f"Voice {voice_id!r} is missing from {voices_path}")
        text = speech_text(segment["auditionText"], nickname)
        if model_key == "zh":
            phonemes, _ = g2p(text)
        else:
            phonemes = model.tokenizer.phonemize(text, lang="en-us")
        started = time.perf_counter()
        samples, sample_rate = model.create(
            phonemes, voice=voice_id, speed=1.0, is_phonemes=True
        )
        synthesis_seconds = time.perf_counter() - started
        duration_seconds = len(samples) / sample_rate
        output_path = output_dir / f"{locale}-{gender}-{SEGMENT_ID}.wav"
        sf.write(output_path, samples, sample_rate, subtype="PCM_16")
        print(
            f"{output_path}: {duration_seconds:.2f}s audio, "
            f"{synthesis_seconds:.2f}s synthesis, "
            f"RTF {synthesis_seconds / duration_seconds:.2f}"
        )


def main():
    args = parse_args()
    locales = ("zh-CN", "en") if args.locale == "all" else (args.locale,)
    genders = ("female", "male") if args.voice == "both" else (args.voice,)
    for locale in locales:
        generate_locale(locale, genders)


if __name__ == "__main__":
    main()
