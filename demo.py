from __future__ import annotations

import argparse
import json
from typing import Iterable

from inboxhero.pipeline import InboxHeroPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="inboxHero demo runner")
    parser.add_argument("--cap", choices=["R1", "R2", "R3", "R4", "R5", "R6", "X1", "X2", "X3", "X4"], help="Run a single capability")
    parser.add_argument("--all", action="store_true", help="Run every capability in the manifest order")
    parser.add_argument("--msg", default=None, help="Optional message id used by grounded drafting checks")
    parser.add_argument("--dry-run", action="store_true", help="Show proposed irreversible actions without executing them")
    parser.add_argument("--approve", action="store_true", help="Approve the proposed send actions and write them to outbox/")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline = InboxHeroPipeline()

    if args.all:
        for capability_id in ["R1", "R2", "R3", "R4", "R5", "R6", "X1", "X2", "X3", "X4"]:
            result = pipeline.run_capability(capability_id, message_id=args.msg, dry_run=args.dry_run, approve=args.approve)
            print(json.dumps(result, indent=2, sort_keys=True))
        return

    if args.cap is None:
        raise SystemExit("Choose either --cap <id> or --all.")

    result = pipeline.run_capability(args.cap, message_id=args.msg, dry_run=args.dry_run, approve=args.approve)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
