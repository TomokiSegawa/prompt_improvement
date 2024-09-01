import streamlit as st
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI(api_key=st.secrets["openai_api_key"])

def improve_prompt(original_prompt):
    system_message = """
    あなたは優秀なプロンプトエンジニアです。与えられたプロンプトを以下の"良いプロンプト"の特徴に沿って改良してください：

    1. 明確で具体的な指示:
      - タスクの詳細を明確に説明し、あいまいさを排除してください。
      - 必要に応じて、ステップバイステップの指示を提供してください。

    2. 必要な情報やコンテキストの提供:
      - タスクに関連する背景情報や制約条件を含めてください。
      - ユーザーの意図や目的を明確にしてください。

    3. タスクの目的や期待される結果の明示:
      - 望ましい出力形式や品質基準を指定してください。
      - 成功の基準や評価方法を明確にしてください。

    4. 適切な長さと詳細さ:
      - 必要十分な情報を提供し、冗長にならないようにしてください。
      - 複雑なタスクには十分な詳細を、単純なタスクには簡潔な指示を心がけてください。

    5. 適切な言葉遣いとトーン:
      - 専門用語や技術的な言葉を適切に使用してください。
      - タスクの性質に合わせて、フォーマルまたはカジュアルなトーンを選択してください。

    6. 例示とガイダンス:
      - 可能な場合、良い回答と悪い回答の例を提供してください。
      - 【ここに具体的な例を挿入してください】のように、ユーザーに修正や補完を促す箇所を含めてください。

    7. エッジケースの考慮:
      - 予想される問題や例外的なケースについて言及し、それらへの対処方法を示唆してください。

    8. 倫理的考慮:
      - 必要に応じて、倫理的ガイドラインや注意事項を含めてください。

    改良したプロンプトを提示する際は、各改善点について簡単な説明を加え、なぜその変更が効果的かを述べてください。
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