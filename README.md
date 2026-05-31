# GPUCache Website

Static landing page for [RustFS GPUCache](https://github.com/rustfs/GPUCache).

GPUCache offloads KV cache for LLM inference onto BlueField DPUs and NVMe flash, giving GPU clusters a shared L4 context-memory tier.

## Files

- `index.html` — page markup
- `styles.css` — visual system and responsive layout
- `script.js` — reveal animation and screenshot helper
- `design-tokens.md` — local design constraints used for this prototype

## Local preview

Open `index.html` directly in a browser, or run a simple static server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080`.
