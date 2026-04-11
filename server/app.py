"""
FastAPI application for the Email Triage Environment.
"""

from openenv.core.env_server.http_server import create_app
from openenv.core.env_server.mcp_types import CallToolAction, CallToolObservation

try:
    from .email_triage_environment import EmailTriageEnvironment
except ImportError:
    from server.email_triage_environment import EmailTriageEnvironment

app = create_app(
    EmailTriageEnvironment,
    CallToolAction,
    CallToolObservation,
    env_name="email_triage_env"
)


def main():
    """Entry point for direct execution."""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
