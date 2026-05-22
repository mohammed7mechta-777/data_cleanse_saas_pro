import streamlit as st
import pandas as pd
import json
import requests
from groq import Groq
from streamlit_lottie import st_lottie

# 1. إعداد الواجهة الاحترافية
st.set_page_config(page_title="Enterprise Data Cleanse", layout="wide")

def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# رسوم متحركة 3D (تضفي طابع الاحترافية)
lottie_data = load_lottie("https://assets5.lottiefiles.com/packages/lf20_4cup433w.json")

st.title("🌐 Enterprise Data Transformation Engine")
st_lottie(lottie_data, height=200, key="data_animation")

# 2. إعداد الـ Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 3. محرك القراءة الذكي
def process_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1]
    if ext == 'csv': return pd.read_csv(uploaded_file)
    elif ext == 'xlsx': return pd.read_excel(uploaded_file)
    elif ext == 'json': return pd.read_json(uploaded_file)
    return None

# 4. الواجهة المركزية
uploaded_file = st.file_uploader("📂 اسحب ملف البيانات الخاص بك", type=["csv", "xlsx", "json"])

if uploaded_file:
    df = process_file(uploaded_file)
    if df is not None:
        st.success(f"تم تحميل الملف: {uploaded_file.name} - {df.shape[0]} سجل")
        
        # إجراءات احترافية
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🧼 تنظيف الذكاء الاصطناعي"):
                st.info("جاري المعالجة المتقدمة...")
                # هنا منطق المعالجة
        with col2:
            st.download_button("📥 تحميل CSV", df.to_csv(), "cleaned_data.csv", "text/csv")
        with col3:
            st.metric("عدد الأعمدة", df.shape[1])

# 5. وكيل الدردشة الذكي في المنتصف
st.markdown("---")
st.subheader("💬 مستشارك للبيانات")
if prompt := st.chat_input("اطلب مني تعديل البيانات..."):
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
        st.markdown(response)
