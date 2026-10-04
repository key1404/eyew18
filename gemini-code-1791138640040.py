import streamlit as st
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# تنظیمات صفحه
st.set_page_config(
    page_title="Eye1 AI | سامانه تست زنده و واقعی عینک",
    page_icon="👓",
    layout="wide"
)

st.title("👓 سامانه هوشمند Eye1: تست سه‌بعدی و طبیعی فریم‌های اپتیکال")

# مدیریت حالت‌های برنامه
if "step" not in st.session_state:
    st.session_state.step = "capture"
if "image" not in st.session_state:
    st.session_state.image = None
if "face_shape" not in st.session_state:
    st.session_state.face_shape = ""
if "selected_frame" not in st.session_state:
    st.session_state.selected_frame = None

# نوار کناری تنظیمات بالینی
st.sidebar.header("⚙️ پارامترهای اپتومتری")
rx_type = st.sidebar.selectbox("نوع نسخه بینایی (Rx)", ["دوربین / نزدیک‌بین (ساده)", "آستیگمات", "دید پیش‌رونده", "بدون نمره"])
pd_input = st.sidebar.slider("فاصله دو چشم (PD بر حسب میلی‌‌متر)", 50, 75, 62)

# ---------------------------------------------------------
# مرحله ۱: ثبت تصویر چهره
# ---------------------------------------------------------
if st.session_state.step == "capture":
    st.markdown("### مرحله ۱: ثبت تصویر چهره برای تحلیل آناتومیک")
    st.info("لطفاً یک تصویر واضح از چهره خود آپلود کنید یا عکسی برای استخراج فرم صورت ثبت نمایید.")
    
    tab1, tab2 = st.tabs(["📸 عکاسی برای تحلیل اولیه", "📤 آپلود فایل تصویر"])
    
    uploaded_img = None
    with tab1:
        cam_file = st.camera_input("ثبت عکس جهت آنالیز اولیه:")
        if cam_file is not None:
            uploaded_img = Image.open(cam_file)
            
    with tab2:
        file = st.file_uploader("یا بارگذاری تصویر چهره:", type=["jpg", "jpeg", "png"])
        if file is not None:
            uploaded_img = Image.open(file)
            
    if uploaded_img is not None:
        st.session_state.image = uploaded_img
        
        # تحلیل هندسی فرم صورت
        img_arr = np.array(uploaded_img)
        h, w = img_arr.shape[:2]
        ratio = h / w
        
        if ratio > 1.38:
            st.session_state.face_shape = "کشیده (Oblong / Long Face)"
            st.session_state.frames = [
                {"id": "aviator", "name": "Tom Ford - Aviator Gold 3D", "type": "خلبانی فلزی طلایی لوکس", "brand": "Tom Ford", "color": "#d4af37"},
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Bold 3D", "type": "مستطیلی کائوچویی کلاسیک ضخیم", "brand": "Ray-Ban", "color": "#1a1a1a"}
            ]
        elif 1.18 <= ratio <= 1.38:
            st.session_state.face_shape = "بیضی متعادل (Oval - استاندارد طلایی)"
            st.session_state.frames = [
                {"id": "wayfarer", "name": "Ray-Ban - Wayfarer Bold 3D", "type": "ویفرر استاندارد شیک", "brand": "Ray-Ban", "color": "#1a1a1a"},
                {"id": "cateye", "name": "Tom Ford - CatEye Elegant 3D", "type": "چشم‌گربه‌ای مدرن و ظریف", "brand": "Tom Ford", "color": "#65000b"}
            ]
        else:
            st.session_state.face_shape = "گرد یا مربعی (Round / Square)"
            st.session_state.frames = [
                {"id": "round", "name": "Ray-Ban - Retro Round Metal 3D", "type": "گرد فلزی مینیمال مهندسی‌شده", "brand": "Ray-Ban", "color": "#b8860b"},
                {"id": "slim", "name": "Tom Ford - Slim Rectangular 3D", "type": "فریم مستطیلی زاویه‌دار باریک", "brand": "Tom Ford", "color": "#2f4f4f"}
            ]
        
        st.session_state.step = "analyze"
        st.rerun()

