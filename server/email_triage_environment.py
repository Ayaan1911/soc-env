"""
Email Triage Environment Implementation.
"""

import json
import os
from typing import Any, Dict, List, Optional
from uuid import uuid4
from collections import defaultdict

try:
    from openenv.core.env_server.mcp_environment import MCPEnvironment
    from openenv.core.env_server.types import Action, Observation, State
except ImportError:
    from openenv.core.env_server.mcp_environment import MCPEnvironment
    from openenv.core.env_server.types import Action, Observation, State

from fastmcp import FastMCP

try:
    from .tasks import TASKS, TaskDefinition, grade_triage
except ImportError:
    from server.tasks import TASKS, TaskDefinition, grade_triage


class EmailTriageEnvironment(MCPEnvironment):
    """
    An environment where agents triage emails.
    """

    def __init__(self):
        """Initialize with MCP server and triage tools."""
        mcp = FastMCP("email_triage_env")
        self._task: Optional[TaskDefinition] = None
        self._current_email_index: int = 0
        self._last_result: str = ""
        self._cumulative_score: float = 0.0
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._done = False

        @mcp.tool
        def triage_email(classification: str, action: str, reasoning: str) -> str:
            """
            Triage the current email.
            classification: SPAM, HAM, or PHISHING
            action: DELETE, KEEP, REPORT, or ESCALATE
            reasoning: Brief explanation of the decision
            """
            return self._exec_triage_email(classification, action, reasoning)

        super().__init__(mcp)

    def _exec_triage_email(self, classification: str, action: str, reasoning: str) -> str:
        if self._task is None:
            return "Error: No task loaded. Call reset() first."
        
        if self._current_email_index >= len(self._task.emails):
            return "Error: All emails in this task have been triaged."

        current_email = self._task.emails[self._current_email_index]
        score = grade_triage(
            {"classification": classification, "action": action},
            current_email
        )
        
        self._cumulative_score += score
        self._current_email_index += 1
        
        self._last_result = (
            f"Successfully triaged email {current_email.email_id}. "
            f"Score for this step: {score:.2f}. "
            f"Reasoning provided: {reasoning}"
        )
        
        if self._current_email_index >= len(self._task.emails):
            self._done = True
            
        return self._last_result

    def _get_observation_dict(self) -> Dict[str, Any]:
        """Build observation for the current state."""
        if self._task is None or self._current_email_index >= len(self._task.emails):
            return {
                "email_id": "N/A",
                "subject": "N/A",
                "sender": "N/A",
                "body": "N/A",
                "metadata": {},
                "step": self._current_email_index,
                "total_steps": len(self._task.emails) if self._task else 0,
                "task_id": self._task.id if self._task else "",
                "last_action_result": self._last_result,
                "progress": self._cumulative_score / len(self._task.emails) if self._task and self._task.emails else 0.0,
            }

        email = self._task.emails[self._current_email_index]
        return {
            "email_id": email.email_id,
            "subject": email.subject,
            "sender": email.sender,
            "body": email.body,
            "metadata": email.metadata,
            "step": self._current_email_index + 1,
            "total_steps": len(self._task.emails),
            "task_id": self._task.id,
            "last_action_result": self._last_result,
            "progress": self._cumulative_score / len(self._task.emails),
        }

    def _step_impl(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Handle non-MCP actions (returns error — use MCP tools instead)."""
        return Observation(
            done=False,
            reward=0.0,
            metadata={
                "error": f"Unknown action type: {type(action).__name__}. "
                "Use MCP tools (triage_email)",
            },
        )

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Observation:
        """Reset environment with a specific task."""
        task_id = kwargs.get("task", "task1")
        if task_id not in TASKS:
            task_id = "task1"
            
        self._task = TASKS[task_id]
        self._current_email_index = 0
        self._cumulative_score = 0.0
        self._last_result = "Environment reset. Ready to triage emails."
        self._done = False
        self._state = State(
            episode_id=episode_id or str(uuid4()),
            step_count=0,
        )
        
        obs_data = self._get_observation_dict()
        return Observation(
            done=False,
            reward=0.0,
            metadata=obs_data
        )

    def step(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Execute a step, tracking reward delta."""
        self._state.step_count += 1
        prev_score = self._cumulative_score
        
        # Dispatch to MCP tools via base class
        obs = super().step(action, timeout_s=timeout_s, **kwargs)
        
        # Compute reward as delta in cumulative score
        reward = self._cumulative_score - prev_score
        
        obs.reward = round(reward, 4)
        obs.done = self._done
        if obs.metadata is None:
            obs.metadata = {}
        obs.metadata.update(self._get_observation_dict())
        
        return obs

    async def step_async(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Async version for WebSocket compatibility."""
        self._state.step_count += 1
        prev_score = self._cumulative_score
        
        obs = await super().step_async(action, timeout_s=timeout_s, **kwargs)
        
        reward = self._cumulative_score - prev_score
        
        obs.reward = round(reward, 4)
        obs.done = self._done
        if obs.metadata is None:
            obs.metadata = {}
        obs.metadata.update(self._get_observation_dict())
        
        return obs

    @property
    def state(self) -> State:
        return self._state
