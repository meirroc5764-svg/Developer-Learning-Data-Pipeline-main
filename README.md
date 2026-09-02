# Day 4 Project — Start Here

1. **Read `PROJECT_GUIDE.md`** in this folder — it explains the whole project, phase by phase.
2. **The raw dataset** is at `data/developer_ai_learning_raw.csv`. Read-only — never modify it.
3. **Validators** live in `validation/01_cleaning/`, `validation/02_processed_data/`
 — each folder has its own copy of its validator script, ready to run:
   ```bash
   python3 validation/01_cleaning/validate_cleaned.py path/to/your_cleaned.jsonl
   ```
4. **If a check fails**, open the matching folder's README — it explains what the check means, why it exists, and where to look in your own code.

These 2 checkpoints (Clean Data, Processed Data, Standalone Processor) are as far as automated validation goes in this project. Once Checkpoint 2 passes, you have verified, correct data — build Kafka, MongoDB, and the API from there yourself, using `PROJECT_GUIDE.md` as your spec.

## How checkpoints work

```
Implement → Run Validation → Investigate Failures → Fix → Validate Again → Continue
```

**Do not continue to the next phase until the current checkpoint passes.** A mistake in cleaning silently becomes a wrong Kafka message, a wrong MongoDB document, and a wrong API result — validating at each boundary catches it early, where it's cheap to fix.

Start with `PROJECT_GUIDE.md` Section 5 (Phase 1 — Data Investigation).
