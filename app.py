import streamlit as st
import pandas as pd
from groq import Groq
import os

# 1. إعداد الصفحة
st.set_page_config(page_title="Enterprise Data Agent", layout="wide")

# إعداد المساعد (تأكد من وضع GROQ_API_KEY في Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Data Cleanse Enterprise Agent")

# 2. إدارة سجل المحادثة (Persistence)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. محرك معالجة الملفات المتعددة
st.subheader("📂 إدارة ملفات البيانات")
uploaded_files = st.file_uploader("ارفع ملفاتك (CSV, Excel, JSON)", type=["csv", "xlsx", "json"], accept_multiple_files=True)

data_frames = {}

if uploaded_files:
    for file in uploaded_files:
        try:
            if file.name.endswith('.csv'): data_frames[file.name] = pd.read_csv(file)
            elif file.name.endswith('.xlsx'): data_frames[file.name] = pd.read_excel(file)
            elif file.name.endswith('.json'): data_frames[file.name] = pd.read_json(file)
            st.write(f"✅ تم تحميل: {file.name}")
        except Exception as e:
            st.error(f"خطأ في ملف {file.name}: {e}")

# 4. عرض المحادثة كاملة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الدردشة مع الذكاء الاصطناعي (محدث للموديل المستقر)
if prompt := st.chat_input("اطلب مني تنظيف أو تحليل البيانات المرفوعة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل مستقر ومتاح حالياً
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            ).choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("حدث خطأ أثناء الاتصال بالمساعد. يرجى مراجعة مفتاح API.")
