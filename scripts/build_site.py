#!/usr/bin/env python3
"""Build the static site, including a crawlable English handbook at /en/."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
EN_URL = "https://www.fdebok.com/en/"
INDEXNOW_KEY = "e4d857d027c4cf696ae94c8f95b07043"
EN_TITLE = "FDEBOK: Forward Deployed Engineer Guide & Handbook"
EN_DESCRIPTION = (
    "The FDEBOK guide explains what a Forward Deployed Engineer (FDE) does, "
    "the role's skills and career paths, and how to deliver enterprise AI—from "
    "discovery and engineering through evaluation and operations."
)
EN_IMAGE_URL = "https://www.fdebok.com/share-card-en-v3.png"
ZH_URL = "https://www.fdebok.com/"
SHARE_PLATFORMS = {
    "zh": ("wechat", "douyin"),
    "en": ("facebook", "linkedin", "x"),
}
PLATFORM_ACCENTS = {
    "wechat": "#65b99a",
    "douyin": "#d2ae58",
    "facebook": "#83aee3",
    "linkedin": "#7eb8ce",
    "x": "#d2ae58",
}
SHARE_FACTS = {
    "zh": ("22 章", "十大知识域", "六阶段交付", "L1–L5 能力框架", "20 类常见痛点", "9 份现场模板"),
    "en": ("22 chapters", "Ten knowledge domains", "Six delivery stages", "L1–L5 competency framework", "20 common challenges", "Nine field templates"),
}
STATIC_FILES = (
    f"{INDEXNOW_KEY}.txt",
    "LICENSE",
    "index.html",
    "llms.txt",
    "apple-touch-icon.png",
    "brand-logo.svg",
    "brand-mark.svg",
    "favicon.svg",
    "og-image.png",
    "og-image-en.png",
    "robots.txt",
    "share-card-en-v3.png",
    "share-card-zh-v3.png",
    "sitemap.xml",
    "share-qr-en.png",
    "share-qr-zh.png",
)
HAN_CHAR = re.compile(r"[\u3400-\u9fff]")
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


def load_translations(source: str) -> tuple[dict[str, str], dict[str, str]]:
    scripts = re.findall(r"<script\b[^>]*>([\s\S]*?)</script>", source, re.IGNORECASE)
    translation_script = next((item for item in scripts if "var ENG=" in item), None)
    if translation_script is None:
        raise RuntimeError("Could not find the ENG translation map in index.html")

    extractor = r"""
