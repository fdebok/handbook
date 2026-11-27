import html
import json
import re
import struct
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
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
                    alternate_locale = "zh_CN" if locale == "en" else "en_US"
                    self.assertIn(
                        f'<meta property="og:locale:alternate" content="{alternate_locale}"/>',
                        page,
                    )
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
            sitemap_root = ET.parse(output / "sitemap.xml").getroot()
            sitemap_ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            xhtml_ns = "{http://www.w3.org/1999/xhtml}"
            entries = sitemap_root.findall("sm:url", sitemap_ns)
            self.assertEqual(len(entries), 2)
            expected_alternates = {
                "zh-CN": build_site.ZH_URL,
                "en": build_site.EN_URL,
                "x-default": build_site.EN_URL,
            }
            for entry in entries:
                loc = entry.findtext("sm:loc", namespaces=sitemap_ns)
                self.assertIn(loc, {build_site.ZH_URL, build_site.EN_URL})
                alternates = {
                    link.attrib["hreflang"]: link.attrib["href"]
                    for link in entry.findall(f"{xhtml_ns}link")
                }
                self.assertEqual(alternates, expected_alternates)

    def test_indexnow_key_is_published_and_notified_after_deployment(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            key_file = output / f"{build_site.INDEXNOW_KEY}.txt"
            self.assertEqual(key_file.read_text(encoding="utf-8").strip(), build_site.INDEXNOW_KEY)

        workflow = (ROOT / ".github" / "workflows" / "static.yml").read_text(encoding="utf-8")
        deploy_step = workflow.index("- name: Deploy to GitHub Pages")
        verify_step = workflow.index("- name: Verify published discovery endpoints")
        notify_step = workflow.index("- name: Notify IndexNow")
        self.assertLess(deploy_step, verify_step)
        self.assertLess(verify_step, notify_step)
        self.assertIn("--retry 5 --retry-all-errors", workflow)
        self.assertIn("Unexpected sitemap URLs", workflow)
        self.assertIn("hreflang=\"x-default\"", workflow)
        self.assertIn("https://api.indexnow.org/indexnow", workflow)
        self.assertIn(f'"key":"{build_site.INDEXNOW_KEY}"', workflow)
        self.assertIn(f"https://www.fdebok.com/{build_site.INDEXNOW_KEY}.txt", workflow)
        self.assertIn('"urlList":["https://www.fdebok.com/","https://www.fdebok.com/en/"]', workflow)

    def test_robots_allows_search_and_ai_crawlers(self):
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        for user_agent in (
            "Googlebot",
            "Googlebot-Image",
            "bingbot",
            "Applebot",
            "Applebot-Extended",
            "Baiduspider",
            "OAI-SearchBot",
            "ChatGPT-User",
            "GPTBot",
            "Claude-SearchBot",
            "Claude-User",
            "ClaudeBot",
            "PerplexityBot",
            "Perplexity-User",
            "*",
        ):
            with self.subTest(user_agent=user_agent):
                self.assertIn(f"User-agent: {user_agent}\nAllow: /", robots)
        self.assertIn("Sitemap: https://www.fdebok.com/sitemap.xml", robots)

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

    def test_primary_pages_have_localized_search_metadata_and_structured_data(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            pages = {
                "zh": (output / "index.html").read_text(encoding="utf-8"),
                "en": (output / "en" / "index.html").read_text(encoding="utf-8"),
            }

        expectations = {
            "zh": {
                "language": "zh-CN",
                "url": build_site.ZH_URL,
                "title": "FDEBOK｜FDE 指南：前线部署工程师知识体系与企业 AI 交付",
                "description_phrase": "FDE 是什么",
                "keyword": "FDE 职业发展",
                "badge_keyword": "FDEBOK A/P/M 学习徽章",
                "organization_phrase": "官方发布",
                "slogan": "三点架成桥，洞察连工程，AI 稳落地，价值步步通",
                "teaches_phrase": "FDE 角色与职责",
            },
            "en": {
                "language": "en",
                "url": build_site.EN_URL,
                "title": build_site.EN_TITLE,
                "description_phrase": "Forward Deployed Engineer (FDE)",
                "keyword": "FDE career development",
                "badge_keyword": "FDEBOK A/P/M learning badges",
                "organization_phrase": "official publication",
                "slogan": "Three points form a bridge: insight meets engineering, AI lands reliably, and value flows through every step.",
                "teaches_phrase": "Forward Deployed Engineer roles",
            },
        }
        for locale, page in pages.items():
            expected = expectations[locale]
            with self.subTest(locale=locale):
                self.assertIn(f'<html lang="{expected["language"]}"', page)
                self.assertIn(f"<title>{expected['title']}</title>", page)
                self.assertIn(f'<link rel="canonical" href="{expected["url"]}"/>', page)
                self.assertIn(
                    f'hreflang="{"en" if locale == "zh" else "zh-CN"}"',
                    page,
                )
                self.assertIn(expected["description_phrase"], html.unescape(page))

                match = re.search(
                    r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                    page,
                    re.DOTALL,
                )
                self.assertIsNotNone(match)
                graph = json.loads(match.group(1))["@graph"]
                organization = next(item for item in graph if item["@type"] == "Organization")
                webpage = next(item for item in graph if item["@type"] == "WebPage")
                handbook = next(
                    item
                    for item in graph
                    if "CreativeWork" in (
                        item["@type"] if isinstance(item["@type"], list) else [item["@type"]]
                    )
                )
                self.assertEqual(organization["sameAs"], "https://github.com/fdebok/handbook")
                self.assertIn(expected["organization_phrase"], organization["description"])
                self.assertEqual(organization["slogan"], expected["slogan"])
                self.assertEqual(handbook["author"], {"@id": organization["@id"]})
                self.assertEqual(handbook["publisher"], {"@id": organization["@id"]})
                self.assertIn("LearningResource", handbook["@type"])
                self.assertEqual(webpage["inLanguage"], expected["language"])
                self.assertEqual(webpage["url"], expected["url"])
                self.assertIn(expected["keyword"], handbook["keywords"])
                self.assertIn(expected["badge_keyword"], handbook["keywords"])
                self.assertEqual(len(handbook["citation"]), 4)
                self.assertTrue(handbook["teaches"])
                self.assertTrue(
                    any(expected["teaches_phrase"] in item for item in handbook["teaches"])
                )
                self.assertIn(
                    "Professional handbook" if locale == "en" else "专业知识手册",
                    handbook["learningResourceType"],
                )

    def test_feedback_and_repository_links_point_to_the_canonical_project(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("github.com/fdebok/fdebok", source)
        self.assertIn("https://github.com/fdebok/handbook/issues/new?template=content-feedback.yml", source)
        self.assertIn("https://github.com/fdebok/handbook/issues/new?template=assessment-feedback.yml", source)

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

    def test_mobile_share_fallback_is_localized_and_compact(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            chinese = (output / "index.html").read_text(encoding="utf-8")
            english = (output / "en" / "index.html").read_text(encoding="utf-8")

        for page, button_label, copy_label in (
            (chinese, "复制配文和链接", "分享内容（配文与链接）"),
            (english, "Copy message and link", "Share message and link"),
        ):
            with self.subTest(button_label=button_label):
                self.assertIn('id="share-quick-copy-button"', page)
                self.assertIn(button_label, page)
                self.assertIn(copy_label, page)
                self.assertIn('.share-panel[data-mode="quick"] .share-platform-picker', page)
                self.assertIn('.share-panel[data-mode="quick"] .share-quick-actions{display:flex}', page)
                self.assertIn("navigator.share", page)

    def test_brand_slogan_is_metadata_only_and_logo_scales_with_wordmark(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            chinese = (output / "index.html").read_text(encoding="utf-8")
            english = (output / "en" / "index.html").read_text(encoding="utf-8")

        for locale, page in (("zh", chinese), ("en", english)):
            with self.subTest(locale=locale):
                self.assertNotIn('class="brand-meaning"', page)
                self.assertIn('<h1><img alt="" class="cover-brand-mark"', page)
                self.assertIn('gap:.16em', page)
                self.assertIn('.cover-brand-mark{width:.82em;height:.82em', page)
                self.assertIn('font-size:clamp(46px,14vw,68px)', page)

    def test_branding_assets_and_locale_share_cards_are_published(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            chinese = (output / "index.html").read_text(encoding="utf-8")
            english = (output / "en" / "index.html").read_text(encoding="utf-8")
            wechat = (output / "share" / "zh" / "wechat" / "index.html").read_text(encoding="utf-8")
            linkedin = (output / "share" / "en" / "linkedin" / "index.html").read_text(encoding="utf-8")
            assets = {
                name: (output / name).read_bytes()
                for name in (
                    "favicon.svg",
                    "brand-mark.svg",
                    "brand-logo.svg",
                    "apple-touch-icon.png",
                    "og-image.png",
                    "og-image-en.png",
                    "share-card-zh-v4.png",
                    "share-card-en-v4.png",
                )
            }

        for asset in ("favicon.svg", "brand-mark.svg", "brand-logo.svg", "apple-touch-icon.png"):
            with self.subTest(asset=asset):
                self.assertTrue(assets[asset])

        svg_namespace = "{http://www.w3.org/2000/svg}"
        for asset in ("favicon.svg", "brand-mark.svg", "brand-logo.svg"):
            with self.subTest(asset=asset):
                root = ET.fromstring(assets[asset])
                self.assertEqual(root.tag, f"{svg_namespace}svg")

        logo_root = ET.fromstring(assets["brand-logo.svg"])
        self.assertTrue(logo_root.find(f".//{svg_namespace}symbol[@id='fde-mark']") is not None)
        self.assertTrue(logo_root.find(f".//{svg_namespace}use[@href='#fde-mark']") is not None)

        self.assertIn('href="/favicon.svg?v=4"', chinese)
        self.assertIn('href="/apple-touch-icon.png?v=4"', chinese)
        self.assertIn('src="/brand-mark.svg?v=4"', chinese)
        self.assertIn('src="/brand-logo.svg?v=4"', wechat)
        self.assertIn(".brand-logo{width:min(190px,48vw)}", wechat)
        self.assertIn("neural FDE monogram over a subtle globe grid", assets["brand-mark.svg"].decode())
        self.assertIn('content="https://www.fdebok.com/share-card-zh-v4.png"', chinese)
        self.assertIn('content="https://www.fdebok.com/share-card-en-v4.png"', english)
        self.assertIn('og:image" content="https://www.fdebok.com/share-card-zh-v4.png"', wechat)
        self.assertIn('og:image" content="https://www.fdebok.com/share-card-en-v4.png"', linkedin)
        for filename, dimensions in (
            ("share-card-zh-v4.png", (1200, 630)),
            ("share-card-en-v4.png", (1200, 630)),
            ("og-image.png", (1200, 630)),
            ("og-image-en.png", (1200, 630)),
            ("apple-touch-icon.png", (180, 180)),
        ):
            with self.subTest(filename=filename):
                image_header = assets[filename][:24]
                self.assertEqual(image_header[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", image_header[16:24]), dimensions)

    def test_badge_program_is_localized_and_clearly_separate_from_certification(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "site"
            build_site.build(output)
            chinese = (output / "index.html").read_text(encoding="utf-8")
            english = (output / "en" / "index.html").read_text(encoding="utf-8")
            llms = (output / "llms.txt").read_text(encoding="utf-8")

            for filename in ("badge-a.png", "badge-p.png", "badge-m.png"):
                image = (output / filename).read_bytes()
                self.assertEqual(image[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(struct.unpack(">II", image[16:24]), (320, 390))

            self.assertFalse((output / "assets" / "fdebok-badges-approved-v28-source.png").exists())

        self.assertIn('id="fde-badges"', chinese)
        self.assertIn("A/P/M 徽章是 FDEBOK 独立项目，与本手册 L1–L5 能力自查体系不可互换或换算", chinese)
        self.assertIn("政府职业资格或行业统一认证，也不代表雇主背书", chinese)
        self.assertIn("邮件人工办理", chinese)
        self.assertIn('href="mailto:x@fdebok.com?subject=FDEBOK%20Badge%20Inquiry"', chinese)
        self.assertIn("A/P/M Learning Badges", english)
        self.assertIn("A · Engineer", english)
        self.assertIn("FDE practitioner · recommendation · knowledge assessment", english)
        self.assertIn("P · Professional", english)
        self.assertIn("practical project-delivery assessment and peer review", english)
        self.assertIn("M · Master", english)
        self.assertIn("verifiable professional experience or project endorsement", english)
        self.assertIn("badge-status verification", english)
        self.assertIn("handled manually by email", english)
        self.assertIn("not government-issued qualifications or industry-wide certifications", english)
        self.assertIn("separate from the handbook's L1–L5 self-assessment", english)
        self.assertIn("The FDEBOK volunteer team reviews applications and issues A/P/M", llms)
        self.assertIn("FDEBOK 志愿者团队面向 FDE 从业者审核并发放", llms)
        self.assertIn("Do FDEBOK A/P/M badges count as formal FDE certifications?", llms)

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
