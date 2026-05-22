import streamlit as st
from groq import Groq

st.set_page_config(page_title="Data Cleanse Agent", layout="centered")

# إعداد Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🤖 Data Cleanse Agent")

# إعداد سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا مساعدك الذكي لتنظيف البيانات. كيف يمكنني خدمتك اليوم؟"}
    ]

# عرض الرسائل في الوسط
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إظهار أزرار الوصول السريع (تظهر في الوسط بمجرد بدء المحادثة)
col1, col2 = st.columns(2)
with col1:
    if st.button("🧼 تنظيف بياناتي"):
        st.session_state.messages.append({"role": "user", "content": "أريد تنظيف ملف البيانات الخاص بي."})
        st.rerun()
with col2:
    if st.button("📊 تحليل وإحصائيات"):
        st.session_state.messages.append({"role": "user", "content": "أريد إجراء تحليل سريع لبياناتي."})
        st.rerun()

# حقل الإدخال في الوسط (Chat Input)
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
