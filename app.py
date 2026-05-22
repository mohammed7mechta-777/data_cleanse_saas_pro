import streamlit as st
import pandas as pd
import requests
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")

# محاولة تحميل مكتبة الرسوم المتحركة بمرونة
try:
    from streamlit_lottie import st_lottie
    HAS_LOTTIE = True
except ImportError:
    HAS_LOTTIE = False

def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. إدارة شاشة الترحيب (Session State)
if "show_welcome" not in st.session_state: st.session_state.show_welcome = True

if st.session_state.show_welcome:
    st.markdown("<h1 style='text-align: center;'>Data Cleanse Agent</h1>", unsafe_allow_html=True)
    if HAS_LOTTIE:
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json"
        st_lottie(load_lottie(lottie_url), height=300)
    
    if st.button("ابدأ العمل الآن 🚀", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
else:
    # 3. المنطق الأساسي للتطبيق
    st.title("🌐 لوحة تحكم البيانات")
    
    # إعداد الـ Client (تأكد من إعداد المفتاح في Secrets)
    api_key = st.secrets.get("GROQ_API_KEY")
    client = Groq(api_key=api_key) if api_key else None

    uploaded_file = st.file_uploader("📥 ارفع ملف البيانات الخاص بك", type=["csv", "xlsx"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.dataframe(df.head(10))
            st.success("تم رفع الملف بنجاح!")
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")

    # 4. المساعد الذكي
    st.markdown("---")
    st.subheader("💬 مستشارك للبيانات")
    if prompt := st.chat_input("اطلب مني تنظيف أو تحليل البيانات..."):
        if not client:
            st.error("لم يتم العثور على مفتاح الـ API في الإعدادات.")
        else:
            with st.chat_message("assistant"):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant", # الموديل المحدث والمتاح
                        messages=[{"role": "user", "content": prompt}]
                    ).choices[0].message.content
                    st.markdown(response)
                except Exception as e:
                    st.error("خطأ في الاتصال بالذكاء الاصطناعي، يرجى مراجعة الموديل أو مفتاح الـ API.")
