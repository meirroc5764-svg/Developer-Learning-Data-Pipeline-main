# Checkpoints — Overview

This folder covers the first 3 checkpoints from `PROJECT_GUIDE.md` — the
Pandas/data-preparation side of the project. Each checkpoint folder
contains its own validator script, ready to run, plus a short README that
explains:

- what the validator checks,
- what each PASS/FAIL message means,
- why the requirement exists,
- common reasons for failure,
- where to look in your own code.

**Kafka, MongoDB, and the API have no validator here.** Once Checkpoint 3
passes, you have proven your data is clean, correctly enriched, and that
your standalone processor reproduces it exactly from the raw CSV — that's
the point where this project stops handing you automated checks. Building
the streaming pipeline, the consumer, the storage layer, and the API from
there is on you, using `PROJECT_GUIDE.md` as your spec.

## The 3 checkpoints

| # | Checkpoint | Validator | Your input |
|---|---|---|---|
| 1 | [Clean Data](01_cleaning/README.md) | `validate_cleaned.py` | your cleaned JSONL file |
| 2 | [Processed / Enriched Data](02_processed_data/README.md) | `validate_processed.py` | your processed JSONL file |
| 3 | [Standalone Processor](03_processor/README.md) | `validate_processor_output.py` | your processor's output JSONL file |

## How to run any of them

Each validator lives inside its own checkpoint folder and only needs your
file path — no need to `cd` anywhere special:

```bash
python3 validation/01_cleaning/validate_cleaned.py path/to/your_cleaned.jsonl
python3 validation/02_processed_data/validate_processed.py path/to/your_processed.jsonl
python3 validation/03_processor/validate_processor_output.py path/to/your_processor_output.jsonl
```

(paths above assume you're running from the `student/` folder — adjust if you're elsewhere)

## Reading the output

Every checkpoint prints the same style of report:

```text
========================================
CHECKPOINT — CLEAN DATA
========================================

[PASS] Record count matches raw
[FAIL] YearsCode is integer or null for every record

Problem:
ResponseId=1842 has YearsCode='14' (str)

Expected:
integer or null

Check:
Review the YearsCode conversion in your cleaning step.

RESULT: 6/7 checks passed
CHECKPOINT FAILED
```

- **[PASS] / [FAIL]** lines: one per check. This is your quick scoreboard.
- **Problem**: a concrete example from YOUR data showing what's wrong (usually one specific `ResponseId` / `responseId`).
- **Expected**: what the correct result should look like.
- **Check**: which part of your implementation to go look at.
- **RESULT / CHECKPOINT PASSED or FAILED**: the exit code matches this — `0` when everything passes, `1` when something fails.

The terminal tells you **what failed and where to look**. It does not explain the full reasoning — that's what each checkpoint's README is for. If a check fails, open the matching README section and read the entry for that specific check name.

## The golden sample

Several checks compare your data against a small set of **18 real, known
respondents**, hand-picked to cover tricky cases: missing fields,
single-selection vs multi-selection answers, different experience levels,
and so on. If your implementation is correct for these 18 respondents, it
is very likely correct for all 49,191. If it's wrong for one of them, the
failure message tells you exactly which `ResponseId` and which field —
that's usually much faster to debug than staring at a report about "40
records failed somewhere." These respondents are part of the answer key,
so this project doesn't hand you the file to browse — trace the
respondent's raw CSV row through your own pipeline instead.

## The workflow (same as PROJECT_GUIDE.md Section 4)

```
Implement → Run Validation → Investigate Failures → Fix → Validate Again → Continue
```

Do not move to the next phase until the current checkpoint passes.
