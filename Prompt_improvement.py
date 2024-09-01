import streamlit as st
from openai import OpenAI

# OpenAIクライアントの初期化
client = OpenAI(api_key=st.secrets["openai_api_key"])

def improve_prompt(original_prompt):
    system_message = """
    あなたは専門的なプロンプトエンジニアです。与えられたプロンプトを分析し、以下のステップに従って改良してください：

    1. プロンプトの分析:
      - プロンプトの主な目的を特定する
      - 不足している情報や曖昧な部分を指摘する

    2. 構造の改善:
      - 必要に応じて、プロンプトを複数のセクションに分割する
      - 各セクションに明確な見出しをつける（例：背景、タスク、制約条件、期待される出力）

    3. 具体性の追加:
      - 抽象的な指示を具体的なものに置き換える
      - 必要に応じて、例や参照を追加する

    4. 文脈の強化:
      - タスクの背景や重要性を説明する文脈情報を追加する
      - 対象読者や使用目的を明確にする

    5. 出力形式の指定:
      - 期待される回答の形式や構造を詳細に指定する
      - 必要に応じて、出力例を提供する

    6. 制約条件の明確化:
      - タスクに関連する制限事項や条件を明確に述べる
      - 倫理的考慮事項や注意点を含める

    7. インタラクティブ要素の追加:
      - ユーザーに追加情報を求める指示を含める（例：【ここに具体的な例を挿入してください】）

    8. 最終チェック:
      - 改良されたプロンプトが元の意図を保持しているか確認する
      - 簡潔さと詳細さのバランスを取る

    改良したプロンプトを提示する際は、以下の形式で回答してください：

    改良されたプロンプト：
    [ここに改良されたプロンプトを記載]

    改善点の説明：
    1. [主な改善点とその理由を箇条書きで説明]
    2. [...]

    追加のアドバイス：
    - [プロンプトの使用や更なる改善に関するアドバイスを提供]
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"以下のプロンプトを改良してください：\n\n{original_prompt}"}
        ],
        max_tokens=1500,
        temperature=0.7
    )

    return response.choices[0].message.content

st.title("プロンプト改良アプリ")

original_prompt = st.text_area("改良したいプロンプトを入力してください：")

if st.button("プロンプトを改良"):
    if original_prompt:
        improved_prompt = improve_prompt(original_prompt)
        st.write(improved_prompt)
        
        # 改良されたプロンプトのみを抽出
        improved_prompt_only = improved_prompt.split("改良されたプロンプト：")[1].split("改善点の説明：")[0].strip()
        
        # コピー用のテキストエリアを追加
        st.text_area("改良されたプロンプト（コピー用）:", value=improved_prompt_only, height=200)
        
    else:
        st.warning("プロンプトを入力してください。")

st.sidebar.header("使い方")
st.sidebar.write("""
1. 改良したいプロンプトを入力欄に貼り付けます。
2. 「プロンプトを改良」ボタンをクリックします。
3. AIが改良したプロンプトと改善点の説明が表示されます。
4. 改良されたプロンプトは、専用のテキストエリアに表示されます。このテキストを選択してコピーしてください。
5. 必要に応じて、提案された改善点を参考にプロンプトをさらに編集してください。
""")