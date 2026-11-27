import argparse
import json
import os
from pathlib import Path


WORKSPACE = Path("/workspace")
AUDIO_ROOT = Path(os.environ.get("AUDIO_ROOT", WORKSPACE / "audio"))
PROFILES_PATH = WORKSPACE / "voice-profiles.json"
MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
MODEL_REVISION = "85e237c12c027371202489a0ec509ded67b5e4b5"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate one local, review-only voice audition from a pilot script."
    )
    parser.add_argument("--locale", choices=("zh-CN", "en", "all"), required=True)
    parser.add_argument("--voice", choices=("female", "male", "both"), required=True)
    parser.add_argument("--segment", required=True, help="Pilot segment ID, e.g. c1-s1")
    return parser.parse_args()


def load_segment(locale, segment_id, audio_root=AUDIO_ROOT):
    script_locale = {"zh-CN": "zh", "en": "en"}.get(locale)
    if script_locale is None:
        raise ValueError(f"Unsupported locale: {locale}")
    script_path = audio_root / "scripts" / script_locale / "c01.json"
    script = json.loads(script_path.read_text(encoding="utf-8"))
    if script.get("locale") != locale or script.get("chapterId") != "c1":
        raise ValueError(f"Unexpected pilot script metadata in {script_path}")
    segment = next(
        (item for item in script.get("segments", []) if item.get("id") == segment_id),
        None,
    )
    if segment is None:
        raise ValueError(f"Segment {segment_id!r} is not in {script_path}")
    if not segment.get("auditionText", "").strip():
        raise ValueError(f"Segment {segment_id!r} has no short audition text")
    return segment


def render_host_name(text, voice):
    return text.replace("{host_name}", voice["nickname"])


def main():
    args = parse_args()
    profiles = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    if (
        profiles.get("model") != MODEL_ID
        or profiles.get("revision") != MODEL_REVISION
        or profiles.get("license") != "Apache-2.0"
    ):
        raise ValueError("Voice profile model metadata does not match the pinned model")

    try:
        import soundfile as sf
        import torch
        from qwen_tts import Qwen3TTSModel
    except ImportError as error:
        raise RuntimeError(
            "The isolated TTS dependencies are missing; build the service Docker image first."
        ) from error

    locales = ("zh-CN", "en") if args.locale == "all" else (args.locale,)
    genders = ("female", "male") if args.voice == "both" else (args.voice,)
    auditions = [
        (locale, gender, load_segment(locale, args.segment), profiles["voices"][locale][gender])
        for locale in locales
        for gender in genders
    ]

    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "2")))
    torch.manual_seed(2026)
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        revision=MODEL_REVISION,
        device_map="cpu",
        dtype=torch.bfloat16,
        attn_implementation="eager",
    )

    output_dir = AUDIO_ROOT / "pilot" / "audition"
    output_dir.mkdir(parents=True, exist_ok=True)
    for locale, gender, segment, voice in auditions:
        language = "Chinese" if locale == "zh-CN" else "English"
        waveforms, sample_rate = model.generate_custom_voice(
            text=render_host_name(segment["auditionText"], voice),
            language=language,
            speaker=voice["speaker"],
            instruct=voice["instruct"],
            max_new_tokens=512,
        )
        output_path = output_dir / f"{locale}-{gender}-{args.segment}.wav"
        sf.write(output_path, waveforms[0], sample_rate, subtype="PCM_16")
        print(f"Generated review-only audition: {output_path}")


if __name__ == "__main__":
    main()
