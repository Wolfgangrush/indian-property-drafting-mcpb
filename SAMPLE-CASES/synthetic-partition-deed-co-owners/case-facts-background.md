# Case Facts Background — Partition Deed (transactional · co-owners of intestate estate)

This fixture is **transactional**, not litigation. The connector drafts a partition deed from instructions; the Reader stage reads instructions + party particulars + schedule of properties to produce a draft deed.

All party names, addresses, PAN, monetary figures, property descriptions, and ancillary dates are fictional placeholders.

## Parties

- **Co-owner A:** [Co-owner-A], aged [Age-A-Placeholder], son of late [Father-Placeholder] (the Common Ancestor), resident of [Address-A-Placeholder], PAN [PAN-A-Placeholder].
- **Co-owner B:** [Co-owner-B], aged [Age-B-Placeholder], son of late [Father-Placeholder], resident of [Address-B-Placeholder], PAN [PAN-B-Placeholder].
- **Co-owner C:** [Co-owner-C], aged [Age-C-Placeholder], daughter of late [Father-Placeholder], resident of [Address-C-Placeholder], PAN [PAN-C-Placeholder].

## Common Ancestor

- Late [Father-Placeholder], who passed away intestate on [Date-of-Death-Placeholder]. Class I heirs under Schedule I, Hindu Succession Act 1956, are the three Co-owners — and no others.

## Statutory framework

- Hindu Succession Act, 1956, as amended by the Hindu Succession (Amendment) Act, 2005.
- Section 6 — daughter is a coparcener by birth in the same manner as a son (Vineeta Sharma v. Rakesh Sharma (2020) 9 SCC 1).
- Schedule I — Class I heirs — equal share per stirpes.

## Allotment plan

- **Schedule A — Immovables:**
  - Bungalow → [Co-owner-A] (with adjustment of Rs. [Adjustment-A-Placeholder]/- to [Co-owner-C])
  - Agricultural land → [Co-owner-B] (full ownership)
  - Commercial shop → [Co-owner-C] (with Rs. [Adjustment-A-Placeholder]/- adjustment received from [Co-owner-A])
- **Schedule B — Movables / Cash:** Equal 1/3 division
- **Schedule C — Jewellery / Personal effects:** As per Annexure I to the deed

## Case type

`partition-deed`

## Tax / regulatory framework

- Partition between coparceners is **not a transfer** under Section 47(i) IT Act 1961; no capital gains liability.
- Stamp duty — payable as applicable in [State-Placeholder] under the State Stamp Act / Indian Stamp Act 1899 Schedule I-A entry for partition deeds.
- Registration — under Section 17 of the Registration Act 1908 — compulsorily registrable as it deals with immovable property.

## How to use this fixture

1. Point `read_case_folder(path)` at this directory.
2. Reader extracts drafting instructions from `01-drafting-instructions-partition-deed.docx` + property schedule from `02-schedule-of-properties.docx` + this `case-facts-background.md`.
3. Call `get_case_type_format("partition-deed")`.
4. The Format stage maps the parties, properties, and allotment instructions into the partition-deed template.
5. The Drafter authors the full partition deed — recitals, statutory framework, schedules, cross-release clauses, indemnity, allotment paragraphs, stamp / registration / tax recitals, execution block.
6. The Verifier confirms that every property in the schedules has been allotted; that the statutory framework recital is accurate; that cross-releases are reciprocal; that stamp / registration / tax recitals are correctly stated.
7. The Refiner polishes language and harmonises defined terms.
8. The Overseer reads with an opposing-co-owner lens — identifies under-described items, missing indemnities, unbalanced valuations, future-claim vulnerabilities.
9. Output: `final-draft.docx` — a ship-ready partition deed for registration.

## Carve-outs flagged for human-counsel review

(i) Whether any earlier oral partition / family arrangement should be expressly recited and superseded.
(ii) Treatment of Schedule C jewellery — whether the parties wish to fully enumerate or refer to an external agreed list.
(iii) Whether the partition is to be registered immediately or executed first and registered within the 4-month statutory window under Section 23 Registration Act.
(iv) Whether to expressly recite Section 47(i) IT Act 1961 non-taxability — recommended.
