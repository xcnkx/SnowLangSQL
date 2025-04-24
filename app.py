import streamlit as st
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI

from snowlangsql import config
from snowlangsql.agent import Agent
from snowlangsql.repository.snowflake import SnowflakeRepository
from snowlangsql.st_callable_util import get_streamlit_cb


def run_graph(messages: list[AnyMessage], config_params: dict) -> str:
    try:
        snowflake_repository = SnowflakeRepository(
            account=config_params["SNOWFLAKE_ACCOUNT"],
            user=config_params["SNOWFLAKE_USER"],
            warehouse=config_params["SNOWFLAKE_WAREHOUSE"],
            database=config_params["SNOWFLAKE_DATABASE"],
            schema=config_params["SNOWFLAKE_SCHEMA"],
            role=config_params.get("SNOWFLAKE_ROLE"),
            private_key_path=config_params.get("SNOWFLAKE_PRIVATE_KEY_PATH"),
            private_key_passphrase=config_params.get("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE"),
        )
        llm = ChatOpenAI(model=config_params["TOOLS_LLM_MODEL_NAME"], temperature=0, streaming=True)
        agent = Agent(llm=llm, repository=snowflake_repository)

        graph = agent.get_graph()

        inputs = {"messages": messages}
        response = ""
        for s in graph.stream(input=inputs, stream_mode="values", config={"callbacks": [get_streamlit_cb(st.empty())]}):
            response = s["messages"][-1].content
        return response
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return ""


def main():
    st.title("❄️️ Snowflake Natural Language Query with History Chat 🤖️")
    st.write(
        "このアプリでは、自然言語を使用してSnowflakeデータベースにクエリを実行できます。対話履歴もサポートしています。"
    )

    # サイドバーでの設定入力
    st.sidebar.title("設定")
    SNOWFLAKE_ACCOUNT = config.SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER = config.SNOWFLAKE_USER
    SNOWFLAKE_WAREHOUSE = st.sidebar.text_input("Snowflakeウェアハウス", value=config.SNOWFLAKE_WAREHOUSE)
    SNOWFLAKE_DATABASE = st.sidebar.text_input("Snowflakeデータベース", value=config.SNOWFLAKE_DATABASE)
    SNOWFLAKE_SCHEMA = st.sidebar.text_input("Snowflakeスキーマ", value=config.SNOWFLAKE_SCHEMA)
    TOOLS_LLM_MODEL_NAME = st.sidebar.selectbox("Chat OpenAIモデル", ("gpt-4o", "gpt-4o-mini", "gpt-4.1"), index=0)

    # 区切り線を追加
    st.sidebar.markdown("---")

    # リセットボタン
    if st.sidebar.button("メッセージをリセット", type="primary"):
        st.session_state["messages"] = [AIMessage(content="ご用件をお聞かせください。")]

    # 設定パラメータを辞書にまとめる
    config_params = {
        "SNOWFLAKE_ACCOUNT": SNOWFLAKE_ACCOUNT,
        "SNOWFLAKE_USER": SNOWFLAKE_USER,
        "SNOWFLAKE_WAREHOUSE": SNOWFLAKE_WAREHOUSE,
        "SNOWFLAKE_DATABASE": SNOWFLAKE_DATABASE,
        "SNOWFLAKE_SCHEMA": SNOWFLAKE_SCHEMA,
        "SNOWFLAKE_ROLE": config.SNOWFLAKE_ROLE,
        "TOOLS_LLM_MODEL_NAME": TOOLS_LLM_MODEL_NAME,
    }

    # 必須の設定が全て入力されているか確認
    if all(config_params.values()):
        # Snowflakeへの接続情報を追加
        config_params.update({
            "SNOWFLAKE_PRIVATE_KEY_PATH": config.SNOWFLAKE_PRIVATE_KEY_PATH,
            "SNOWFLAKE_PRIVATE_KEY_PASSPHRASE": config.SNOWFLAKE_PRIVATE_KEY_PASSPHRASE,
        })

        # メッセージのセッション状態を初期化
        if "messages" not in st.session_state:
            st.session_state["messages"] = [AIMessage(content="ご用件をお聞かせください。")]

        # 過去のメッセージを表示
        for msg in st.session_state.messages:
            if isinstance(msg, AIMessage):
                st.chat_message("assistant").write(msg.content)
            if isinstance(msg, HumanMessage):
                st.chat_message("user").write(msg.content)

        # ユーザーからの入力
        if prompt := st.chat_input():
            # ユーザーメッセージを履歴に追加
            st.session_state["messages"].append(HumanMessage(content=prompt))
            st.chat_message("user").write(prompt)

            # クエリの処理
            with st.chat_message("assistant"):
                response = run_graph(st.session_state["messages"], config_params)
                st.write(response)
                # アシスタントのレスポンスを履歴に追加
                st.session_state["messages"].append(AIMessage(content=response))
    else:
        st.sidebar.error("全ての設定項目を入力してください。")


if __name__ == "__main__":
    main()
