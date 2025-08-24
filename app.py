import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

def ask_llm(input_text: str, expert_mode: str) -> str:
    """
    入力テキストと専門家モード（"A"または"B"）を受け取り、LLMの回答を返す。
    """
    if not input_text:
        return "入力テキストが空です。内容を入力してください。"

    system_prompts = {
        "A": "あなたはお金に詳しい専門家です。",
        "B": "あなたはプログラミングに詳しい専門家です。"
    }

    if expert_mode not in system_prompts:
        return "無効な専門家モードが選択されました。"

    messages = [
        SystemMessage(content=system_prompts[expert_mode]),
        HumanMessage(content=input_text)
    ]

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
    return llm(messages).content

# =============================
# Streamlit UI
# =============================

st.title("専門家LLM質問アプリ")
st.write(
    """
    入力フォームにテキストを入力し、ラジオボタンで **専門家モード（A/B）** を選択して送信すると、
    選択した専門家としてLLMが回答します。
    """
)
st.write("##### モードA: お金に詳しい専門家")
st.write("##### モードB: プログラミングに詳しい専門家")

mode_options = {
    "お金に詳しい専門家（モードA）": "A",
    "プログラミングに詳しい専門家（モードB）": "B"
}

selected_label = st.radio(
    "動作モードを選択してください。",
    list(mode_options.keys())
)
expert_mode = mode_options[selected_label]

input_label = "お金に関する質問内容を入力してください。" if expert_mode == "A" else "プログラミングに関する質問内容を入力してください。"
input_message = st.text_input(label=input_label)

if st.button("実行"):
    st.divider()
    response = ask_llm(input_message, expert_mode)
    if input_message:
        st.write(response)
    else:
        st.error(f"{input_label}入力してから「実行」ボタンを押してください。")