const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync("index.html", "utf8");
const scripts = [...source.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)].map(
  (match) => match[1],
);
const bootstrap = scripts.find((script) => script.includes("root.dataset.themeStorage='unavailable'"));
const mainScript = scripts.find((script) => script.includes("function initializeColorTheme(){"));
assert.ok(bootstrap, "theme preference bootstrap exists");
assert.ok(mainScript, "theme initializer exists");

const start = mainScript.indexOf(" function initializeColorTheme(){");
const end = mainScript.indexOf("\n function initializeReadingTools(){", start);
assert.ok(start >= 0 && end > start, "theme initializer boundaries exist");
const initializer = `${mainScript.slice(start, end)};globalThis.initializeColorTheme=initializeColorTheme;`;

class Element {
  constructor(value = "") {
    this.value = value;
    this.dataset = {};
    this.checked = false;
    this.textContent = "";
    this.handlers = {};
    this.content = "";
  }

  addEventListener(name, callback) {
    this.handlers[name] = callback;
  }
}

function createHarness({ savedTheme = null, readFails = false, writeFails = false } = {}) {
  const root = { dataset: { theme: "classic" } };
  const status = new Element();
  const themeMeta = new Element();
  const radios = ["classic", "forest", "plum"].map((theme) => new Element(theme));
  const options = ["classic", "forest", "plum"].map((theme) => {
    const option = new Element();
    option.dataset.themeValue = theme;
    return option;
  });
  const stored = new Map(savedTheme ? [["fdebok-color-theme-v1", savedTheme]] : []);
  const errors = [];
  const context = {
    document: {
      documentElement: root,
      querySelector: () => themeMeta,
      querySelectorAll: (selector) =>
        selector === 'input[name="color-theme"]' ? radios : options,
      getElementById: () => status,
    },
    localStorage: {
      getItem(key) {
        if (readFails) throw new Error("storage read blocked");
        return stored.get(key) || null;
      },
      setItem(key, value) {
        if (writeFails) throw new Error("storage write blocked");
        stored.set(key, value);
      },
    },
    console: {
      warn: (...args) => errors.push(args),
      error: (...args) => errors.push(args),
    },
  };
  vm.runInNewContext(bootstrap, context);
  vm.runInNewContext(initializer, context);
  context.initializeColorTheme();
  return { context, errors, options, radios, root, status, stored, themeMeta };
}

assert.ok(source.includes(":root{"));
for (const theme of ["forest", "plum"]) {
  assert.ok(source.includes(`:root[data-theme="${theme}"]`));
}
for (const theme of ["classic", "forest", "plum"]) {
  assert.match(source, new RegExp(`value="${theme}"`));
}
assert.match(source, /<html lang="zh-CN" data-theme="classic">/);

const restored = createHarness({ savedTheme: "forest" });
assert.equal(restored.root.dataset.theme, "forest");
assert.equal(restored.themeMeta.content, "#19372f");
assert.equal(restored.radios.find((radio) => radio.value === "forest").checked, true);
assert.equal(restored.options.find((option) => option.dataset.themeValue === "forest").dataset.selected, "true");

const plumRadio = restored.radios.find((radio) => radio.value === "plum");
plumRadio.checked = true;
plumRadio.handlers.change();
assert.equal(restored.root.dataset.theme, "plum");
assert.equal(restored.themeMeta.content, "#272a3b");
assert.equal(restored.stored.get("fdebok-color-theme-v1"), "plum");
assert.equal(restored.options.find((option) => option.dataset.themeValue === "plum").dataset.selected, "true");
assert.match(restored.status.textContent, /配色已应用并保存在本机/);

const invalidStoredTheme = createHarness({ savedTheme: "unsupported" });
assert.equal(invalidStoredTheme.root.dataset.theme, "classic");
assert.equal(invalidStoredTheme.radios.find((radio) => radio.value === "classic").checked, true);

const blockedStorage = createHarness({ readFails: true, writeFails: true });
assert.equal(blockedStorage.root.dataset.themeStorage, "unavailable");
assert.match(blockedStorage.status.textContent, /无法读取本机保存状态/);
const forestRadio = blockedStorage.radios.find((radio) => radio.value === "forest");
forestRadio.checked = true;
forestRadio.handlers.change();
assert.equal(blockedStorage.root.dataset.theme, "forest");
assert.match(blockedStorage.status.textContent, /无法保存在本机/);
assert.equal(blockedStorage.errors.length, 2);

console.log("color themes: restoration, selection, persistence, invalid values, and storage errors passed");
