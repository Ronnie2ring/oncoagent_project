from typing import List
from .types import Fact


class SharedMemory:
    """共享工作记忆池（向量存储简化版）"""
    def __init__(self):
        self.facts: List[Fact] = []

    def add_fact(self, fact: Fact):
        self.facts.append(fact)

    def get_facts_by_keywords(self, keywords: List[str]) -> List[Fact]:
        """简单关键词匹配检索"""
        results = []
        for fact in self.facts:
            text = fact.content.lower()
            if any(kw.lower() in text for kw in keywords):
                results.append(fact)
        return results

    def get_all_facts(self) -> List[Fact]:
        return self.facts

    def clear(self):
        self.facts = []