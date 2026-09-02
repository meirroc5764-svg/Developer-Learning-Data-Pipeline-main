# Checkpoint 2 — Processed / Enriched Data

Validator: `validate_processed.py` (in this folder)

```bash
python3 validate_processed.py path/to/your_processed.jsonl
```

This checks your final Pandas result — cleaning **and** enrichment together — against `PROJECT_GUIDE.md` Section 10–11.

## What each check means

**Record count matches raw respondents / responseId is unique / Same respondents as raw dataset**
Same idea as Checkpoint 1, now on your processed file. No respondent should appear, disappear, or duplicate during enrichment.

**Exactly 15 operational fields per record**
The camelCase schema from `PROJECT_GUIDE.md` Section 10 has exactly 15 fields — no more, no less.
*If it fails:* the report shows the actual field list for one bad record. Compare it against the expected 15. A common cause is leaving in a leftover raw field name (e.g. both `LearnCode` and `learningMethods`) or forgetting one of the 4 enrichment fields.

**learningMethods / aiLearningMethods remain arrays or null**
These must still be real lists — not exploded into multiple records, not joined back into a string.
*If it fails:* check whatever step maps your cleaned dataset to the processed schema — are you passing the list through unchanged, or accidentally transforming it?

**experienceLevel matches the YearsCode rule**
Checked against the exact business rule from `PROJECT_GUIDE.md` Section 10 (0–2 Beginner, 3–5 Early Career, 6–10 Experienced, 11+ Highly Experienced, missing → Unknown).
*If it fails:* the report shows the specific `yearsCode` / `experienceLevel` pair that doesn't match. **If it's failing specifically on records with a missing `yearsCode`**, this is almost certainly the classic pitfall described in `PROJECT_GUIDE.md` Section 10: comparing a missing value with `<=` silently returns `False` instead of raising an error, so "missing" respondents can quietly fall into "Highly Experienced" instead of "Unknown." Check that you detect missing values explicitly, before doing any numeric comparison.

**usesDocumentation / usesAIForLearning / usesStackOverflow match their option rules**
Each must be `True` only when `learningMethods` contains the *exact* matching option text, `False` otherwise (including when `learningMethods` is missing).
*If it fails:* the report shows the respondent's actual `learningMethods` list next to the wrong boolean. The most common cause is matching against a slightly wrong string — extra/missing punctuation, different capitalization, or a shortened version of the option text. Go back to your Phase 1 exploration and copy the option text exactly.

**yearsCode is null if and only if experienceLevel is Unknown**
A consistency check between the two fields — this is a second angle on the same missing-value pitfall described above.

**Pass-through fields (age, devType, learnCodeChoose, learnCodeAI, aiUsage, aiTrust, aiSentiment) are unchanged**
These 7 fields only get renamed during the schema mapping — their *value* should be identical to the raw CSV. This checks every record, not just a sample.
*If it fails:* the report names the exact `responseId` and field. Check your schema-mapping step for an accidental transformation on a field that should just pass through.

**Golden sample: all known respondents are present / match the reference values exactly**
Same idea as Checkpoint 1 — 18 hand-picked respondents, checked field by field.

## Why this checkpoint exists

This is the last Pandas-side checkpoint. Once this passes, you have proven — on real data, not just a few examples you thought of yourself — that your cleaning and enrichment rules are correct. Checkpoint 3 (the standalone processor) exists to catch *pipeline* bugs — a reimplementation drifting from what you already proved correct here — not *business rule* bugs, but only if this checkpoint is solid first. Once Checkpoint 3 passes too, you're building the rest of the system (Kafka, MongoDB, the API) on data you already know is right.

## How to reason about a fix

If several checks fail together (e.g. `experienceLevel` and the null-consistency check both fail), look for one shared root cause rather than fixing each symptom separately — they are very often the same bug seen from two angles.
