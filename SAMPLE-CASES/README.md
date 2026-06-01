# Sample Cases — Reviewer Examples

Three anonymised fact patterns. All party names are placeholders.

## Example 1 — gift-deed

> *"Use the connector to draft a gift deed (Gift deed under Section 122 Transfer of Property Act 1882). Use anonymised placeholders for party names and figures."*

Tool sequence: list_case_types → get_case_type_format("gift-deed") → get_pleading_base → draft → save_draft_as_docx

## Example 2 — mortgage-deed

> *"Use the connector to draft a mortgage deed (Mortgage deed (English / simple / equitable) under Sections 58-104 TPA). Use anonymised placeholders for party names and figures."*

Tool sequence: list_case_types → get_case_type_format("mortgage-deed") → get_pleading_base → draft → save_draft_as_docx

## Example 3 — partition-deed

> *"Use the connector to draft a partition deed (Partition deed for co-owned / ancestral / joint family property). Use anonymised placeholders for party names and figures."*

Tool sequence: list_case_types → get_case_type_format("partition-deed") → get_pleading_base → draft → save_draft_as_docx

## Notes for the reviewer

- All examples use placeholders.
- No external API keys / accounts required.
- `save_draft_as_docx` requires `pandoc`.
- Three-layer privacy firewall applies throughout.

---

## Synthetic case folder for Anthropic reviewer

A fully-fictional, AAAK-pseudonymised case folder is bundled at:

`SAMPLE-CASES/synthetic-partition-deed-co-owners/`

It contains 2 source documents (.docx) plus a `case-facts-background.md` narrative.

**To exercise the pipeline end-to-end**, point `read_case_folder(path)` at this folder and follow the orchestration script returned by `get_agent_instructions()`. The Reader stage will extract facts, the Format stage will load the case-type SKILL.md template, and the remaining four agents (Drafter → Verifier → Refiner → Overseer) will produce `final-draft.docx`.

All identifiers in the bundled documents are structural placeholders. The Pseudonymisation Gateway is therefore exercising against pre-pseudonymised content; reviewers seeking to test re-substitution may replace placeholders with their own fictional values before invoking the pipeline.

