import streamlit as st
import pandas as pd
import requests
from groq import Groq

# 1. إعدادات الواجهة الاحترافية (SaaS Look & Feel)
st.set_page_config(page_title="Data Cleanse Pro | Enterprise Engine", layout="wide")

# محاولة تحميل مكتبات الواجهة بمرونة
try:
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except ImportError:
    HAS_LOTTIE = False

# 2. إعداد المساعد (تأكد من إعداد API KEY في إعدادات Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. وظيفة الترحيب الاحترافية
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# إدارة حالة شاشة الإقلاع (تظهر مرة واحدة فقط)
if "show_welcome" not in st.session_state: st.session_state.show_welcome = True

if st.session_state.show_welcome:
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في Data Cleanse Pro 🚀</h1>", unsafe_allow_html=True)
    if HAS_LOTTIE:
        lottie_welcome = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
        st_lottie(lottie_welcome, height=300)
    st.markdown("<p style='text-align: center;'>الجيل القادم من محركات معالجة وتحليل البيانات الذكية.</p>", unsafe_allow_html=True)
    if st.button("ابدأ تشغيل المحرك الآن", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
else:
    # 4. الواجهة الرئيسية للمحرك
    st.sidebar.title("⚙️ لوحة التحكم")
    st.title("🌐 Enterprise Data Transformation Engine")

    # التوجيه الذكي (System Prompt)
    SYSTEM_PROMPT = """أنت خبير بيانات محترف. مهمتك تنظيف وتحليل الملفات. 
    يجب أن ترد دائماً بنفس اللغة التي يستخدمها المستخدم (دارجة جزائرية، عربية، إنجليزية). 
    التزم بلغة المستخدم طوال المحادثة."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # معالجة الملفات
    uploaded_files = st.file_uploader("📂 اسحب ملفاتك هنا (CSV, Excel, JSON)", accept_multiple_files=True)
    
    if uploaded_files:
        for file in uploaded_files:
            st.success(f"تم تحميل: {file.name}")
            # عرض معاينة
            df = pd.read_csv(file) if file.name.endswith('.csv') else pd.read_excel(file)
            with st.expander(f"عرض بيانات {file.name}"):
                st.dataframe(df.head(5))

    # 5. منطق المحادثة الاحترافي
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("تحدث مع بياناتك... (يدعم الدارجة، العربية، والإنجليزية)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages
                ).choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("خطأ تقني في الاتصال بالمحرك، يرجى مراجعة إعدادات الـ API.")
