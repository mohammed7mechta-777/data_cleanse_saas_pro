import streamlit as st
import pandas as pd
import requests
from groq import Groq
from streamlit_lottie import st_lottie

# 1. إعداد الصفحة والواجهة
st.set_page_config(page_title="Enterprise Data Cleanse", layout="wide")

# دالة لتحميل الرسوم المتحركة
def load_lottie(url):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# 2. إدارة حالة الإقلاع
if "show_welcome" not in st.session_state: st.session_state.show_welcome = True

if st.session_state.show_welcome:
    st.markdown("<h1 style='text-align: center;'>مرحباً بك في Data Cleanse AI</h1>", unsafe_allow_html=True)
    lottie_welcome = load_lottie("https://assets9.lottiefiles.com/packages/lf20_jcikwtux.json")
    st_lottie(lottie_welcome, height=300)
    if st.button("ابدأ العمل الآن 🚀", use_container_width=True):
        st.session_state.show_welcome = False
        st.rerun()
else:
    # 3. الكود الأساسي للعمل
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.title("🌐 Enterprise Data Transformation Engine")

    # محرك القراءة الذكي
    def process_file(uploaded_file):
        try:
            if uploaded_file.name.endswith('.csv'): return pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'): return pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.json'): return pd.read_json(uploaded_file)
        except Exception as e: return None

    uploaded_file = st.file_uploader("📂 ارفع ملف البيانات الخاص بك", type=["csv", "xlsx", "json"])

    if uploaded_file:
        df = process_file(uploaded_file)
        if df is not None:
            st.success("تم تحميل الملف بنجاح!")
            st.dataframe(df.head(10))
            
            # ميزة التحميل
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 تحميل الملف المعالج", csv, "data.csv", "text/csv")

    # وكيل الدردشة الذكي
    st.markdown("---")
    st.subheader("💬 مستشارك للبيانات")
    if prompt := st.chat_input("اطلب مني تنظيف أو تحليل البيانات..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}]
                ).choices[0].message.content
                st.markdown(response)
            except Exception as e:
                st.error("خطأ في الاتصال بالمساعد، يرجى مراجعة إعدادات الـ API.")
