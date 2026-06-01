# Wolfgang Rush — Indian Property & Conveyancing Drafting

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

## License

MIT.

## Publisher

**Rushikesh R. Mahajan**, Advocate, Bombay HC Nagpur, publishing as **Wolfgang Rush**. advrushikeshravindramahajan@gmail.com

## Source

<https://github.com/Wolfgangrush/indian-property-drafting-mcpb>

## Sample cases

See `SAMPLE-CASES/`.
