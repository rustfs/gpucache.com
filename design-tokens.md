# GPUCache webpage design tokens

Visual source: the RustFS design system published at <https://design.rustfs.com/zh/downloads/> (`DESIGN.md`, `tokens/tokens.css`, `tokens/tokens.json`, checked 2026-10-15).

GPUCache borrows that system’s color, type, shape, and elevation rules. It does not reuse the RustFS parity-stripe graphic, because that graphic describes a durability layout this product does not use.

## Languages

- English at `/` (`en`), also `x-default`
- 日本語 at `/ja/` (`ja`)
- Deutsch at `/de/` (`de`)
- Français at `/fr/` (`fr`)
- 中文 at `/zh/` (`zh-CN` on the document, `zh` in hreflang)
- Every page emits `hreflang` alternates for `en`, `ja`, `de`, `fr`, `zh`, and `x-default`.

## Color roles

| Token | Value | Role |
| --- | --- | --- |
| Signal Blue | `#0062FF` | The only brand blue. Primary buttons, current tier, links’ hover partner, “implemented” marker. |
| Signal hover / links | `#014FDD` | Text links on white. |
| Signal on dark | `#5C99FF` | Syntax keywords inside Ink code blocks. |
| Oxide | `#FF5E14` | Square marker for “in development” only. One job: preview status. Not a decoration, not an error color, not a large fill. |
| Oxide text | `#B33A10` | The “in development” label on light surfaces. |
| Ink | `#0B0E14` | Text, the closing band, code blocks. |
| Paper | `#F4F6F9` | Alternate section surface. |
| Surface | `#FFFFFF` | Page background. |
| Muted text | `#5A616D` | Secondary text. Do not go lighter on white. |
| Outline | `#DCE0E6` | 1px rules. |

Do not introduce other blues, gradients, glows, or glass.

## Typography

- Tier numerals in the stack diagram and the docs tier chain: Archivo, width 125%, weight 800.
- Headlines, including the homepage hero: Archivo at the headline scale, not the display scale. Width 112%, weight 750 (700 on the smallest headline). Hero is `--text-headline-lg` (40px, 32px below 640px), section titles are `--text-headline-md` (30px, 26px below 640px). Line-height 1.15–1.2. Tracking is 0 so the wide cut reads open rather than compressed.
- Body and UI: Geist 400/500. Body line-height 1.65. Large body and ledes 18px at 1.6.
- Eyebrows, status, paths, code: Geist Mono, uppercase, 0.08em tracking in Latin. Chinese and Japanese labels use the same mono face with tracking set to 0.
- Chinese and Japanese: HarmonyOS Sans SC or Source Han Sans SC when installed, otherwise Noto Sans SC / Noto Sans JP from the stylesheet. Half-width space between Han and Latin or digits. Chinese quotation marks are 「」. Headlines use tracking 0 and line-height of at least 1.15.

## Shape and elevation

- Corners are square: buttons, chips, cards, code, tables, the tier chain.
- Separate regions with 1px borders and Paper versus white. No drop shadows and no blurred translucent bars.
- Status markers are 10px squares, not dots or pills.
- The only Oxide on a screen is the in-development marker.

## Layout

- Content width 1240px. Side gutter at least 16px. Section padding is 112px, 80px from 640px to 1023px, and 72px below 640px.
- Sections use a mono label, then a 5/7 split where the page has a headline and a lede.
- The homepage hero uses that split, then one full-width stack diagram: G1 HBM → G2 DRAM → G3 NVMe (node-local) → G3.5 GPUCache → G4 RustFS. Shard count marks distance from the GPU against shareability. G3.5 is the only Signal fill. It is the shared KV Cache hot tier between GPU memory and object storage. A miss is recomputed, then written back. Durability is named on G4, which is RustFS, not a second product brand. Oxide stays on the in-development marker and does not sit on the Signal row. Below 1024px the diagram stacks under the copy.

## Copy constraints

- The tier name on every page is G3.5.
- GPUCache is a DPU-based GDS KVCache. BlueField-3 support, the direct data path, and vLLM / TensorRT-LLM integration stay marked in development.
- Name only BlueField-3, and only as in development.
- The storage side does not need an x86 storage host. KV on the hot path is not forwarded by the host CPU. Compute nodes still register memory, submit requests, and collect completions.
- RustFS is the G4 capacity tier and owns cold-data durability. A G3.5 loss is a clean miss: recompute, then write back. Say that, and stop there.
- Do not publish a competitor comparison, a performance number, or any community count, in any language, including the docs.
- The main branch of <https://github.com/rustfs/GPUCache> currently contains `README.md` and `LICENSE` only. The V1 core is in development in a separate pull request and is not described as implemented.
- PagedAttention is spelled with a d. Feedback goes to Issues.
