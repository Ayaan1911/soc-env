"""
Data models for the Email Triage Environment.
"""

from typing import Any, Dict, List, Optional
from pydantic import Field

try:
    from openenv.core.env_server.types import Action, Observation
except ImportError:
    from openenv.core.env_server.types import Action, Observation


class EmailTriageAction(Action):
    """Action for the Email Triage environment."""
    
    classification: str = Field(..., description="Classification: SPAM, HAM, or PHISHING")
    action: str = Field(..., description="Action: DELETE, KEEP, REPORT, or ESCALATE")
    reasoning: str = Field(..., description="Reasoning behind the classification and action")


class EmailTriageObservation(Observation):
    """Observation from the Email Triage environment."""
    
    email_id: str = Field(..., description="Unique identifier for the email")
    subject: str = Field(..., description="Subject line of the email")
    sender: str = Field(..., description="Sender's email address")
    body: str = Field(..., description="Content of the email")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional email metadata")
    step: int = Field(..., description="Current email index (1-based)")
    total_steps: int = Field(..., description="Total emails in the task")
    task_id: str = Field(..., description="ID of the current task")
    last_action_result: str = Field(default="", description="Result of the last action")
    progress: float = Field(default=0.0, ge=0.0, le=1.0, description="Task progress (0.0-1.0)")
