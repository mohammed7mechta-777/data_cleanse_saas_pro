import streamlit as st
import pandas as pd
from groq import Groq

# 1. إعداد الصفحة والـ Client
st.set_page_config(page_title="Enterprise Data Agent", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Data Cleanse Enterprise Agent")

# 2. التوجيه الذكي (System Prompt) لتمكينه من الدارجة الجزائرية وغيرها
SYSTEM_PROMPT = """
أنت خبير بيانات محترف. مهمتك هي مساعدة المستخدم في تنظيف، تحليل، ومعالجة ملفات البيانات. 
أنت تفهم جميع اللغات بطلاقة، بما في ذلك الدارجة الجزائرية (مثل: واش راك، نظف البيانات، دير تحليل)، 
واللغة العربية الفصحى، والإنجليزية. جاوب المستخدم بنفس اللغة التي يتحدث بها. 
إذا طلب المستخدم تنظيف ملف، اشرح له الخطوات بوضوح وبلهجته.
"""

# 3. إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4. معالجة الملفات
uploaded_files = st.file_uploader("📂 ارفع ملفاتك (CSV, Excel, JSON)", type=["csv", "xlsx", "json"], accept_multiple_files=True)

# 5. عرض السجل
for message in st.session_state.messages:
    if message["role"] != "system": # لا نعرض الـ system prompt للمستخدم
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. منطق الدردشة
if prompt := st.chat_input("أهدر معايا بالدارجة ولا بالعربية..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استدعاء الموديل مع سجل المحادثة الكامل
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("خطأ في الاتصال، تأكد من إعدادات الـ API.")
