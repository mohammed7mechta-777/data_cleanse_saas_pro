import streamlit as st
import pandas as pd
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Data Cleanse Pro", layout="wide")

st.title("🌐 Enterprise Data Transformation Engine")

# 2. إنشاء صف الأيقونات التفاعلي
col1, col2, col3 = st.columns(3)

# دالة لتسجيل الحالة
if "action" not in st.session_state: st.session_state.action = None

with col1:
    if st.button("🧹 تنظيف البيانات"): st.session_state.action = "clean"
with col2:
    if st.button("📈 تحليل إحصائي"): st.session_state.action = "analyze"
with col3:
    if st.button("📄 تحويل الصيغ"): st.session_state.action = "convert"

# 3. معالجة الملفات
uploaded_file = st.file_uploader("📂 اسحب ملفك هنا (CSV, XLSX)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.write("### معاينة البيانات:")
    st.dataframe(df.head())

    # تنفيذ الإجراء بناءً على الزر المضغوط
    if st.session_state.action == "clean":
        st.info("🧹 جاري تنظيف البيانات... (حذف القيم الفارغة)")
        df_cleaned = df.dropna()
        st.write("تم التنظيف بنجاح!")
        
        # 4. إضافة زر تحميل الملف المنظف
        csv = df_cleaned.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 تحميل الملف المنظف (CSV)",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
        st.session_state.action = None # إعادة التعيين

    elif st.session_state.action == "analyze":
        st.write("📈 الإحصائيات الوصفية:")
        st.write(df.describe())
        st.session_state.action = None
