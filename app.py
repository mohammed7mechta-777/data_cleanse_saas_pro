import streamlit as st
import pandas as pd
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Data Cleanse Enterprise Agent")

# 2. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. معالجة الملفات
uploaded_files = st.file_uploader("📂 ارفع ملفاتك هنا", accept_multiple_files=True)

# عرض الرسائل السابقة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. منطق الدردشة "الصارم" (يقوم بفرض اللغة في كل مرة)
if prompt := st.chat_input("تحدث مع بياناتك..."):
    # الرسالة التي سنرسلها للموديل تحتوي على "أمر فرض اللغة"
    STRICT_LANGUAGE_INSTRUCTION = f"""
    ملاحظة هامة: المستخدم كتب هذه الرسالة: "{prompt}". 
    يجب أن ترد عليه **بنفس اللغة تماماً** التي استخدمها في هذه الرسالة (إذا كانت دارجة جزائرية، أجب بالدارجة؛ إذا كانت فرنسية، أجب بالفرنسية).
    التزم بهذه اللغة في كامل ردك.
    """
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # نرسل سجل المحادثة مع التعليمات المحدثة لكل رسالة
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": STRICT_LANGUAGE_INSTRUCTION}] + st.session_state.messages
            ).choices[0].message.content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("خطأ في الاتصال بالمحرك.")
