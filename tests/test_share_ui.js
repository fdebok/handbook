const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync("index.html", "utf8");
const scripts = [...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
const mainScript = scripts.map((match) => match[1]).find((script) =>
  script.includes("function initializeSharing(){"),
);
assert.ok(mainScript, "share UI initializer exists");

const start = mainScript.indexOf(" function initializeSharing(){");
const end = mainScript.indexOf("\n window.addEventListener('DOMContentLoaded'", start);
assert.ok(start >= 0 && end > start, "share UI initializer boundaries exist");
const initializer = `${mainScript.slice(start, end)};globalThis.initializeSharing=initializeSharing;`;
const shareContent = JSON.parse(
  source.match(/<script id="share-content-data" type="application\/json">([\s\S]*?)<\/script>/)[1],
);
const shareIntro = source.match(/<p[^>]*id="share-intro">([^<]+)<\/p>/)[1];
assert.doesNotMatch(shareIntro, /系统分享/);
assert.doesNotMatch(shareContent.zh.wechat.note, /系统分享/);
assert.doesNotMatch(shareContent.zh.douyin.note, /系统分享/);
assert.doesNotMatch(source, /微信或抖音用户可使用系统分享/);

class Element {
  constructor(id, dataset = {}) {
    this.id = id;
    this.dataset = dataset;
    this.attributes = {};
    this.handlers = {};
    this.hidden = false;
    this.disabled = false;
    this.href = "";
    this.value = "";
    this.textContent = "";
    this.style = {};
  }

  addEventListener(name, callback) {
    this.handlers[name] = callback;
  }

  setAttribute(name, value) {
    this.attributes[name] = String(value);
  }

  removeAttribute(name) {
    delete this.attributes[name];
  }

  focus() {
    this.focused = true;
  }

  select() {
    this.selected = true;
  }
  remove() {}
}

async function exerciseLocale(
  locale,
  unsupportedNativeShare = false,
  rejectClipboard = false,
  isMobile = false,
  rejectShare = false,
) {
  const ids = [
    "share-trigger", "share-panel", "share-close", "share-native",
    "share-copy-text", "share-copy-link", "share-open-platform", "share-url",
    "share-quick-actions", "share-quick-copy", "share-quick-copy-button",
    "share-status", "share-qr-image", "share-preview-caption",
    "share-preview-title", "share-preview-kicker", "share-platform-note",
    "share-qr-note", "share-intro", "share-content-data",
  ];
  const elements = Object.fromEntries(ids.map((id) => [id, new Element(id)]));
  elements["share-panel"].hidden = true;
  elements["share-quick-actions"].hidden = true;
  elements["share-content-data"].textContent = JSON.stringify(shareContent);
  const platforms = ["wechat", "douyin", "facebook", "linkedin", "x"].map(
    (platform) => new Element(`platform-${platform}`, { sharePlatform: platform }),
  );
  elements["share-panel"].querySelectorAll = () => platforms;

  const copied = [];
  const loggedErrors = [];
  let shared;
  let selectedText;
  const selection = {
    removeAllRanges() {},
    addRange(range) {
      selectedText = range.node;
    },
  };
  const context = {
    document: {
      documentElement: { lang: locale },
      getElementById: (id) => elements[id],
      addEventListener() {},
      body: { appendChild() {} },
      createElement: (tag) => new Element(tag),
      createRange: () => ({
        selectNodeContents(node) {
          this.node = node;
        },
      }),
      getSelection: () => selection,
      execCommand: () => false,
    },
    window: { isSecureContext: true, getSelection: () => selection },
    navigator: {
      clipboard: {
        writeText: (value) => {
          if (rejectClipboard) return Promise.reject(new Error("Clipboard unavailable"));
          copied.push(value);
          return Promise.resolve();
        },
      },
      ...(unsupportedNativeShare
        ? {}
        : {
            share: (value) => {
              shared = value;
              return rejectShare
                ? Promise.reject(new Error("Share unavailable"))
                : Promise.resolve();
            },
          }),
    },
    console: {
      error: (...args) => loggedErrors.push(args),
    },
    URLSearchParams,
  };
  context.window.matchMedia = () => ({ matches: isMobile });
  vm.runInNewContext(initializer, context);
  context.initializeSharing();
  if (!isMobile) {
    elements["share-trigger"].handlers.click();
    assert.equal(elements["share-panel"].hidden, false);
    assert.equal(elements["share-trigger"].attributes["aria-expanded"], "true");
  }

  const initialPlatform = locale === "zh" ? "wechat" : "linkedin";
  const nextPlatform = locale === "zh" ? "douyin" : "x";
  const initialContent = shareContent[locale][initialPlatform];
  assert.equal(elements["share-url"].value, `https://www.fdebok.com/share/${locale}/${initialPlatform}/`);
  assert.equal(elements["share-preview-title"].textContent, initialContent.title);
  assert.equal(elements["share-preview-caption"].textContent, initialContent.caption);
  assert.equal(elements["share-native"].hidden, unsupportedNativeShare);

  const unavailablePlatform = platforms.find(
    (button) => button.dataset.sharePlatform === (locale === "zh" ? "facebook" : "wechat"),
  );
  assert.equal(unavailablePlatform.hidden, true);

  platforms.find((button) => button.dataset.sharePlatform === nextPlatform).handlers.click();
  const nextContent = shareContent[locale][nextPlatform];
  const destination = `https://www.fdebok.com/share/${locale}/${nextPlatform}/`;
  assert.equal(elements["share-url"].value, destination);
  assert.equal(elements["share-preview-title"].textContent, nextContent.title);

  if (nextPlatform === "x") {
    assert.match(elements["share-open-platform"].href, /^https:\/\/twitter\.com\/intent\/tweet\?/);
    assert.equal(new URLSearchParams(elements["share-open-platform"].href.split("?")[1]).get("url"), destination);
  }

  if (!unsupportedNativeShare && !isMobile) {
    elements["share-native"].handlers.click();
    await Promise.resolve();
    assert.equal(shared.url, destination);
    assert.equal(shared.text, nextContent.caption);
  }

  elements["share-copy-text"].handlers.click();
  if (rejectClipboard) {
    await new Promise(setImmediate);
    assert.equal(elements["share-status"].textContent, "复制失败，请手动选择配文复制。");
    assert.equal(selectedText, elements["share-preview-caption"]);
  } else {
    await Promise.resolve();
    assert.equal(copied[0], nextContent.caption);
  }
  elements["share-copy-link"].handlers.click();
  if (rejectClipboard) {
    await new Promise(setImmediate);
    assert.equal(elements["share-url"].focused, true);
    assert.equal(elements["share-url"].selected, true);
  } else {
    await Promise.resolve();
    assert.equal(copied[1], destination);
  }

  if (isMobile) {
    elements["share-trigger"].handlers.click();
    if (unsupportedNativeShare) {
      assert.equal(elements["share-panel"].hidden, false);
      assert.equal(elements["share-panel"].dataset.mode, "quick");
      assert.equal(elements["share-quick-actions"].hidden, false);
      assert.equal(elements["share-quick-copy"].value,
        `${nextContent.caption}\n\n${locale === "en" ? "https://www.fdebok.com/en/" : "https://www.fdebok.com/"}`);
      elements["share-quick-copy-button"].handlers.click();
      if (rejectClipboard) {
        await new Promise(setImmediate);
        assert.equal(elements["share-quick-copy"].focused, true);
        assert.equal(elements["share-quick-copy"].selected, true);
      } else {
        await Promise.resolve();
        assert.equal(copied.at(-1), elements["share-quick-copy"].value);
      }
      elements["share-close"].handlers.click();
      assert.equal(elements["share-panel"].hidden, true);
      assert.equal(elements["share-trigger"].attributes["aria-expanded"], "false");
    } else if (rejectShare) {
      await new Promise(setImmediate);
      assert.equal(elements["share-panel"].hidden, false);
      assert.equal(elements["share-panel"].dataset.mode, "quick");
      assert.equal(elements["share-quick-actions"].hidden, false);
      assert.equal(loggedErrors[0][0], "System sharing failed");
    } else {
      await Promise.resolve();
      assert.equal(elements["share-panel"].hidden, true);
      assert.equal(shared.url, locale === "en" ? "https://www.fdebok.com/en/" : "https://www.fdebok.com/");
      assert.equal(shared.text, nextContent.caption);
    }
  } else {
    elements["share-close"].handlers.click();
    assert.equal(elements["share-panel"].hidden, true);
    assert.equal(elements["share-trigger"].attributes["aria-expanded"], "false");
  }
  console.log(`${locale}: platform selection, preview, share, and copy actions passed`);
}

(async () => {
  await exerciseLocale("zh");
  await exerciseLocale("en");
  await exerciseLocale("en", true);
  await exerciseLocale("zh", false, true);
  await exerciseLocale("zh", false, false, true);
  await exerciseLocale("zh", true, false, true);
  await exerciseLocale("zh", true, true, true);
  await exerciseLocale("en", false, false, true, true);
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
