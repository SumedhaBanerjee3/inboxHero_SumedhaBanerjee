# CAPABILITIES.md

**Student:** Suemdha Banerjee, evernorth-aai-817080
**Repository:** https://github.com/SumedhaBanerjee3/inboxHero_SumedhaBanerjee.git

Run everything through one entry point:

```bash
python demo.py --cap R1
python demo.py --all
```

---

## The system, in one paragraph

This project is a local Python inbox triage system that treats email as untrusted content, routes obvious noise through deterministic rules, and only escalates ambiguous or sensitive messages into a guarded model-backed path. It keeps every decision auditable through `trace.jsonl`, persists user preferences to disk, and requires explicit approval before any irreversible send or delete action is written to the outbox. The design is intentionally minimal: a rule router, a model fallback, a preference store, and a CLI that exposes every capability as a single command.

## Design choices you were asked to state

- **Framework:** none. The task is a bounded workflow rather than a multi-agent system. A rule path, a model path, a preference store, and a guardrail layer are sufficient and easier to inspect and audit.
- **Retrieval:** thread-walk. The inbox already contains `thread_id`, so the system reads earlier messages from the same thread before drafting a grounded reply. This is cheaper and more precise than embeddings for the provided mock data.
- **Reversible vs irreversible:** `send` and `delete` are irreversible; `draft`, `label`, `archive`, and `defer` are reversible. The project keeps irreversible actions behind the approval gate because there is no undo stage and no trash model in the mock mailbox.
- **Where the gate sits:** the irreversible action path is centralized behind one approval gate before anything reaches `outbox/`. A dry-run shows what would happen without writing files, and an explicit `--approve` is required for actual outbound output.
- **Escalation line:** the system escalates to a human before sending externally or acting on money or legal risk. Routine internal handling, defers, and noise cleanup remain automatic. The trade-off is that a few borderline cases are held back for approval, but the system avoids silent, high-risk actions.

## Capabilities

| id | name | tier | one-line claim |
|----|------|------|----------------|
| R1 | Zero the inbox | C | Every message gets exactly one disposition and a recorded reason, with no message left undecided |
| R2 | Grounded reply | B | Drafts a reply backed by a specific earlier message from the thread |
| R3 | Gate the irreversible | C | Prevents send/delete without approval or explicit dry-run |
| R4 | Persistent preference | C | Stores a preference on disk and applies it in a later run |
| R5 | Refuse embedded instructions | C | Detects hostile instructions, logs the refusal, and leaves the email in place |
| R6 | Dashboard | C | Produces a three-pane dashboard grounded in the run and surfaced conflicts |
| X1 | Follow-up tracking | B | Finds unanswered sent mail and drafts a chase |
| X2 | Morning digest | B | Groups tasks into needs-you, can-wait, and auto-archived |
| X3 | Unread-by-sender summary | A | Lists unread mail by sender in one quick, inspectable output |
| X4 | Structured deadline extraction | A | Extracts deadlines and ownership into a structured list |

The machine-readable manifest in `capabilities.json` mirrors the same list and is the format the grader script reads. This file is the human-readable version and explains the design trade-offs behind the system.

## Final Report

This project intentionally draws a clear line around what it automates. It refuses hostile instructions embedded in message bodies, it does not allow irreversible actions without approval, and it keeps the action layer separate from the untrusted email content. In practice, the system can confidently handle noise, grounded drafts, persistent preferences, and dashboard reporting while forcing human review before anything external or risky is sent.

The design trades a little conservatism for safety: routine internal archives and defers run automatically, but anything that touches money, legal risk, or external sending is gated. The project stays explainable because each run logs the decision, the cited evidence, and the approval outcome in `trace.jsonl`, so a wrong send can be traced back to the exact message id and decision point.
