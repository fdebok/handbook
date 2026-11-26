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
