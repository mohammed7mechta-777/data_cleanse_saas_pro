import streamlit as st
import pandas as pd
from groq import Groq

# إعداد واجهة المستخدم
st.set_page_config(page_title="Data Cleanse SaaS", layout="wide")
st.title("🚀 Data Cleanse SaaS - الإصدار التحليلي")

# إعداد مفتاح API
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. نظام مدقق البيانات
def validate_and_clean(df):
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    return df

# 2. وظيفة التحليل البصري (الميزة الجديدة)
def generate_insights(df):
    st.write("### 📊 تحليل سريع للبيانات")
    # حساب عدد القيم الفارغة في كل عمود
    missing_data = df.isnull().sum()
    st.bar_chart(missing_data)
    st.write("هذا الرسم يوضح توزيع البيانات المفقودة في أعمدة ملفك.")

# 3. وظيفة التنظيف بالذكاء الاصطناعي
def clean_with_ai(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"صحح الأخطاء الإملائية في هذا النص فقط: {text}"}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except:
        return text

# واجهة رفع الملف
uploaded_file = st.file_uploader("ارفع ملف CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if not df.empty:
            df = validate_and_clean(df)
            
            # عرض التحليل قبل التنظيف
            generate_insights(df)
            
            st.write("### معاينة البيانات")
            st.dataframe(df.head())
            
            if st.button("تنفيذ المعالجة الذكية"):
                progress_bar = st.progress(0)
                total_rows = len(df)
                cleaned_data = []
                
                for index, row in df.iterrows():
                    target_col = df.columns[0]
                    row[target_col] = clean_with_ai(str(row[target_col]))
                    cleaned_data.append(row)
                    progress_bar.progress((index + 1) / total_rows)
                
                cleaned_df = pd.DataFrame(cleaned_data)
                st.success("تم التنظيف بنجاح!")
                
                # تحميل الملف
                csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button("تحميل البيانات المنظفة", csv, "full_cleaned_data.csv", "text/csv")
        else:
            st.warning("الملف المرفوع فارغ.")
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
