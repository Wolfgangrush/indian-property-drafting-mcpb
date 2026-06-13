# wolfgang_rush — Indian Property & Conveyancing Drafting

**MCPB Desktop Extension** for Indian advocates using Claude Desktop App. Local-execution. Zero data collection.

> *Also available as a Claude Code Plugin:* *[github.com/Wolfgangrush/indian-property-drafting](https://github.com/Wolfgangrush/indian-property-drafting)*

## What this connector does

Sale, gift, mortgage, lease, partition, settlement, exchange, release, wakf, private-trust deeds + title-investigation reports. Stamp + Registration + Suraj Lamp compliance. 8 State exemplars.

## Case types

- `gift-deed` — Gift deed under Section 122 Transfer of Property Act 1882
- `mortgage-deed` — Mortgage deed (English / simple / equitable) under Sections 58-104 TPA
- `partition-deed` — Partition deed for co-owned / ancestral / joint family property
- `settlement-deed` — Settlement deed under Section 17 Registration Act
- `exchange-deed` — Exchange deed under Section 118 TPA
- `release-deed` — Release deed / relinquishment instrument
- `easement-deed` — Easement deed under the Indian Easements Act 1882
- `wakf-deed` — Wakf deed under the Wakf Act 1995
- `private-trust-deed` — Private trust deed under the Indian Trusts Act 1882
- `title-investigation-report` — Title-investigation report (advocate's certificate of title)

## Install

1. Claude Desktop App → **Settings → Extensions → Install Extension**
2. Select `wolfgang-indian-property-drafting.mcpb`
3. Enable

## System requirements

Claude Desktop App ≥ 0.10.0 · Python ≥ 3.10 · `pandoc` for .docx · `pdftotext` for PDF case-files (optional)

## Privacy

Zero data collection. Three-layer privacy firewall. Canonical policy: **<https://wolfgangrush.github.io/privacy/>**


## Architecture · how the six agents work

This connector runs a strict six-agent pipeline locally on your machine:

| Agent | What it does | Output |
|---|---|---|
| **Reader** | Reads every input document. Extracts facts with per-document audit log. **Applies the pseudonymisation firewall** (see below). Halts if a required statute PDF is missing. | `case-facts.md` |
| **Format** | Loads the case-type-specific skill + bench/state/forum-config + pleading base. Maps Reader's facts into the format placeholders. | `format-shell.md` |
| **Drafter** | Writes the first complete draft — Cause Title, Statutory Opening, Synopsis, Statement of Facts, Grounds, Prayer, Verification, Counsel Block, Index, Annexure List. | `draft-v1.md` + `draft-v1.docx` |
| **Verifier** | Anti-hallucination firewall. Compares draft-v1 against case-facts.md fact-by-fact. Flags hallucinated dates, fabricated citations, unsupported assertions, orphan annexure markers, missing factual basis. | `verification-report.md` |
| **Refiner** | Applies every Verifier flag. Polishes language to formal Indian pleading register. Enforces Registry formatting. Strips AI-style markers. | `draft-v2.md` + `draft-v2.docx` |
| **Overseer** | Reads draft-v2 with opposing-counsel lens. Finds weak prayers, contradictory facts, attackable defects, missing limbs of argument. Suggests hardening. | `opposing-notes.md` + `final-draft.docx` |

The pipeline is **forced by the connector itself** — the `get_agent_instructions()` tool is the mandatory first call when you ask for a draft and returns an 11-step orchestration script that names every agent's tool call. The Drafter cannot legitimately produce final output without the Reader having saved `case-facts.md` first. The `save_artifact` tool's allow-list rejects standalone python-docx or JavaScript generator scripts.

→ **Full pipeline architecture: [wolfgangrush.github.io/mcpb/agents/](https://wolfgangrush.github.io/mcpb/agents/)**

## 🔒 Pseudonymisation gateway — what gets substituted

The Reader agent applies a privacy firewall **before any downstream agent sees the facts**. The following are substituted with structural placeholders:

- **Party identifiers** — Petitioner / Respondent / Plaintiff / Defendant / Accused / Complainant / Witness names → `[Petitioner-A]`, `[Respondent-B]`, `[Witness-A]`
- **Addresses** — Full residential / business addresses → `[Address-Placeholder]`
- **Government identifiers** — PAN, Aadhaar, TAN, DIN, GSTIN → `[PAN-Placeholder]`, `[Aadhaar-Placeholder]`, etc.
- **Case numbers** — FIR / CR / Crime / SLP / Diary / CC / SC / RCS / lower-court case numbers → `[Crime-No-Placeholder]`, `[SLP-No-Placeholder]`, `[Lower-Court-Case-No-Placeholder]`
- **Financial figures** — Amounts in dispute, compensation, tax assessed → `[Amount-Placeholder]`
- **Statutory notice references** — Section 106 TPA notice dates, statutory demand-notice dates → `[Notice-Date-Placeholder]`

The Drafter, Verifier, Refiner, and Overseer agents process **placeholders only**. At the final `save_draft_as_docx` step, the placeholders are re-substituted with the real values **on your local machine**. The LLM never sees the re-substituted output.

This is the connector's contribution to your **Section 8(5) DPDP Act 2023** safeguard.

→ **Full pseudonymisation mechanism: [wolfgangrush.github.io/mcpb/agents/#pseudonymisation-gateway-what-gets-substituted](https://wolfgangrush.github.io/mcpb/agents/#pseudonymisation-gateway--what-gets-substituted)**

## ⚖️ DPDP Act 2023 — what this means for you

**Publisher position.** wolfgang_rush, in its capacity as software publisher, is **neither a Data Fiduciary nor a Data Processor** under the DPDP Act 2023 in respect of this connector. The connector runs entirely on your machine. There is no wolfgang_rush server, no telemetry, no API endpoint that the publisher controls. Section 2(i) requires "determining purpose and means of processing" — wolfgang_rush determines neither.

**User position.** You — the advocate using this connector — are the **Data Fiduciary** for your own client's personal data. This was true before installing the connector and remains true after. Your obligations under Sections 4, 5, 6, 8, 9, 11, 13 of the DPDP Act 2023 continue independent of this connector.

**What the connector helps with.** The pseudonymisation gateway is an architectural safeguard within the meaning of Section 8(5) (reasonable security safeguards). Local-only processing supports your minimisation posture (Section 8). The Reader's per-document audit log supports Section 8(8) (data accuracy). The Section 17(2)(a) exemption ("personal data processed for the purposes of any legal proceeding") substantially covers most everyday advocate processing.

**What the connector does not do.** It does not, by itself, satisfy any DPDP notice / consent / grievance-redressal obligation. Those remain yours to operationalise. It does not cover Anthropic's position as the LLM operator — that is governed by Anthropic's own terms.

→ **Full DPDP applicability analysis: [wolfgangrush.github.io/mcpb/dpdp/](https://wolfgangrush.github.io/mcpb/dpdp/)**

## Multilingual install guides

[हिन्दी](https://wolfgangrush.github.io/mcpb/hi/) · [मराठी](https://wolfgangrush.github.io/mcpb/mr/) · [தமிழ்](https://wolfgangrush.github.io/mcpb/ta/) · [తెలుగు](https://wolfgangrush.github.io/mcpb/te/) · [বাংলা](https://wolfgangrush.github.io/mcpb/bn/) · [ગુજરાતી](https://wolfgangrush.github.io/mcpb/gu/) · [ಕನ್ನಡ](https://wolfgangrush.github.io/mcpb/kn/) · [ਪੰਜਾਬੀ](https://wolfgangrush.github.io/mcpb/pa/) · [മലയാളം](https://wolfgangrush.github.io/mcpb/ml/) · [اردو](https://wolfgangrush.github.io/mcpb/ur/)

## ⚠️ AI verification disclaimer · 🔒 Pseudonymisation procedure

> **⚠️ AI can make mistakes — please verify the information before filing.**
> Every draft produced by this connector is a STARTING POINT. The Verifier
> agent runs an anti-hallucination firewall and the Overseer agent runs an
> opposing-counsel review, but neither replaces an advocate's independent
> verification of statutory references, citation accuracy, factual fidelity,
> and Registry-formatting compliance with the user's High Court / forum.
> The advocate filing the pleading remains responsible for the contents.
>
> **🔒 Protected by pseudonymisation procedure.** The Reader agent applies a
> domain-specific privacy firewall as the first step of the pipeline — party
> names, addresses, identifying numbers (FIR / CR / Crime / Suit / Diary /
> SLP / lower-court case numbers), PAN / Aadhaar references, financial
> figures, witness names, and statutory-notice references are substituted
> with structural placeholders BEFORE any downstream agent sees the facts.
> The Drafter, Verifier, Refiner, and Overseer agents process placeholders
> only. Real values are re-substituted at the final docx render step on the
> user's local machine. No real identifying data leaves the case folder.

## Examples

Three example prompts that demonstrate core functionality. Full prompt text with expected tool sequence is in `SAMPLE-CASES/README.md`.

- *"Draft a suit for partition of joint family property under the Hindu Succession Act 1956."*
- *"Draft a Section 6 Specific Relief Act suit for recovery of possession dispossessed without due process."*
- *"Draft an injunction suit under Order XXXIX Rules 1 and 2 CPC restraining alienation."*

See `SAMPLE-CASES/README.md` for the full prompt text and the expected tool-call sequence the Anthropic reviewer can use to exercise the pipeline end-to-end.

## License

MIT.

## Publisher

**wolfgang_rush** — independent open-source legal-tech publisher. Contact: wolfgangrush@gmail.com

## Source

<https://github.com/Wolfgangrush/indian-property-drafting-mcpb>

## Sample cases

See `SAMPLE-CASES/`.
