# inboxHero

Public repository: https://github.com/SumedhaBanerjee3/inboxHero_SumedhaBanerjee.git

## Architecture

This project is a single-entry-point Python pipeline for a local mock inbox. It reads messages from `inbox.json`, routes rule-based noise through a deterministic router, and leaves higher-risk or ambiguous messages to a model-backed decision path. The system records decisions to `trace.jsonl`, stores persistent preferences in `prefs.json`, and writes outbound messages to `outbox/` only when the gate allows it.

## LLM vs non-LLM flow

### Non-LLM / deterministic work
These steps do not call the Gemini API and are handled by rules and local code:
noisy mail detection (receipts, newsletters, notifications, alerts),
message classification into rule vs model path,
preference persistence and retrieval,
irreversible-action gate checks,
outbox write logic and logging,
dashboard generation and digest aggregation from stored run data.

### LLM-backed work
These parts call Gemini only when a real `GEMINI_API_KEY` is present in `.env` and the message is routed into the model path:
ambiguous reply decisions,grounded drafting based on earlier thread content,
risk-aware classification for legal, approval, or sensitive correspondence,
higher-level reasoning for the agentic capability outputs that require judgment rather than deterministic structure.

When no valid key is configured, the project falls back to deterministic local logic with a safe, auditable response. The boundary is explicit: if a message can be decided safely through pattern matching, it never reaches the model.

## Framework choice

The project uses no external framework. The task is fundamentally a routing and guardrail problem, not a graph of agents. A linear pipeline is sufficient because the system mostly has a rule path, a model path, and a human gate. This keeps the architecture explainable and safer than a heavier multi-agent setup.

## Disposition vocabulary and gate

The disposition vocabulary used in the implementation is: `reply`, `archive`, `defer`, `delegate`, and `escalate`. The irreversible actions are `send` and `delete`. Drafting, labeling, archiving, and deferring are treated as reversible because they can be undone or revised. The approval gate is enforced before any irreversible action is taken; dry-run mode shows the proposed action without executing it, and an explicit `--approve` flag writes the approved sends to `outbox/` as one file per message.

### Part 4: outbox requirement

The project now follows the assignment requirement that outbound sends are written to `outbox/`, one file per message, and nowhere else. When a send is proposed:

 `python demo.py --cap R3 --dry-run` shows the target message and the action without writing any file;
`python demo.py --cap R3 --approve` writes the approved send to `outbox/<message_id>.eml` and logs the approval in `trace.jsonl`;
if approval is not granted, the system keeps the message in the decision layer and writes nothing anywhere else.

This preserves the assignment’s safety boundary while satisfying the required outbox contract.

## Retrieval strategy

The retrieval strategy is a thread-walk. The inbox already carries `thread_id`, and the path of most value is to read the earlier messages in the same thread before drafting a grounded reply. This is cheaper and more reliable than embeddings for the assignment data.

## Personalization and persistence (Part 5)

The project records a preference in a JSON file and re-reads it on a later run after a full process restart. The demonstrated preference is: `m015` is a Legal email, and the system honours a rule to CC the co-founder on Legal mail. That preference is stored in `prefs.json` and then applied on a later run, proving that memory survives across restarts.

## Hostile inbox protection (Part 6)

The system treats inbound email as untrusted text. It refuses embedded instructions such as attempts to forward the inbox, delete a message, or trigger a silent action. Refusals are logged with the message id and the attempted action, and the email is left in place without any outbox output or deletion.

## Dashboard and commitments (Part 7)

The dashboard is generated from a completed run and is reproducible rather than hand-built. Running `python demo.py --cap R6` writes:
- `dashboard.json`: machine-readable data with exactly three panes: `pending`, `flagged`, and `commitments`.
- `dashboard.html`: a rendered three-pane view for easy inspection in a browser or terminal preview.

Each commitment cites the message ids it came from, and any same-day overlap is surfaced as a conflict inside the commitments pane. The generated data is derived from the actual inbox content so it can be recreated on every run without manual editing.

## Product capabilities (Part 8)

The system includes required capabilities R1 through R6 and adds the extra capabilities X1 and X2. These are designed to be runnable individually via a single command and produce a visible result someone else can judge.

## Manifest and pitch (Part 9)

The project follows the expected manifest pattern in `CAPABILITIES.md` and `capabilities.json`, using the same fields and structure expected by the grader. The human-readable file explains the design trade-offs, while the JSON file stores the short machine-readable facts expected by the marking script.



## Running the project

1. Create a local environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```
2. Create your local environment file from the sample:
   ```bash
   copy .env.example .env
   ```
   Then edit `.env` and replace `YOUR_GEMINI_API_KEY_HERE` with your actual Gemini API key.
3. Run a single capability:
   ```bash
   python demo.py --cap R1
   ```
4. Run all capabilities in the required order:
   ```bash
   python demo.py --all
   ```
5. Run a grounded reply check for a specific message:
   ```bash
   python demo.py --cap R2 --msg m008
   ```
6. Check the irreversible action gate in dry-run mode:
   ```bash
   python demo.py --cap R3 --dry-run
   python demo.py --cap R3 --approve
   ```
7. Demonstrate a persistent preference (Part 5):
   ```bash
   python demo.py --cap R4
   ```
8. Demonstrate hostile-inbox refusal (Part 6):
   ```bash
   python demo.py --cap R5
   ```
9. Generate the three-pane dashboard (Part 7):
   ```bash
   python demo.py --cap R6
   ```
   This creates both `dashboard.json` and `dashboard.html` from the current inbox run.
10. Run the extra capabilities (Part 8):
   ```bash
   python demo.py --cap X1
   python demo.py --cap X2
   python demo.py --cap X3
   python demo.py --cap X4
   ```

## Final Report

1. What did you refuse to automate? 
Answer: The system refuses to act on hostile instructions embedded inside email content. For example, a message that attempts to forward the inbox or trigger a silent delete is left in place and logged as refused, because the system treats email text as untrusted data and does not allow irreversible actions without a gate.

2. Where does untrusted text enter your system?
Answer:  Untrusted email content enters at the mailbox read boundary and is routed through the decision pipeline without being treated as executable instruction. The attacker would have to defeat the router, the human approval gate, and the separation between message content and the action layer to make the system act on their behalf.

3. Who is accountable when it sends the wrong thing? 
Answer: The system records the exact message id, the route used, the proposed action, and the approval outcome in `trace.jsonl`, so the action can be traced back to the authoring step and to the human approval decision. This gives an audit trail for wrong wording, bad facts, or wrong recipients.

4. Name your own machinery. 
Answer: The code exposes the roles of a framework via a simple router, a persistent preference store, a pipeline orchestrator, and a guarded outbox writer. A framework would offer concurrency, orchestration libraries, and more elaborate tool-call plumbing, but for this assignment the built-in components keep the architecture clearer and safer than a heavyweight multi-agent setup.


What to verify:
- the CLI exits cleanly with no syntax errors,
- the capability output is JSON-serializable,
- each run writes or updates the expected artifacts (`trace.jsonl`, `prefs.json`, `dashboard.json`, and/or the `outbox` directory),
- the dry-run gate does not create real outbound messages,
- hostile instructions are refused and remain in place,
- the preference survives a restart and changes later behavior,
- the environment stays free of secrets by using `.env` locally and keeping `.env.example` as the safe template.

## Notes

- The project uses a placeholder Gemini API key in the config files for compatibility with the required LLM integration.
- Do not commit `.env` to source control; keep `.env.example` as the public template.
