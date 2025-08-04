# 🧠 MEMORY BANK

A living "working memory" for the project. Only content that is mature and useful enough for conversations with the LLM, decision-making, or idea generation is stored here.

```text
memory_bank/
├── active_memory/        ← loaded via .cursor-rules
│   ├── mindset/          ← current thinking frameworks and mental models
│   ├── portfolio/        ← position and allocation snapshots
│   ├── indicators/       ← aggregated metrics / signal systems
│   ├── trade_journal/    ← short trade logs / P&L
│   ├── prompts/           ← working LLM prompt templates
│   └── index.md          ← manually curated map of active concepts
│
├── tasks/                ← half-baked tasks, ideas, inbox
├── sandbox/              ← drafts, experiments, obsolete versions
└── README.md             ← this file
```

## Principles
1. **active_memory/** — only up-to-date `.md` files with self-contained content; the LLM should understand them without extra context.
2. **tasks/** — the “inbox” for ideas; not yet refined into meaning.
3. **sandbox/** — temporary storage; nothing is deleted recklessly—move legacy items here.
4. Every file must be **self-sufficient**: opened on its own, the idea is clear.

## File Format in active_memory/
- Name: `YYYYMMDD-topic-slug.md` (creation date + short title)
- Start with a front-matter block: `id`, `tags`, `updated`.
- Then the content: concise and structured.

## Workflow
1. Capture an idea/task → **tasks/**.
2. Once refined → copy/move the `.md` into **active_memory/**.
3. Update **index.md** to keep the memory map current.
4. Anything outdated → **sandbox/** (don’t delete; may be useful for retrospectives).

## Why Bother?
✓ Maintains **clarity of thought**: only genuinely important items stay active.  
✓ Enables **experimentation** without clutter (sandbox).  
✓ Gives full **manual control** over what the AI “feeds on”.  
✓ Separates **reflection** (tasks / sandbox) from the **operational knowledge base** (active_memory).

> *I don’t store everything. I store only what I’m ready to read and use again.*