import os
import json
import shutil

# Paths configuration
SRC_DIR = "src"
DATA_FILE = os.path.join(SRC_DIR, "data", "logos.json")
BRAND_MANUALS_FILE = os.path.join(SRC_DIR, "data", "brand_manuals.json")
TEMPLATES_DIR = os.path.join(SRC_DIR, "templates")
PUBLIC_DIR = "public"
DIST_DIR = "dist"

CATEGORIES = {
    "government": "جهات حكومية",
    "private": "شركات وخاص",
    "education": "تعليم وجامعات",
    "sports": "رياضة وأندية",
    "vision": "مشاريع ورؤية 2030"
}

def load_logos():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_and_setup_dist():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR, exist_ok=True)
    
    # Copy public assets to dist
    if os.path.exists(PUBLIC_DIR):
        for item in os.listdir(PUBLIC_DIR):
            s = os.path.join(PUBLIC_DIR, item)
            d = os.path.join(DIST_DIR, item)
            if os.path.isdir(s):
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
    print("✓ Copied public assets to dist/")

    # Also copy the data logos.json file directly to dist so JavaScript can fetch it
    shutil.copy2(DATA_FILE, os.path.join(DIST_DIR, "logos.json"))
    if os.path.exists(BRAND_MANUALS_FILE):
        shutil.copy2(BRAND_MANUALS_FILE, os.path.join(DIST_DIR, "brand_manuals.json"))
    print("✓ Copied logos.json and brand_manuals.json databases to dist/ for search availability")

def load_template(name):
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_logo_card(logo):
    cat_display = CATEGORIES.get(logo["category"], logo["category"])
    downloads_display = f"{logo['downloads']:,}"
    return f"""
    <div class="logo-card">
      <a href="/logos/{logo['slug']}">
        <div class="logo-preview-box">
          <img src="{logo['svg_path']}" alt="{logo['name_ar']}" class="logo-preview-img" loading="lazy">
        </div>
      </a>
      <div class="logo-card-info">
        <span class="logo-card-cat">{cat_display}</span>
        <a href="/logos/{logo['slug']}">
          <h3 class="logo-card-title">{logo['name_ar']}</h3>
        </a>
        <div class="logo-card-meta">
          <span class="logo-card-downloads">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-left: 2px; vertical-align: middle;">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            {downloads_display} تحميل
          </span>
          <div class="logo-card-formats">
            <span class="format-badge">SVG</span>
            <span class="format-badge">PNG</span>
            <span class="format-badge">PDF</span>
          </div>
        </div>
      </div>
    </div>
    """

def render_guideline_card(gm):
    return f"""
    <div class="logo-card">
      <a href="{gm['pdf_url']}" target="_blank">
        <div class="logo-preview-box" style="height: 180px; padding: 0; background-color: #03070d; border-bottom: 1px solid var(--border-color); overflow: hidden; display: flex; align-items: center; justify-content: center;">
          <img src="{gm['thumbnail_url']}" alt="{gm['name_ar']}" style="width: 100%; height: 100%; object-fit: cover;" loading="lazy">
        </div>
      </a>
      <div class="logo-card-info" style="padding: 1.25rem;">
        <span class="logo-card-cat" style="background: rgba(217, 119, 6, 0.15); color: var(--accent-gold); font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 6px; font-weight: 700;">كتاب دليل الهوية</span>
        <a href="{gm['pdf_url']}" target="_blank" style="text-decoration: none;">
          <h3 class="logo-card-title" style="margin-top: 0.5rem; font-size: 0.95rem; font-weight: 700; color: var(--text-primary); text-overflow: ellipsis; overflow: hidden; white-space: nowrap;">{gm['name_ar']}</h3>
        </a>
        <div class="logo-card-meta" style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center;">
          <a href="{gm['pdf_url']}" target="_blank" class="btn-secondary" style="font-size: 0.75rem; padding: 0.4rem 0.8rem; border-radius: 6px; width: 100%; display: flex; justify-content: center; align-items: center; gap: 0.25rem; text-decoration: none; cursor: pointer;">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            تحميل الدليل (PDF)
          </a>
        </div>
      </div>
    </div>
    """

