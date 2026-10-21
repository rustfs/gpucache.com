#!/usr/bin/env python3
"""Check the static site without a server, network access or third-party packages."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://gpucache.com"
LOCALES = {"en": "", "ja": "ja/", "de": "de/", "fr": "fr/", "zh": "zh/"}
TOPICS = ("architecture", "tiering", "roadmap", "quickstart", "scaling")
ROUTES = ("", "docs/") + tuple("docs/" + topic + "/" for topic in TOPICS)
VOID = set("area base br col embed hr img input link meta param source track wbr".split())
BLOCK = set("address article aside blockquote div dl fieldset footer form h1 h2 h3 h4 h5 h6 header hr main nav ol p pre section table ul".split())
PARENTS = {
    "head": {"html"}, "body": {"html"}, "li": {"ul", "ol", "menu"},
    "thead": {"table"}, "tbody": {"table"}, "tfoot": {"table"},
    "tr": {"table", "thead", "tbody", "tfoot"}, "td": {"tr"}, "th": {"tr"},
}
# Reject the retired no-code copy in every locale, while allowing the truthful
# statement that an installable release and production qualification are absent.
STALE_COPY = tuple(re.compile(pattern, re.I) for pattern in (
    r"does not contain application code|is not on the main branch",
    r"main(?: branch|-branch).{0,60}(?:has no|contains no) (?:application )?code",
    r"(?:only|nur|seulement).{0,30}readme(?:\.md)?.{0,30}licen[cs]e",
    r"no (?:build|run) instructions",
    r"主分支(?:上)?(?:还|尚)?没有(?:应用)?代码|不在主分支上",
    r"主分支.{0,30}只有.{0,20}readme",
    r"main ブランチには(?:まだコードがない|ありません)",
    r"(?:ビルド|実行)手順はない",
    r"main-branch enthält noch keinen anwendungscode|liegt nicht auf dem main-branch",
    r"keine (?:build|run)-anleitung",
    r"branche main ne contient pas encore de code|n'est pas sur la branche main",
    r"pas d'instructions de (?:build|exécution)",
))


def page_url(locale, route):
    return ORIGIN + "/" + LOCALES[locale] + route


class Page(HTMLParser):
    """The site uses explicit closing tags; validate that stricter convention."""

    def __init__(self, path, source):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.errors = []
        self.stack = []
        self.counts = Counter()
        self.ids = set()
        self.references = []
        self.canonicals = []
        self.alternates = {}
        self.language_links = []
        self.navigation = {"docs-nav": set(), "doc-links": set(), "footer": set()}
        self.copy = []
        self.lang = None
        self.doctypes = 0
        self.feed(source)
        self.close()
        if self.stack:
            self.error("unclosed tags: " + ", ".join(tag for tag, _ in self.stack))
        for tag in ("html", "head", "body", "main", "h1"):
            if self.counts[tag] != 1:
                self.error("expected one <{}>, found {}".format(tag, self.counts[tag]))
        if self.doctypes != 1:
            self.error("expected one <!doctype html>")
        text = " ".join(" ".join(self.copy).split()).replace("’", "'")
        for pattern in STALE_COPY:
            match = pattern.search(text)
            if match:
                self.error("retired no-code copy: " + match.group())

    def error(self, message):
        self.errors.append("{}:{}: {}".format(self.path, self.getpos()[0], message))

    def handle_decl(self, decl):
        if decl.lower() == "doctype html":
            self.doctypes += 1
        else:
            self.error("unexpected declaration: " + decl)

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if len(data) != len(attrs):
            self.error("duplicate attribute on <{}>".format(tag))
        parent = self.stack[-1][0] if self.stack else None
        if tag == "html" and self.stack:
            self.error("<html> must be the root element")
        if tag in PARENTS and parent not in PARENTS[tag]:
            self.error("invalid parent <{}> for <{}>".format(parent, tag))
        if tag in BLOCK and any(ancestor == "p" for ancestor, _ in self.stack):
            self.error("block element <{}> inside <p>".format(tag))
        self.counts[tag] += 1
        identifier = data.get("id")
        if identifier is not None:
            if not identifier or identifier in self.ids:
                self.error("empty or duplicate id: {!r}".format(identifier))
            self.ids.add(identifier)
        if tag == "html":
            self.lang = data.get("lang")
        if tag == "base":
            self.error("<base> is unsupported; use the site's ordinary URL paths")
        for attr in ("href", "src", "poster"):
            if attr in data:
                if data[attr] is None or not data[attr].strip():
                    self.error("empty {} on <{}>".format(attr, tag))
                else:
                    self.references.append((data[attr], self.getpos()[0]))
        if tag == "link":
            rel = (data.get("rel") or "").split()
            if "canonical" in rel:
                self.canonicals.append(data.get("href"))
            if "alternate" in rel and "hreflang" in data:
                language = data["hreflang"]
                if language in self.alternates:
                    self.error("duplicate hreflang alternate: " + str(language))
                self.alternates[language] = data.get("href")
        if tag == "a":
            href = data.get("href")
            if "hreflang" in data:
                self.language_links.append((data["hreflang"], href))
            for ancestor, attributes in self.stack:
                if ancestor == "footer":
                    self.navigation["footer"].add(href)
                for group in ("docs-nav", "doc-links"):
                    if group in (attributes.get("class") or "").split():
                        self.navigation[group].add(href)
        if tag == "meta" and data.get("content"):
            self.copy.append(data["content"])
        if tag not in VOID:
            self.stack.append((tag, data))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.error("non-void HTML element <{}> cannot self-close".format(tag))
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1][0] != tag:
            self.error("unexpected </{}>; open tag is <{}>".format(
                tag, self.stack[-1][0] if self.stack else "none"))
        else:
            self.stack.pop()

    def handle_data(self, data):
        if not any(tag in ("script", "style") for tag, _ in self.stack):
            self.copy.append(data)


def check_site(root):
    errors = []
    expected = {
        LOCALES[locale] + route + "index.html": (locale, route)
        for locale in LOCALES for route in ROUTES
    }
    actual = {path.relative_to(root).as_posix(): path for path in root.rglob("*.html")
              if not any(part.startswith(".") for part in path.relative_to(root).parts)}
    for name in sorted(expected.keys() - actual.keys()):
        errors.append(name + ": required localized page is missing")
    for name in sorted(actual.keys() - expected.keys()):
        errors.append(name + ": unexpected page; update ROUTES/LOCALES to validate its alternates")
    pages = {}
    for name, path in sorted(actual.items()):
        try:
            pages[name] = Page(name, path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append("{}: cannot read UTF-8 HTML: {}".format(name, exc))
            continue
        errors.extend(pages[name].errors)

    for name, page in pages.items():
        if name not in expected:
            continue
        locale, route = expected[name]
        canonical = page_url(locale, route)
        language = "zh-CN" if locale == "zh" else locale
        if page.lang != language:
            errors.append("{}: html lang must be {}".format(name, language))
        if page.canonicals != [canonical]:
            errors.append("{}: expected one canonical {}".format(name, canonical))
        alternates = {lang: page_url(lang, route) for lang in LOCALES}
        alternates["x-default"] = page_url("en", route)
        if page.alternates != alternates:
            errors.append(name + ": hreflang alternates must map all five locales and x-default to the same page")
        for lang, href in page.language_links:
            if lang not in LOCALES or urljoin(canonical, href or "") != alternates[lang]:
                errors.append("{}: language switch {} has wrong target {!r}".format(name, lang, href))
        for other_locale in LOCALES:
            other = pages.get(LOCALES[other_locale] + route + "index.html")
            if other and other.alternates.get(locale) != canonical:
                errors.append("{}: {} alternate does not link back to this canonical".format(name, other_locale))
        topics = {"/" + LOCALES[locale] + "docs/" + topic + "/" for topic in TOPICS}
        groups = ("footer", "doc-links" if route in ("", "docs/") else "docs-nav")
        for group in groups:
            missing = topics - page.navigation[group]
            if missing:
                errors.append("{}: {} is missing local topic links: {}".format(name, group, ", ".join(sorted(missing))))

        for reference, line in page.references:
            try:
                url = urlsplit(urljoin(canonical, reference))
            except ValueError as exc:
                errors.append("{}:{}: invalid URL {!r}: {}".format(name, line, reference, exc))
                continue
            if url.scheme not in ("http", "https") or url.netloc != "gpucache.com":
                continue
            target = root / unquote(url.path).lstrip("/")
            if target.is_dir():
                target /= "index.html"
            try:
                target_name = target.resolve().relative_to(root.resolve()).as_posix()
            except ValueError:
                errors.append("{}:{}: link escapes site root: {}".format(name, line, reference))
                continue
            if not target.is_file():
                errors.append("{}:{}: missing internal target: {}".format(name, line, reference))
            elif url.fragment:
                target_page = pages.get(target_name)
                if target_page is None or unquote(url.fragment) not in target_page.ids:
                    errors.append("{}:{}: missing HTML fragment: {}".format(name, line, reference))
    return errors, len(pages)


def main():
    errors, count = check_site(ROOT)
    if errors:
        print("Site checks failed ({} errors across {} HTML pages):".format(len(errors), count), file=sys.stderr)
        for error in errors:
            print("- " + error, file=sys.stderr)
        return 1
    print("PASS: {} HTML pages, five locales, structure, IDs, local links/fragments, canonical/hreflang, topic navigation and current copy.".format(count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
