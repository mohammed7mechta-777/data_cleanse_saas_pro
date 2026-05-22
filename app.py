import streamlit as st
import pandas as pd
import json
from groq import Groq

# إعدادات الواجهة الاحترافية
st.set_page_config(page_title="Enterprise Data Engine", layout="wide")

# إعداد الـ Client مع التحقق من وجود مفتاح API
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("🚀 Enterprise Data Transformation Engine")

# محرك قراءة الملفات المتعدد (CSV, Excel, JSON)
def load_data(file):
    if file.name.endswith('.csv'): return pd.read_csv(file)
    elif file.name.endswith('.xlsx'): return pd.read_excel(file)
    elif file.name.endswith('.json'): return pd.read_json(file)
    return None

uploaded_file = st.file_uploader("📥 ارفع ملف البيانات (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.success(f"تم تحميل الملف بنجاح: {uploaded_file.name}")
        st.dataframe(df.head()) # معاينة سريعة

        # ميزة التحميل الاحترافية
        csv = df.to_csv(index=False)
        st.download_button("📥 تحميل الملف المعالج", csv, "cleaned_data.csv", "text/csv")

# وكيل الدردشة الذكي
st.subheader("💬 مستشار البيانات الذكي")
if prompt := st.chat_input("اطلب مني تنظيف أو تحليل البيانات..."):
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192", # موديل عالي الأداء
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content
            st.markdown(response)
        except Exception as e:
            st.error("يرجى التأكد من صلاحية مفتاح الـ API وتحديث الموديل.")
