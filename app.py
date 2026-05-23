import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")

# 2. الواجهة الترحيبية (تظهر فقط في البداية)
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

if not st.session_state.file_uploaded:
    st.title("Data Cleanse Pro مرحباً بك في 🚀")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=600", width=400)
    if st.button("ابدأ تشغيل المحرك الآن"):
        st.session_state.file_uploaded = True
        st.rerun()
else:
    # 3. واجهة التطبيق الرئيسية (تظهر بعد الترحيب)
    st.title("🌐 Enterprise Data Transformation Engine")
    
    # صف الأيقونات
    col1, col2, col3 = st.columns(3)
    if "action" not in st.session_state: st.session_state.action = None

    with col1:
        if st.button("🧹 تنظيف البيانات"): st.session_state.action = "clean"
    with col2:
        if st.button("📈 تحليل إحصائي"): st.session_state.action = "analyze"
    with col3:
        if st.button("📄 تحويل الصيغ"): st.session_state.action = "convert"

    # معالجة الملف
    uploaded_file = st.file_uploader("📂 اسحب ملفك هنا (CSV, XLSX)", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        # تنفيذ الأوامر
        if st.session_state.action == "clean":
            st.info("🧹 جاري التنظيف...")
            df_cleaned = df.dropna()
            st.dataframe(df_cleaned.head())
            
            # زر التحميل
            csv = df_cleaned.to_csv(index=False).encode('utf-8')
            st.download_button("📥 تحميل الملف المنظف", csv, "cleaned_data.csv", "text/csv")
            
        elif st.session_state.action == "analyze":
            st.write("📈 الإحصائيات:", df.describe())
            
        elif st.session_state.action == "convert":
            json_data = df.to_json(orient="records")
            st.download_button("📥 تحميل بصيغة JSON", json_data, "data.json", "application/json")
