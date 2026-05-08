import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from oncoagent.core.memory import SharedMemory
from oncoagent.agents import GenomicAgent
from oncoagent.core.types import AgentRole, SubTask


def test_genomic_agent():
    memory = SharedMemory()
    agent = GenomicAgent(AgentRole.GENOMIC, memory)
    task = SubTask("test", AgentRole.GENOMIC, {"mutations": ["EGFR L858R"], "tmb": 5})
    output = agent.process(task)
    assert output.success
    assert len(output.facts) >= 2
    print("GenomicAgent test passed.")


if __name__ == "__main__":
    test_genomic_agent()