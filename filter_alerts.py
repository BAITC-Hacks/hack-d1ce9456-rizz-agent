#!/usr/bin/env python3
"""Print critical events from an NDJSON event stream."""

import json
from pathlib import Path


EVENTS_FILE = Path(__file__).with_name("events.json")


def main() -> None:
    critical_count = 0

    for line in EVENTS_FILE.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event["level"] == "critical":
            print(event["event"])
            critical_count += 1

    print(f"критичных {critical_count}")


if __name__ == "__main__":
    main()
