import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_site


class SharePageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.content = build_site.load_share_content(source)

    def test_platform_pages_have_distinct_previews_and_canonical_handbook_urls(self):
        for locale, platforms in build_site.SHARE_PLATFORMS.items():
            canonical = build_site.EN_URL if locale == "en" else build_site.ZH_URL
            for platform in platforms:
                with self.subTest(locale=locale, platform=platform):
                    page = build_site.render_share_page(
                        locale, platform, self.content[locale][platform]
                    )
                    share_url = f"https://www.fdebok.com/share/{locale}/{platform}/"
                    self.assertIn(f'<meta name="robots" content="noindex,follow', page)
                    self.assertIn(
                        "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; "
                        "script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'",
                        page,
                    )
                    self.assertIn(f'<link rel="canonical" href="{canonical}"/>', page)
                    self.assertIn(f'<meta property="og:url" content="{share_url}"/>', page)
                    self.assertIn(
                        f'<meta property="og:description" content="{self.content[locale][platform]["caption"]}"/>',
                        page,
                    )
                    self.assertIn(self.content[locale][platform]["title"], page)
                    self.assertIn(self.content[locale][platform]["kicker"], page)
                    self.assertNotIn("<script", page.lower())

    def test_platform_content_is_escaped_before_rendering(self):
        unsafe_content = dict(self.content["en"]["facebook"])
        unsafe_content["caption"] = '<img src=x onerror="alert(1)"> & trusted text'
        page = build_site.render_share_page("en", "facebook", unsafe_content)
        self.assertIn(
            "&lt;img src=x onerror=&quot;alert(1)&quot;&gt; &amp; trusted text",
            page,
        )
        self.assertNotIn('<img src=x onerror="alert(1)">', page)

    def test_build_writes_all_supported_platform_routes(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            for locale, platforms in build_site.SHARE_PLATFORMS.items():
                for platform in platforms:
                    route = output / "share" / locale / platform / "index.html"
                    self.assertTrue(route.is_file(), route)

            sitemap = (output / "sitemap.xml").read_text(encoding="utf-8")
            self.assertNotIn("/share/", sitemap)

    def test_build_renders_correct_english_titles_and_related_copy(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            english = (output / "en" / "index.html").read_text(encoding="utf-8")

        for expected in (
            "<h2>Growth and assessment</h2>",
            "Capability can be developed, but only by taking responsibility for outcomes.",
            "Learning roadmap and getting started in 90 days",
            "<h4>21.1 · A 30-day cadence</h4>",
            "<h4>21.2 · Strengths and gaps for career changers</h4>",
            "Hiring assessment and personal self-assessment",
            "<h4>22.1 · Six interview questions</h4>",
            "<h4>22.2 · Ten-question self-assessment</h4>",
            "<h2>Appendices</h2>",
            "APPENDIX A · Terminology</span>Chinese–English quick reference",
            "Three reading paths",
            "<h4>Stuck on a project?</h4>",
            "<h4>Building a delivery team</h4>",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, english)

    def test_build_does_not_render_print_or_pdf_button(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            chinese = (output / "index.html").read_text(encoding="utf-8")
            english = (output / "en" / "index.html").read_text(encoding="utf-8")

        for page in (chinese, english):
            self.assertNotIn("domain-check-print", page)
            self.assertNotIn("window.print()", page)
            self.assertNotIn("打印 / 保存为 PDF", page)
            self.assertNotIn("Print / Save as PDF", page)

    def test_build_keeps_english_tables_and_reading_paths_aligned(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        translations, _ = build_site.load_translations(source)
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            english = (output / "en" / "index.html").read_text(encoding="utf-8")

        for key, expected in (
            ("英文", "English"),
            ("中文", "Chinese"),
            ("含义要点", "Key points"),
            ("目标", "Goal"),
            ("必须完成的具体产出", "Required deliverables"),
            ("考察题", "Interview question"),
            ("想看到什么", "What to look for"),
            ("危险信号", "Red flags"),
            ("产品反哺", "Product feedback loop"),
            (
                "最近一个我交付的功能，我能说出它改变了哪个具体业务指标吗",
                "For the last feature I delivered, can I name the specific business metric it changed?",
            ),
        ):
            with self.subTest(key=key):
                self.assertEqual(translations[key], expected)

        for expected in (
            '<th style="width:230px">English</th><th style="width:150px">Chinese</th><th>Key points</th>',
            '<td>Forward Deployed Engineer</td><td>Forward Deployed Engineer</td><td>An end-to-end problem owner who builds production systems',
            '<tr><td>Use-case Pool</td><td>Use-case pool</td>',
            '<th style="width:120px">Stage</th><th>Goal</th><th>Required deliverables</th>',
            '<th style="width:210px">Interview question</th><th>What to look for</th><th>Red flags</th>',
            '<div class="kk">Path 1</div><h4>Stuck on a project?</h4>',
            '<a class="xref" href="#c7">skills matrix</a> to identify areas where you have only observed others; use the <a class="xref" href="#c21">90-day path</a>',
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, english)

    def test_share_content_defines_only_supported_platforms(self):
        invalid = json.dumps({"zh": {}, "en": {}})
        source = (
            '<script id="share-content-data" type="application/json">'
            + invalid
            + "</script>"
        )
        with self.assertRaisesRegex(RuntimeError, "Unexpected platform list"):
            build_site.load_share_content(source)

    def test_x_post_copy_leaves_room_for_the_link(self):
        x_caption = self.content["en"]["x"]["caption"]
        self.assertLessEqual(len(x_caption) + 23, 280)


if __name__ == "__main__":
    unittest.main()