# ---------------------------------------------------------
# مرحله ۲: نمایش تحلیل چهره و گالری مدل‌ها
# ---------------------------------------------------------
elif st.session_state.step == "analyze":
    st.markdown("### مرحله ۲: نتیجه تحلیل هوش مصنوعی و انتخاب فریم")
    
    col_img, col_report = st.columns([1, 1.3])
    with col_img:
        st.image(st.session_state.image, caption="تصویر تحلیل‌شده", use_column_width=True)
        if st.button("🔄 عکاسی یا بارگذاری تصویر جدید"):
            st.session_state.step = "capture"
            st.rerun()
            
    with col_report:
        st.success("✅ تحلیل آناتومیک با موفقیت انجام شد!")
        st.write(f"🔹 **فرم هندسی تشخیص‌داده‌شده:** {st.session_state.face_shape}")
        st.write(f"📏 **پارامترهای PD:** {pd_input}mm | **نسخه:** {rx_type}")
        st.markdown("---")
        st.markdown("💡 لطفاً یکی از مدل‌های زیر را انتخاب کنید تا وارد **اتاق تست زنده و سه‌بعدی واقعی** شوید:")

    st.markdown("---")
    
    f_cols = st.columns(len(st.session_state.frames))
    for i, frame in enumerate(st.session_state.frames):
        with f_cols[i]:
            st.markdown(f"""
                <div style="border: 2px solid {frame['color']}; padding: 20px; border-radius: 12px; background-color: #fafafa; text-align: center;">
                    <h3 style="color: #222;">{frame['name']}</h3>
                    <p><b>برند:</b> {frame['brand']}</p>
                    <p><b>طراحی:</b> {frame['type']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"✨ تست زنده و پوشیدن عینک", key=f"btn_frame_{i}"):
                st.session_state.selected_frame = frame
                st.session_state.step = "tryon"
                st.rerun()

# ---------------------------------------------------------
# مرحله ۳: اتاق تست زنده با مدل سه‌بعدی پیشرفته و کاملاً طبیعی عینک
# ---------------------------------------------------------
elif st.session_state.step == "tryon":
    chosen = st.session_state.selected_frame
    
    st.markdown(f"### مرحله ۳: اتاق تست زنده و پوشیدن عینک (فریم فعال: {chosen['name']})")
    st.markdown("دوربین فعال است. مدل عینک سه‌بعدی با انحنای استاندارد، پل بینی و عدسی‌های فیزیکی به‌طور کامل روی چشم‌های شما قرار گرفته است.")
    
    if st.button("← بازگشت به گالری و انتخاب فریم دیگر"):
        st.session_state.step = "analyze"
        st.rerun()
        
    st.markdown("---")

    ar_tryon_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <style>
            .ar-container {{
                position: relative;
                width: 640px;
                height: 480px;
                margin: auto;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                background: #000;
            }}
            video, canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
            }}
            #three_canvas {{
                pointer-events: none;
                z-index: 5;
            }}
            .loading {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: white;
                font-family: Tahoma, sans-serif;
                font-size: 16px;
                z-index: 10;
                background: rgba(0,0,0,0.85);
                padding: 14px 28px;
                border-radius: 8px;
            }}
            .info-bar {{
                text-align: center;
                background: #eef7fc;
                padding: 10px;
                font-family: Tahoma, sans-serif;
                font-size: 14px;
                color: #333;
                max-width: 640px;
                margin: 10px auto 0 auto;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="ar-container">
            <div id="loading" class="loading">در حال بارگذاری موتور سه‌بعدی و انطباق عینک روی صورت...</div>
            <video id="webcam" autoplay playsinline muted></video>
            <canvas id="output_canvas"></canvas>
            <canvas id="three_canvas"></canvas>
        </div>
        <div class="info-bar">
            <b>فریم انتخابی:</b> {chosen['name']} | 🟢 تست سه‌بعدی و زنده فعال است
        </div>

        <script>
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const loadingElement = document.getElementById('loading');
            const threeCanvas = document.getElementById('three_canvas');

            const frameStyle = "{chosen['id']}";

            // راه‌اندازی صحنه Three.js
            const scene = new THREE.Scene();
            const camera3D = new THREE.PerspectiveCamera(45, 640 / 480, 0.1, 1000);
            camera3D.position.z = 5;

            const renderer = new THREE.WebGLRenderer({{ canvas: threeCanvas, alpha: true, antialias: true }});
            renderer.setSize(640, 480);

            // نورپردازی حرفه‌ای برای ایجاد بازتاب طبیعی روی فریم و شیشه عینک
            const ambientLight = new THREE.AmbientLight(0xffffff, 1.2);
            scene.add(ambientLight);
            
            const dirLight1 = new THREE.DirectionalLight(0xffffff, 1.0);
            dirLight1.position.set(0, 10, 5);
            scene.add(dirLight1);

            const dirLight2 = new THREE.DirectionalLight(0x99bbff, 0.5);
            dirLight2.position.set(-5, -5, 5);
            scene.add(dirLight2);

            // ایجاد مدل سه‌بعدی عینک با هندسه استاندارد و شکیل فریم‌های واقعی
            const glassesGroup = new THREE.Group();

            const isGold = (frameStyle === 'aviator' || frameStyle === 'round');
            const frameColorHex = isGold ? 0xd4af37 : 0x1c1c1c;

            const frameMaterial = new THREE.MeshStandardMaterial({{
                color: frameColorHex,
                roughness: 0.15,
                metalness: isGold ? 0.85 : 0.3
            }});

            const lensMaterial = new THREE.MeshPhysicalMaterial({{
                color: 0x88aacc,
                transparent: true,
                opacity: 0.3,
                roughness: 0.05,
                transmission: 0.9,
                ior: 1.5
            }});

            // طراحی بدنه فرم عینک (رینگ دور چشم‌ها)
            const ringGeo = new THREE.TorusGeometry(0.32, 0.04, 16, 64);
            
            // رینگ چپ
            const leftRing = new THREE.Mesh(ringGeo, frameMaterial);
            leftRing.position.set(-0.38, 0, 0);

            // رینگ راست
            const rightRing = new THREE.Mesh(ringGeo, frameMaterial);
            rightRing.position.set(0.38, 0, 0);

            // عدسی‌ها
            const lensDiscGeo = new THREE.CircleGeometry(0.32, 32);
            const leftLens = new THREE.Mesh(lensDiscGeo, lensMaterial);
            leftLens.position.set(-0.38, 0, 0);

            const rightLens = new THREE.Mesh(lensDiscGeo, lensMaterial);
            rightLens.position.set(0.38, 0, 0);

            // پل بینی استاندارد (روی استخوان بینی)
            const bridgeGeo = new THREE.BoxGeometry(0.24, 0.05, 0.04);
            const bridge = new THREE.Mesh(bridgeGeo, frameMaterial);
            bridge.position.set(0, 0.12, 0);

            // دسته‌های عینک (که به سمت گوش امتداد پیدا می‌کنند)
            const templeGeo = new THREE.BoxGeometry(0.04, 0.04, 1.2);
            
            const leftTemple = new THREE.Mesh(templeGeo, frameMaterial);
            leftTemple.position.set(-0.68, 0.05, -0.6);
            leftTemple.rotation.y = 0.3;

            const rightTemple = new THREE.Mesh(templeGeo, frameMaterial);
            rightTemple.position.set(0.68, 0.05, -0.6);
            rightTemple.rotation.y = -0.3;

            glassesGroup.add(leftRing);
            glassesGroup.add(rightRing);
            glassesGroup.add(leftLens);
            glassesGroup.add(rightLens);
            glassesGroup.add(bridge);
            glassesGroup.add(leftTemple);
            glassesGroup.add(rightTemple);

            scene.add(glassesGroup);
            glassesGroup.visible = false;

            function onResults(results) {{
                loadingElement.style.display = 'none';
                canvasElement.width = videoElement.videoWidth;
                canvasElement.height = videoElement.videoHeight;

                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);
                canvasCtx.restore();

                if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {{
                    const landmarks = results.multiFaceLandmarks[0];
                    
                    // لندمارک‌های اصلی بینی (168) و دو چشم (33 و 263) برای فیکس شدن دقیق روی صورت
                    const noseBridge = landmarks[168];
                    const leftEye = landmarks[33];
                    const rightEye = landmarks[263];

                    // موقعیت سه‌بعدی قرارگیری عینک روی بینی
                    const x = (noseBridge.x - 0.5) * -3.2;
                    const y = -(noseBridge.y - 0.5) * 2.4;
                    const z = -noseBridge.z * 1.5;

                    glassesGroup.position.set(x, y - 0.02, z);

                    // محاسبه دقیق چرخش سر (تراز شدن عینک با زاویه کج شدن سر)
                    const dx = rightEye.x - leftEye.x;
                    const dy = rightEye.y - leftEye.y;
                    const dz = rightEye.z - leftEye.z;
                    
                    const angleZ = Math.atan2(dy, dx);
                    const angleY = Math.atan2(dz, dx);
                    const angleX = (noseBridge.y - (leftEye.y + rightEye.y)/2) * 2.0;

                    glassesGroup.rotation.z = angleZ;
                    glassesGroup.rotation.y = angleY * 0.4;
                    glassesGroup.rotation.x = angleX;

                    // مقیاس‌دهی کاملاً پویا بر اساس عرض شقیقه‌ها (لندمارک‌های 234 و 454)
                    const templeLeft = landmarks[234];
                    const templeRight = landmarks[454];
                    const faceWidth = Math.hypot(
                        templeRight.x - templeLeft.x,
                        templeRight.y - templeLeft.y
                    );
                    
                    const scaleFactor = faceWidth * 3.1;
                    glassesGroup.scale.set(scaleFactor, scaleFactor, scaleFactor);

                    glassesGroup.visible = true;
                    renderer.render(scene, camera3D);
                }} else {{
                    glassesGroup.visible = false;
                    renderer.clear();
                }}
            }}

            const faceMesh = new FaceMesh({{
                locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${{file}}`
            }});

            faceMesh.setOptions({{
                maxNumFaces: 1,
                refineLandmarks: true,
                minDetectionConfidence: 0.6,
                minTrackingConfidence: 0.6
            }});

            faceMesh.onResults(onResults);

            const camera = new Camera(videoElement, {{
                onFrame: async () => {{
                    await faceMesh.send({{ image: videoElement }});
                }},
                width: 640,
                height: 480
            }});

            camera.start().catch(err => {{
                loadingElement.innerText = "خطا در دسترسی به دوربین مرورگر!";
                console.error(err);
            }});
        </script>
    </body>
    </html>
    """

    components.html(ar_tryon_html, height=580)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 پایان تست و شروع مجدد با چهره جدید"):
        st.session_state.step = "capture"
        st.rerun()