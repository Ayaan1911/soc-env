"""
Email Triage Environment Client.
"""

from openenv.core.mcp_client import MCPToolClient


class EmailTriageEnv(MCPToolClient):
    """
    Client for the Email Triage Environment.
    
    Inherits from MCPToolClient to provide tool-calling style interactions:
    - list_tools(): Discover available triage tools
    - call_tool(name, **kwargs): Call a triage tool (triage_email)
    - reset(**kwargs): Reset with a new set of emails
    - step(action): Execute a triage action
    """
    pass
