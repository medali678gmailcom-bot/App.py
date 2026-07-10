import streamlit as st
import requests
import base64

# ضبط إعدادات الصفحة وجعلها مهيأة تماماً للهاتف
st.set_page_config(
    page_title="PriceFinder Pro",
    page_icon="🛍️",
    layout="centered"
)

# تصميم واجهة ثورية باستخدام CSS حديث ونظيف (إلغاء التصميم القديم تماماً)
st.markdown("""
    <style>
    /* تحسين الخلفية العامة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* تصميم عنوان رئيسي فخم */
    .hero-title {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        color: #57606f;
        text-align: center;
        font-size: 14px;
        margin-bottom: 25px;
    }
    /* تصميم بطاقة المنتج الأنيقة */
    .product-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border: 1px solid #e1e8ed;
        margin-bottom: 20px;
    }
    /* تصميم كروت الأسعار الفاخرة */
    .price-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-right: 6px solid #2ecc71;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .store-name {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
    }
    .price-tag {
        font-size: 18px;
        font-weight: bold;
        color: #2ecc71;
    }
    /* زر الشراء الاحترافي الذي لا يعلق */
    .buy-btn {
        display: block;
        width: 100%;
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white !important;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(30,60,114,0.2);
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# عرض الواجهة الجديدة
st.markdown("<div class='hero-title'>🛍️ PriceFinder Pro</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>الجيل الجديد لمقارنة الأسعار الذكية عبر الصور</div>", unsafe_allow_html=True)

# وضع المفاتيح في قائمة منسدلة جانبية أو علوية مخفية للحفاظ على جمال الموقع
with st.expander("🔑 إعدادات مفاتيح التشغيل (اضغط للفتح)"):
    hf_token = st.text_input("Hugging Face Token:", type="password")
    serp_api_key = st.text_input("SerpApi Key:", type="password")

# حاوية رفع الصورة والتفاصيل
st.markdown("<div class='product-card'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("📥 اختر أو التقط صورة المنتج:", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    st.image(uploaded_file, caption="📸 المنتج المطلوب فصحه", use_container_width=True)

additional_details = st.text_input("✍️ اكتب اسم المنتج أو الماركة لتأكيد دقة الأسعار (ينصح به):")
st.markdown("</div>", unsafe_allow_html=True)

# زر البحث الكبير والحديث
if st.button("🔍 ابحث عن أقل سعر الآن", use_container_width=True):
    if not uploaded_file or not hf_token or not serp_api_key:
        st.error("⚠️ يرجى رفع الصورة وإدخال المفاتيح أولاً!")
    else:
        # معالجة الصورة
        uploaded_file.seek(0)
        image_bytes = uploaded_file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        image_data_url = f"data:image/jpeg;base64,{base64_image}"
        
        # 1. استخراج اسم المنتج
        with st.spinner("🧠 الذكاء الاصطناعي يحلل الصورة..."):
            hf_url = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-11B-Vision-Instruct"
            headers = {"Authorization": f"Bearer {hf_token}", "Content-Type": "application/json"}
            prompt_text = "What is the product name in English? One short line only."
            
            payload = {
                "inputs": [{"role": "user", "content": [{"type": "text", "text": prompt_text}, {"type": "image_url", "image_url": {"url": image_data_url}}]}],
                "parameters": {"max_new_tokens": 15}
            }
            
            try:
                response = requests.post(hf_url, json=payload, headers=headers)
                hf_result = response.json()
                if isinstance(hf_result, list) and len(hf_result) > 0:
                    product_name = hf_result[0].get("generated_text", "").strip()
                elif isinstance(hf_result, dict) and "generated_text" in hf_result:
                    product_name = hf_result["generated_text"].strip()
                else:
                    product_name = additional_details if additional_details else "Product"
            except:
                product_name = additional_details if additional_details else "Product"

        # إذا كتب المستخدم بيده، ندمج كلامه للحصول على أعلى دقة في جوجل
        search_query = additional_details if additional_details else product_name

        # 2. جلب الأسعار من جوجل بالتصميم الجديد وحل مشكلة الروابط
        with st.spinner(f"🔍 جاري جلب أفضل عروض الأسعار لـ ({search_query})..."):
            serp_url = "https://serpapi.com/search.json"
            params = {
                "q": search_query,
                "engine": "google_shopping",
                "google_domain": "google.com",
                "hl": "ar",  # جلب الأسعار والمتاجر باللغة العربية ودعم العملة المحلية
                "api_key": serp_api_key
            }
            
            try:
                serp_response = requests.get(serp_url, params=params)
                results = serp_response.json()
                
                st.markdown("### 🏷️ العروض المتاحة في السوق:")
                
                if "shopping_results" in results and len(results["shopping_results"]) > 0:
                    # فرز وتصفيف العروض كروت جذابة
                    for item in results["shopping_results"][:4]: # جلب أفضل 4 عروض
                        title = item.get('title', 'منتج بدون اسم')
                        source = item.get('source', 'متجر غير معروف')
                        price = item.get('price', 'غير محدد')
                        link = item.get('link', '#')
                        
                        # تصميم كرت سعر متكامل ونظيف يحل مشكلة تعليق الروابط
                        st.markdown(f"""
                            <div class="price-box">
                                <div>
                                    <div class="store-name">🏪 {source}</div>
                                    <div style="font-size:12px; color:#7f8c8d; margin-top:4px;">{title[:40]}...</div>
                                </div>
                                <div class="price-tag">{price}</div>
                            </div>
                            <a href="{link}" target="_blank" class="buy-btn">🛒 اذهب للمتجر والشراء</a>
                            <br>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("💡 لم نجد نتائج تسوق دقيقة، حاول تعديل الاسم في خانة التأكيد المكتوبة.")
            except:
                st.error("❌ حدث خطأ أثناء الاتصال بمحرك البحث.")
