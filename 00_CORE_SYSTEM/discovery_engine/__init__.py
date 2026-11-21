"""Discovery Engine package for Master AI."""

from .github_discovery import GitHubDiscoveryEngine
from .repo_evaluator import RepositoryEvaluator, EvaluationScorecard
from .repo_catalog import RepositoryCatalogManager
from .capability_gap_engine import CapabilityGapEngine
from .skills_intelligence import SkillsIntelligenceEngine
from .repo_sandbox_tester import RepoSandboxTester
from .integration_workflow import GovernedIntegrationWorkflow, WorkflowState
from .discovery_scheduler import DiscoveryScheduler

__all__ = [
    "GitHubDiscoveryEngine",
    "RepositoryEvaluator",
    "EvaluationScorecard",
    "RepositoryCatalogManager",
    "CapabilityGapEngine",
    "SkillsIntelligenceEngine",
    "RepoSandboxTester",
    "GovernedIntegrationWorkflow",
    "WorkflowState",
    "DiscoveryScheduler",
]
