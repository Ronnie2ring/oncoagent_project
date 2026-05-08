from abc import ABC, abstractmethod
from .types import AgentRole, SubTask, AgentOutput, Fact
from .memory import SharedMemory


class BaseAgent(ABC):
    def __init__(self, role: AgentRole, memory: SharedMemory):
        self.role = role
        self.memory = memory

    @abstractmethod
    def process(self, task: SubTask) -> AgentOutput:
        pass

    def _add_fact(self, content: str, confidence: float, **metadata) -> Fact:
        fact = Fact(content=content, source_agent=self.role, confidence=confidence, metadata=metadata)
        self.memory.add_fact(fact)
        return fact