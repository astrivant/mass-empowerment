# Technical inspirations and weekly review

The book is fiction. Its notes identify narrower, public technical inspirations;
they do not claim that present software implements consciousness, personhood,
mind transfer, a fictional economy or the civic systems in Lowreach.

`source-revisions.json` records each cited public file, immutable commit and blob,
review timestamp, claim and evidence level. Implementation links are supplementary
corroboration. Reading code is not running tests or validating a deployment.

## Editorial source of truth

- `footnotes.json`: note identifiers, chapter anchors, wording and rendered links.
- `manuscript/ch*.md`: literary chapter text. A citation-only review must not edit it.
- `The Hours We Keep.md`: generated reading source; rebuild from the chapter sources.
- `citations/reviews/YYYY-MM-DD.md`: append-only review reports.
- Git history: prior book editions and citation states. Do not rewrite or force-push.

## Weekly procedure

1. Fetch the current book repository without overwriting uncommitted work. Read its
   instructions and current publication/signing policy. Check for an already open
   citation update before creating another.
2. Check that every cited repository and source remains public. Resolve each current
   default branch to a commit. Compare the cited documentation and relevant code
   with the previously reviewed commit. Record deletions, inaccessible files and
   non-fast-forward history honestly; never silently invent replacement evidence.
3. Revise only notes whose wording or evidence needs an update. Distinguish documented
   behavior, implementation, measured results, proposals and literary extrapolation.
   Keep existing note IDs and anchors. Pin citation links to exact verified commits.
4. Update the provenance and add a dated report, including an explicit no-material-
   change result when appropriate. Do not churn book wording merely because unrelated
   source files changed. Do not include private source material or conversation logs.
5. Run the citation check; compare chapter hashes before and after. Rebuild affected
   reading/PDF outputs, check note placement, links, page breaks and artwork visually,
   and preserve earlier editions in Git history.
6. Use a separate review branch and pull request only when publication is authorized
   and the repository's signing requirements are satisfied. Do not merge, change
   visibility, weaken checks, introduce credentials or bypass signing. If blocked,
   preserve the patch and report the precise missing access or approval.
7. Report material changes or an actionable blocker to the owner with the commit or
   pull-request link. A scheduled run is not proof that publication succeeded.

This document defines the review procedure; it does not install or claim that a
weekly schedule exists.
