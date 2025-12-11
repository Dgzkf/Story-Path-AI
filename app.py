import streamlit as st
import google.generativeai as genai

# 1. КОНФИГУРАЦИЯ НА СТРАНИЦАТА
st.set_page_config(page_title="Хроникьорът на Световете", page_icon="📖")

st.title("📖 Хроникьорът на Световете")
st.caption("Интерактивна книга-игра, захранвана от Google Gemini")

# 2. НАСТРОЙКА НА API КЛЮЧА
# В реално приложение ключът се взима от тайните на Streamlit (st.secrets)
# За локален тест можеш да го сложиш тук, но не го споделяй публично!
api_key = st.secrets.get("GOOGLE_API_KEY") 

if not api_key:
    st.error("Моля, добавете своя Google API Key в настройките на приложението.")
    st.stop()

genai.configure(api_key=api_key)

# 3. СИСТЕМНИЯТ ПРОМПТ (ВАЙБ КОДЪТ)
# Тук слагаш целия текст от "ПЪЛЕН СИСТЕМЕН ПРОМПТ (Версия 2.0)"
SYSTEM_PROMPT = """
Ти си "Хроникьорът на Световете" – високотехнологичен творчески ИИ...
[... ТУК ПОСТАВИ ЦЕЛИЯ ДЪЛЪГ ТЕКСТ НА ИНСТРУКЦИИТЕ ...]
"""

# 4. ИНИЦИАЛИЗАЦИЯ НА МОДЕЛА И ИСТОРИЯТА
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Добавяме системния промпт като скрита първа инструкция
    # Забележка: При Gemini Pro често е по-добре да се ползва system_instruction при създаването
    
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Или "gemini-1.5-pro" за по-високо качество
        system_instruction=SYSTEM_PROMPT,
        generation_config={"temperature": 1.0}
    )
    st.session_state.chat_session = model.start_chat(history=[])
    
    # Автоматичен старт - моделът да заговори пръв
    response = st.session_state.chat_session.send_message("Старт")
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# 5. ПОКАЗВАНЕ НА ЧАТА
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. ПОЛЕ ЗА ВЪВЕЖДАНЕ ОТ ПОТРЕБИТЕЛЯ
if prompt := st.chat_input("Твоят избор..."):
    # Показване на съобщението на потребителя
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Генериране на отговор от ИИ
    with st.chat_message("assistant"):
        with st.spinner("Хроникьорът пише..."):
            try:
                response = st.session_state.chat_session.send_message(prompt)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Възникна грешка: {e}")