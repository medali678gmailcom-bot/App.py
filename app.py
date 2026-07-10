import streamlit as st
import requests
import base64

# ضبط الصفحة لتطابق أبعاد شاشات الهواتف الذكية
st.set_page_config(
    page_title="StoreFinder Pro",
    page_icon="👟",
    layout="centered"
)

# هندسة التصميم (CSS) لمحاكاة واجهات Nike الاحترافية التي أرسلتها بالكامل
st.markdown("""
    <style>
    /* تحويل الخلفية إلى اللون الأبيض النظيف والناعم المريح للعين */
    .stApp {
        background-color: #f9f9f9;
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
        color: #111111;
    }
    
    /* تصميم الحاوية أو الهيدر الرئيسي */
    .brand-header {
        text-align: center;
        padding: 15px 0;
        margin-bottom: 20px;
    }
    .brand-logo {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -1px;
        color: #111111;
        text-transform: uppercase;
    }
    
    /* تصميم بنر العرض التقديمي (مثل بنر الخصم 50% في الصورة) */
    .promo-banner {
        background-color: #111111;
        color: #ffffff;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    .promo-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .promo-subtitle {
        font-size: 13px;
        color: #cccccc;
        line-height: 1.5;
    }
    
    /* تصميم كروت دليل الخطوات */
    .guide-box {
        background: #ffffff;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #e5e5e5;
        text-align: right;
    }
    .guide-num {
        font-size: 12px;
        font-weight: bold;
        color: #888888;
        text-transform: uppercase;
    }
    .guide-text {
        font-size: 15px;
        font-weight: 600;
        color: #111111;
        margin-top: 2px;
    }
    
    /* زر تصفح وبدء التجربة الفخم (أسود بالكامل مثل أزرار Nike) */
    .nike-btn {
        display: block;
        width: 100%;
        background-color: #111111;
        color: #ffffff !important;
        text-align: center;
        padding: 15px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 15px;
        text-decoration: none !important;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-top: 15px;
        transition: 0.2s;
    }
    
    /* تخصيص صناديق المدخلات ورفع الملفات لتصبح دائرية وجميلة */
    .stFileUploader {
        border: 2px dashed #cccccc !important;
        border-radius: 20px !important;
        background-color: #ffffff !important;
    }
    
    /* تصميم شبكة عرض عروض الأسعار (Product Grid Card) */
    .product-grid-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 16px;
        border: 1px solid #eeeeee;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .grid-store {
        font-size: 16px;
        font-weight: 800;
        color: #111111;
    }
    .grid-details {
        font-size: 12px;
        color: #666666;
        margin: 4px 0 12px 0;
        line-height: 1.4;
    }
    .grid-price-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }
    .grid-price {
        font-size: 20px;
        font-weight: 800;
        color: #111111;
    }
    
    /* زر الشراء الصغير الخاص بكل كرت منتج */
    .buy-now-btn {
        background-color: #111111;
        color: white !important;
        padding: 8px 18px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        text-decoration: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة التنقل وحفظ الحالة
if "explore_mode" not in st.session_state:
    st.session_state.explore_mode = False

# هيدر التطبيق الثابت ليعطي انطباع البراند المحترف
st.markdown("<div class='brand-header'><div class='brand-logo'>⚡ EXPLORE PRO</div></div>", unsafe_allow_html=True)

# =========================================================
# المرحلة الأولى: العرض التقديمي المتطابق مع صور المتاجر
# =========================================================
if not st.session_state.explore_mode:
    # البنر الإعلاني الفاخر في المقدمة
    st.markdown("""
        <div class="promo-banner">
            <div class="promo-title">Visual Search Engine</div>
            <div class="promo-subtitle">اكتشف أسعار المنتجات في المتاجر العالمية والمحلية بمجرد التقاط صورة لها من كاميرا هاتفك.</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h5 style='text-align: right; font-weight:800; margin-bottom:15px; color:#111111;'>دليل الاستخدام السريع:</h5>", unsafe_allow_html=True)
    
    # خطوات تفاعلية أنيقة
    st.markdown("<div class='guide-box'><div class='guide-num'>01 . الرفع الذكي</div><div class='guide-text'>ارفع صورة حذاء، ساعة، أو ملابس بدقة عالية.</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='guide-box'><div class='guide-num'>02 . الفحص الفوري</div><div class='guide-text'>يقوم نظامنا بمسح ملامح وشعار المنتج وتحديده.</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='guide-box'><div class='guide-num'>03 . مقارنة الأسعار</div><div class='guide-text'>تظهر لك المتاجر التي تبيعه مع تصفية لأقل سعر متوفر.</div></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # زر تشغيل الواجهة
    if st.button("اكتشف الميزة الآن (Explore)", use_container_width=True):
        st.session_state.explore_mode = True
        st.rerun()

# =========================================================
# المرحلة الثانية: واجهة البحث الاحترافية (تطابق صفحة تفاصيل المنتج)
# =========================================================
else:
    if st.button("⬅️ العودة للدليل"):
        st.session_state.explore_mode = False
        st.rerun()
        
    st.markdown("<h4 style='font-weight:800; color:#111111;'>🔍 مستكشف الأسعار البصري</h4>", unsafe_allow_html=True)

    # إعدادات المطور بشكل منسق ونظيف
    with st.expander("🔑 مفاتيح ربط السيرفر الآمنة"):
        hf_token = st.text_input("Hugging Face Token:", type="password")
        serp_api_key = st.text_input("SerpApi Key:", type="password")

    st.markdown("<p style='font-size:14px; font-weight:700; color:#111111; margin-bottom:5px;'>قم برفع الصورة لمعاينتها وتحليلها:</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        uploaded_file.seek(0)
        # إطار ناعم لعرض الصورة المرفوعة مثل صورة حذاء نايكي في تطبيقك
        st.image(uploaded_file, caption="📸 جاري تجهيز المنتج للفحص البصري", use_container_width=True)

    additional_details = st.text_input("✍️ تفاصيل إضافية أو تأكيد الموديل يدوياً (اختياري):")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 ابدأ البحث والمقارنة الحية", use_container_width=True):
        if not uploaded_file or not hf_token or not serp_api_key:
            st.error("⚠️ يرجى تعبئة مفاتيح الربط أولاً ورفع صورة منتجك.")
        else:
            uploaded_file.seek(0)
            image_bytes = uploaded_file.read()
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            image_data_url = f"data:image/jpeg;base64,{base64_image}"
            
            with st.spinner("🧠 نظام الرؤية يحلل تفاصيل المنتج المرفوع..."):
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

            search_query = additional_details if additional_details else product_name

            with st.spinner(f"🔍 جاري جلب الأسعار المباشرة لـ ({search_query})..."):
                serp_url = "https://serpapi.com/search.json"
                params = {
                    "q": search_query,
                    "engine": "google_shopping",
                    "google_domain": "google.com",
                    "hl": "ar", 
                    "api_key": serp_api_key
                }
                
                try:
                    serp_response = requests.get(serp_url, params=params)
                    results = serp_response.json()
                    
                    st.markdown("<h5 style='font-weight:800; margin-top:15px; color:#111111;'>🎯 أفضل العروض المتاحة في الأسواق:</h5>", unsafe_allow_html=True)
                    
                    if "shopping_results" in results and len(results["shopping_results"]) > 0:
                        # عرض العروض على شكل بطاقات تسوق بيضاء فاخرة مطابقة لصورك
                        for item in results["shopping_results"][:3]:
                            title = item.get('title', 'منتج متوفر')
                            source = item.get('source', 'متجر إلكتروني')
                            price = item.get('price', 'عرض خاص')
                            link = item.get('link', '#')
                            
                            st.markdown(f"""
                                <div class="product-grid-card">
                                    <div class="grid-store">🏪 {source}</div>
                                    <div class="grid-details">{title[:55]}...</div>
                                    <div class="grid-price-row">
                                        <div class="grid-price">{price}</div>
                                        <a href="{link}" target="_blank" class="buy-now-btn">Buy Now</a>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("💡 لم نجد نتائج تسوق مطابقة تماماً للموديل المرفوع، اكتب اسم الماركة لتوجيه محرك البحث.")
                except:
                    st.error("❌ حدث خطأ غير متوقع أثناء معالجة الأسعار والمتاجر.")

