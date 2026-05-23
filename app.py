import streamlit as st
import pandas as pd
import requests
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="Data Cleanse Pro | Enterprise Engine", layout="wide")

# محاولة تحميل مكتبات الواجهة بمرونة
try:
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except ImportError:
    HAS_LOTTIE = False

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# وظيفة الترحيب
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# إدارة حالة التطبيق
if "show_welcome" not in st.session_state: st.session_state.show_welcome = True
if "messages" not in st.session_state: st.session_state.messages = []

if st.session_state.show_welcome:
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في Data Cleanse Pro 🚀</h1>", unsafe_allow_html=True)
    if HAS_LOTTIE:
        lottie_welcome = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
        st_lottie(lottie_welcome, height=300)
    if st.button("ابدأ تشغيل المحرك الآن", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
else:
    st.title("🌐 Enterprise Data Transformation Engine")

    # 2. صف الأيقونات التفاعلي
    col1, col2, col3, col4 = st.columns(4)
    def set_action(action): st.session_state.pending_action = action

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
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"تم تحميل: {file.name}")

    # 4. منطق المحادثة مع فرض اللغة
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("تحدث مع بياناتك..."):
        # التعليمات الصارمة
        SYSTEM_INSTRUCTION = "أنت خبير بيانات. يجب أن ترد دائماً بنفس لغة المستخدم (دارجة/عربية/إنجليزية) وبشكل احترافي."
        
        # دمج طلب الخدمة مع الرسالة
        user_input = prompt
        if "pending_action" in st.session_state:
            user_input = f"بخصوص خدمة {st.session_state.pending_action}: {prompt}"
            del st.session_state.pending_action

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": SYSTEM_INSTRUCTION}] + st.session_state.messages
                ).choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception:
                st.error("خطأ تقني في الاتصال.")
