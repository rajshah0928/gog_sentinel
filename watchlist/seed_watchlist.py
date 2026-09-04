"""
Populates a small representative watchlist for demonstration purposes, as
explicitly permitted by the hackathon rules ("participants may use their
own representative watchlist database"). Edit WATCHLIST_ENTRIES to include
a plate you can actually get in front of a camera for the live trace test.
"""
from watchlist.db import init_db, add_watchlist_entry

WATCHLIST_ENTRIES = [
    ("GJ05AB1234", "Reported stolen - FIR 2026/0341", "stolen"),
    ("GJ01CD5678", "Wanted - outstanding warrant", "wanted"),
    ("GJ18EF9012", "Suspect vehicle - robbery case", "suspect"),
    ("MH12GH3456", "Flagged - interstate stolen vehicle alert", "stolen"),
]


def seed():
    init_db()
    for plate, reason, category in WATCHLIST_ENTRIES:
        add_watchlist_entry(plate, reason, category)
        print(f"Added {plate} ({category}): {reason}")


if __name__ == "__main__":
    seed()
