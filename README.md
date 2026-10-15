# GPUCache website

Static site for [GPUCache](https://github.com/rustfs/GPUCache), the DPU-based GDS KVCache at the G3.5 tier.

GPUCache gives a GPU cluster a shared KV Cache hot tier. It is written in Rust, licensed under Apache 2.0, and in development. RustFS is the G4 capacity tier.

## Languages

| Language | Path |
| --- | --- |
| English (`x-default`) | `/` |
| 日本語 | `/ja/` |
| Deutsch | `/de/` |
| Français | `/fr/` |
| 中文 | `/zh/` |

Each language has a docs section: architecture, tiering, roadmap, and quick start. Pages include `hreflang` alternates for `en`, `ja`, `de`, `fr`, `zh`, and `x-default`.

## Files

- `index.html` and `ja/`, `de/`, `fr/`, `zh/` — landing pages
- `docs/` — English docs; other languages live under their prefix
- `styles.css` — RustFS design tokens and layout
- `script.js` — menu and code-copy button
- `design-tokens.md` — token roles and copy constraints
- `favicon.svg` — site icon

## Local preview

From the repository root:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080/`. Root-relative links need a server; opening a file directly will not resolve them.
