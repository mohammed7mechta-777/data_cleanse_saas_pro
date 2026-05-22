import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Data Cleanse Agent", layout="centered")

# إعداد الـ Client مع حماية المفتاح
api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    st.error("مفتاح API غير موجود. يرجى إضافته في إعدادات Secrets.")
    st.stop()
client = Groq(api_key=api_key)

st.title("🤖 Data Cleanse Agent")

# إعداد سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "أهلاً بك! أنا مساعدك الذكي لتنظيف البيانات. كيف يمكنني خدمتك اليوم؟"}
    ]

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# أزرار الوصول السريع (في الوسط)
col1, col2 = st.columns(2)
with col1:
    if st.button("🧼 تنظيف بياناتي"):
        st.session_state.messages.append({"role": "user", "content": "أريد تنظيف ملف البيانات الخاص بي."})
        st.rerun()
with col2:
    if st.button("📊 تحليل وإحصائيات"):
        st.session_state.messages.append({"role": "user", "content": "أريد إجراء تحليل سريع لبياناتي."})
        st.rerun()

# حقل الدردشة الذكي
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # طلب استجابة من Groq
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"عذراً، حدث خطأ أثناء الاتصال بـ Groq: {e}")
            # إضافة رسالة توضيحية للسجل لتجنب تكرار الخطأ
            st.session_state.messages.append({"role": "assistant", "content": "حدث خطأ تقني، يرجى المحاولة مرة أخرى."})
