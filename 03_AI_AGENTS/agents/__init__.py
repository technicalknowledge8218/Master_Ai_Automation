# 03_AI_AGENTS/agents package
from .base_agent import BaseSpecialistAgent
from .research_agent import ResearchAgent
from .software_architect import SoftwareArchitect
from .coding_agent import CodingAgent
from .testing_agent import TestingAgent
from .documentation_agent import DocumentationAgent
from .security_auditor import SecurityAuditor
from .capability_discovery_agent import CapabilityDiscoveryAgent

AGENT_REGISTRY_MAP = {
    "AGT-001": ResearchAgent,
    "AGT-002": SoftwareArchitect,
    "AGT-003": CodingAgent,
    "AGT-004": TestingAgent,
    "AGT-005": DocumentationAgent,
    "AGT-006": SecurityAuditor,
    "AGT-007": CapabilityDiscoveryAgent
}
