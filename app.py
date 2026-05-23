import streamlit as st
import pandas as pd
import pdfplumber
import time
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Data Cleanse Pro - Enterprise Engine", layout="wide")

# إعداد الذاكرة
if "file_uploaded" not in st.session_state: st.session_state.file_uploaded = False
if "action" not in st.session_state: st.session_state.action = None

# 2. الواجهة الترحيبية
if not st.session_state.file_uploaded:
    st.title("Data Cleanse Pro مرحباً بك في 🚀")
    st.write("### المحرك المؤسسي لتحويل ومعالجة البيانات")
    if st.button("ابدأ تشغيل المحرك الآن"):
        st.session_state.file_uploaded = True
        st.rerun()
else:
    # 3. الواجهة الرئيسية
    st.title("🌐 Enterprise Data Transformation Engine")
    
    # صف الأيقونات
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🧹 تنظيف البيانات"): st.session_state.action = "clean"
    with col2:
        if st.button("📈 تحليل إحصائي"): st.session_state.action = "analyze"
    with col3:
        if st.button("📄 تحويل الصيغ"): st.session_state.action = "convert"

    # منطقة رفع الملف
    uploaded_file = st.file_uploader("📂 اسحب ملفك هنا (PDF, CSV, XLSX)", type=['pdf', 'csv', 'xlsx'])

    if uploaded_file:
        # معالجة الملف حسب نوعه
        df = None
        if uploaded_file.name.endswith('.pdf'):
            with pdfplumber.open(uploaded_file) as pdf:
                page = pdf.pages[0]
                table = page.extract_table()
                if table: df = pd.DataFrame(table[1:], columns=table[0])
        elif uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # تنفيذ الإجراء
        if st.session_state.action and df is not None:
            # شريط التقدم
            my_bar = st.progress(0, text="جاري المعالجة... يرجى الانتظار")
            for i in range(100):
                time.sleep(0.01)
                my_bar.progress(i + 1)
            
            st.success("تمت المعالجة بنجاح!")
            
            # معاينة البيانات
            st.write("### معاينة البيانات:")
            st.dataframe(df.head())

            # الإجراءات المحددة
            if st.session_state.action == "clean":
                df = df.dropna()
                st.info("تم حذف القيم الفارغة.")
            elif st.session_state.action == "analyze":
                st.write("📈 الإحصائيات الوصفية:")
                st.write(df.describe())

            # أزرار التحميل المتعددة
            st.write("---")
            st.write("### 📥 خيارات التحميل:")
            c1, c2, c3 = st.columns(3)
            
            # تحميل CSV
            csv = df.to_csv(index=False).encode('utf-8')
            c1.download_button("📥 تحميل CSV", csv, "data.csv", "text/csv")
            
            # تحميل Excel
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            c2.download_button("📥 تحميل XLSX", buffer.getvalue(), "data.xlsx", "application/vnd.ms-excel")
            
            # تحميل JSON
            json_str = df.to_json(orient="records")
            c3.download_button("📥 تحميل JSON", json_str, "data.json", "application/json")
            
            # إعادة ضبط الحالة
            if st.button("تحديث العملية"):
                st.session_state.action = None
                st.rerun()
