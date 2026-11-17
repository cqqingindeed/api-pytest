---
name: research-to-slides
description: Research-first planning for new work in the api-pytest project. Use this skill whenever the user asks to create a new project or sub-project here (e.g. CI pipeline, reporting, test-data setup), or add a new feature, module, integration, test suite or capability to api-pytest — even if they don't ask for research or a design doc. Before writing any code, search online, analyze the options, and write a high-level design file docs/todo/<name>_blueprint.txt covering what to do, possible approaches, tools & technologies, and references. Do not use for bug fixes, small edits, refactors, renames, or questions about existing code.
---

# Research to Blueprint

When someone asks for a new project or a new feature, the expensive mistakes happen before the first line of code: picking the wrong library, missing an existing solution, or misunderstanding the scope. This skill puts a short research-and-design step in front of the build, and leaves a written blueprint the user can review, edit and keep.

## Workflow

### 1. Pin down the request

Work out from the request and the codebase:
- **Name**: a short identifier for the project or feature. Use lowercase words joined by hyphens (e.g. `api-key-rotation`, `job-tracker-dashboard`). It becomes the file name.
- **Goal**: what the user wants to exist when this is done, and for whom.
- **Context**: this is the api-pytest project, a Python + pytest API test-automation suite. Read `README.md` (including its "Planned additions" list, which often names the feature being asked for), `requirements.txt`, `pytest.ini`, `conftest.py`, and the folders the work touches (`tests/`, `clients/`, `helpers/`, `configs/`, `docs/`). The blueprint must fit this stack and layout — reuse `clients/api_client.py`, the helpers and the pytest markers rather than proposing a different framework, unless there is a strong reason and you say what it is.

Ask the user only if the goal is truly unclear. Otherwise state your assumptions in the blueprint and keep going.

### 2. Research online

Use WebSearch (and fetch pages when a result looks useful) to find:
- How others have solved this problem: official docs, well-known libraries, reference architectures, good blog posts or examples.
- Current versions and maintenance status of candidate tools. Prefer actively maintained, widely used options, and note anything deprecated.
- Known pitfalls, limits, security or licensing concerns.

Run several searches from different angles in one go (e.g. "<problem> python library", "<problem> best practices", "<tool A> vs <tool B>"). Aim for enough sources to compare at least two approaches — usually 3–8 good references. Keep the URL of every source you use; references are part of the deliverable.

If web search is unavailable, say so in the blueprint and mark the tool/version notes as unverified knowledge.

### 3. Analyze

Compare the approaches against the user's goal and (for features) the existing codebase: effort, fit with the current stack, maintenance burden, risks. Pick a recommendation and say why. A blueprint that lists options without choosing is less useful than one with a clear, reasoned pick.

### 4. Write the blueprint

Write the file to `docs/todo/<name>_blueprint.txt` under the api-pytest project root (create `docs/todo/` if needed). This holds for a new sub-project too (e.g. a CI pipeline or reporting setup): the blueprint lives in this repo's `docs/todo/`. If a blueprint with that name already exists, show the user and ask whether to overwrite it or write a `-v2` file.

It is plain text, so use simple headings, dashes for lists and indentation — no Markdown tables. Keep it high level: a reader should understand the plan in a few minutes. Use this structure:

```
<TITLE IN CAPS> — BLUEPRINT
Date: <YYYY-MM-DD>
Type: New project | New feature in <project name>
Status: Draft for review

1. WHAT TO DO
   Goal: <one or two sentences>
   Scope:
   - <in scope item>
   Out of scope:
   - <item>
   Assumptions:
   - <assumption made because the request didn't say>

2. POSSIBLE APPROACHES
   A. <approach name>
      How it works: <short description>
      Pros: ...
      Cons: ...
   B. <approach name>
      ...
   Recommendation: <A/B/...> — <why it fits best>

3. TOOLS AND TECHNOLOGIES
   - <tool/library> (<version if known>) — <what it's used for>; <why chosen>
   - ...
   Fits the existing stack: <for features: what is reused, what is new>

4. HIGH-LEVEL PLAN
   1) <step>
   2) <step>
   Risks / open questions:
   - <risk or question for the user>

5. REFERENCES
   [1] <title> — <URL>
       <one line on what it contributed>
   [2] ...
```

Sections 1, 2, 3 and 5 are required because the user asked for them. Section 4 is a short bridge from design to work. Cite references by number (e.g. "[2]") where they back a claim in the other sections.

### 5. Hand off

Tell the user where the file is, give a 3–5 line summary (the recommendation and the main tools), and list any open questions. Then offer the next step: run the `evident-research` agent on the blueprint, which verifies its references, confirms or revises the recommendation, and writes the detailed design to `docs/design/<name>_design.txt`. Building starts from that design once the user approves it. Do not start implementing in the same turn: the point of the blueprint is that the user gets to review the direction first.
