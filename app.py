import streamlit as st
import pandas as pd
from groq import Groq
import io

# إعداد واجهة المستخدم
st.set_page_config(page_title="Data Cleanse SaaS", layout="wide")
st.title("🚀 Data Cleanse SaaS - الإصدار الاحترافي")

# إعداد مفتاح API من Secrets
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. نظام مدقق البيانات (Data Validator)
def validate_and_clean(df):
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')
    return df

# 2. وظيفة التنظيف بالذكاء الاصطناعي
def clean_with_ai(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"صحح الأخطاء الإملائية في هذا النص فقط: {text}"}],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except:
        return text

# 3. واجهة رفع الملفات مع دعم أنواع متعددة
uploaded_file = st.file_uploader("ارفع ملف البيانات (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])

if uploaded_file is not None:
    try:
        # قراءة ذكية بناءً على نوع الملف
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_json(uploaded_file)

        # حماية من الملفات الفارغة
        if not df.empty:
            df = validate_and_clean(df)
            st.write("### معاينة البيانات قبل المعالجة")
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
                st.dataframe(cleaned_df.head())
                
                # تحميل الملف
                csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button("تحميل البيانات المنظفة", csv, "full_cleaned_data.csv", "text/csv")
        else:
            st.warning("الملف المرفوع فارغ، يرجى رفع ملف يحتوي على بيانات.")
            
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
