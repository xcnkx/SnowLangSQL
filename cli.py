import argparse

from langchain_core.messages import HumanMessage
from langchain_openai.chat_models import ChatOpenAI

from snowlangsql import config
from snowlangsql.agent import Agent
from snowlangsql.repository.snowflake import SnowflakeRepository


def query(query: str) -> None:
    snowflake_repository = SnowflakeRepository(
        account=config.SNOWFLAKE_ACCOUNT,
        user=config.SNOWFLAKE_USER,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
    )
    llm = ChatOpenAI(model=config.TOOLS_LLM_MODEL_NAME, temperature=0)
    agent = Agent(llm=llm, repository=snowflake_repository)

    graph = agent.get_graph()

    inputs = {"messages": [HumanMessage(content=query)]}
    for s in graph.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


def main():
    parser = argparse.ArgumentParser(description="CLI for snowlangsql")
    parser.add_argument(
        "--display-graph",
        action="store_true",
        help="Display the workflow graph",
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Execute a NLP query",
    )
    args = parser.parse_args()

    if args.query:
        query(args.query)


if __name__ == "__main__":
    main()
