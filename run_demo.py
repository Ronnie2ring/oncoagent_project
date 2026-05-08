#!/usr/bin/env python3
"""OncoAgent demo entry point."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from oncoagent.core.memory import SharedMemory
from oncoagent.core.orchestrator import Orchestrator


def demo_patient():
    """Return sample data for an advanced NSCLC patient."""
    return {
        "genomic": {
            "mutations": ["KRAS G12C", "STK11 loss"],
            "tmb": 18,
        },
        "transcriptomic": {
            "tgf_beta_enriched": True,
            "treg_high": True,
            "cd8_low": True,
        },
        "radiomic": {
            "fibrosis": 60,
            "pd_l1_pattern": "stromal",
        },
        "kg_query": "KRAS G12C, STK11, TGF-beta",
    }


if __name__ == "__main__":
    memory = SharedMemory()
    orchestrator = Orchestrator(memory)

    query = "Should this advanced NSCLC patient respond to anti-PD-1 monotherapy?"
    result = orchestrator.run(query, demo_patient())

    print("\nDemo completed.")
    print(f"Consensus reached: {result['consensus_reached']}")