def compile_page(template_content, base_template, context):
    page = base_template
    # Replace content first
    page = page.replace("{{ content }}", template_content)
    
    # Replace metadata variables
    for key, val in context.items():
        placeholder = f"{{{{ {key} }}}}"
        page = page.replace(placeholder, str(val))
    
    # Clean remaining active states placeholders
    for active_tag in ["active_home", "active_browse", "active_guidelines", "active_request", "active_contact"]:
        page = page.replace(f"{{{{ {active_tag} }}}}", "")
        
    return page

def build_site():
    logos = load_logos()
    # Sort logos by downloads desc for recent/popular sorting
    logos_by_downloads = sorted(logos, key=lambda x: x["downloads"], reverse=True)
    # Sort by date added desc for recent additions
    logos_by_date = sorted(logos, key=lambda x: x["date_added"], reverse=True)
    
    clean_and_setup_dist()
    
    base_template = load_template("base.html")
    
    # 1. Build Home Page (index.html)
    print("Building Home Page...")
    home_content = load_template("home.html")
    
    # Generate recent logos list (first 6 items sorted by date)
    recent_logos_html = "".join([render_logo_card(l) for l in logos_by_date[:6]])
    home_content = home_content.replace("{{ recent_logos }}", recent_logos_html)
    
    # Calculate dynamic total logos count rounded to the nearest hundred (e.g. 1448 -> 1400)
    total_logos_count = (len(logos) // 100) * 100
    home_content = home_content.replace("{{ total_logos_count }}", f"{total_logos_count:,}")
    
    home_context = {
        "title": "شعارات السعودية - أكبر مكتبة رقمية للشعارات السعودية بدقة عالية",
        "meta_description": "تحميل شعارات الجهات الحكومية والوزارات والشركات والجامعات السعودية بدقة عالية مجاناً وبأحجام مرنة بصيغ SVG و PNG و PDF.",
        "canonical": "https://saudi-logos.vercel.app/",
        "og_title": "شعارات السعودية - مكتبة الشعارات السعودية المتكاملة",
        "og_description": "تحميل شعارات الجهات الحكومية والشركات والجامعات السعودية بدقة عالية مجاناً بصيغ SVG و PNG و PDF",
        "active_home": "active"
    }
    
    home_rendered = compile_page(home_content, base_template, home_context)
    with open(os.path.join(DIST_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_rendered)
    print("✓ Home Page built.")
        
    # 2. Build Browse Page (browse.html)
    print("Building Browse Page...")
    browse_content = load_template("browse.html")
    
    # Render all logos for static SEO indexing
    all_logos_html = "".join([render_logo_card(l) for l in logos_by_downloads])
    browse_content = browse_content.replace("{{ all_logos }}", all_logos_html)
    
    browse_context = {
        "title": "تصفح مكتبة الشعارات - شعارات السعودية",
        "meta_description": "البحث وتصفح جميع شعارات السعودية المصنفة حسب القطاعات: جهات حكومية، شركات خاصة، جامعات وتعليم، أندية رياضية، مشاريع الرؤية.",
        "canonical": "https://saudi-logos.vercel.app/browse",
        "og_title": "تصفح مكتبة شعارات السعودية",
        "og_description": "ابحث وحمّل شعارات الجهات الحكومية والشركات السعودية المتنوعة بدقة فيكتور عالية.",
        "active_browse": "active"
    }
    
    browse_rendered = compile_page(browse_content, base_template, browse_context)
    # Write both browse.html and browse/index.html for clean URLs routing compatibility
    with open(os.path.join(DIST_DIR, "browse.html"), "w", encoding="utf-8") as f:
        f.write(browse_rendered)
        
    os.makedirs(os.path.join(DIST_DIR, "browse"), exist_ok=True)
    with open(os.path.join(DIST_DIR, "browse", "index.html"), "w", encoding="utf-8") as f:
        f.write(browse_rendered)
    print("✓ Browse Page built.")
        
    # 3. Build Request Page (request.html)
    print("Building Request Page...")
    request_content = load_template("request.html")
    request_context = {
        "title": "طلب واقتراح شعار جديد - شعارات السعودية",
        "meta_description": "اطلب توفير شعار جديد لجهة حكومية أو شركة سعودية، أو أرسل شعارات بصيغة فيكتور لنشرها ومساعدتك للمصممين بالمملكة.",
        "canonical": "https://saudi-logos.vercel.app/request",
        "og_title": "طلب واقتراح شعار جديد - مكتبة شعارات السعودية",
        "og_description": "أرسل شعارك أو اطلب توفير شعار مخصص بدقة عالية من فريق عمل شعارات السعودية.",
        "active_request": "active"
    }
    request_rendered = compile_page(request_content, base_template, request_context)
    with open(os.path.join(DIST_DIR, "request.html"), "w", encoding="utf-8") as f:
        f.write(request_rendered)
        
    os.makedirs(os.path.join(DIST_DIR, "request"), exist_ok=True)
    with open(os.path.join(DIST_DIR, "request", "index.html"), "w", encoding="utf-8") as f:
        f.write(request_rendered)
    print("✓ Request Page built.")
        
    # 4. Build Contact Page (contact.html)
    print("Building Contact Page...")
    contact_content = load_template("contact.html")
    contact_context = {
        "title": "اتصل بنا - شعارات السعودية",
        "meta_description": "تواصل معنا لأي استفسارات أو مقترحات أو للإبلاغ عن حقوق ملكية فكرية أو تعديل شعار في مكتبة شعارات السعودية.",
        "canonical": "https://saudi-logos.vercel.app/contact",
        "og_title": "اتصل بنا - مكتبة شعارات السعودية",
        "og_description": "نموذج التواصل السريع مع إدارة منصة شعارات السعودية.",
        "active_contact": "active"
    }
    contact_rendered = compile_page(contact_content, base_template, contact_context)
    with open(os.path.join(DIST_DIR, "contact.html"), "w", encoding="utf-8") as f:
        f.write(contact_rendered)
        
    os.makedirs(os.path.join(DIST_DIR, "contact"), exist_ok=True)
    with open(os.path.join(DIST_DIR, "contact", "index.html"), "w", encoding="utf-8") as f:
        f.write(contact_rendered)
    print("✓ Contact Page built.")

    # 4.5. Build Guidelines Page (guidelines.html)
    print("Building Guidelines Page...")
    guidelines_content = load_template("guidelines.html")
    
    # Load brand manuals
    brand_manuals = []
    if os.path.exists(BRAND_MANUALS_FILE):
        with open(BRAND_MANUALS_FILE, "r", encoding="utf-8") as f:
            brand_manuals = json.load(f)
            
    # Sort brand manuals by date added desc
    brand_manuals_sorted = sorted(brand_manuals, key=lambda x: x.get("date_added", ""), reverse=True)
    all_guidelines_html = "".join([render_guideline_card(gm) for gm in brand_manuals_sorted])
    guidelines_content = guidelines_content.replace("{{ all_guidelines }}", all_guidelines_html)
    
    guidelines_context = {
        "title": "أدلة الهوية البصرية الرسمية - شعارات السعودية",
        "meta_description": "تحميل وقراءة كتب أدلة الهوية البصرية الرسمية للوزارات والجهات والشركات السعودية بصيغة PDF مباشرة.",
        "canonical": "https://saudi-logos.vercel.app/guidelines",
        "og_title": "أدلة الهوية البصرية الرسمية للجهات والشركات السعودية",
        "og_description": "تصفح وتحميل كتب أدلة تصميم الهوية البصرية المعتمدة للجهات الحكومية والشركات السعودية.",
        "active_guidelines": "active"
    }
    guidelines_rendered = compile_page(guidelines_content, base_template, guidelines_context)
    with open(os.path.join(DIST_DIR, "guidelines.html"), "w", encoding="utf-8") as f:
        f.write(guidelines_rendered)
        
    os.makedirs(os.path.join(DIST_DIR, "guidelines"), exist_ok=True)
    with open(os.path.join(DIST_DIR, "guidelines", "index.html"), "w", encoding="utf-8") as f:
        f.write(guidelines_rendered)
    print("✓ Guidelines Page built.")

    # 5. Build Individual Logo Pages (logos/[slug]/index.html)
    print("Building Logo Detail Pages...")
    detail_template = load_template("logo_detail.html")
    
    for logo in logos:
        # Generate related logos (up to 3, same category, excluding current)
        related = [l for l in logos if l["category"] == logo["category"] and l["slug"] != logo["slug"]]
        if len(related) < 3:
            # Fallback to other categories if not enough in same category
            fillers = [l for l in logos if l["slug"] != logo["slug"] and l not in related]
            related.extend(fillers[:3 - len(related)])
            
        related_html = "".join([render_logo_card(l) for l in related[:3]])
        
        # Build PDF download block conditionally
        pdf_path = logo["pdf_path"]
        if pdf_path and (pdf_path.lower().endswith(".pdf") or ".pdf" in pdf_path.lower()):
            pdf_download_block = f"""
          <!-- PDF Download -->
          <a href="{pdf_path}" download="Saudi-Logos-{logo['slug']}.pdf" class="download-item" onclick="triggerDownload('pdf', '{logo['name_ar']}')">
            <div class="download-meta">
              <div class="file-type-icon icon-pdf">PDF</div>
              <div class="download-details">
                <span class="download-title">صيغة PDF للطباعة</span>
                <span class="download-desc">ملف فيكتور جاهز للاستخدام المباشر في المطبوعات واللوحات</span>
              </div>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="color: var(--accent-green);">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </a>
            """
        else:
            pdf_download_block = ""

        # Build page variables
        logo_content = detail_template.replace("{{ related_logos }}", related_html)
        logo_content = logo_content.replace("{{ pdf_download_block }}", pdf_download_block)
        
        logo_context = {
            "slug": logo["slug"],
            "name_ar": logo["name_ar"],
            "name_en": logo["name_en"],
            "category_name": CATEGORIES.get(logo["category"], logo["category"]),
            "description": logo["description"],
            "svg_path": logo["svg_path"],
            "png_path": logo["png_path"],
            "pdf_path": logo["pdf_path"],
            "downloads": f"{logo['downloads']:,}",
            "date_added": logo["date_added"],
            
            # Global page metadata
            "title": f"تحميل شعار {logo['name_ar']} بدقة عالية SVG, PNG, PDF",
            "meta_description": f"تحميل الشعار الرسمي لـ {logo['name_ar']} بدقة عالية مجاناً. ملف فيكتور قابل للتعديل بصيغة SVG، خلفية مفرغة PNG، وملف طباعة PDF.",
            "canonical": f"https://saudi-logos.vercel.app/logos/{logo['slug']}",
            "og_title": f"تحميل شعار {logo['name_ar']} بدقة عالية - شعارات السعودية",
            "og_description": f"تحميل شعار {logo['name_ar']} متوفر بصيغ SVG و PNG و PDF للتحميل المجاني المباشر."
        }
        
        # Compile logo details content inside base layout
        logo_rendered = compile_page(logo_content, base_template, logo_context)
        
        # Write to logos/[slug]/index.html for clean SEO urls (/logos/vision-2030)
        logo_dir = os.path.join(DIST_DIR, "logos", logo["slug"])
        os.makedirs(logo_dir, exist_ok=True)
        with open(os.path.join(logo_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(logo_rendered)
            
        # Also write logos/[slug].html for vercel routing flexibility
        with open(os.path.join(DIST_DIR, "logos", f"{logo['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(logo_rendered)
            
        print(f"✓ Detail page built: {logo['slug']}")
        
    print("\n🎉 Website generation completed successfully!")

if __name__ == "__main__":
    build_site()
