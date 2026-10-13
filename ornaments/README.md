# Page ornaments

Eleven transparent, 600-DPI PNGs reproduce every distinct decorative design used in the 98-page edition of *The Hours We Keep*: three side-border families in left and right orientations, two top-corner brackets, and three alternating section dividers.

These ornaments were drawn as vector linework. The PNGs are rasterizations of the original PDF paths, not newly generated images or recovered original raster files. Text, illustrations and annotations were excluded before rendering. Original stroke widths, muted colors and inward-fading border layers are preserved. The light appearance is intentional.

## Assets

| File | Pixels | Use |
| --- | --- | --- |
| [corner-left.png](corner-left.png) | 200 × 200 | Subtle upper-left corner linework. |
| [border-network-left.png](border-network-left.png) | 229 × 513 | Three inward-fading layers of connected node geometry for the left margin. |
| [corner-right.png](corner-right.png) | 201 × 200 | Subtle upper-right corner linework. |
| [border-hexagonal-right.png](border-hexagonal-right.png) | 226 × 476 | Three inward-fading layers of linked hexagonal geometry for the right margin. |
| [border-hexagonal-left.png](border-hexagonal-left.png) | 225 × 476 | Three inward-fading layers of linked hexagonal geometry for the left margin. |
| [border-circuit-right.png](border-circuit-right.png) | 244 × 601 | Three inward-fading layers of stepped circuit traces for the right margin. |
| [border-circuit-left.png](border-circuit-left.png) | 244 × 602 | Three inward-fading layers of stepped circuit traces for the left margin. |
| [border-network-right.png](border-network-right.png) | 229 × 512 | Three inward-fading layers of connected node geometry for the right margin. |
| [divider-electronic.png](divider-electronic.png) | 1126 × 168 | A central processor symbol with branching electronic traces. |
| [divider-orchid.png](divider-orchid.png) | 1034 × 192 | An orchid-like blossom with curved stems and leaves. |
| [divider-pencil.png](divider-pencil.png) | 1075 × 67 | Three overlapping hand-drawn pencil-like curves. |

## Placement and reuse

- All files use RGBA with a transparent background and at least two PDF points of clear padding around the strokes.
- The 600-DPI metadata describes native book size. For example, a roughly 1,100-pixel divider is about 1.8 inches wide at that resolution. Preserve aspect ratio when placing assets.
- Side motifs include all three fading layers. Use the left and right versions as supplied; their inward fade is oriented for the corresponding page edge.
- Electronic, orchid and pencil dividers recur in that order through the story. There are 29 placements: 10 electronic, 10 orchid and 9 pencil.
- `manifest.json` provides checksums, exact dimensions, source crop coordinates and every occurrence. Page numbers are one-based PDF pages, not printed folios. It covers 552 corner/motif placements on 92 pages. The six full-page interior illustration pages do not have borders.

Repeated motifs are represented once per design/orientation. Changing a motif’s position on the page does not create another design; all those positions remain in the inventory. Ordinary citation underlines, footnote rules and appendix-table rules are not decorative ornaments and are excluded.

## Fidelity

Exports were rendered directly from the original vector commands at 600 DPI, without tracing, redesign, recoloring or image generation. PNG compression is lossless, but rendering vectors to pixels necessarily fixes a finite resolution. The inventory does not claim original-raster byte identity.
