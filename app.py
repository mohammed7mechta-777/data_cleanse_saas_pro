import streamlit as st
import pandas as pd
from groq import Groq

# إعداد الصفحة لتكون مركزية
st.set_page_config(page_title="Data Cleanse Agent", layout="centered")

# إعداد الـ Client
api_key = st.secrets.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("🤖 Data Cleanse Agent")

# 1. ميزة رفع الملفات (تظهر في الأعلى بوضوح)
uploaded_file = st.file_uploader("📂 ارفع ملف CSV لبدء المعالجة", type=["csv"])

# 2. إعداد سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا مساعدك الذكي. ارفع ملفك وسأقوم بتنظيفه أو تحليله لك."}
    ]

# عرض رسائل الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. وظيفة التنظيف بالذكاء الاصطناعي (محدثة بموديل مستقر)
def clean_with_ai(text):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": f"صحح الأخطاء الإملائية لهذا النص فقط: {text}"}],
            model="llama3-8b-8192", 
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return text

# 4. معالجة الملف والأزرار
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("تم رفع الملف بنجاح!")
        
        # أزرار الوصول السريع
        col1, col2 = st.columns(2)
        
        if col1.button("🧼 تنظيف البيانات"):
            with st.spinner("جاري تنظيف البيانات... يرجى الانتظار (نقوم بمعالجة عينة لضمان الاستقرار)"):
                # معالجة أول 5 أسطر فقط لضمان عدم التوقف (تبلوكا)
                df_preview = df.head(5).copy()
                first_col = df_preview.columns[0]
                df_preview[first_col] = df_preview[first_col].apply(clean_with_ai)
                st.success("تم تنظيف العينة بنجاح!")
                st.dataframe(df_preview)
        
        if col2.button("📊 تحليل البيانات"):
            st.bar_chart(df.isnull().sum())
            
    except Exception as e:
        st.error(f"خطأ في قراءة الملف: {e}")

# 5. الدردشة (في الأسفل)
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=st.session_state.messages
            )
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"خطأ في الاتصال بالذكاء الاصطناعي: {e}")
