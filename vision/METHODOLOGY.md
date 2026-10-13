# Coverage method and contribution guide

Draft review edition, 2026-10-13. No publication or execution authorization is conferred by these files.

## Units and selection

Ten public-facing indicators span physical infrastructure (A01), task automation (A02), learning and portability (A03–A04), authorization and confidentiality (A05–A06), accountability (A07), economic independence (A08), civic and identity remedies (A09), and subjective continuity (A10). This is a purposive literary checklist, not a systematic review, probability sample or full backlog census. It was constructed during this review, not preregistered. Items are not statistically independent; equal weighting is a display convention, not a judgment of importance.

The denominator is all ten rows, including unknowns. Never count multiple source documents as multiple fulfilled indicators. Do not weight by RFC volume. Splitting a broad indicator can inflate the total; preserve versioned definitions and show counts whenever the taxonomy changes. The full criterion, rather than the short chart label, determines status.

## Conceptual column

Reviewed a current research-index snapshot and selected source proposals covering learning, portability, authorization, evaluation, economic use, lifecycle control and bounded execution. This is a high-level thematic mapping, not an exhaustive line-by-line audit of every proposal. Superseded and restaged versions are not independent accomplishments.

- Covered: reviewed material explicitly addresses the high-level theme as a research/design objective. Does not imply the full public criterion is implemented, accepted or even feasible.
- Partial: adjacent objectives occur, but the full social/technical theme is not explicitly addressed.
- Not found: no qualifying match established in the reviewed corpus. This is not evidence of global absence or a declaration that every private document was inspected.
- Unknown: source access or ambiguity prevents classification (available category; zero rows in this draft).

Confidential source details, names, identifiers, paths, counts, timelines, implementation claims and excerpts are excluded. The public bundle exposes only generalized themes and the editorial mapping. Its conceptual column cannot be independently reproduced from public sources alone; readers should not mistake it for a publicly audited backlog measure.

## Real-world column

- Observed: at least one cited public primary source documents an actual event or released capability satisfying the entire operational criterion within the stated scope. A vendor release can establish a documented release; it does not independently verify reliability or every advertised benefit.
- Partial: a standard, design, prototype, adjacent product or narrower observed capability supports only part of the criterion. Standards are not deployment evidence; announcements are not outcome evidence.
- Unknown: this review has not established sufficient evidence for the criterion, including no qualifying evidence found. This never means zero worldwide.
- Absent: direct evidence establishes the criterion is not met in a defined, exhaustively assessed scope (available category; zero rows here). Global absence is not claimed.

The historical occurrence test asks whether an ingredient has been documented by the review date, not whether a particular product is still offered to all users on that day. Current availability, laws and regional prevalence would require separate audits. Every source predates or equals the review date. Live pages have a review date, and historic policy reports are not used as legal advice.

Counts: Covered 7/10 = 70%; Partial 1/10 = 10%; Not found 2/10 = 20%. Observed 2/10 = 20%; Partial 6/10 = 60%; Unknown 2/10 = 20%. Do not calculate (Observed + 0.5 × Partial), add the columns, subtract them, or label either “percent of future.” No confidence interval is appropriate for this nonrandom editorial checklist.

Confidence: High means the primary source and category boundary clearly support the narrow classification. Medium means vendor reporting, indirect relevance or jurisdictional limits warrant extra caution. Low means little qualifying evidence was established. It is qualitative assessment confidence, not a statistical probability or proof of nonexistence.

## Contributions

Provide the indicator ID; proposed criterion/status change; a public primary source and publication date; review date; geographic and operational scope; a short paraphrase; limitations/counterevidence; and what observation would change the classification. If evidence supports only part, say which part. Distinguish source claims from your inference.

Discuss governance independently: consent, refusal, bargaining power, exit, appeal, infrastructure burdens, distribution of benefits, privacy and access. Do not turn people or communities into capability scores. The governance questions are editorial prompts, not causal findings or binary labels for society.

Keep private research and sensitive personal data out of submissions. Strip confidential names and specifics before proposing a public concept. Preserve past versions; record rationale for additions, removals, splits and merges; recompute with the full revised denominator; offer both old and new results when feasible. There is no guarantee of acceptance, legal protection, income or product performance.

## Published files

- vision-indicators.csv: the ten indicators, criteria, classifications and limits.
- public-sources.json: the public evidence register keyed to source IDs.
- APPENDIX.md: the book-facing discussion and public references.
- README-SECTION.md: the introductory discussion for the repository.
- figure-summary.json: the counts and review date represented by the figure.
- vision-coverage-book.png: the readable, labeled evidence matrix.

The PNG is the reviewed figure; its byte checksum is recorded in the repository.
The text and dataset expose the assessment for review. Executable plotting and
book-rendering helpers, SVG/PDF exports of the standalone chart, original-resolution
illustrations and font files are not included in this edition. This is not a
complete reproducible book-build package. A future plotting tool should derive
labels, dates and totals from the dataset, validate category values and demonstrate
that changed rows alter the result correctly before it is accepted.

Alt text and row-level prose are in the appendix and CSV. Status is written in each
cell, so color is redundant. Public contributors can reproduce the arithmetic and
challenge the public-source classifications without access to private research.
