import streamlit as st
import google.generativeai as genai

st.title("🔍 Диагностика на Ключа")

# Взимане на ключа
api_key = st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("Няма намерен ключ в Secrets!")
    st.stop()

try:
    genai.configure(api_key=api_key)
    
    st.write("📡 Свързване с Google...")
    st.write("Списък на моделите, достъпни за твоя ключ:")
    
    found_any = False
    # Извличане на всички налични модели
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            st.code(f"Име: {m.name}")
            found_any = True
            
    if not found_any:
        st.error("😱 Списъкът е празен! Твоят ключ е валиден, но няма достъп до никакви модели.")
        
except Exception as e:
    st.error(f"❌ Грешка при свързване: {e}")
    st.warning("Това обикновено означава, че ключът е грешен, изтрит или не е от AI Studio.")
