from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent

from snowlangsql.repository.snowflake import SnowflakeRepository


class Agent:
    def __init__(self, llm: BaseChatModel, repository: SnowflakeRepository) -> None:
        self.llm = llm
        self.toolkit = SQLDatabaseToolkit(db=repository.get_sqldatabase(), llm=llm)

        search = DuckDuckGoSearchRun()
        self.tools = self.toolkit.get_tools() + [search]

    def get_tools(self) -> list[BaseTool]:
        return self.tools

    def get_toolkit(self) -> SQLDatabaseToolkit:
        return self.toolkit

    @property
    def sql_prefix(self) -> str:
        return """
You are an agent designed to interact with a SQL database on Snowflake warehouse.
Given an input question, create a syntactically correct SQL query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
If the user does not specify the period of the query, always set the query range to the past 3 days.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

To start you should ALWAYS look at the tables in the database to see what you can query.
Do NOT skip this step.
Then you should query the schema of the most relevant tables.
"""  # noqa: E501

    @property
    def system_message(self) -> SystemMessage:
        return SystemMessage(content=self.sql_prefix)

    def get_graph(self) -> CompiledGraph:
        return create_react_agent(model=self.llm, tools=self.tools, messages_modifier=self.system_message)
