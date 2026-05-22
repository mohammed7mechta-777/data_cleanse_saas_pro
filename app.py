import streamlit as st
import pandas as pd
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("🌐 Enterprise Data Transformation Engine")

# 2. إنشاء صف الأيقونات التفاعلي (Service Icons)
col1, col2, col3, col4 = st.columns(4)

# دالة لتسجيل الإجراء المختار
def set_action(action):
    st.session_state.pending_action = action

with col1:
    if st.button("🧹 تنظيف البيانات"): set_action("تنظيف البيانات")
with col2:
    if st.button("📈 تحليل إحصائي"): set_action("تحليل إحصائي")
with col3:
    if st.button("📄 تحويل الصيغ"): set_action("تحويل الصيغ")
with col4:
    if st.button("🤖 دردشة ذكية"): set_action("دردشة عامة")

# 3. معالجة الملفات
uploaded_files = st.file_uploader("📂 اسحب ملفاتك (CSV, XLSX, JSON)", accept_multiple_files=True)

# 4. سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. منطق الدردشة مع فرض اللغة
if prompt := st.chat_input("تحدث مع بياناتك..."):
    # إذا ضغط المستخدم على أيقونة، ندمجها مع الرسالة ليعرف المساعد سياق طلبه
    user_input = prompt
    if "pending_action" in st.session_state:
        user_input = f"بخصوص خدمة {st.session_state.pending_action}: {prompt}"
        del st.session_state.pending_action

    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # التعليمات الصارمة لفرض اللغة
    SYSTEM_INSTRUCTION = "يجب أن ترد دائماً بنفس لغة المستخدم (دارجة/عربية/إنجليزية). التزم بهذه اللغة طوال المحادثة."
    
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
            st.error("خطأ في الاتصال بالمحرك.")
