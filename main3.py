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

st.title('ITstep чат бот')

st.markdown('простий бот для спілкуванння')


# додаємо історію повідомлень до сесії

# якщо це тільки початок застосунку, додаємо історію повідомлень
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
    st.markdown(message.content)