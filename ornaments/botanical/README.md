# Botanical ornament set

<!-- toc:start -->
**Table of contents**

- [Deliverables and geometry](#deliverables-and-geometry)
- [Restrained placement plan](#restrained-placement-plan)
- [Palette](#palette)
- [Botanical provenance and scope](#botanical-provenance-and-scope)
- [Quality checks](#quality-checks)
- [Vertical revision v2 — natural hanging plants](#vertical-revision-v2--natural-hanging-plants)
<!-- toc:end -->

Original vector-native ornaments for *The Hours We Keep*. Three unchanged Corinthian botanical dividers and three revised natural hanging-plant families in left/right orientations. These are deliberately stylized botanical drawings, not taxonomic botanical plates. The vertical revision contains actual cascading stems, leaves, flowers and roots; all ornamental acanthus/scroll spines have been removed.

## Deliverables and geometry

- `divider-corinthian-orchid`, `divider-corinthian-oncidium`, `divider-corinthian-ceratostema`: each 129 × 16 pt; 1075 × 134 px at 600 dpi. Center at x = 216 pt, so left edge x = 151.5 pt. Preserve the existing 32 pt vertical separator allocation; center this 16 pt image within it. These replace only nature/orchid divider slots.
- `trailing-pendant-left/right`, `trailing-orchid-left/right`, and `trailing-grammatophyllum-acianthera-left/right`: each 28 × 190 pt; 234 × 1584 px at 600 dpi. Each supplied as SVG, vector PDF, and transparent RGBA PNG.
- `manifest.json`: per-file SHA-256, point dimensions, pixel dimensions, and nontransparent pixel bounds.

The electronic divider and revised cursive divider retain their distinct roles. This directory supplies only the reusable ornament assets and their public provenance; review mockups are excluded.

## Restrained placement plan

1. Rotate the three botanical horizontal designs through existing nature/orchid slots. Preserve the electronic and cursive section dividers.
2. Use paired hanging plants at the top left and top right of selected ordinary text pages, approximately one in every six eligible pages. Exclude illustration-only, chapter-opening, front-matter and appendix pages.
3. Anchor each footprint at y = 5 pt from the top. Left footprints begin at x = 5 pt; right footprints end at x = 427 pt. Keep plants entirely within the outer margin bands, away from body text at x = 46..390 pt and from running headers.
4. Scale proportionally from the 28 × 190 pt source, varying displayed heights from 142 to 190 pt. Use different heights on the two corners and rotate botanical families. Do not stretch the artwork independently in either dimension.
5. Omit all geometric edge motifs and both corner brackets on plant pages. Preserve approved horizontal section dividers, text, footnotes and navigation.
6. Use the supplied vector PDFs for the print master and retain SVG/600-dpi PNG sources for reuse. Lightness is built into the palette.

## Palette

Revised vertical stems #9FA79A, foliage #D9DFD1, leaf veins #B3B9AC, roots #B9B1A5, petal outline #AC96A7. Unchanged horizontal main warm gray-green #A4A7A1; light leaf fill #E9ECE5 / #F2F3F0; orchid gray-mauve #B5A4B0 with #F3ECEF fill; pendant pink-white #F2E7EB; muted Oncidium gray-gold #BCB79E with #F1EFE5 fill. Gray dominates so the decoration remains below the reading contrast of body text.

## Botanical provenance and scope

- Oncidium-style spray structure is informed by NParks' Oncidesa Golden Wish record (formerly Oncidium Golden Wish): large-lipped yellow flowers on branched arching spikes. This is a form reference, not a claim that the ornament identifies that hybrid. https://www.nparks.gov.sg/florafaunaweb/flora/3/3/3375 (read 2026-10-14).
- Ceratostema-inspired flowers use pendant pink-white tubes with a swollen upper portion and split long lower lobes. The genus-level NYBG reference was located during reference research; direct retrieval returned 403. Thus this set makes no verified species-level Ceratostema claim. https://www.nybg.org/bsci/res/lut2/ceratostema.html
- Broad moth-orchid forms, fern pinnae, and vines are intentionally generic. Curled, lobed acanthus leaves remain ONLY in the unchanged horizontal dividers. Revised vertical assets use natural leaf and root forms instead.
- Added Grammatophyllum-inspired motifs have narrow spreading greenish-yellow tepals with broad brown markings, an elongated floral axis, and downward-curving strap-like leaves. Reference: NParks Grammatophyllum speciosum description, read 2026-10-14: https://www.nparks.gov.sg/florafaunaweb/flora/2/0/2041
- Added Acianthera recurva-inspired motifs have compact oval-leaf mats, wiry roots, and tiny grouped blooms. Reference: Smithsonian Gardens accession 2015-1510A, https://gardens.si.edu/collections/explore/object/ofeo-sg_2015-1510A and its indexed collection image https://ids.si.edu/ids/deliveryService?id=SG-2015-1510A-101&max=980 . The collection search-index description was available; direct image/page retrieval failed. These are explicitly habit-informed ornamental simplifications, not verified taxonomic flower portraits. No other Acianthera species was substituted.
- Current vertical revision: v2-natural-hanging-plants. The prior vertical designs are retained separately in the authoring history. All nine source/PNG/PDF files belonging to the three horizontal dividers remain byte-identical. Current hashes are in manifest.json and SHA256SUMS.
- Original SVG paths were authored expressly for this edition. No reference photographs were embedded or traced. PNGs were rasterized from the vector paths, not AI-generated or upscaled raster imagery.

## Quality checks

Reviewed enlarged contact sheet and a page-scale actual text-page mockup. Main text remains clear; trail is entirely in the edge band. Transparent PNGs retain full native 600 dpi resolution; vector PDF companions preserve scalable paths. All nontransparent bounds were checked against asset edges. Editable SVGs and checksums are supplied for reuse and verification.

## Vertical revision v2 — natural hanging plants

- Ceratostema pair: unequal branching leafy shoots, alternate oval leaves, and naturally suspended split-tube flowers. No decorative scroll structure.
- Orchid-spray pair: basal arching strap leaves and many uneven branches of small Oncidium-style blooms, with epiphytic roots.
- Mixed epiphyte pair: spotted Grammatophyllum-inspired floral axis and strap leaves, with compact Acianthera recurva-inspired leafy clumps, miniature bloom groups and hanging roots.
- Left/right variants differ in branching/flower or clump positions as well as inward orientation.
- All six retain the 28 × 190 pt transparent footprint and original asset names, so the approved placement plan needs no geometric change.
- Six current PNGs are RGBA at 600 dpi; SVG and vector PDF sources are supplied. Bounds verification passes for every file.
