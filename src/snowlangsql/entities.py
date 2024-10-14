from typing import Annotated

from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict


# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
