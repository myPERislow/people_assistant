import os
import streamlit as st
from streamlit_chat import message
import openai
from os.path import join, dirname
from dotenv import load_dotenv

# APIキーの設定
load_dotenv(join(dirname(__file__), '.env'))
# load_dotenv: .envファイルを読み込み、その中の環境変数をロードする
# join: パスを結合する
# dirname(__file__): このファイルの絶対パスを取得
# 現在のスクリプトと同じディレクトリにある.envファイルを探し、そのファイルの中にある環境変数をロードする
# これにより、スクリプト内でos.getenv('MY_VARIABLE')のようなコードを使用して、.envファイルに定義された環境変数を取得することができる

openai.api_key = os.getenv("OPENAI_API_KEY")

# 「送信」ボタンがクリックされた場合に、OpenAIに問い合わせる
def do_question():
    condition = st.session_state.condition_input.strip()
    if condition and condition != st.session_state.condition:
        st.session_state.condition = condition
        st.session_state.messages.append({"role": "system", "content": condition}})
    
    question = st.session_state.question_input.strip()
    # Streamlitのセッション状態からquestion_inputを取得し、その値を変数questionに格納する
    # strip(): 文字列の先頭と末尾の空白文字を削除する
    if question:
        # メッセージに質問を追加
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.question_input = ""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        # OpenAIのAPIを使って、GPT-3.5-turboモデルを使ったチャットセッションを作成し、その結果をresponseという変数に格納する
        # openai.ChatCompletion.create: OpenAIのAPIを呼び出す
        # messages: モデルに投げるメッセージのリストを指定する
        )

        message = response.choices[0]["message"]
        # OpenAIのAPIの結果から、回答を取得し、answerという変数に格納する
        # choicesはOpenAIのAPIレスポンスの1部で、モデルが生成した可能性のある回答をリストとして格納
        # 殆どのケースでは、choicesリストには1つの要素しか含まれていないので、[0]を使ってリストの最初の要素を取得
        # choicesリストの各回答は辞書形式で2つのキー"role"と"message"が含まれている
        st.session_state.messages.append(message)
        # 回答をQAに追加


def main():
    # セッションステートにmessagesリストを初期化する
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.condition = ""

    # タイトル
    st.title("Chatbot")
    # テキストボックスに役割を入力
    st.text_input("役割を入力してください", key="condition_input")
    # テキストボックスで質問を入力
    st.text_input("質問を入力してください", key="question_input")
    # 入力ボックスの値は、st.session_state.question_inputというキーに格納される
    # 送信ボタンがクリックするとOpenAIに問い合わせる
    st.button("送信", on_click=do_question)
    # ユーザーがボタンをクリックすると、do_question()関数が実行される

    # リストをループして、質問と回答を表示
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        # 右側に表示する回答はisUserをTrueとする
        message((msg["content"]), is_user=msg["role"] == "assistant")

if __name__ == "__main__":
    main()
# スクリプトが直接実行された場合にのみ、main()関数を実行する