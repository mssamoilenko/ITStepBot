# Завдання 2
# Напишіть додаток, який симулює проходження
# співбесіди на певну посаду.
# Користувач може ввести назву посади через st.text_input()
# Користувач може ввести опис вакансії через
# st.file_uploader()
# Далі починається чат з спілкуванням
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    trim_messages
)

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash',
    google_api_key=st.secrets.get('GEMINI_API_KEY')
)

st.title('Симулятор співбесіди')
job_position = st.text_input("Введіть назву посади: ")
file_position = st.file_uploader("Підвантажте файл з описом вакансії: ")

if file_position:
    desc_descript = file_position.getvalue().decode('utf-8')
    print(desc_descript)

if st.button('Start'):
    st.session_state.messages = [
        SystemMessage(content=f"""
            Ти симулюєш співбесіду на вкансію {job_position}.
            Ти повинен задавати питанння згідно цього опису вакансії.
            Ось опис вакансії {desc_descript}
            """)
    ]

if 'messages' not in st.session_state:

    st.session_state.messages = [
        SystemMessage(content="""
        Ти вічливий чат бот. Відповідай коротко та чітко.
        """)
    ]

user_input = st.chat_input('Введіть ваше повідомлення')

if user_input is not None:
    human_message = HumanMessage(content=user_input)
    st.session_state.messages.append(human_message)
    # виклик моделі
    response = llm.invoke(st.session_state.messages)

    st.session_state.messages.append(response)
    print(user_input)
    print(response.content)

# відображення історії спілкування(в streamlit)

for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        role = 'human'
    elif isinstance(message, AIMessage):
        role = 'ai'
    else:
        continue
    with st.chat_message(role):
        st.markdown(message.content)
