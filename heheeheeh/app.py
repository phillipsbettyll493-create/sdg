# app.py
from flask import Flask, request, render_template_string
import requests, urllib.parse

app = Flask(__name__)

# === CONFIG ===
OPENROUTER_API_KEY = "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"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "gpt-4o-mini"

# === GỌI OPENROUTER TẠO NỘI DUNG ===
def generate_ai_content(keyword, main_link):
    prompt = f"""
请用中文写一段大约五句连贯的简短说明文字，主题是“{keyword}”。
要求：
1. 文风自然、正式、有信息性；
2. 在内容中重复出现“{keyword}”2到3次；
3. 不要出现“资讯来源”字样；
4. 不要添加标题或额外符号；
5. 只生成说明段落。
"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional Chinese SEO content writer."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
    }
    try:
        r = requests.post(OPENROUTER_URL, json=data, headers=headers, timeout=20)
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"].strip()
        # Gắn theo mẫu: toàn bộ nội dung nhúng link
        html_block = f'<a href="{main_link}" target="_blank">{keyword} -【网址：{main_link}】- {text}</a>'
        return html_block
    except Exception as e:
        return f'<a href="{main_link}" target="_blank">{keyword} -【网址：{main_link}】- AI生成失败：{e}</a>'

# === FORM GIAO DIỆN ===
FORM_HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anime Content Generator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Kanit:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600&display=swap');
        
        :root {
            --primary: #FF6B6B;
            --primary-dark: #FF4757;
            --secondary: #7871FF;
            --success: #00D2D3;
            --warning: #FFA502;
            --background: #2C2F4A;
            --card-bg: #353B64;
            --text-primary: #FFFFFF;
            --text-secondary: #B8C6DB;
            --border: #4B4F7C;
            --accent: #FF6B6B;
            --gradient-1: linear-gradient(135deg, #FF6B6B, #FFA502);
            --gradient-2: linear-gradient(135deg, #7871FF, #00D2D3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--background) 0%, #1e1b4b 100%);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 2.5rem;
            padding: 2rem 0;
            position: relative;
        }

        .header::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--warning));
            border-radius: 2px;
        }

        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 1rem;
        }

        .logo-icon {
            font-size: 2.5rem;
            color: var(--warning);
        }

        /* make inline svg icons adopt theme color */
        .logo-icon, .icon {
            color: var(--accent);
            display: inline-block;
        }

        .icon path, .icon circle, .icon rect { stroke: currentColor; fill: currentColor; }

        .logo-text {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--warning) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 400;
            max-width: 600px;
            margin: 0 auto;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1.5rem;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
        }

        .card-header {
            background: rgba(30, 41, 59, 0.8);
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border);
        }

        .card-title {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
        }

        .card-title i {
            color: var(--primary);
        }

        .card-body {
            padding: 1.5rem;
        }

        .form-label {
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .form-label i {
            color: var(--primary);
            font-size: 0.9rem;
        }

        .form-control, .form-select {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .form-control:focus, .form-select:focus {
            background: rgba(15, 23, 42, 0.9);
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.2);
            color: var(--text-primary);
        }

        .form-control::placeholder {
            color: var(--text-secondary);
        }

        textarea.form-control {
            min-height: 120px;
            resize: vertical;
        }

        .input-group-text {
            background: var(--border);
            border: 1px solid var(--border);
            color: var(--text-secondary);
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            border: 2px solid var(--primary);
            color: white;
            padding: 0.875rem 2rem;
            border-radius: 0;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(255, 107, 107, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            width: 100%;
            position: relative;
            clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%);
            text-transform: uppercase;
            letter-spacing: 2px;
            animation: buttonGlow 2s infinite;
        }

        @keyframes buttonGlow {
            0%, 100% { box-shadow: 0 0 15px rgba(255, 107, 107, 0.3); }
            50% { box-shadow: 0 0 30px rgba(255, 107, 107, 0.6); }
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.4);
            background: linear-gradient(135deg, var(--primary-dark) 0%, #1e40af 100%);
        }

        .form-hint {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }

        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1.5rem 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border);
        }

        .step-indicator {
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            position: relative;
        }

        .step-indicator::before {
            content: '';
            position: absolute;
            top: 15px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--border);
            z-index: 1;
        }

        .step {
            display: flex;
            flex-direction: column;
            align-items: center;
            position: relative;
            z-index: 2;
        }

        .step-number {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: var(--border);
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            margin-bottom: 0.5rem;
            transition: all 0.3s ease;
        }

        .step.active .step-number {
            background: var(--primary);
            color: white;
        }

        .step-label {
            font-size: 0.875rem;
            color: var(--text-secondary);
            text-align: center;
        }

        .step.active .step-label {
            color: var(--primary);
            font-weight: 500;
        }

        @media (max-width: 768px) {
            .container {
                padding: 0 10px;
            }
            
            .logo-text {
                font-size: 1.8rem;
            }
            
            .card-body {
                padding: 1.25rem;
            }
            
            .step-label {
                font-size: 0.75rem;
            }
        }
        
        /* Anime character and sparkle decorations */
        .anime-character {
            position: absolute;
            width: 220px;
            max-width: 28%;
            right: 10px;
            top: 10px;
            z-index: 5;
            pointer-events: none;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.6));
            transform-origin: center;
            animation: floaty 6s ease-in-out infinite;
        }

        .anime-gif-small {
            position: absolute;
            width: 120px;
            left: 10px;
            bottom: -10px;
            z-index: 4;
            opacity: 0.95;
            animation: sway 5s ease-in-out infinite;
            pointer-events: none;
        }

        .lottie-box {
            position: absolute;
            left: 8px;
            top: 8px;
            width: 100px;
            height: 100px;
            z-index: 6;
            pointer-events: none;
            opacity: 0.98;
        }

        /* single character + sparkle decorations */
        .lottie-character {
            position: absolute;
            right: 8px;
            top: 6px;
            width: 120px;
            height: 160px;
            z-index: 6;
            pointer-events: none;
            animation: floaty 5.5s ease-in-out infinite;
        }

        .lottie-character lottie-player { width:100%; height:100%; }

        .sparkle-container { position:absolute; left:40%; top:6px; width:240px; height:120px; pointer-events:none; z-index:5; }
        .sparkle { position:absolute; width:14px; height:14px; opacity:0.0; transform-origin:center; }
        .sparkle.s1 { left:10%; top:10%; animation: sparklePop 3s infinite; }
        .sparkle.s2 { left:30%; top:40%; animation: sparklePop 4s 0.6s infinite; }
        .sparkle.s3 { left:70%; top:20%; animation: sparklePop 3.5s 0.2s infinite; }

        @keyframes floaty {
            0% { transform: translateY(0) rotate(-2deg); }
            50% { transform: translateY(-14px) rotate(2deg); }
            100% { transform: translateY(0) rotate(-2deg); }
        }

        @keyframes sway {
            0% { transform: translateX(0) rotate(0deg); }
            50% { transform: translateX(8px) rotate(2deg); }
            100% { transform: translateX(0) rotate(0deg); }
        }

        /* little animated sparkles using pseudo elements */
        .header::before {
            content: '';
            position: absolute;
            top: -20px;
            left: -40px;
            width: 240px;
            height: 240px;
            background: radial-gradient(circle at 20% 20%, rgba(255,107,107,0.08), transparent 15%),
                        radial-gradient(circle at 80% 80%, rgba(120,113,255,0.06), transparent 15%);
            z-index: 0;
            transform: rotate(5deg);
            pointer-events: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="position:relative;min-height:80px;">
                <div class="logo animate__animated animate__bounceIn">
                    <!-- Inline anime-styled crest SVG -->
                    <svg class="logo-icon" width="56" height="56" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="g1" x1="0" x2="1">
                                <stop offset="0" stop-color="#FF6B6B" />
                                <stop offset="1" stop-color="#FFA502" />
                            </linearGradient>
                        </defs>
                        <circle cx="32" cy="32" r="30" fill="url(#g1)" opacity="0.14" />
                        <path d="M20 44c6-6 18-6 24 0" stroke="#FF6B6B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M32 12c4 6 12 10 18 12-6 2-10 6-18 6s-12-4-18-6c6-2 14-6 18-12z" fill="#FF6B6B" />
                        <circle cx="32" cy="28" r="3" fill="#fff" opacity="0.9" />
                    </svg>
                    <div class="logo-text cyberpunk">JinShuaiGe Pro Max Premium</div>
                </div>
                <p class="subtitle animate__animated animate__fadeIn">
                    <i class="fas fa-robot mx-2"></i>
                    Tạo nội dung SEO tối ưu với AI - Nhanh chóng & Hiệu quả
                    <i class="fas fa-bolt mx-2"></i>
                </p>

                <!-- Left badge (small) -->
                <div class="lottie-box">
                    <lottie-player src="https://assets6.lottiefiles.com/packages/lf20_jbrw3hcz.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>
                </div>

                <!-- Single standing anime character (smaller, non-intrusive) -->
                <div class="lottie-character">
                    <lottie-player src="https://assets9.lottiefiles.com/packages/lf20_0yfsb3a1.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>
                </div>

                <!-- Small sparkle/light effects (CSS animated) -->
                <div class="sparkle-container" aria-hidden="true">
                    <svg class="sparkle s1" viewBox="0 0 10 10"><circle cx="5" cy="5" r="2" fill="#FFD166"/></svg>
                    <svg class="sparkle s2" viewBox="0 0 10 10"><circle cx="5" cy="5" r="1.6" fill="#FF6B6B"/></svg>
                    <svg class="sparkle s3" viewBox="0 0 10 10"><circle cx="5" cy="5" r="1.2" fill="#78B0FF"/></svg>
                </div>
            </div>
        </div>

        <div class="step-indicator">
            <div class="step active">
                <div class="step-number">1</div>
                <div class="step-label">Thông tin cơ bản</div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-label">Từ khóa & Liên kết</div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-label">Xem kết quả</div>
            </div>
        </div>

        <form method="post">
            <div class="card">
                <div class="card-header">
                    <h2 class="card-title"><svg class="icon icon-sword" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; margin-right:8px;"><path d="M3 21l18-18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 11l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg> Thông tin chính</h2>
                </div>
                <div class="card-body">
                    <div class="mb-4">
                            <label class="form-label"><svg class="icon icon-shuriken" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; margin-right:6px;"><path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3 3-7z" stroke="currentColor" stroke-width="0.9" stroke-linejoin="round" fill="none"/></svg> Từ khóa chính</label>
                        <input type="text" name="main_kw" class="form-control" placeholder="Ví dụ: World Cup 2026, Công nghệ AI, Du lịch Việt Nam" required>
                        <div class="form-hint">Từ khóa trung tâm cho nội dung của bạn</div>
                    </div>
                    
                    <div class="mb-4">
                            <label class="form-label"><svg class="icon icon-chain" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; margin-right:6px;"><path d="M10 14a3.5 3.5 0 0 1 0-5l2-2a3.5 3.5 0 0 1 5 5l-1 1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 10a3.5 3.5 0 0 1 0 5l-2 2a3.5 3.5 0 0 1-5-5l1-1" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg> Liên kết chính</label>
                        <input type="url" name="main_link" class="form-control" placeholder="https://example.com" required>
                        <div class="form-hint">URL đích chính cho chiến dịch SEO</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-header">
                    <h2 class="card-title"><svg class="icon icon-scroll" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; margin-right:8px;"><path d="M4 7v10a2 2 0 0 0 2 2h12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 7V5a2 2 0 0 1 2-2h2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg> Từ khóa phụ & Liên kết</h2>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6 mb-4">
                            <label class="form-label"><i class="fas fa-tags"></i> Từ khóa phụ</label>
                            <textarea name="sub_kw" class="form-control" placeholder="Mỗi dòng một từ khóa&#10;Ví dụ:&#10;World Cup 2026 vòng loại&#10;Đội tuyển World Cup&#10;Lịch thi đấu World Cup" required></textarea>
                            <div class="form-hint">Mỗi từ khóa phụ trên một dòng</div>
                        </div>
                        
                        <div class="col-md-6 mb-4">
                            <label class="form-label"><i class="fas fa-external-link-alt"></i> Liên kết phụ</label>
                            <textarea name="sub_links" class="form-control" placeholder="Mỗi dòng một URL&#10;Ví dụ:&#10;https://site1.com&#10;https://site2.com&#10;https://site3.com"></textarea>
                            <div class="form-hint">Liên kết bổ sung cho đa dạng hóa</div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label"><i class="fas fa-heading"></i> Tiêu đề đã thu thập</label>
                        <textarea name="titles" class="form-control" placeholder="Mỗi dòng một tiêu đề&#10;Ví dụ:&#10;World Cup 2026: Những điều cần biết&#10;Đội tuyển tham dự World Cup 2026&#10;Lịch thi đấu chi tiết World Cup"></textarea>
                        <div class="form-hint">Tiêu đề tương ứng với các liên kết phụ</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <div class="card-body">
                    <button type="submit" class="btn btn-primary">
                        <svg class="icon icon-spark" width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; margin-right:8px;"><path d="M12 2l1.6 4.3L18 8l-4 1.1L12 14l-2-4.9L6 8l4.4-1.7L12 2z" fill="currentColor"/></svg> Tạo nội dung AI
                    </button>
                </div>
            </div>
        </form>

        <div class="footer">
            <p>© 2024 JinShuaiGe Pro Max Premium | Powered by AI Technology</p>
        </div>
    </div>

    <script>
        // Simple form validation enhancement
        document.querySelector('form').addEventListener('submit', function(e) {
            const mainKw = document.querySelector('input[name="main_kw"]').value.trim();
            const mainLink = document.querySelector('input[name="main_link"]').value.trim();
            const subKw = document.querySelector('textarea[name="sub_kw"]').value.trim();
            
            if (!mainKw || !mainLink || !subKw) {
                e.preventDefault();
                alert('Vui lòng điền đầy đủ các trường bắt buộc: Từ khóa chính, Liên kết chính và Từ khóa phụ.');
            }
        });
    </script>
</body>
</html>
"""

