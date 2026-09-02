# Checkpoint 1 — Clean Data

Validator: `validate_cleaned.py` (in this folder)

```bash
python3 validate_cleaned.py path/to/your_cleaned.jsonl
```

This checks your cleaned dataset against the cleaning contract from `PROJECT_GUIDE.md` Section 6–7. It only checks the **result** — record count, field types, and values. It does not care how your notebook code is written.

## What each check means

**Record count matches raw**
Your file must have the same number of records as `developer_ai_learning_raw.csv` — because no real duplicate rows exist in this dataset, nothing should have been removed.
*If it fails:* you probably called something like `dropna()` on the whole DataFrame, which deletes any row with at least one missing value (almost every row has at least one).

**Every record has exactly the 11 expected fields**
No renamed, dropped, or extra fields.
*If it fails:* check your column selection and any `rename()` calls.

**ResponseId is unique / Same ResponseIds as raw dataset**
The respondent ID is the primary key of this project. It must stay unique, and the exact same set of respondents must exist before and after cleaning.
*If it fails:* something in your pipeline is duplicating or dropping specific rows — look for a merge/join, or an accidental filter.

**YearsCode is integer or null for every record**
Real answers should become plain integers. Missing answers should stay missing — never `0`, never a string, never a float like `14.0`.
*If it fails:* you likely used a numpy `int` type (which can't hold missing values) instead of a nullable integer type, or didn't handle missing values before converting.

**LearnCode is list or null / AILearnHow is list or null**
These are the multi-select fields. A real answer becomes a list of strings. A missing answer stays `null` — never an empty list, never the original `;`-joined string.
*If it fails:* check your string-splitting logic — did you split before checking for missing values, or after? An empty list means "asked and picked nothing," which is different from "not asked."

**AISelect / AIAcc / AISent values are within the known valid category set**
These three fields have a small, fixed set of real survey answers. Your cleaned values must be exactly one of those, or `null`.
*If it fails:* you likely reworded, trimmed, or "corrected" some text that should have been left untouched.

**Original survey answers (Age, DevType, LearnCodeChoose, LearnCodeAI, AISelect, AIAcc, AISent) are unchanged**
This checks every single record — not just a sample — against the raw CSV, for every field that cleaning is not supposed to touch.
*If it fails:* the report tells you the exact `ResponseId` and field. Go find where that value could have been altered — a normalization step, a typo fix, a category mapping you weren't asked to do.

**Golden sample: all 18 known respondents are present / match the reference values exactly**
A small set of hand-picked respondents is checked in full detail. If one of these fails, the report names the exact `ResponseId` and field that's wrong — that's usually the fastest way to find your bug, because each golden respondent was chosen specifically to stress one tricky case (missing `LearnCode`, a single-selection answer, missing `YearsCode`, and so on).

## Why this checkpoint exists

Every stage after this one builds on your cleaned data. If a respondent silently disappears here, they will never make it to Kafka, MongoDB, or the API. If `YearsCode` isn't a real nullable integer, your `experienceLevel` enrichment in the next phase will silently break for missing values (this is a documented, easy-to-make mistake — see `PROJECT_GUIDE.md` Section 10's "Watch out" box).

## How to reason about a fix

Don't guess-and-check. When a check fails:
1. Note the exact `ResponseId` (or field) named in the failure message.
2. Go back to your notebook and look up that respondent in the **raw** CSV — what does their real answer look like?
3. Trace your cleaning step for that field, line by line, for that one respondent.
4. Fix the general rule (not just that one respondent) and re-run the validator.
