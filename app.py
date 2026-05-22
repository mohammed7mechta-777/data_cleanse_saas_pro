import streamlit as st
import pandas as pd
from groq import Groq

st.set_page_config(page_title="Data Cleanse Agent", layout="centered")

# إعداد الـ Client
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("🤖 Data Cleanse Agent")

# 1. ميزة رفع الملفات (في الأعلى)
uploaded_file = st.file_uploader("📂 ارفع ملف CSV لبدء المعالجة", type=["csv"])

# 2. إعداد سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا مساعدك الذكي. ارفع ملفك وسأقوم بتنظيفه أو تحليله لك."}
    ]

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. معالجة الملف إذا تم رفعه
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("تم رفع الملف بنجاح!")
    
    # أزرار الوصول السريع بعد رفع الملف
    col1, col2 = st.columns(2)
    if col1.button("🧼 تنظيف البيانات"):
        st.write("جاري التنظيف بالذكاء الاصطناعي...")
        # هنا يتم استدعاء منطق التنظيف
    if col2.button("📊 تحليل البيانات"):
        st.bar_chart(df.isnull().sum())

# 4. الدردشة (في الأسفل)
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تم تحديث الموديل إلى نسخة نشطة
            stream = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=st.session_state.messages
            )
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")
