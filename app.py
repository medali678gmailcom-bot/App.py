import streamlit as st
import requests
import base64

# تصميم واجهة الموقع التجريبي
st.title("🔍 مستكشف الأسعار الذكي (نسخة تجريبية)")
st.write("ارفع صورة المنتج، وسيقوم الذكاء الاصطناعي بالتعرف عليه والبحث عن أقل سعر في جوجل!")

# خانات إدخال البيانات من المستخدم
uploaded_file = st.file_uploader("قم برفع صورة المنتج هنا...", type=["jpg", "jpeg", "png"])
additional_details = st.text_input("تفاصيل إضافية لمساعدتنا في البحث (اختياري)")

# خانات سريّة لوضع المفاتيح لتشغيل الموقع التجريبي مجاناً
hf_token = st.text_input("أدخل مفتاح Hugging Face Token الخاص بك:", type="password")
serp_api_key = st.text_input("أدخل مفتاح SerpApi Key الخاص بك:", type="password")

if st.button("ابحث عن أقل سعر بضغطة زر"):
    if not uploaded_file or not hf_token or not serp_api_key:
        st.error("الرجاء رفع الصورة وإدخال مفاتيح الـ API (Hugging Face و SerpApi) أولاً!")
    else:
        # قراءة الصورة وتحويلها إلى صيغة Base64 ليقبلها الذكاء الاصطناعي
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_data_url = f"data:image/jpeg;base64,{base64_image}"
        
        # 1. الاتصال بنموذج الذكاء الاصطناعي Llama 3.2 Vision للتعرف على الصورة
        with st.spinner("جاري تحليل الصورة والتعرف على المنتج عبر الذكاء الاصطناعي..."):
            hf_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"
            headers = {
                "Authorization": f"Bearer {hf_token}",
                "Content-Type": "application/json"
            }
            
            # صياغة الطلب مع إرسال الصورة بصيغة URL والرابط التوجيهي
            prompt_text = "What is the exact product model name in this image? Respond ONLY with the product name in English in one short line without extra words."
            if additional_details:
                prompt_text += f" Context clue: {additional_details}"
                
            payload = {
                "inputs": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt_text},
                            {"type": "image_url", "image_url": {"url": image_data_url}}
                        ]
                    }
                ],
                "parameters": {"max_new_tokens": 20}
            }
            
            try:
                response = requests.post(hf_url, json=payload, headers=headers)
                hf_result = response.json()
                
                # استخراج النص المولد من الإجابة
                if isinstance(hf_result, list) and len(hf_result) > 0:
                    product_name = hf_result[0].get("generated_text", "").strip()
                elif isinstance(hf_result, dict) and "generated_text" in hf_result:
                    product_name = hf_result["generated_text"].strip()
                else:
                    product_name = additional_details if additional_details else "Product"
            except Exception as e:
                product_name = additional_details if additional_details else "Product"
        
        # 2. البحث في جوجل باستخدام موديول SerpApi بناءً على الاسم المستخرج
        with st.spinner(f"تم التعرف على المنتج باسم: ({product_name})! جاري البحث عن أرخص الأسعار في جوجل..."):
            serp_url = "https://serpapi.com/search.json"
            params = {
                "q": f"{product_name} price",
                "engine": "google_shopping",
                "api_key": serp_api_key
            }
            
            try:
                serp_response = requests.get(serp_url, params=params)
                results = serp_response.json()
                
                # 3. عرض النتائج النهائية للمخدم على الشاشة مباشرة
                st.success("إليك أرخص الأسعار التي تم العثور عليها في الأسواق:")
                
                if "shopping_results" in results:
                    for item in results["shopping_results"][:3]:  # جلب أفضل وأرخص 3 نتائج
                        st.write(f"🔹 **المتجر:** {item.get('source')}")
                        st.write(f"💰 **السعر:** {item.get('price')}")
                        st.write(f"🔗 [رابط الشراء المباشر]({item.get('link')})")
                        st.write("---")
                else:
                    st.warning("لم نجد نتائج تسوق مباشرة للمنتج، جرب كتابة تفاصيل أدق في الخانة الاختيارية.")
            except Exception as e:
                st.error("حدث خطأ أثناء الاتصال بمحرك بحث جوجل.")
