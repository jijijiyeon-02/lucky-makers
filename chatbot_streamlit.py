
import streamlit as st
import openai

# GPT-4o API 키 입력
import os
from dotenv import load_dotenv
import gpts_prompt

load_dotenv()


# --- OpenAI API KEY ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 배경색만 적용 (예: 연한 민트색)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF6E0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <h1 style='font-size: 2.7rem; text-align: center;'>🍀오늘의 행운, 지금 열어보세요🍀</h1>
""", unsafe_allow_html=True)
# 아래 이미지는 예시입니다. 원하는 이미지 파일명으로 변경하세요.
st.markdown(
    f"""
    <div style='display: flex; justify-content: center;'>
        <img src=\"https://sdmntprcentralus.oaiusercontent.com/files/00000000-422c-61f5-ab78-9d5b454c60ae/raw?se=2025-07-08T08%3A10%3A28Z&sp=r&sv=2024-08-04&sr=b&scid=f6be538d-d1d8-5ec1-af3f-1665486c85fa&skoid=5c72dd08-68ae-4091-b4e1-40ccec0693ae&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-07-07T21%3A49%3A59Z&ske=2025-07-08T21%3A49%3A59Z&sks=b&skv=2024-08-04&sig=5zgNQHE0wzjEr4oOfCeqiMLcWrLYTczT4nKn0zMryh8%3D\" width=\"156\" style=\"margin-bottom: 10px;\"/>
    </div>
    """,
    unsafe_allow_html=True
)

# 세션 상태에 대화 기록 저장
def get_chat_history():
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    return st.session_state["chat_history"]



# 시스템 프롬프트는 대화에만 적용, 화면에는 표시하지 않음
chat_history = get_chat_history()
if not chat_history:
    chat_history.append({"role": "system", "content": gpts_prompt.SYSTEM_PROMPT})

user_input = st.text_input("당신의 운세, 오늘 조심해야할 행동이 궁금하시면 '호잇'을 작성해주세요!", key="user_input")



# 하루에 1개의 답변만 고정으로 제공
import datetime
today_key = f"fortune_{datetime.date.today()}"

if st.button("전송") and user_input:
    if user_input.strip() == "호잇":
        chat_history.append({"role": "user", "content": user_input})
        # 이미 오늘의 답변이 있으면 재사용
        if today_key in st.session_state:
            bot_message = st.session_state[today_key]
        else:
            # GPT-4o API 호출 (openai 1.x 방식)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=chat_history,
                    temperature=0.7,
                    max_tokens=1024,
                )
                bot_message = response.choices[0].message.content.strip()
                st.session_state[today_key] = bot_message
            except Exception as e:
                bot_message = f"오류 발생: {e}"
        chat_history.append({"role": "assistant", "content": bot_message})
    else:
        st.warning("'호잇'이라고 입력해야 답변을 받을 수 있습니다. 다시 입력해주세요.")


# 대화 내용 출력 (system 프롬프트는 화면에 표시하지 않음)
for msg in chat_history:
    if msg["role"] == "system":
        continue
    elif msg["role"] == "user":
        st.markdown(f"**나:** {msg['content']}")
    else:
        # assistant 답변은 마크다운 렌더링, 텍스트 크기도 키움
        st.markdown(
            f"<div style='font-size:1.1rem;'>**GPT-4o:** {msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("Made with Streamlit & GPT-4o API")