const fs = require('fs');
const vm = require('vm');
const source = fs.readFileSync(process.argv[1], 'utf8');
const scripts = [...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
const script = scripts.map(match => match[1]).find(text => text.includes('var ENG='));
if (!script) throw new Error('ENG map not found');
const engStart = script.indexOf('var ENG=');
const attrStart = script.indexOf('var ATTR=', engStart);
const guidanceStart = script.indexOf('var selfCheckGuidance=', attrStart);
if (engStart < 0 || attrStart < 0 || guidanceStart < 0) {
  throw new Error('Translation map boundaries not found');
}
const context = {};
vm.runInNewContext(
  script.slice(engStart, attrStart) + ';globalThis.__ENG=ENG;',
  context,
  {timeout: 2000}
);
vm.runInNewContext(
  script.slice(attrStart, guidanceStart) + ';globalThis.__ATTR=ATTR;',
  context,
  {timeout: 2000}
);
process.stdout.write(JSON.stringify({eng: context.__ENG, attr: context.__ATTR}));
"""
    try:
        result = subprocess.run(
            ["node", "-e", extractor, str(ROOT / "index.html")],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("Node.js is required to read the existing translation map") from error
    data = json.loads(result.stdout)
    return data["eng"], data["attr"]


def load_share_content(source: str) -> dict[str, dict[str, dict[str, str]]]:
    match = re.search(
        r"<script\b(?=[^>]*\bid=[\"']share-content-data[\"'])[^>]*>"
        r"([\s\S]*?)</script>",
        source,
        re.IGNORECASE,
    )
    if match is None:
        raise RuntimeError("Could not find platform-specific share content in index.html")
    try:
        content = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        raise RuntimeError("Platform-specific share content is not valid JSON") from error

    if set(content) != set(SHARE_PLATFORMS):
        raise RuntimeError("Share content must define exactly the supported Chinese and English platforms")
    required_fields = {
        "kicker", "title", "caption", "story", "audience", "cta", "note", "qrNote"
    }
    for locale, platforms in SHARE_PLATFORMS.items():
        if set(content[locale]) != set(platforms):
            raise RuntimeError(f"Unexpected platform list for locale {locale}")
        for platform, values in content[locale].items():
            if set(values) != required_fields or not all(
                isinstance(value, str) and value.strip() for value in values.values()
            ):
                raise RuntimeError(f"Incomplete or invalid share content for {locale}/{platform}")
    return content


def render_share_page(locale: str, platform: str, content: dict[str, str]) -> str:
    if locale not in SHARE_PLATFORMS or platform not in SHARE_PLATFORMS[locale]:
        raise ValueError(f"Unsupported sharing route: {locale}/{platform}")

    is_english = locale == "en"
    language = "en" if is_english else "zh-CN"
    canonical_url = EN_URL if is_english else ZH_URL
    share_url = f"https://www.fdebok.com/share/{locale}/{platform}/"
    share_image = EN_IMAGE_URL if is_english else "https://www.fdebok.com/share-card-zh-v3.png"
    accent = PLATFORM_ACCENTS[platform]
    page_title = f"{content['title']} | FDEBOK"
    description = content["caption"]
    facts_title = "What the handbook covers" if is_english else "手册内容速览"
    facts = "\n".join(f"<li>{html.escape(fact)}</li>" for fact in SHARE_FACTS[locale])
    audience_title = "Who it's for" if is_english else "适合阅读的人"
    switch_label = "Read in Chinese" if is_english else "Read in English"
    switch_url = ZH_URL if is_english else EN_URL
    footer_text = (
        "A practical, open handbook for Forward Deployed Engineers and enterprise AI delivery teams."
        if is_english
        else "面向前线部署工程师与企业 AI 交付团队的开放实践手册。"
    )

    return f"""<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="description" content="{html.escape(description, quote=True)}"/>
<meta name="robots" content="noindex,follow,max-image-preview:large"/>
<meta name="theme-color" content="#142238"/>
<meta name="referrer" content="strict-origin-when-cross-origin"/>
<link rel="icon" href="/favicon.svg?v=3" type="image/svg+xml"/>
<link rel="apple-touch-icon" href="/apple-touch-icon.png?v=3" sizes="180x180"/>
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'"/>
<link rel="canonical" href="{canonical_url}"/>
<title>{html.escape(page_title)}</title>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="FDEBOK"/>
<meta property="og:url" content="{share_url}"/>
<meta property="og:locale" content="{'en_US' if is_english else 'zh_CN'}"/>
<meta property="og:locale:alternate" content="{'zh_CN' if is_english else 'en_US'}"/>
<meta property="og:title" content="{html.escape(content['title'], quote=True)}"/>
<meta property="og:description" content="{html.escape(description, quote=True)}"/>
<meta property="og:image" content="{share_image}"/>
<meta property="og:image:secure_url" content="{share_image}"/>
<meta property="og:image:type" content="image/png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="{'FDEBOK: Forward Deployed Engineer Body of Knowledge' if is_english else 'FDEBOK：前线部署工程师知识体系手册'}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{html.escape(content['title'], quote=True)}"/>
<meta name="twitter:description" content="{html.escape(description, quote=True)}"/>
<meta name="twitter:image" content="{share_image}"/>
<meta name="twitter:image:alt" content="{'FDEBOK: Forward Deployed Engineer Body of Knowledge' if is_english else 'FDEBOK：前线部署工程师知识体系手册'}"/>
<style>
:root{{color-scheme:light;--ink:#142238;--ink2:#223c5e;--gold:#d2ae58;--paper:#f4f5f2;--text:#26313f;--sub:#596879;--line:#dfe4e7;--accent:{accent};font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",Arial,sans-serif}}
*{{box-sizing:border-box}}
body{{min-height:100vh;margin:0;color:var(--text);background:radial-gradient(ellipse at 86% 4%,rgba(210,174,88,.13),transparent 30rem),var(--paper)}}
a{{color:inherit}}
.page{{width:min(100% - 32px,960px);margin:0 auto;padding:24px 0 32px}}
.masthead{{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:8px 2px 22px}}
.brand{{display:inline-flex;align-items:center;gap:12px;color:var(--ink);font-weight:850;letter-spacing:.04em;text-decoration:none}}
.brand-logo{{display:block;width:190px;height:auto;flex:none}}
.masthead-note{{color:var(--sub);font-size:11px;font-weight:750;letter-spacing:.12em;text-align:right;text-transform:uppercase}}
.card{{position:relative;overflow:hidden;padding:clamp(24px,6vw,58px);border:1px solid rgba(30,53,82,.12);border-radius:22px;background:linear-gradient(145deg,#fff 0%,#fbfcfb 62%,#f2f5f4 100%);box-shadow:0 24px 70px rgba(27,45,68,.10)}}
.card::before{{position:absolute;inset:0 auto 0 0;width:5px;background:linear-gradient(var(--accent),var(--gold));content:""}}
.eyebrow{{display:flex;align-items:center;gap:9px;margin:0 0 19px;color:var(--ink2);font-size:11px;font-weight:800;letter-spacing:.14em;text-transform:uppercase}}
.eyebrow::before{{width:19px;height:2px;background:var(--accent);content:""}}
h1{{max-width:760px;margin:0;color:var(--ink);font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:clamp(31px,6vw,58px);letter-spacing:-.025em;line-height:1.13}}
.story{{max-width:760px;margin:20px 0 0;color:#405166;font-size:clamp(16px,2.2vw,20px);line-height:1.75}}
.post-copy{{max-width:760px;margin:20px 0 0;padding:17px 19px;border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:0 11px 11px 0;background:#f8faf9;color:var(--text);font-size:15px;line-height:1.8}}
.details{{margin-top:30px;padding-top:24px;border-top:1px solid var(--line)}}
.details h2,.audience h2{{margin:0 0 13px;color:var(--ink2);font-size:12px;font-weight:850;letter-spacing:.12em;text-transform:uppercase}}
.facts{{display:flex;flex-wrap:wrap;gap:9px;margin:0;padding:0;list-style:none}}
.facts li{{padding:8px 12px;border:1px solid #dfe5e7;border-radius:999px;background:#fff;color:#34465b;font-size:13px;font-weight:700}}
.audience{{margin-top:25px}}
.audience p{{margin:0;color:var(--sub);font-size:14px;line-height:1.7}}
.actions{{display:flex;flex-wrap:wrap;align-items:center;gap:14px;margin-top:30px}}
.cta{{display:inline-flex;min-height:50px;align-items:center;justify-content:center;gap:12px;padding:12px 19px;border:1px solid var(--ink);border-radius:9px;background:var(--ink);color:#fff;font-size:14px;font-weight:800;text-decoration:none;transition:transform .18s,background .18s}}
.cta:hover{{transform:translateY(-1px);background:#223c5e}}
.switch{{color:var(--ink2);font-size:13px;font-weight:700;text-decoration-thickness:1px;text-underline-offset:4px}}
.footer{{display:flex;justify-content:space-between;gap:18px;margin-top:20px;padding:0 3px;color:#687687;font-size:12px;line-height:1.6}}
.footer p{{margin:0}}
@media(max-width:600px){{.page{{width:min(100% - 22px,960px);padding-top:12px}}.masthead{{padding:7px 3px 15px}}.brand-logo{{width:min(190px,48vw)}}.masthead-note{{max-width:120px;font-size:9px;line-height:1.5}}.card{{border-radius:16px}}.post-copy{{padding:14px}}.actions{{align-items:stretch;flex-direction:column}}.cta{{width:100%}}.switch{{text-align:center}}.footer{{flex-direction:column;gap:4px}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{scroll-behavior:auto!important;transition:none!important}}}}
</style>
</head>
<body>
<div class="page">
<header class="masthead">
<a class="brand" href="{canonical_url}">
<img alt="FDEBOK · Forward Deployed Engineer Body of Knowledge" class="brand-logo" height="43" src="/brand-logo.svg?v=3" width="190"/>
</a>
<span class="masthead-note">Forward Deployed Engineer<br/>Body of Knowledge</span>
</header>
<main>
<article class="card" data-platform="{platform}">
<p class="eyebrow">{html.escape(content['kicker'])}</p>
<h1>{html.escape(content['title'])}</h1>
<p class="story">{html.escape(content['story'])}</p>
<p class="post-copy">{html.escape(description)}</p>
<section class="details" aria-labelledby="facts-heading">
<h2 id="facts-heading">{facts_title}</h2>
<ul class="facts">{facts}</ul>
</section>
<section class="audience" aria-labelledby="audience-heading">
<h2 id="audience-heading">{audience_title}</h2>
<p>{html.escape(content['audience'])}</p>
</section>
<div class="actions">
<a class="cta" href="{canonical_url}">{html.escape(content['cta'])}<span aria-hidden="true">→</span></a>
<a class="switch" href="{switch_url}">{switch_label}</a>
</div>
</article>
</main>
<footer class="footer"><p>{html.escape(footer_text)}</p><p>© 2026 FDEBOK · MIT License</p></footer>
</div>
</body>
</html>
"""


class EnglishRenderer(HTMLParser):
    def __init__(self, translations: dict[str, str], attributes: dict[str, str]) -> None:
        super().__init__(convert_charrefs=True)
        self.translations = translations
        self.attribute_translations = attributes
        self.parts: list[str] = []
        self.stack: list[tuple[str, str, str | None]] = []
        self.untranslated_text: set[str] = set()
        self.untranslated_attributes: set[tuple[str, str, str]] = set()
        self.translated_nodes = 0

    def _active(self, tag: str) -> bool:
        return any(item[0] == tag for item in self.stack)

    def _in_langbar(self) -> bool:
        return any("langbar" in item[1].split() for item in self.stack)

    def _script_type(self) -> str | None:
        return next((item[2] for item in reversed(self.stack) if item[0] == "script"), None)

    def _translate_attribute(self, tag: str, key: str, value: str | None, attrs: dict[str, str | None]) -> str | None:
        if value is None:
            return value

        element_id = attrs.get("id")
        known = {
            ("div", "aria-label", "Language / 语言"): "Language selector",
            ("button", "aria-label", "中文 — 切换到中文"): "Chinese — switch to Chinese",
            ("nav", "aria-label", "章节导航"): "Chapter navigation",
            ("span", "aria-label", "全站访问量加载中"): "Site visit count is loading",
            ("button", "aria-label", "返回顶部"): "Back to top",
            ("button", "title", "返回顶部"): "Back to top",
        }
        value = known.get((tag, key, value), value)
        if not self._in_langbar() and key in {
            "alt", "aria-label", "placeholder", "title", "value"
        }:
            value = self.translations.get(value, self.attribute_translations.get(value, value))
            if HAN_CHAR.search(value):
                self.untranslated_attributes.add((tag, key, value))

        if element_id == "btnzh":
            if key == "aria-label":
                return "Chinese — switch to Chinese"
            if key == "aria-pressed":
                return "false"
            if key == "class":
                return " ".join(part for part in (value or "").split() if part != "on")
        if element_id == "btnen":
            if key == "aria-label":
                return "EN — Switch to English"
            if key == "aria-pressed":
                return "true"
            if key == "class":
                classes = (value or "").split()
                return " ".join(classes if "on" in classes else classes + ["on"])
        if tag == "div" and "langbar" in (attrs.get("class") or "").split() and key == "aria-label":
            return "Language selector"
        if tag == "html" and key == "lang":
            return "en"
        if tag == "link" and attrs.get("rel") == "canonical" and key == "href":
            return EN_URL
        if tag == "meta" and key == "content":
            prop = attrs.get("property")
            name = attrs.get("name")
            if name == "description":
                return EN_DESCRIPTION
            if prop in {"og:title"} or name == "twitter:title":
                return EN_TITLE
            if prop == "og:description" or name == "twitter:description":
                return EN_DESCRIPTION
            if prop == "og:url":
                return EN_URL
            if prop == "og:locale":
                return "en_US"
            if prop == "og:locale:alternate":
                return "zh_CN"
            if prop in {"og:image", "og:image:secure_url"} or name == "twitter:image":
                return EN_IMAGE_URL
            if prop == "og:image:alt" or name == "twitter:image:alt":
                return "FDEBOK: Forward Deployed Engineer Body of Knowledge handbook"
        if tag == "img" and element_id == "share-qr-image":
            if key == "src":
                return "/share-qr-en.png"
            if key == "alt":
                return "QR code for the FDEBOK English handbook"
        if tag == "input" and element_id == "share-url" and key == "value":
            return EN_URL
        if tag == "a" and element_id in {"share-facebook", "share-linkedin", "share-x"} and key == "href":
            if element_id == "share-facebook":
                return "https://www.facebook.com/sharer/sharer.php?" + urlencode({"u": EN_URL})
            if element_id == "share-linkedin":
                return "https://www.linkedin.com/sharing/share-offsite/?" + urlencode({"url": EN_URL})
            return "https://twitter.com/intent/tweet?" + urlencode({"url": EN_URL, "text": EN_TITLE})
        return value

    def _start_tag(self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool = False) -> str:
        attr_map = dict(attrs)
        changed_attrs = [
            (key, self._translate_attribute(tag, key, value, attr_map))
            for key, value in attrs
        ]
        rendered = ["<", tag]
        for key, value in changed_attrs:
            rendered.extend([" ", key])
            if value is not None:
                rendered.extend(['="', html.escape(value, quote=True), '"'])
        rendered.append("/>" if self_closing else ">")
        return "".join(rendered)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self._start_tag(tag, attrs))
        if tag not in VOID_TAGS:
            attr_map = dict(attrs)
            self.stack.append((tag, attr_map.get("class") or "", attr_map.get("type")))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.parts.append(self._start_tag(tag, attrs, self_closing=True))

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(f"</{tag}>")
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_comment(self, data: str) -> None:
        self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.parts.append(f"<!{decl}>")

    def handle_entityref(self, name: str) -> None:
        self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.parts.append(f"&#{name};")

    def handle_pi(self, data: str) -> None:
        self.parts.append(f"<?{data}>")

    def unknown_decl(self, data: str) -> None:
        self.parts.append(f"<![{data}]>")

    def handle_data(self, data: str) -> None:
        if self._script_type() == "application/ld+json":
            self.parts.append(self._localize_jsonld(data))
            return
        if self._active("script") or self._active("style") or self._in_langbar():
            self.parts.append(data)
            return
        if self._active("title"):
            self.parts.append(EN_TITLE)
            return
        stripped = data.strip()
        if not stripped or not self._active("body"):
            self.parts.append(data)
            return
        translation = self.translations.get(stripped)
        if translation is None:
            if HAN_CHAR.search(stripped):
                self.untranslated_text.add(stripped)
            self.parts.append(data)
            return
        if translation == stripped:
            self.parts.append(data)
            return
        left = data[: len(data) - len(data.lstrip())]
        right = data[len(data.rstrip()) :]
        self.parts.append(left + translation + right)
        self.translated_nodes += 1

    @staticmethod
    def _localize_jsonld(data: str) -> str:
        try:
            structured_data = json.loads(data)
        except json.JSONDecodeError as error:
            raise RuntimeError("The page's JSON-LD could not be parsed") from error
        for item in structured_data.get("@graph", []):
            item_types = item.get("@type", [])
            if isinstance(item_types, str):
                item_types = [item_types]
            if "Organization" in item_types:
                item["slogan"] = (
                    "Three points form a bridge: insight meets engineering, AI lands "
                    "reliably, and value flows through every step."
                )
                item["description"] = (
                    "FDEBOK is an open bilingual handbook project for Forward Deployed "
                    "Engineers; this website and its GitHub repository are its official "
                    "publication and contribution channels."
                )
            elif "WebPage" in item_types:
                item.update(
                    {
                        "@id": EN_URL + "#webpage",
                        "url": EN_URL,
                        "name": EN_TITLE,
                        "description": EN_DESCRIPTION,
                        "inLanguage": "en",
                        "mainEntity": {"@id": EN_URL + "#handbook"},
                    }
                )
            elif "CreativeWork" in item_types:
                item.update(
                    {
                        "@id": EN_URL + "#handbook",
                        "name": EN_TITLE,
                        "alternateName": "前线部署工程师知识体系手册",
                        "url": EN_URL,
                        "mainEntityOfPage": {"@id": EN_URL + "#webpage"},
                        "description": EN_DESCRIPTION,
                        "inLanguage": "en",
                        "learningResourceType": "Professional handbook and self-study guide",
                        "educationalLevel": "Foundational to advanced",
                        "teaches": [
                            "Forward Deployed Engineer roles and responsibilities",
                            "FDE competency frameworks and career development",
                            "Enterprise AI delivery and operations",
                            "AI system evaluation, safety, and governance",
                        ],
                        "keywords": [
                            "Forward Deployed Engineer",
                            "Forward Deployed Engineer guide",
                            "FDE role and responsibilities",
                            "FDE career development",
                            "FDE interview guide",
                            "enterprise AI delivery",
                            "enterprise AI implementation",
                            "AI engineering practice",
                            "FDE competency model",
                            "AI evaluation and operations",
                        ],
                    }
                )
        return json.dumps(structured_data, ensure_ascii=False, indent=2)


def build(output_dir: Path) -> int:
    if output_dir == ROOT:
        raise ValueError("The output directory must not be the repository root")
    source_path = ROOT / "index.html"
    source = source_path.read_text(encoding="utf-8")
    translations, attributes = load_translations(source)
    share_content = load_share_content(source)
    renderer = EnglishRenderer(translations, attributes)
    renderer.feed(source)
    renderer.close()

    if renderer.untranslated_text:
        examples = "\n".join(sorted(renderer.untranslated_text)[:20])
        raise RuntimeError(f"Untranslated Chinese body text found:\n{examples}")
    if renderer.untranslated_attributes:
        examples = "\n".join(
            f"<{tag} {key}={value!r}>" for tag, key, value in sorted(renderer.untranslated_attributes)
        )
        raise RuntimeError(f"Untranslated Chinese accessibility attributes found:\n{examples}")

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in STATIC_FILES:
        source_file = ROOT / filename
        if not source_file.is_file():
            raise FileNotFoundError(f"Required site asset is missing: {source_file}")
        shutil.copy2(source_file, output_dir / filename)
    english_dir = output_dir / "en"
    english_dir.mkdir(parents=True, exist_ok=True)
    (english_dir / "index.html").write_text("".join(renderer.parts), encoding="utf-8")
    for locale, platforms in SHARE_PLATFORMS.items():
        for platform in platforms:
            share_dir = output_dir / "share" / locale / platform
            share_dir.mkdir(parents=True, exist_ok=True)
            page = render_share_page(locale, platform, share_content[locale][platform])
            (share_dir / "index.html").write_text(page, encoding="utf-8")
    return renderer.translated_nodes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="Directory for the Pages upload artifact (default: ./dist)",
    )
    args = parser.parse_args()
    translated_nodes = build(args.output_dir.resolve())
    print(f"Built static site in {args.output_dir.resolve()}")
    print(f"Pre-rendered {translated_nodes} English text nodes at /en/")
    print(f"Generated {sum(map(len, SHARE_PLATFORMS.values()))} platform-specific share landing pages")


if __name__ == "__main__":
    main()
