# Lazy import to avoid module loading during pip install
def get_root_agent():
    from .agent import root_agent
    return root_agent

__all__ = ["get_root_agent"]
