# Day 4 Project: How Developers Learn in the AI Era

## 1. Introduction

This project uses real data from the **Stack Overflow Developer Survey 2025**.

Every year, Stack Overflow asks developers around the world about how they work, learn, and use technology. The 2025 survey received answers from more than **49,000 developers and people who code, from 177 countries**. It is one of the largest and most used snapshots of the developer community.

The survey is a great real-world dataset, but it is not perfect. It does not represent every developer in the world — only the people who chose to answer it. Keep that in mind while you work.

Official survey links:
- [Stack Overflow Developer Survey](https://survey.stackoverflow.co/)
- [2025 Survey](https://survey.stackoverflow.co/2025/)

The full survey has many questions. For this project, we picked **11 fields** related to learning and AI, and reduced the data to **49,191 respondent records**.

You will work with this file:

```
shared/data/developer_ai_learning_raw.csv
```

**Each row in this file is one survey respondent.** This rule stays true through the whole project — no matter what you build, one respondent must always stay one record.

## 2. Project Story: How Developers Learn in the AI Era

Our goal is to understand how developers learn today, and how AI tools are becoming part of that learning process.

Questions we want to explore:
- What learning resources do developers use the most?
- How important is technical documentation?
- How often do developers use AI tools?
- Do developers trust AI to be accurate?
- How are developers learning AI-related skills?
- Does learning behavior look different for developers with different experience levels?

We are **not** doing deep statistical research. Our real goal is a **Data Engineering** goal: build a reliable pipeline that can prepare, move, store, and serve this data correctly.

## 3. Technology Stack Requirements

**IMPORTANT:** This project has specific technology requirements for each component:

### Required Technologies:

| Component | Technology | Required |
|-----------|-----------|----------|
| Data Investigation & Cleaning | **Pandas (Python)** | ✅ Required |
| Raw Producer (Kafka) | **Python** | ✅ Required |
| Processing Service (Kafka) | **Python** | ✅ Required |
| Consumer (Kafka → MongoDB) | **C# (.NET)** | ✅ Required |
| API | **ASP.NET Core (C#)** | ✅ Required |
| Message Broker | **Kafka** | ✅ Required |
| Database | **MongoDB** | ✅ Required |

### Deployment Requirement:

**You MUST submit your project with Docker Compose configuration that:**
- Starts the entire system with a single command: `docker-compose up`
- Includes all services: Kafka, Zookeeper, MongoDB, Producer, Processor, Consumer, API
- Properly configures networking between services
- Includes health checks where appropriate
- Uses environment variables for configuration

**Your submission must include:**
1. `docker-compose.yml` - Main compose file
2. `Dockerfile` for each custom service (Producer, Processor, Consumer, API)
3. `README.md` with clear instructions on how to run the system

**The instructor will test your project by running:**
```bash
docker-compose up
```

If the system does not start correctly with this single command, the project will not be accepted.

## 4. The System We Are Going to Build

By the end of the project, you will have built a small, real, service-based data pipeline:

```
Raw Survey CSV
   → Raw Producer
   → Kafka Raw Topic
   → Python Processing Service
   → Kafka Processed Topic
   → C# Consumer
   → MongoDB
   → ASP.NET Core API
```

Before building this operational pipeline, you will first use **Pandas** to investigate the data and decide exactly how it should be cleaned and enriched. Only after those decisions are proven correct will you turn them into a real pipeline.

Short description of each part:

**Pandas Notebook** — Used to investigate the raw data, decide how to clean it, analyze it, and define the transformations the rest of the pipeline will later automate.

**Standalone Python Processor** — Takes the decisions you made in the notebook and turns them into normal, reusable Python code. It must be tested on its own, before Kafka is involved.

**Raw Producer** — Reads raw respondent records and sends them to the raw Kafka topic. It does **not** clean or transform anything.

**Python Processing Service** — Reads raw records from Kafka, applies the same processing logic already tested in the standalone processor, and sends clean, enriched records to the processed Kafka topic.

**C# Consumer** — Reads processed records from Kafka and saves them into MongoDB. It does not invent new cleaning or transformation rules.

**MongoDB** — Stores the final processed respondent documents. Fields like learning methods stay as arrays.

**ASP.NET Core API** — Reads from MongoDB and answers questions through HTTP endpoints. It queries already-processed data. It does not clean anything.

### Solution Notebooks Available

After attempting each phase, you can review the solution notebooks in the `solutions/` folder:
- `01_exploration_solution.ipynb` - Example exploration approach
- `02_cleaning_solution.ipynb` - Complete cleaning implementation
- `03_enrichment_solution.ipynb` - Complete enrichment implementation
- `04_processor_solution.py` - Standalone processor example
- `MONGODB_GUIDE.md` - MongoDB setup and query examples

**Important:** Try to solve each phase yourself first before looking at the solutions. The solutions are there to help you learn, not to copy.

## 5. Important Workflow: Validate Before You Continue

This project is built in **stages**. Do not rush from one stage to the next.

At every important checkpoint, you will run a validator. The workflow is always:

```
Implement → Run Validation → Investigate Failures → Fix → Validate Again → Continue
```

**Why this matters:** a small mistake in cleaning can quietly turn into a wrong Kafka message, which becomes a wrong MongoDB document, which becomes a wrong API result. Validating at each step means every next component always receives data it can trust.

> **Rule: Do not continue to the next major stage until the current checkpoint passes.**

Validators check the **result**, not your code style. Your implementation does not need to look like anyone else's. It only needs to produce the correct data.

## 6. Phase 1 — Data Investigation

**Why are we doing this?**

Before you change any data, you need to understand what is actually inside it. Investigation and cleaning are two different jobs. During investigation, **the raw dataset must stay unchanged** — you are only looking, not editing.

Open a Jupyter Notebook and inspect the raw file. You should look at:

- shape (how many rows and columns)
- columns and dtypes
- general info (`info()`)
- missing values per column
- duplicate rows
- whether `ResponseId` is unique
- the main categorical values
- value distributions
- which columns hold multiple answers in one cell

Use these Pandas operations:

| Operation | Use it to check |
|---|---|
| `pd.read_csv()` | Load the data |
| `head()` | Look at real rows |
| `sample()` | Look at random rows |
| `shape` | Row and column count |
| `columns` | Column names |
| `dtypes` | Data types per column |
| `info()` | Types + non-null counts together |
| `isna().sum()` | Missing values per column |
| `duplicated().sum()` | Full duplicate rows |
| ResponseId duplicate check | Is the respondent ID unique? |
| `nunique()` | Number of distinct values per column |
| `unique()` | The actual distinct values |
| `value_counts()` | How common each value is |

We will **not** tell you the exact numbers you should find — discover them yourself. You should be able to answer: how many rows and columns are there, are there duplicate rows, is `ResponseId` unique, how much is missing in each column, and which columns are multi-select (look for `;` inside the values).

**Out of scope for this phase:** correlation analysis, advanced statistics, anomaly detection, or checking relationships between missing values. Keep it simple.

**Deliverable:** a notebook section where you write down, in your own words, what you found and what you think needs to be handled during cleaning.

## 7. Phase 2 — Cleaning

**Why are we doing this?**

Cleaning does **not** mean deleting every missing value or "fixing" everything that looks unusual. A good cleaning decision solves a real problem while keeping as much real information as possible.

The most important rule of this whole project:

> **ONE RESPONDENT = ONE RECORD.**

Every cleaning decision must respect this rule.

### What you must do

- Keep every respondent. Do not remove a row just because one optional question was skipped.
- Check if duplicate rows actually exist before deciding whether to remove anything. Do not assume — verify it.
- Keep `ResponseId` unique after cleaning.
- Convert `YearsCode` into a **nullable integer**: real answers become whole numbers, missing answers stay missing (not `0`, not deleted).
- Correctly prepare the multi-select fields (see Section 7 below).

### What you must NOT do

- Do not run a global `dropna()` on the whole dataset.
- Do not "clean up" category text that already looks fine (do not shorten or reword answers).
- Do not invent placeholder values like `"Unknown"` inside the original survey fields.
- Do not aggregate or summarize data at this stage.
- Do not add enrichment fields yet — that comes later.

## 8. Guided Concept — Multi-Select Data

Some survey questions allowed a respondent to pick **more than one** answer. In the raw CSV, those answers are stored as one string, separated by `;`.

Example of one cell:

```
"Online Courses or Certification (includes all media types);Stack Overflow or Stack Exchange"
```

This one string actually means the respondent picked **two** options.

Because our rule is **one respondent = one record**, the cleaned dataset must **not** use `explode()` here.

Instead, use Pandas string splitting:

```python
Series.str.split(";")
```

### `split()` vs `explode()`

**`split()`**
- Turns one string into a list of strings.
- The respondent stays in exactly one row.
- A list works naturally later as a JSON array and as a MongoDB array.

**`explode()`**
- Turns one row with a list into several rows — one row per item.
- This changes the meaning ("grain") of the dataset.
- The same respondent can end up in multiple rows.

`explode()` will be useful later, but only **temporarily**, during analysis, to count how often each option was chosen. It must never replace your real, saved dataset.

Make sure you understand this difference clearly before moving on — it affects everything that comes after.

## 9. Checkpoint — Clean Data

Before continuing, validate your cleaned result.

Run the cleaning validator provided for this project:

```bash
python3 validation/01_cleaning/validate_cleaned.py path/to/your_cleaned.jsonl
```

See `validation/01_cleaning/README.md` if a check fails and you're not sure why.

The validator checks things like:
- record count,
- required fields are present,
- `ResponseId` is unique,
- `YearsCode` is stored correctly (integer or missing),
- multi-select fields are stored correctly (list or missing),
- missing values were preserved, not removed or replaced,
- original survey answers were not changed.

**If validation fails:**
1. Read the failed check carefully.
2. Go back to your notebook.
3. Find the transformation that causes the problem.
4. Fix it.
5. Run the validator again.

Do not move to Phase 3 until this checkpoint passes.

## 10. Phase 3 — Pandas Analysis

**Why are we querying the data with Pandas if we will later query MongoDB through an API?**

Good question — here is the difference:

> **Pandas = understand and validate the data, before it is used operationally.**
> **MongoDB + API = serve the already processed data, to real applications and users.**

Pandas analysis happens once, while you are preparing the data. It helps you understand it, check that your cleaning worked, and confirm the data can actually answer useful questions. The API will later serve fast, simple queries on data that is already known to be correct — it is not the place to explore or investigate.

Using your **cleaned** dataset, answer these fixed questions:

1. What are the most common learning methods (`LearnCode`)?
2. What are the most common methods developers use to learn AI (`AILearnHow`)?
3. What is the distribution of AI trust/accuracy answers (`AIAcc`)?
4. What is the distribution of AI usage frequency (`AISelect`)?
5. How does learning behavior differ across experience levels? (You will be able to fully answer this after Phase 4, once `experienceLevel` exists.)

For questions 1 and 2, you are counting individual selections inside a multi-select field. You may create a **temporary copy** of the column and use `explode()` there, only to count.

> **Do not save the exploded DataFrame as your production dataset.** It is a counting tool, not a deliverable.

## 11. Phase 4 — Enrichment

Now that you understand the data, you can calculate a few extra fields that will make later queries much simpler.

You must create **exactly** these four fields — no more, no less:

### `experienceLevel`

Built from `YearsCode`, using these ranges:

| YearsCode | experienceLevel |
|---|---|
| 0–2 | Beginner |
| 3–5 | Early Career |
| 6–10 | Experienced |
| 11+ | Highly Experienced |
| missing | Unknown |

This is a fixed business rule, not something to guess — use these exact ranges.

> **Watch out:** if `YearsCode` is missing, make sure your check actually catches that (`pd.isna(...)`), and returns `Unknown`. A comparison like `years_code <= 2` against a missing value does not raise an error and does not return `True` — it silently returns `False`, so a careless implementation can put "missing" respondents into "Highly Experienced" by accident. Test this case directly.

### `usesDocumentation`, `usesAIForLearning`, `usesStackOverflow`

Three `True`/`False` fields. Each one is `True` only when `LearnCode` contains one specific option:

- `usesDocumentation` → the option about **technical documentation**.
- `usesAIForLearning` → the option about **AI CodeGen tools / AI-enabled apps**.
- `usesStackOverflow` → the option about **Stack Overflow or Stack Exchange**.

All three are `False` when `LearnCode` is missing, or when the respondent simply did not pick that option.

**Do not guess the exact option text.** Go back to your Phase 1 exploration and find the exact wording of these options as they appear in the real data (`unique()` on the exploded `LearnCode` values is a good way to see them). Match the text **exactly** — a small difference (missing punctuation, different wording) means the check will never match.

`False` for `usesDocumentation` means *"technical documentation was not observed among this respondent's recorded learning methods."* It does not mean the respondent definitely never uses documentation in real life — it only reflects what this survey field shows.

Do not invent new enrichment fields beyond these four.

**Why bother?** Without enrichment, every consumer of this data (the API, other services, other students) would have to re-read and re-interpret the raw survey text every single time. By calculating these fields once, correctly, we save that work for everyone downstream — Kafka, MongoDB, and the API all benefit from it.

## 12. Checkpoint — Processed Data

Validate your final Pandas result — cleaning **and** enrichment together:

```bash
python3 validation/02_processed_data/validate_processed.py path/to/your_processed.jsonl
```

See `validation/02_processed_data/README.md` if a check fails.

The validator checks:
- respondent count is correct,
- the schema has exactly the expected fields,
- `responseId` is unique,
- multi-select fields are still real arrays (not exploded),
- missing values are handled correctly,
- `experienceLevel` is correct,
- the three boolean enrichment fields are correct.

Once this passes, your Pandas/data-discovery work is done. Well done — this is the foundation everything else is built on.

## 13. Phase 5 — Turn the Notebook into Reusable Python

**Why are we doing this?**

A notebook is great for exploring and experimenting. But a real data pipeline needs code that can run automatically, again and again, on new input — without a person manually clicking through notebook cells.

> **Notebook = discover the logic.**
> **Processor = automate the logic.**

**Important: you are not converting the whole notebook into a processor.** Your notebook contains two different kinds of work:

1. **Dataset-level work** — things like `value_counts()`, `groupby()`, temporary `explode()`, distributions, comparisons. These need many (or all) records at once, to understand and validate the dataset. This stays in the notebook — it does not belong in the processor.
2. **Record-level work** — splitting multi-select fields, converting `YearsCode`, calculating `experienceLevel`, the boolean enrichment fields, mapping the final schema. Each of these only needs **one respondent** to run. This is what becomes reusable processing code.

Think of it as a transition:

```
Notebook  →  discover and verify the transformation rules

Raw record  →  process_record(record)  →  processed record
```

The standalone processor simply calls `process_record()` once per row, for every row in the CSV. Later, the Kafka Processing Service will reuse **the exact same function** — only what feeds it changes:

```
Kafka message  →  process_record(message)  →  processed Kafka message
```

> **Simple rule:** if a transformation can be calculated from one respondent alone, it belongs in `process_record()`. If it needs many respondents together, it belongs to the analysis stage in the notebook — not to this processor.

This is also why we test the processor against the full CSV before Kafka is involved: running `process_record()` on every row proves the record-level logic is correct across the whole dataset. Kafka later changes **how records arrive** (one message at a time, continuously) — it does not change the transformation rules applied to each respondent.

Take the record-level cleaning and enrichment decisions you already proved correct, and turn them into normal, reusable Python functions (a `.py` file, not a notebook).

Your processor must be able to start from the **original raw CSV** and produce the full final processed result on its own. It must not depend on any file you already prepared manually in the notebook.

## 14. Critical Checkpoint — Test the Processor Before Kafka

This step is very important. Do **not** put untested processing code directly inside your Kafka service.

First, run it standalone:

```
Raw CSV → Standalone Python Processor → Processed Output
```

Run your processor against the original raw dataset, then run the provided validator on the output:

```bash
python3 validation/03_processor/validate_processor_output.py path/to/your_processor_output.jsonl
```

It must match the expected processed data contract exactly. See `validation/03_processor/README.md` if a check fails.

**Only after this passes**, connect your processing logic to Kafka. This is the last automated checkpoint this project gives you — from here on (Kafka, MongoDB, the API), you're building and verifying the rest of the system yourself, using the sections below as your spec.

**Why this order matters:** if your standalone processor is already proven correct, and something breaks later inside the Kafka pipeline, you immediately know the cleaning logic is not the problem. The bug is more likely in messaging, serialization, or how the service consumes/produces messages. This separation of concerns is a real Data Engineering debugging habit — it saves a lot of time.

## 15. Phase 6 — Build the Streaming Pipeline

Now you build the live, operational system.

### Raw Producer

Reads raw respondent records and publishes them to the raw Kafka topic. **One respondent = one message.** The producer does not clean or enrich anything — it only moves raw data.

### Python Processing Service

Consumes raw messages from Kafka. Applies the **same** processing logic you already tested in your standalone processor (do not write it a second time from scratch — reuse it). Publishes the result to the processed Kafka topic.

**Checkpoint:** no automated validator is provided for this stage — before moving on to MongoDB, verify it yourself: take a few known respondents (pick some `ResponseId`s you already traced through Checkpoint 3), confirm their raw record made it onto the raw topic unchanged, and confirm the corresponding processed message matches what your standalone processor produced for that same respondent. If your Processing Service is really reusing the same tested logic (as it should — see Section 12), this is a quick spot-check, not a new investigation.

## 16. Phase 7 — C# Consumer and MongoDB

The C# consumer's job is simple and specific:

```
Kafka → deserialize → MongoDB
```

It should **not** invent any new business rules or transformations — the data arriving from Kafka should already be correct.

MongoDB documents must preserve the processed schema. Learning-method fields must stay as arrays, not be flattened or joined into strings.

**Checkpoint:** no automated validator is provided for this stage — before building the API, verify it yourself: query your collection for a few known respondents and confirm every field matches what left the processed Kafka topic (same values, arrays still arrays, nulls still null, plus Mongo's own `_id`).

## 17. Phase 8 — ASP.NET Core Query API

At this point, the data is cleaned, enriched, streamed, and stored. The API's job is to **answer questions** using the processed data already sitting in MongoDB.

This is not a CRUD-heavy API. Think of it mainly as a **query layer**.

Build endpoints for these tasks:

1. Return respondents who use technical documentation for learning.
2. Return respondents who use both technical documentation **and** AI tools for learning.
3. Filter respondents by AI trust/accuracy category.
4. Filter respondents by experience level.
5. Return up to 20 back-end developers who use AI for learning, ordered by years of coding experience, from highest to lowest.

Use MongoDB queries to answer these. Keep endpoints focused on querying — do not add any Pandas-style cleaning logic inside the API. If you find yourself needing to "fix" the data inside the API, that is a sign something upstream needs to be corrected instead.

**Checkpoint:** no automated validator is provided for this stage — once your API is running, call each of the 5 endpoints yourself and sanity-check the results (right count, right respondents, right order for Task 5) against a few records you already know are correct from earlier checkpoints.

## 18. Final Validation and Submission

At the end, the complete system represents this full flow:

```
Raw CSV → Kafka Raw → Python Processor → Kafka Processed → C# Consumer → MongoDB → ASP.NET Core API
```

Pick a few known respondents and trace them through the whole pipeline, end to end. Confirm that the final API results match what you would expect from the original raw data.

> **Reliable systems are built by validating each boundary, not only by checking the final output.**

### Submission Requirements

Your final submission MUST include:

1. **docker-compose.yml** - Complete Docker Compose configuration
2. **Dockerfiles** - One for each custom service (Producer, Processor, Consumer, API)
3. **Source Code** - All Python and C# code properly organized
4. **README.md** - Clear instructions on:
   - How to start the system (`docker-compose up`)
   - How to verify it's working
   - API endpoints and example queries
   - Any environment variables or configuration needed

### Testing Your Submission

Before submitting, test that your system works from scratch:

```bash
# Clean everything
docker-compose down -v

# Start fresh
docker-compose up

# Verify:
# 1. Kafka topics are created
# 2. Data flows through the pipeline
# 3. MongoDB contains processed records
# 4. API responds to queries
```

**The instructor will test your project by running `docker-compose up` and nothing else.**

If the system does not start and work correctly with this single command, the project will be returned for fixes.

## 19. Quick Reference — What to Build, Phase by Phase

| Phase | You build | Checkpoint |
|---|---|---|
| 1. Investigation | Notebook exploration | — (no file produced) |
| 2. Cleaning | Cleaned dataset | ✅ Clean Data validator |
| 3. Analysis | Notebook answers to 5 questions | — (no file produced) |
| 4. Enrichment | 4 derived fields | ✅ Processed Data validator |
| 5. Processor | Reusable Python code | ✅ Processor-vs-reference validator |
| 6. Streaming | Producer + Processing Service | manual spot-check (no validator) |
| 7. Storage | C# Consumer + MongoDB | manual spot-check (no validator) |
| 8. API | ASP.NET Core query endpoints | manual spot-check (no validator) |

Checkpoints 1–3 have automated validators — one per checkpoint folder inside `validation/` next to this guide (`validation/01_cleaning/`, `validation/02_processed_data/`, `validation/03_processor/`), each with its own README explaining what it checks and why, and where to look in your own code if it fails. That's where this project's automated testing stops: once Checkpoint 3 passes, you know your data is correct, and Phases 6–8 are yours to build and verify using the guide above as your spec.

Good luck — build it one trustworthy step at a time.
