from threading import RLock
from typing import List

from .types import Fact


class SharedMemory:
    """Thread-safe shared working memory for agent facts."""

    def __init__(self):
        self._facts: List[Fact] = []
        self._lock = RLock()

    def add_fact(self, fact: Fact) -> None:
        with self._lock:
            self._facts.append(fact)

    def extend_facts(self, facts: List[Fact]) -> None:
        with self._lock:
            self._facts.extend(facts)

    def get_facts_by_keywords(self, keywords: List[str]) -> List[Fact]:
        lowered_keywords = [keyword.lower() for keyword in keywords]
        with self._lock:
            facts = tuple(self._facts)

        return [
            fact
            for fact in facts
            if any(keyword in fact.content.lower() for keyword in lowered_keywords)
        ]

    def get_all_facts(self) -> List[Fact]:
        with self._lock:
            return list(self._facts)

    def clear(self) -> None:
        with self._lock:
            self._facts.clear()
