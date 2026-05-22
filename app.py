import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data App", layout="wide")

st.title("🚀 Data Cleanse Engine")

# إزالة الرسوم المتحركة مؤقتاً للتأكد من الإقلاع
st.info("مرحباً بك في نظام معالجة البيانات.")

uploaded_file = st.file_uploader("ارفع ملفك", type=["csv", "xlsx"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.dataframe(df)
    except Exception as e:
        st.error(f"خطأ: {e}")
