import streamlit as st
import pandas as pd
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Enterprise Data Agent", layout="wide")

# إعداد الـ Client (تأكد من إعداد المفتاح في Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Data Cleanse Enterprise Agent")

# 2. التوجيه الذكي (System Prompt) لفرض الالتزام باللغة
SYSTEM_PROMPT = """
أنت خبير بيانات محترف. مهمتك هي مساعدة المستخدم في تنظيف، تحليل، ومعالجة ملفات البيانات.
تعليمات صارمة:
1. يجب عليك دائماً الرد على المستخدم **بنفس اللغة** التي يستخدمها (الدارجة الجزائرية، العربية الفصحى، الفرنسية، الإنجليزية، إلخ).
2. إذا خاطبك المستخدم بالدارجة الجزائرية، أجب بالدارجة الجزائرية بطلاقة واحترافية.
3. التزم بلغة المستخدم طوال فترة المحادثة ولا تغيرها عشوائياً.
4. أنت تفهم اللهجة الجزائرية جيداً، استخدمها بذكاء عند الحاجة.
"""

# 3. إدارة سجل المحادثة مع التوجيه
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. معالجة الملفات المتعددة
st.subheader("📂 إدارة ملفات البيانات")
uploaded_files = st.file_uploader("ارفع ملفاتك (CSV, Excel, JSON)", type=["csv", "xlsx", "json"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.write(f"✅ تم تحميل: {file.name}")

# عرض سجل المحادثة (باستثناء الـ system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطق الدردشة التفاعلي
if prompt := st.chat_input("اطلب مني تنظيف أو تحليل البيانات..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل مستقر ومتاح (llama-3.1-8b-instant)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            ).choices[0].message.content
            
            # عرض الرد وإضافته للسجل
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("خطأ في الاتصال بالمساعد. تأكد من إعدادات الـ API والموديل.")