# === KẾT QUẢ MỚI ===
# === KẾT QUẢ MỚI - HIỂN THỊ MỖI BÀI VIẾT TRÊN MỘT HÀNG ===
RESULT_HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kết quả - JinShuaiGe Pro Max Premium</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #64748b;
            --success: #10b981;
            --warning: #f59e0b;
            --background: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --border: #334155;
        }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--background) 0%, #1e1b4b 100%);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1.5rem 0;
        }

        .logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 1rem;
        }

        .logo-icon {
            font-size: 2.2rem;
            color: var(--warning);
        }

        .logo-text {
            font-size: 2.2rem;
            font-weight: 700;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 3px 3px 6px rgba(255, 107, 107, 0.3);
            letter-spacing: 2px;
            position: relative;
            animation: textGlow 2s ease-in-out infinite;
        }
        /* Extra decorations for result page */
        .result-lottie {
            position: absolute;
            right: 12px;
            top: 6px;
            width: 120px;
            z-index: 6;
            pointer-events: none;
            animation: floaty 5s ease-in-out infinite;
        }

        .result-anime {
            position: absolute;
            left: 8px;
            bottom: -6px;
            width: 140px;
            z-index: 4;
            pointer-events: none;
            animation: sway 5s ease-in-out infinite;
        }
        .result-lottie-2 {
            position: absolute;
            right: 180px;
            top: 0px;
            width: 100px;
            height: 100px;
            z-index: 6;
            pointer-events: none;
            animation: floaty 6s ease-in-out infinite;
        }
        .result-lottie-2 lottie-player { width:100%; height:100%; }

        @media (max-width: 768px) {
            .result-lottie, .result-lottie-2 { display: none; }
        }
        
        .cyberpunk {
            position: relative;
            display: inline-block;
        }
        
        .cyberpunk::before,
        .cyberpunk::after {
            content: attr(data-text);
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            opacity: 0.8;
        }
        
        .cyberpunk::before {
            animation: glitch-1 2s infinite linear alternate-reverse;
            text-shadow: 2px 0 #ff0000;
            left: 2px;
        }
        
        .cyberpunk::after {
            animation: glitch-2 3s infinite linear alternate-reverse;
            text-shadow: -2px 0 #00ff00;
            left: -2px;
        }
        
        @keyframes glitch-1 {
            0% { clip-path: inset(20% 0 30% 0); }
            100% { clip-path: inset(10% 0 40% 0); }
        }
        
        @keyframes glitch-2 {
            0% { clip-path: inset(40% 0 10% 0); }
            100% { clip-path: inset(30% 0 20% 0); }
        }
        
        @keyframes textGlow {
            0%, 100% { text-shadow: 0 0 10px var(--primary), 0 0 20px var(--primary); }
            50% { text-shadow: 0 0 20px var(--primary), 0 0 30px var(--primary); }
        }

        /* single small character and subtle sparkles for result page */
        .result-lottie-character {
            position: absolute;
            right: 8px;
            top: 8px;
            width: 110px;
            height: 150px;
            z-index: 6;
            pointer-events: none;
            animation: floaty 5s ease-in-out infinite;
        }

        .result-lottie-character lottie-player { width:100%; height:100%; }

        .result-sparkles { position:absolute; left:40%; top:8px; width:200px; height:120px; pointer-events:none; z-index:5; }
        .result-sparkles .sparkle { position:absolute; width:12px; height:12px; opacity:0; }
        .result-sparkles .s1 { left:5%; top:30%; animation: sparklePop 3.5s infinite; }
        .result-sparkles .s2 { left:40%; top:10%; animation: sparklePop 4s 0.4s infinite; }
        .result-sparkles .s3 { left:75%; top:35%; animation: sparklePop 3s 0.2s infinite; }

        @media (max-width: 768px) {
            .result-lottie-character { display:none; }
            .result-sparkles { display:none; }
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .btn-back {
            background: var(--card-bg);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s ease;
            margin-bottom: 1.5rem;
        }

        .btn-back:hover {
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }

        .articles-table {
            background: var(--card-bg);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }

        .table-header {
            background: rgba(30, 41, 59, 0.9);
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
        }

        .table-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .table-title i {
            color: var(--primary);
        }

        .article-row {
            display: grid;
            grid-template-columns: 80px 1fr 2fr 1fr 1fr;
            gap: 1rem;
            padding: 1.5rem;
            border-bottom: 1px solid var(--border);
            align-items: start;
            transition: all 0.3s ease;
        }

        .article-row:hover {
            background: rgba(15, 23, 42, 0.5);
        }

        .article-row:last-child {
            border-bottom: none;
        }

        .article-number {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
        }

        .article-badge {
            background: var(--primary);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 1rem;
        }

        .article-title-section {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .article-main-title {
            font-weight: 600;
            color: var(--text-primary);
            line-height: 1.4;
        }

        .article-content-section {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .content-item {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }

        .content-item:hover {
            border-color: var(--primary);
            background: rgba(15, 23, 42, 0.7);
        }

        .content-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .content-label i {
            color: var(--primary);
            font-size: 0.7rem;
        }

        .content-text {
            font-size: 0.875rem;
            line-height: 1.4;
            color: var(--text-primary);
            word-break: break-word;
        }

        .links-section {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .actions-section {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .btn-copy {
            background: rgba(37, 99, 235, 0.1);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 4px;
            width: 100%;
        }

        .btn-copy:hover {
            background: var(--primary);
            color: white;
        }

        .link-item {
            display: block;
            padding: 0.5rem 0.75rem;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 6px;
            text-decoration: none;
            color: var(--text-primary);
            border: 1px solid transparent;
            font-size: 0.8rem;
            transition: all 0.3s ease;
            word-break: break-all;
        }

        .link-item:hover {
            background: rgba(37, 99, 235, 0.1);
            border-color: var(--primary);
            color: var(--text-primary);
            text-decoration: none;
        }

        .embedded-links {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .embedded-link {
            font-size: 0.8rem;
            padding: 0.25rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .embedded-link:last-child {
            border-bottom: none;
        }

        .toast {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: var(--success);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s ease;
        }

        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }

        .stats {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
        }

        .stat-item {
            text-align: center;
            padding: 0.5rem;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 8px;
            flex: 1;
        }

        .stat-value {
            font-size: 1rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.125rem;
        }

        .stat-label {
            font-size: 0.7rem;
            color: var(--text-secondary);
        }

        @media (max-width: 1200px) {
            .article-row {
                grid-template-columns: 60px 1fr 1fr;
                gap: 1rem;
            }
            
            .links-section, .actions-section {
                grid-column: span 2;
            }
        }

        @media (max-width: 768px) {
            .container {
                padding: 0 10px;
            }
            
            .article-row {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
            
            .article-number {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }
            
            .stats {
                flex-direction: column;
            }
            
            .actions-section {
                flex-direction: row;
                flex-wrap: wrap;
            }
            
            .btn-copy {
                width: auto;
                flex: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="position:relative; min-height:72px;">
                <div class="logo">
                    <!-- Result page inline crest to match form -->
                    <svg class="logo-icon" width="52" height="52" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <linearGradient id="g2" x1="0" x2="1">
                                <stop offset="0" stop-color="#7871FF" />
                                <stop offset="1" stop-color="#00D2D3" />
                            </linearGradient>
                        </defs>
                        <circle cx="32" cy="32" r="28" fill="url(#g2)" opacity="0.12" />
                        <path d="M18 42c6-6 18-6 24 0" stroke="#7871FF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" />
                        <path d="M32 10c4 6 12 10 18 12-6 2-10 6-18 6s-12-4-18-6c6-2 14-6 18-12z" fill="#7871FF" />
                        <circle cx="32" cy="26" r="3" fill="#fff" opacity="0.9" />
                    </svg>
                    <div class="logo-text">JinShuaiGe Pro Max Premium</div>
                </div>
                <p class="subtitle">Kết quả nội dung đã được tạo thành công - {{ articles|length }} bài viết</p>

                <!-- Single small result character + sparkles -->
                <div class="result-lottie-character">
                    <lottie-player src="https://assets9.lottiefiles.com/packages/lf20_0yfsb3a1.json"  background="transparent"  speed="1"  loop  autoplay></lottie-player>
                </div>
                <div class="result-sparkles" aria-hidden="true">
                    <svg class="sparkle s1" viewBox="0 0 10 10"><circle cx="5" cy="5" r="2" fill="#FFD166"/></svg>
                    <svg class="sparkle s2" viewBox="0 0 10 10"><circle cx="5" cy="5" r="1.6" fill="#FF6B6B"/></svg>
                    <svg class="sparkle s3" viewBox="0 0 10 10"><circle cx="5" cy="5" r="1.2" fill="#78B0FF"/></svg>
                </div>
            </div>
        </div>

        <a href="/" class="btn-back">
            <i class="fas fa-arrow-left"></i> Quay lại tạo mới
        </a>

        <div class="articles-table">
            <div class="table-header">
                <h2 class="table-title"><i class="fas fa-newspaper"></i> Danh sách bài viết đã tạo</h2>
            </div>

            {% for a in articles %}
            <div class="article-row">
                <div class="article-number">
                    <div class="article-badge">{{ a.no }}</div>
                </div>

                <div class="article-title-section">
                    <div class="content-item">
                        <div class="content-label"><i class="fas fa-heading"></i> TIÊU ĐỀ</div>
                        <div class="content-text">{{ a.title }}</div>
                    </div>
                    
                    <div class="content-item">
                        <div class="content-label"><i class="fas fa-robot"></i> NỘI DUNG AI</div>
                        <div class="content-text" id="ai_content_{{ a.no }}">
                            {{ a.ai_html|safe }}
                        </div>
                    </div>
                </div>

                <div class="article-content-section">
                    <div class="content-item">
                        <div class="content-label"><i class="fas fa-sitemap"></i> LIÊN KẾT NHÚNG ({{ a.embedded|length }})</div>
                        <div class="embedded-links" id="embedded_{{ a.no }}">
                            {% for t in a.embedded %}
                            <div class="embedded-link">{{ t.html|safe }}</div>
                            {% endfor %}
                        </div>
                    </div>
                </div>

                <div class="links-section">
                    <div class="content-item">
                        <div class="content-label"><i class="fas fa-link"></i> LIÊN KẾT CHÍNH</div>
                        <a href="{{ a.main_link }}" target="_blank" class="link-item">
                            <i class="fas fa-external-link-alt"></i> {{ a.main_link }}
                        </a>
                    </div>
                    
                    <div class="content-item">
                        <div class="content-label"><i class="fab fa-microsoft"></i> BING SEARCH</div>
                        <a href="{{ a.bing_link }}" target="_blank" class="link-item">
                            <i class="fas fa-search"></i> {{ a.bing_link|truncate(50) }}
                        </a>
                    </div>
                </div>

                <div class="actions-section">
                    <button class="btn-copy" onclick="copyText('{{ a.title|e }}', 'Tiêu đề bài {{ a.no }}')">
                        <i class="fas fa-copy"></i> Copy Tiêu đề
                    </button>
                    <button class="btn-copy" onclick="copyBlock('ai_content_{{ a.no }}', 'Nội dung AI bài {{ a.no }}')">
                        <i class="fas fa-copy"></i> Copy Nội dung AI
                    </button>
                    <button class="btn-copy" onclick="copyBlock('embedded_{{ a.no }}', 'Liên kết nhúng bài {{ a.no }}')">
                        <i class="fas fa-copy"></i> Copy Links nhúng
                    </button>
                    <button class="btn-copy" onclick="copyText('{{ a.main_link|e }}', 'Link chính bài {{ a.no }}')">
                        <i class="fas fa-copy"></i> Copy Link chính
                    </button>

                      <button class="btn-copy" onclick="copyText('{{a.bing_link|e}}', 'Liên kết Bing bài {{a.no}}')">
                        <i class="fas fa-copy"></i> Copy Bing Link
                    </button>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="articles-table">
            <div class="table-header">
                <h2 class="table-title"><i class="fas fa-chart-bar"></i> Thống kê tổng quan</h2>
            </div>
            <div class="article-row">
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value">{{ articles|length }}</div>
                        <div class="stat-label">Tổng bài viết</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ articles|length * 3 }}</div>
                        <div class="stat-label">Liên kết phụ</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{{ articles|length }}</div>
                        <div class="stat-label">Liên kết chính</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">AI</div>
                        <div class="stat-label">Nội dung chất lượng</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="toast" class="toast">
        <i class="fas fa-check-circle"></i>
        <span id="toast-message">Đã sao chép thành công!</span>
    </div>

    <script>
        function showToast(message) {
            const toast = document.getElementById('toast');
            const toastMessage = document.getElementById('toast-message');
            
            toastMessage.textContent = message;
            toast.classList.add('show');
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }

        function copyText(text, type) {
            navigator.clipboard.writeText(text).then(() => {
                showToast(`✅ Đã sao chép ${type.toLowerCase()}!`);
            }).catch(err => {
                showToast('❌ Lỗi khi sao chép!');
            });
        }

        function copyBlock(id, type) {
            const element = document.getElementById(id);
            let content = element.innerHTML.trim();
            
            const blobHTML = new Blob([content], { type: "text/html" });
            const blobText = new Blob([content.replace(/<[^>]+>/g, '')], { type: "text/plain" });
            
            navigator.clipboard.write([
                new ClipboardItem({
                    "text/html": blobHTML,
                    "text/plain": blobText
                })
            ]).then(() => {
                showToast(`✅ Đã sao chép ${type.toLowerCase()}!`);
            }).catch(err => {
                // Fallback to plain text
                navigator.clipboard.writeText(content.replace(/<[^>]+>/g, '')).then(() => {
                    showToast(`✅ Đã sao chép ${type.toLowerCase()} (văn bản thuần)!`);
                });
            });
        }

        // Auto-adjust row heights for better alignment
        document.addEventListener('DOMContentLoaded', function() {
            const rows = document.querySelectorAll('.article-row');
            rows.forEach(row => {
                const titleSection = row.querySelector('.article-title-section');
                const contentSection = row.querySelector('.article-content-section');
                
                if (titleSection && contentSection) {
                    const titleHeight = titleSection.offsetHeight;
                    const contentHeight = contentSection.offsetHeight;
                    const maxHeight = Math.max(titleHeight, contentHeight);
                    
                    titleSection.style.minHeight = maxHeight + 'px';
                    contentSection.style.minHeight = maxHeight + 'px';
                }
            });
        });
    </script>
</body>
</html>
"""

# === ROUTE CHÍNH ===
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template_string(FORM_HTML)

    main_kw = request.form.get("main_kw","").strip()
    sub_kw = [x.strip() for x in request.form.get("sub_kw","").splitlines() if x.strip()]
    main_link = request.form.get("main_link","").strip()
    sub_links = [x.strip() for x in request.form.get("sub_links","").splitlines() if x.strip()]
    titles = [x.strip() for x in request.form.get("titles","").splitlines() if x.strip()]

    articles = []
    link_idx = 0
    title_idx = 0
    n = len(sub_kw)

    for i, kw in enumerate(sub_kw):
        sub1 = sub_kw[i % n]
        sub2 = sub_kw[(i+1) % n] if n > 1 else sub_kw[i % n]
        title = f"{main_kw}-{sub1}-{sub2}"

        ai_html = generate_ai_content(main_kw, main_link)

        embedded = []
        for _ in range(3):
            if title_idx < len(titles):
                t = titles[title_idx]
                l = sub_links[link_idx] if link_idx < len(sub_links) else "#"
                html = f'<a href="{l}" target="_blank">{t}</a>'
                embedded.append({"html": html})
                title_idx += 1
                link_idx += 1

        bing_link = f"https://www.bing.com/search?q={urllib.parse.quote_plus(title)}"

        articles.append({
            "no": i+1,
            "title": title,
            "ai_html": ai_html,  # HTML có link nhúng
            "main_link": main_link,
            "embedded": embedded,
            "bing_link": bing_link
        })

    return render_template_string(RESULT_HTML, articles=articles)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
