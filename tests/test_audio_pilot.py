import json
import re
import unittest
from pathlib import Path

from services.tts.generate_audition import load_segment, render_host_name


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "audio/pilot/manifest.json"
SOURCE_PATH = ROOT / "src" / "site" / "pages" / "zh" / "index.html"
VOICE_PROFILES_PATH = ROOT / "services/tts/voice-profiles.json"


class AudioPilotTests(unittest.TestCase):
    def test_bilingual_scripts_share_chapter_sections_and_source_anchors(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        source = SOURCE_PATH.read_text(encoding="utf-8")
        chapter = re.search(r'<article id="c1">([\s\S]*?)</article>', source)
        self.assertIsNotNone(chapter)
        source_anchors = set(re.findall(r'<h4 id="([^"]+)"', chapter.group(1)))

        scripts = {}
        for locale, details in manifest["locales"].items():
            script_path = (MANIFEST_PATH.parent / details["script"]).resolve()
            script = json.loads(script_path.read_text(encoding="utf-8"))
            self.assertEqual(script["chapterId"], manifest["chapterId"])
            self.assertEqual(script["locale"], locale)
            scripts[locale] = script

            segment_ids = [segment["id"] for segment in script["segments"]]
            self.assertEqual(len(segment_ids), len(set(segment_ids)))
            for segment in script["segments"]:
                self.assertTrue(segment["transcript"].strip())
                self.assertTrue(
                    segment["transcript"].startswith(
                        "你好！我是{host_name}，FDEBOK 的 AI 讲师。"
                        "欢迎来到《FDE实践指南》。现在进入第一章"
                        if locale == "zh-CN"
                        else "Hello! I'm {host_name}, FDEBOK's AI instructor. "
                        "Welcome to the FDE Practice Guide. We now begin Chapter 1"
                    )
                )
                if segment["id"] == "c1-s4":
                    expected_closing = (
                        "本章就到这里。"
                        if locale == "zh-CN"
                        else "That brings this chapter to a close."
                    )
                else:
                    expected_closing = (
                        "本节就到这里。"
                        if locale == "zh-CN"
                        else "That brings this section to a close."
                    )
                self.assertIn(expected_closing, segment["transcript"])
                self.assertIn("x@fdebok.com", segment["transcript"].splitlines()[-1])
                if segment["id"] == "c1-s1":
                    self.assertTrue(segment["auditionText"].strip())
                    transcript_parts = segment["transcript"].split("\n\n")
                    self.assertTrue(segment["auditionText"].startswith(transcript_parts[0]))
                    self.assertTrue(segment["auditionText"].endswith(transcript_parts[-1]))
                    self.assertTrue(
                        segment["auditionText"].startswith(
                            "你好！我是{host_name}，FDEBOK 的 AI 讲师。"
                            if locale == "zh-CN"
                            else "Hello! I'm {host_name}, FDEBOK's AI instructor."
                        )
                    )
                    self.assertIn("x@fdebok.com", segment["auditionText"])
                self.assertEqual(segment["id"], segment["sourceAnchor"])
                self.assertIn(segment["sourceAnchor"], source_anchors)

        self.assertEqual(set(scripts), {"zh-CN", "en"})
        self.assertEqual(
            [segment["id"] for segment in scripts["zh-CN"]["segments"]],
            [segment["id"] for segment in scripts["en"]["segments"]],
        )

    def test_voice_profiles_cover_requested_locales_and_genders(self):
        profiles = json.loads(VOICE_PROFILES_PATH.read_text(encoding="utf-8"))
        self.assertEqual(profiles["license"], "Apache-2.0")
        self.assertRegex(profiles["revision"], r"^[0-9a-f]{40}$")
        self.assertEqual(set(profiles["voices"]), {"zh-CN", "en"})
        for locale, voices in profiles["voices"].items():
            self.assertEqual(set(voices), {"female", "male"})
            for profile in voices.values():
                self.assertTrue(profile["nickname"])
                self.assertTrue(profile["speaker"])
                self.assertTrue(profile["instruct"])
                self.assertIn("FDEBOK", profile["instruct"])
                self.assertIn("eff-dee-bok", profile["instruct"])
                self.assertNotEqual(
                    render_host_name("{host_name}", profile), "{host_name}"
                )
        self.assertEqual(profiles["voices"]["zh-CN"]["female"]["nickname"], "知微")
        self.assertEqual(profiles["voices"]["zh-CN"]["male"]["nickname"], "行远")
        self.assertEqual(profiles["voices"]["en"]["female"]["nickname"], "Mira")
        self.assertEqual(profiles["voices"]["en"]["male"]["nickname"], "Miles")

    def test_tts_runner_resolves_localized_script_directories(self):
        for locale in ("zh-CN", "en"):
            segment = load_segment(locale, "c1-s1", ROOT / "audio")
            self.assertEqual(segment["id"], "c1-s1")
        with self.assertRaisesRegex(ValueError, "Unsupported locale"):
            load_segment("fr", "c1-s1", ROOT / "audio")


if __name__ == "__main__":
    unittest.main()
