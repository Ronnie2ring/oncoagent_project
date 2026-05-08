import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from oncoagent.agents import GenomicAgent
from oncoagent.core.memory import SharedMemory
from oncoagent.core.orchestrator import Orchestrator
from oncoagent.core.types import AgentRole, SubTask


def patient_data():
    return {
        "genomic": {"mutations": ["EGFR L858R", "STK11 loss"], "tmb": 12},
        "transcriptomic": {
            "tgf_beta_enriched": True,
            "treg_high": True,
            "cd8_low": True,
        },
        "radiomic": {"fibrosis": 65, "pd_l1_pattern": "stromal"},
        "kg_query": "EGFR L858R, STK11, TGF-beta",
    }


def test_genomic_agent_writes_facts_to_memory():
    memory = SharedMemory()
    agent = GenomicAgent(AgentRole.GENOMIC, memory)
    task = SubTask("test", AgentRole.GENOMIC, {"mutations": ["EGFR L858R"], "tmb": 5})

    output = agent.process(task)

    assert output.success
    assert len(output.facts) >= 2
    assert len(memory.get_all_facts()) == len(output.facts)


def test_orchestrator_runs_end_to_end():
    memory = SharedMemory()
    orchestrator = Orchestrator(memory, verbose=False, retain_memory=True)

    result = orchestrator.run("Will anti-PD-1 work?", patient_data())

    assert result["consensus_reached"]
    assert result["confidence"] > 0
    assert result["recommendations"]
    assert len(memory.get_all_facts()) >= 8


def test_orchestrator_isolates_request_memory_by_default():
    memory = SharedMemory()
    orchestrator = Orchestrator(memory, verbose=False)

    orchestrator.run("Will anti-PD-1 work?", patient_data())
    orchestrator.run("Will anti-PD-1 work?", patient_data())

    assert memory.get_all_facts() == []


def test_orchestrator_handles_concurrent_requests():
    def run_one(_):
        memory = SharedMemory()
        orchestrator = Orchestrator(memory, verbose=False)
        result = orchestrator.run("Will anti-PD-1 work?", patient_data())
        return result["consensus_reached"], len(result["recommendations"])

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(run_one, range(16)))

    assert all(consensus for consensus, _ in results)
    assert all(recommendation_count > 0 for _, recommendation_count in results)
