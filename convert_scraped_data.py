import json
import re
import urllib.parse

# Load scraped files
with open("scraped_logos.json", "r", encoding="utf-8") as f:
    scraped_logos = json.load(f)

with open("scraped_categories.json", "r", encoding="utf-8") as f:
    scraped_cats = json.load(f)

# Map category ID -> Category Name
cat_map = {c["id"]: c["name"] for c in scraped_cats}

# Map scraped category name -> our simplified category IDs
def get_our_category(cat_name):
    if not cat_name:
        return "private"
    cat_name = cat_name.strip()
    
    gov_keywords = ["حكومية", "رسمية", "عسكرية", "أمنية", "صحي", "وزارة", "هيئة"]
    edu_keywords = ["تعليم", "جامع", "كلي", "تدريب", "مدارس"]
    sports_keywords = ["رياض", "نادي", "أندية", "اتحاد"]
    vision_keywords = ["رؤية", "2030", "مشاريع كبرى", "نيوم"]
    
    if any(k in cat_name for k in gov_keywords):
        return "government"
    if any(k in cat_name for k in edu_keywords):
        return "education"
    if any(k in cat_name for k in sports_keywords):
        return "sports"
    if any(k in cat_name for k in vision_keywords):
        return "vision"
    
    return "private"

processed_logos = []
seen_slugs = set()

# Process each logo
for logo in scraped_logos:
    if logo.get("status") != "approved":
        continue
        
    title = logo.get("title", "")
    if not title:
        continue
        
    # Clean up the Arabic title
    # Split by common separators: - or | or / or " - "
    parts = re.split(r'[-|/]', title)
    ar_title = parts[0].strip()
    
    # Strip "شعار" prefix if it exists
    if ar_title.startswith("شعار "):
        ar_title = ar_title[len("شعار "):].strip()
    if ar_title.startswith("شعار"):
        ar_title = ar_title[4:].strip()
        
    # Strip common suffixes
    ar_title = re.sub(r'\s+(الجديد|جديد|المعتمد|الرسمي|قديم|القديم)\s*$', '', ar_title)
    ar_title = ar_title.strip()
    
    # English title fallback from title parts
    en_title = ""
    if len(parts) > 1:
        # Check if the second part contains english letters
        candidate = parts[1].strip()
        if re.search(r'[a-zA-Z]', candidate):
            # Clean up words like "Logo", "PNG", "SVG"
            candidate = re.sub(r'(?i)\b(logo|png|svg|pdf|download|vector)\b', '', candidate).strip()
            # Remove trailing/leading spaces or dashes
            candidate = re.sub(r'^[-\s]+|[-\s]+$', '', candidate).strip()
            en_title = candidate
            
    if not en_title:
        # Fallback to display name_en if we can guess, or slug
        en_title = logo.get("name_en") or ""

    # Decode and clean Slug
    slug = logo.get("slug") or ""
    if slug:
        slug = urllib.parse.unquote(slug)
        # Decode and clean slug characters, keep arabic letters, numbers, and dashes
        slug = slug.lower().strip()
        slug = re.sub(r'[^a-zA-Z0-9\u0621-\u064A]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
    
    if not slug:
        slug = f"logo-{logo.get('display_id')}"
        
    # Deduplicate slugs
    base_slug = slug
    counter = 1
    while slug in seen_slugs:
        slug = f"{base_slug}-{counter}"
        counter += 1
    seen_slugs.add(slug)

    # Category
    cat_id = logo.get("category_id")
    scraped_cat_name = cat_map.get(cat_id, "غير مصنف")
    our_cat = get_our_category(scraped_cat_name)

    # URLs
    svg_path = logo.get("svg_url") or logo.get("image_url") or ""
    png_path = logo.get("png_url") or ""
    pdf_path = logo.get("identity_pdf_url") or ""
    
    # Ensure they are absolute URLs pointing to salogos CDN or website
    # Keep pdf_path empty if not a PDF file
    if pdf_path and not pdf_path.lower().endswith('.pdf'):
        pdf_path = ""

        
    # Tags
    tags = logo.get("tags") or []
    if not isinstance(tags, list):
        tags = []
    # Add category names and titles as tags
    tags.extend([ar_title, scraped_cat_name])
    if en_title:
        tags.append(en_title)
    tags = list(set([t.strip() for t in tags if t and len(t.strip()) > 1]))

    # Date
    created_at = logo.get("created_at") or "2026-07-07"
    date_added = created_at.split("T")[0]

    # Description
    description = logo.get("excerpt") or logo.get("image_description") or ""
    if not description:
        description = f"الشعار الرسمي لـ {ar_title} بدقة عالية متوفر للتحميل بصيغ متعددة."

    processed_logos.append({
        "slug": slug,
        "name_ar": ar_title,
        "name_en": en_title or ar_title,
        "category": our_cat,
        "description": description,
        "tags": tags,
        "svg_path": svg_path,
        "png_path": png_path,
        "pdf_path": pdf_path,
        "downloads": logo.get("download_count") or 0,
        "date_added": date_added
    })

# Save new database
output_file = "src/data/logos.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(processed_logos, f, indent=2, ensure_ascii=False)

print(f"🎉 Successfully converted {len(processed_logos)} logos into {output_file}!")
