import streamlit as st
import pandas as pd
import re
from io import StringIO
from groq import Groq

# إعداد واجهة المستخدم
st.set_page_config(page_title="Data Cleanse SaaS", layout="wide")
st.title("🚀 Data Cleanse SaaS - الإصدار السحابي (Cloud Ready)")

# تهيئة Groq API (استخدم Key من إعدادات Streamlit Secrets)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def process_batch(data_text, task):
    prompt = f"""
    أنت محرك معالجة بيانات. المهمة: {task}.
    التعليمات: أعد البيانات بتنسيق CSV (Name,Email,Status).
    لا تضف أي نص توضيحي. يجب أن يحتوي كل سطر على 3 قيم مفصولة بفاصلة.
    البيانات: {data_text}
    """
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        content = chat_completion.choices[0].message.content
        
        # فلترة النتائج المنيعة
        valid_lines = []
        for line in content.split('\n'):
            if line.count(',') == 2:
                valid_lines.append(line.strip())
        return "\n".join(valid_lines)
    except Exception as e:
        return ""

# واجهة رفع الملف
uploaded_file = st.file_uploader("ارفع ملف CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file, on_bad_lines='skip', engine='python')
    st.subheader(f"تم تحميل {len(df)} سطراً")
    
    task = st.selectbox("المهمة:", ["تصحيح إملائي", "توحيد تنسيق الإيميلات"])
    
    if st.button("تنفيذ المعالجة الذكية"):
        batch_size = 50 
        results = ["Name,Email,Status"]
        progress_bar = st.progress(0)
        
        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size]
            batch_csv = batch.to_csv(index=False, header=False)
            
            clean_batch = process_batch(batch_csv, task)
            if clean_batch:
                results.append(clean_batch)
            progress_bar.progress(min((i + batch_size) / len(df), 1.0))
        
        final_csv = "\n".join(results)
        st.success("تم التنظيف بنجاح!")
        st.download_button("📥 تحميل النتائج", final_csv, "cleaned_data.csv", "text/csv")