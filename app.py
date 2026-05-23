import streamlit as st
import pandas as pd
import time
import io

st.set_page_config(page_title="Data Cleanse Pro", layout="wide")

# إعداد الحالة
if "file_uploaded" not in st.session_state: st.session_state.file_uploaded = False
if "action" not in st.session_state: st.session_state.action = None

# 1. الواجهة الترحيبية
if not st.session_state.file_uploaded:
    st.title("Data Cleanse Pro مرحباً بك في 🚀")
    if st.button("ابدأ تشغيل المحرك الآن"):
        st.session_state.file_uploaded = True
        st.rerun()
else:
    # 2. الواجهة الرئيسية
    st.title("🌐 Enterprise Data Transformation Engine")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧹 تنظيف البيانات"): st.session_state.action = "clean"
    with col2:
        if st.button("📈 تحليل إحصائي"): st.session_state.action = "analyze"
    with col3:
        if st.button("📄 تحويل الصيغ"): st.session_state.action = "convert"

    uploaded_file = st.file_uploader("📂 اسحب ملفك هنا (CSV, XLSX)", type=['csv', 'xlsx'])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # معالجة البيانات مع شريط تقدم
        if st.session_state.action:
            progress_text = "جاري المعالجة... يرجى الانتظار"
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=f"المعالجة {percent_complete+1}%")
            
            st.success("تمت المعالجة بنجاح!")
            st.write("### معاينة البيانات المنظفة:")
            st.dataframe(df.head())

            # أزرار التحميل المتعددة
            c1, c2, c3 = st.columns(3)
            
            # CSV
            csv = df.to_csv(index=False).encode('utf-8')
            c1.download_button("📥 تحميل CSV", csv, "data.csv", "text/csv")
            
            # Excel
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            c2.download_button("📥 تحميل XLSX", buffer.getvalue(), "data.xlsx", "application/vnd.ms-excel")
            
            # JSON
            json_str = df.to_json(orient="records")
            c3.download_button("📥 تحميل JSON", json_str, "data.json", "application/json")
            
            st.session_state.action = None # إعادة ضبط
