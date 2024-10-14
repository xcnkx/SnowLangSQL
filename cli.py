import argparse

from langchain_core.runnables.graph import MermaidDrawMethod

from snowlangsql.workflow import build_workflow


def display_graph():
    workflow = build_workflow()
    img_data = workflow.get_graph().draw_mermaid_png(
        draw_method=MermaidDrawMethod.API,
    )
    with open("imgs/workflow_graph.png", "wb") as f:
        f.write(img_data)
    print("画像が 'workflow_graph.png' に保存されました。")


def query(query: str):
    workflow = build_workflow()
    messages = workflow.invoke(
        {
            "messages": [
                ("user", query),
            ]
        }
    )

    result = messages["messages"][-1].tool_calls[0]["args"]["final_answer"]
    return result


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

    if args.display_graph:
        display_graph()
    elif args.query:
        result = query(args.query)
        print(result)


if __name__ == "__main__":
    main()
