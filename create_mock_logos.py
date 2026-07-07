import os
import base64

# Define output folders
SVG_DIR = r"saudi-logos/public/files/svg"
PNG_DIR = r"saudi-logos/public/files/png"
PDF_DIR = r"saudi-logos/public/files/pdf"

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Helper: A tiny 1x1 transparent PNG file as base64 to write mock PNGs
TINY_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
TINY_PNG_BYTES = base64.b64decode(TINY_PNG_B64)

# SVG templates for each logo
SVGS = {
    "vision-2030": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <radialGradient id="gold-glow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="#f59e0b" stop-opacity="1"/>
                <stop offset="100%" stop-color="#d97706" stop-opacity="1"/>
            </radialGradient>
            <linearGradient id="saudi-green" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#10b981"/>
                <stop offset="100%" stop-color="#047857"/>
            </linearGradient>
        </defs>
        <circle cx="200" cy="200" r="180" fill="none" stroke="url(#saudi-green)" stroke-width="6"/>
        <circle cx="200" cy="200" r="150" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="10 5"/>
        <g transform="translate(200, 200)">
            <!-- Stylized Sun/Starburst representing Vision 2030 -->
            <path d="M 0,-80 L 15,-20 L 75,-35 L 30,10 L 60,60 L 0,30 L -60,60 L -30,10 L -75,-35 L -15,-20 Z" fill="url(#gold-glow)"/>
            <circle cx="0" cy="0" r="35" fill="#047857"/>
            <!-- Palm Tree in center -->
            <path d="M-5,15 C-5,5 -15,-5 -25,-10 C-15,-15 -5,-25 -2,-35 C2,-35 15,-15 25,-10 C15,-5 5,5 5,15 Z" fill="#ffffff"/>
            <rect x="-3" y="15" width="6" height="20" rx="2" fill="#ffffff"/>
        </g>
        <text x="200" y="320" font-family="'Tajawal', sans-serif" font-weight="900" font-size="28" fill="#10b981" text-anchor="middle">VISION رؤيــــة</text>
        <text x="200" y="355" font-family="'Tajawal', sans-serif" font-weight="800" font-size="36" fill="#d97706" text-anchor="middle">2030</text>
    </svg>""",

    "ministry-of-education": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <linearGradient id="edu-green" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#059669"/>
                <stop offset="100%" stop-color="#064e3b"/>
            </linearGradient>
        </defs>
        <!-- Dynamic shapes forming an open book and a flying bird/progress -->
        <g transform="translate(200, 180)" fill="url(#edu-green)">
            <!-- Left Wing / Pages -->
            <path d="M-10,30 C-40,-20 -90,-40 -130,-40 C-90,0 -40,40 -10,70 Z"/>
            <path d="M-10,0 C-35,-40 -75,-55 -110,-55 C-80,-20 -35,20 -10,40 Z" opacity="0.8"/>
            <path d="M-10,-30 C-30,-60 -60,-70 -90,-70 C-70,-40 -30,-10 -10,10 Z" opacity="0.6"/>
            
            <!-- Right Wing / Pages -->
            <path d="M10,30 C40,-20 90,-40 130,-40 C90,0 40,40 10,70 Z"/>
            <path d="M10,0 C35,-40 75,-55 110,-55 C80,-20 35,20 10,40 Z" opacity="0.8"/>
            <path d="M10,-30 C30,-60 60,-70 90,-70 C70,-40 30,-10 10,10 Z" opacity="0.6"/>
            
            <!-- Center Flame/Torch of knowledge -->
            <path d="M0,20 C-10,5 0,-25 0,-45 C0,-25 10,5 0,20 Z" fill="#d97706"/>
        </g>
        <text x="200" y="315" font-family="'Tajawal', sans-serif" font-weight="800" font-size="28" fill="#064e3b" text-anchor="middle">وزارة التعليــم</text>
        <text x="200" y="345" font-family="'Tajawal', sans-serif" font-weight="500" font-size="14" fill="#94a3b8" text-anchor="middle">Ministry of Education</text>
    </svg>""",

    "aramco": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <linearGradient id="aramco-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#8ce8a4"/>
                <stop offset="50%" stop-color="#00a896"/>
                <stop offset="100%" stop-color="#028090"/>
            </linearGradient>
        </defs>
        <!-- Abstract star/oil-drop graphic representing energy -->
        <g transform="translate(200, 180)">
            <circle cx="0" cy="0" r="80" fill="none" stroke="url(#aramco-grad)" stroke-width="12"/>
            <!-- Starburst rays inside -->
            <path d="M0,-80 L0,-40 M0,80 L0,40 M-80,0 L-40,0 M80,0 L40,0 M-56,-56 L-28,-28 M56,56 L28,28 M-56,56 L-28,28 M56,-56 L28,-28" stroke="url(#aramco-grad)" stroke-width="8" stroke-linecap="round"/>
            <circle cx="0" cy="0" r="20" fill="#00a896"/>
        </g>
        <text x="200" y="310" font-family="'Tajawal', sans-serif" font-weight="900" font-size="38" fill="#028090" text-anchor="middle">أرامكو aramco</text>
        <text x="200" y="340" font-family="'Tajawal', sans-serif" font-weight="500" font-size="16" fill="#94a3b8" text-anchor="middle">أرامكو السعودية / Saudi Aramco</text>
    </svg>""",

    "neom": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <!-- NEOM logo: clean geometric shapes representing N E O M -->
        <g transform="translate(80, 130)">
            <!-- N: green lines -->
            <path d="M10,100 L10,10 L80,100 L80,10" fill="none" stroke="#10b981" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- E: blue lines -->
            <path d="M175,10 L120,10 L120,100 L175,100 M120,55 L165,55" fill="none" stroke="#3b82f6" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- O: purple circle -->
            <circle cx="230" cy="55" r="45" fill="none" stroke="#8b5cf6" stroke-width="15"/>
            <!-- M: gold/orange -->
            <path d="M295,100 L295,10 L325,60 L355,10 L355,100" fill="none" stroke="#f59e0b" stroke-width="15" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
        <text x="200" y="280" font-family="'Tajawal', sans-serif" font-weight="900" font-size="36" fill="#0f172a" text-anchor="middle">نـيــــوم NEOM</text>
        <text x="200" y="320" font-family="'Tajawal', sans-serif" font-weight="600" font-size="16" fill="#10b981" text-anchor="middle">معيشة مستقبلية ذكية ومستدامة</text>
    </svg>""",

    "sdaia": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <linearGradient id="sdaia-grad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#0284c7"/>
                <stop offset="100%" stop-color="#0f766e"/>
            </linearGradient>
        </defs>
        <!-- Data nodes and neural network theme -->
        <g transform="translate(200, 160)" stroke="url(#sdaia-grad)" stroke-width="4" fill="none">
            <polygon points="0,-70 60,-30 60,40 0,80 -60,40 -60,-30"/>
            <line x1="0" y1="-70" x2="0" y2="80"/>
            <line x1="-60" y1="-30" x2="60" y2="40"/>
            <line x1="60" y1="-30" x2="-60" y2="40"/>
            <!-- Nodes -->
            <circle cx="0" cy="-70" r="10" fill="#0284c7" stroke="#fff" stroke-width="2"/>
            <circle cx="60" cy="-30" r="10" fill="#0f766e" stroke="#fff" stroke-width="2"/>
            <circle cx="60" cy="40" r="10" fill="#10b981" stroke="#fff" stroke-width="2"/>
            <circle cx="0" cy="80" r="10" fill="#0284c7" stroke="#fff" stroke-width="2"/>
            <circle cx="-60" cy="40" r="10" fill="#0f766e" stroke="#fff" stroke-width="2"/>
            <circle cx="-60" cy="-30" r="10" fill="#10b981" stroke="#fff" stroke-width="2"/>
            <circle cx="0" cy="5" r="15" fill="url(#sdaia-grad)" stroke="#fff" stroke-width="2"/>
        </g>
        <text x="200" y="305" font-family="'Tajawal', sans-serif" font-weight="900" font-size="24" fill="#0f766e" text-anchor="middle">سـدايـا SDAIA</text>
        <text x="200" y="335" font-family="'Tajawal', sans-serif" font-weight="700" font-size="12" fill="#94a3b8" text-anchor="middle">الهيئة السعودية للبيانات والذكاء الاصطناعي</text>
    </svg>""",

    "king-saud-university": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <!-- University Shield -->
        <g transform="translate(200, 160)">
            <path d="M-70,-80 L70,-80 L70,-10 C70,40 0,90 0,90 C0,90 -70,40 -70,-10 Z" fill="#0f172a" stroke="#d97706" stroke-width="6"/>
            <!-- Palm Tree in center of shield -->
            <path d="M-8,10 C-8,0 -20,-10 -30,-15 C-20,-20 -8,-30 -5,-40 C2,-40 15,-20 25,-15 C15,-10 5,0 5,10 Z" fill="#d97706"/>
            <rect x="-4" y="10" width="8" height="30" fill="#d97706"/>
            <!-- Swords crossing under palm -->
            <path d="M-40,45 L40,-35 M40,45 L-40,-35" stroke="#ffffff" stroke-width="4" stroke-linecap="round"/>
        </g>
        <text x="200" y="300" font-family="'Tajawal', sans-serif" font-weight="800" font-size="26" fill="#0f172a" text-anchor="middle">جامعة الملك سعود</text>
        <text x="200" y="330" font-family="'Tajawal', sans-serif" font-weight="500" font-size="15" fill="#94a3b8" text-anchor="middle">King Saud University</text>
    </svg>""",

    "saudia": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <linearGradient id="saudia-gold" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#b45309"/>
                <stop offset="100%" stop-color="#f59e0b"/>
            </linearGradient>
        </defs>
        <!-- Stylized Palm Tree and Swords in circular flow (Saudia airline branding style) -->
        <circle cx="200" cy="160" r="85" fill="none" stroke="url(#saudia-gold)" stroke-width="3"/>
        <g transform="translate(200, 165)">
            <!-- Palm Tree -->
            <path d="M-6,5 C-6,-5 -18,-15 -25,-20 C-15,-25 -6,-35 -3,-45 C2,-45 12,-25 22,-20 C12,-15 5,-5 5,5 Z" fill="#047857"/>
            <rect x="-3" y="5" width="6" height="25" fill="#047857"/>
            <!-- Swords -->
            <path d="M-30,35 Q0,25 30,35" fill="none" stroke="url(#saudia-gold)" stroke-width="5" stroke-linecap="round"/>
            <path d="M-35,25 L-25,45 M35,25 L25,45" stroke="url(#saudia-gold)" stroke-width="3"/>
        </g>
        <text x="200" y="300" font-family="'Tajawal', sans-serif" font-weight="900" font-size="34" fill="#047857" text-anchor="middle">السـعودية SAUDIA</text>
        <text x="200" y="330" font-family="'Tajawal', sans-serif" font-weight="500" font-size="14" fill="#94a3b8" text-anchor="middle">عضو تحالف سكاي تيم / SkyTeam Member</text>
    </svg>""",

    "ministry-of-health": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <defs>
            <linearGradient id="health-green" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#10b981"/>
                <stop offset="100%" stop-color="#047857"/>
            </linearGradient>
        </defs>
        <!-- Palm Tree flanked by two caring hands/crescents -->
        <g transform="translate(200, 160)">
            <!-- Caring hands / crescent shield -->
            <path d="M-80,-20 C-80,40 -20,80 0,80 C20,80 80,40 80,-20" fill="none" stroke="url(#health-green)" stroke-width="8" stroke-linecap="round"/>
            <!-- Palm Tree -->
            <path d="M-6,0 C-6,-10 -18,-20 -25,-25 C-15,-30 -6,-40 -3,-50 C2,-50 12,-30 22,-25 C12,-20 5,-10 5,0 Z" fill="#047857"/>
            <rect x="-3" y="0" width="6" height="30" fill="#047857"/>
            <!-- Small golden crescent in center -->
            <path d="M-15,40 A 15,15 0 0,0 15,40 A 12,12 0 0,1 -15,40 Z" fill="#d97706"/>
        </g>
        <text x="200" y="295" font-family="'Tajawal', sans-serif" font-weight="800" font-size="28" fill="#047857" text-anchor="middle">وزارة الصحـة</text>
        <text x="200" y="325" font-family="'Tajawal', sans-serif" font-weight="500" font-size="15" fill="#94a3b8" text-anchor="middle">Ministry of Health</text>
    </svg>""",

    "al-hilal-fc": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
        <!-- Al Hilal Shield (crescent and ball) in deep blue -->
        <defs>
            <linearGradient id="hilal-blue" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#1e40af"/>
                <stop offset="100%" stop-color="#1d4ed8"/>
            </linearGradient>
        </defs>
        <path d="M200,50 C280,50 320,100 320,180 C320,260 250,330 200,350 C150,330 80,260 80,180 C80,100 120,50 200,50 Z" fill="url(#hilal-blue)"/>
        <!-- Golden / White Crescent -->
        <path d="M150,140 A 60,60 0 1,1 250,220 A 70,70 0 1,0 150,140 Z" fill="#ffffff"/>
        <!-- Starburst / Soccer ball shape in center -->
        <circle cx="210" cy="170" r="18" fill="#1e40af" stroke="#ffffff" stroke-width="3"/>
        <text x="200" y="290" font-family="'Tajawal', sans-serif" font-weight="900" font-size="24" fill="#ffffff" text-anchor="middle">الـهـلال ALHILAL</text>
        <text x="200" y="320" font-family="'Tajawal', sans-serif" font-weight="600" font-size="12" fill="#93c5fd" text-anchor="middle">نادي القرن الآسيوي / Saudi Club</text>
    </svg>"""
}

# Write SVGs
for slug, content in SVGS.items():
    svg_path = os.path.join(SVG_DIR, f"{slug}.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created SVG: {svg_path}")

    # Write dummy PNG file
    png_path = os.path.join(PNG_DIR, f"{slug}.png")
    with open(png_path, "wb") as f:
        f.write(TINY_PNG_BYTES)
    print(f"Created PNG placeholder: {png_path}")

    # Write dummy PDF file (just simple text that acts as a PDF downloader trigger)
    pdf_path = os.path.join(PDF_DIR, f"{slug}.pdf")
    with open(pdf_path, "w", encoding="utf-8") as f:
        f.write(f"%PDF-1.4 mock content for {slug}")
    print(f"Created PDF placeholder: {pdf_path}")

print("All mock files created successfully!")
