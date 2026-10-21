# GPUCache website

Static site for [GPUCache](https://github.com/rustfs/GPUCache), the shared KV Cache at the G3.5 tier, with a CPU/TCP implementation and a DPU/GDS target architecture.

GPUCache gives a GPU cluster a shared KV Cache hot tier. It is written in Rust, licensed under Apache 2.0, and in development. RustFS is the G4 capacity tier.

## Languages

| Language | Path |
| --- | --- |
| English (`x-default`) | `/` |
| 日本語 | `/ja/` |
| Deutsch | `/de/` |
| Français | `/fr/` |
| 中文 | `/zh/` |

Each language has a docs section: architecture, tiering, roadmap, quick start, and node scaling. Pages include `hreflang` alternates for `en`, `ja`, `de`, `fr`, `zh`, and `x-default`.

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

## Documentation evidence

The scaling guide describes operator-coordinated membership for 1, 3 and 10 shards. Its executable source is `crates/transport/examples/scaling_smoke.rs` in the GPUCache repository. That example uses independent TCP servers in one localhost process; it is not a physical multi-host or performance qualification. Routes do not fence remote stores, and new stores must be prepared above the previous epoch maximum.

Real RDMA, GDS, BlueField-3, live RustFS and real engine export/import remain unqualified. Keep CPU/mock/fake-block evidence separate from target architecture claims. Run `python3 scripts/check_site.py` before opening a PR. There is no site deployment step in that command.

Reviewed implementation revision: [`af51629`](https://github.com/rustfs/GPUCache/commit/af5162912b87b24a722004aa61fece93b72fb7cf). The scaling guide links to immutable copies of the matching runbook and example.
