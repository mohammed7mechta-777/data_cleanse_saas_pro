import streamlit as st
import pandas as pd
from groq import Groq
import os

# إعداد واجهة المستخدم
st.set_page_config(page_title="Data Cleanse SaaS", layout="wide")
st.title("🚀 Data Cleanse SaaS - الإصدار الاحترافي")

# إعداد مفتاح API من Secrets
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

# 1. نظام مدقق البيانات (Data Validator)
def validate_and_clean(df):
    # إزالة المسافات من أسماء الأعمدة
    df.columns = df.columns.str.strip()
    # حذف الصفوف الفارغة تماماً
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

# واجهة رفع الملف
# 1. تحديث واجهة رفع الملفات لتشمل Excel و JSON
uploaded_file = st.file_uploader("ارفع ملف بياناتك (CSV, Excel, JSON)", type=["csv", "xlsx", "json"])

if uploaded_file:
    # 2. وظيفة ذكية لقراءة أي نوع ملف بناءً على الامتداد
    def load_data(file):
        file_extension = file.name.split('.')[-1].lower()
        try:
            if file_extension == 'csv':
                return pd.read_csv(file)
            elif file_extension == 'xlsx':
                return pd.read_excel(file)
            elif file_extension == 'json':
                return pd.read_json(file)
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")
            return None
        return None

    df = load_data(uploaded_file)
    
    if df is not None:
        # هنا تستدعي دالة التنظيف التي أضفناها سابقاً
        df = validate_and_clean(df) 
        st.write("### معاينة البيانات")
        st.dataframe(df.head())
        # ... (بقية كود المعالجة الخاص بك)
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = validate_and_clean(df)
    
    st.write("### معاينة البيانات قبل المعالجة")
    st.dataframe(df.head())
    
    if st.button("تنفيذ المعالجة الذكية"):
        progress_bar = st.progress(0)
        total_rows = len(df)
        
        # المعالجة صفاً بصف
        cleaned_data = []
        for index, row in df.iterrows():
            # مثال: تنظيف أول عمود في الجدول
            target_col = df.columns[0]
            row[target_col] = clean_with_ai(str(row[target_col]))
            cleaned_data.append(row)
            progress_bar.progress((index + 1) / total_rows)
        
        cleaned_df = pd.DataFrame(cleaned_data)
        st.success("تم التنظيف بنجاح!")
        st.dataframe(cleaned_df.head())
        
        # زر تحميل الملف
        csv = cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button("تحميل البيانات المنظفة", csv, "cleaned_data.csv", "text/csv")