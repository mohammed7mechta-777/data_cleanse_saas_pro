import streamlit as st
import pandas as pd
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Enterprise Data Transformation Engine")

# 2. صف الأيقونات الاحترافي (Service Icons)
st.markdown("### اختر الخدمة:")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🧹 تنظيف البيانات"):
        st.session_state.action = "clean"
with col2:
    if st.button("📈 تحليل إحصائي"):
        st.session_state.action = "analyze"
with col3:
    if st.button("📄 تحويل الصيغ"):
        st.session_state.action = "convert"
with col4:
    if st.button("🤖 دردشة ذكية"):
        st.session_state.action = "chat"

# 3. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. معالجة الملفات
uploaded_files = st.file_uploader("📂 اسحب ملفاتك (CSV, XLSX, JSON)", accept_multiple_files=True)

# 5. منطق الدردشة "الصارم" (الذي يفرض اللغة)
if prompt := st.chat_input("تحدث مع بياناتك... (يدعم الدارجة، العربية، والإنجليزية)"):
    # دمج أمر فرض اللغة مع رسالة المستخدم
    SYSTEM_INSTRUCTION = "يجب الرد دائماً بنفس لغة المستخدم (دارجة/عربية/إنجليزية). التزم بهذه اللغة طوال المحادثة."
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": SYSTEM_INSTRUCTION}] + st.session_state.messages
            ).choices[0].message.content
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("خطأ في الاتصال بالمحرك، تأكد من إعدادات الـ API.")
