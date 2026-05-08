from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class AgentRole(str, Enum):
    GENOMIC = "genomic"
    TRANSCRIPTOMIC = "transcriptomic"
    RADIOMIC = "radiomic"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    REASONER = "reasoner"
    ORCHESTRATOR = "orchestrator"


@dataclass
class Fact:
    """工作记忆中的一条事实，带证据来源"""
    content: str
    source_agent: AgentRole
    confidence: float  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SubTask:
    """子任务定义"""
    description: str
    target_agent: AgentRole
    input_data: Any
    priority: int = 1


@dataclass
class AgentOutput:
    """Agent输出统一格式"""
    success: bool
    facts: List[Fact]   # 产生的新事实
    error: Optional[str] = None