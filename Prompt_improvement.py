import streamlit as st
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI(api_key=st.secrets["openai_api_key"])

def improve_prompt(original_prompt):
    system_message = """
    あなたは優秀なプロンプトライターです。与えられたプロンプトを以下の"良いプロンプト"の特徴に沿って改良してください：

    1. 明確で具体的な指示
    2. 必要な情報やコンテキストの提供
    3. タスクの目的や期待される結果の明示
    4. 適切な長さと詳細さ
    5. 適切な言葉遣いとトーン

    改良する際は、完全な文言だけでなく、例えば【ここに具体的な例を挿入してください】のように、ユーザーに修正を促す箇所も含めてください。
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"以下のプロンプトを改良してください：\n\n{original_prompt}"}
        ],
        max_tokens=1000,
        temperature=0.5
    )

    return response.choices[0].message.content

# アプリケーションのUI部分は変更なし
st.title("プロンプト改良アプリ")

original_prompt = st.text_area("改良したいプロンプトを入力してください：")

if st.button("プロンプトを改良"):
    if original_prompt:
        improved_prompt = improve_prompt(original_prompt)
        st.subheader("改良されたプロンプト：")
        st.write(improved_prompt)
    else:
        st.warning("プロンプトを入力してください。")

st.sidebar.header("使い方")
st.sidebar.write("""
1. 改良したいプロンプトを入力欄に貼り付けます。
2. 「プロンプトを改良」ボタンをクリックします。
3. AIが改良したプロンプトが表示されます。
4. 必要に応じて、提案された修正箇所を編集してください。
""")