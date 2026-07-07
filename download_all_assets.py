import os
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

# Target Directories
SVG_DIR = "public/files/svg"
PNG_DIR = "public/files/png"
PDF_DIR = "public/files/pdf"

os.makedirs(SVG_DIR, exist_ok=True)
os.makedirs(PNG_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# Load database
db_path = "src/data/logos.json"
if not os.path.exists(db_path):
    print(f"✗ Database not found at {db_path}!")
    exit(1)

with open(db_path, "r", encoding="utf-8") as f:
    logos = json.load(f)

print(f"Loaded {len(logos)} logos from database.")
print("Starting download of all assets (SVG, PNG, PDF)... This might take a minute.")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_file(url, local_path):
    if not url or not url.startswith("http"):
        return False
    if os.path.exists(local_path) and os.path.getsize(local_path) > 100:
        # Already downloaded
        return True
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            with open(local_path, "wb") as f:
                f.write(data)
            return True
    except Exception as e:
        # Silently fail or return false
        return False

def process_logo(logo):
    slug = logo["slug"]
    
    # Remote URLs
    svg_url = logo["svg_path"]
    png_url = logo["png_path"]
    pdf_url = logo["pdf_path"]
    
    # Local save paths
    local_svg = os.path.join(SVG_DIR, f"{slug}.svg")
    local_png = os.path.join(PNG_DIR, f"{slug}.png")
    local_pdf = os.path.join(PDF_DIR, f"{slug}.pdf")
    
    downloaded_svg = download_file(svg_url, local_svg)
    downloaded_png = download_file(png_url, local_png)
    downloaded_pdf = download_file(pdf_url, local_pdf)
    
    # Return status and update paths
    return {
        "slug": slug,
        "svg": downloaded_svg,
        "png": downloaded_png,
        "pdf": downloaded_pdf,
        "local_svg_path": f"/files/svg/{slug}.svg" if downloaded_svg else svg_url,
        "local_png_path": f"/files/png/{slug}.png" if downloaded_png else png_url,
        "local_pdf_path": f"/files/pdf/{slug}.pdf" if downloaded_pdf else pdf_url,
    }

# Run concurrent downloads (20 threads)
results = []
success_count = 0
total_files = len(logos)

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(process_logo, logo): logo for logo in logos}
    
    for i, future in enumerate(as_completed(futures)):
        res = future.result()
        results.append(res)
        
        # Calculate downloaded files
        svg_s = "✓" if res["svg"] else "✗"
        png_s = "✓" if res["png"] else "✗"
        pdf_s = "✓" if res["pdf"] else "✗"
        
        if res["svg"] or res["png"]:
            success_count += 1
            
        if (i + 1) % 50 == 0 or (i + 1) == total_files:
            print(f"Progress: {i+1}/{total_files} logos processed. (Successfully downloaded logos: {success_count})")

# Update logos.json with local paths
updated_logos = []
results_map = {r["slug"]: r for r in results}

for logo in logos:
    slug = logo["slug"]
    if slug in results_map:
        res = results_map[slug]
        logo["svg_path"] = res["local_svg_path"]
        logo["png_path"] = res["local_png_path"]
        logo["pdf_path"] = res["local_pdf_path"]
    updated_logos.append(logo)

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(updated_logos, f, indent=2, ensure_ascii=False)

print("\n🎉 Download complete!")
print(f"Total logos processed: {total_files}")
print(f"Successfully downloaded to local folders: {success_count}")
print(f"Local database {db_path} has been updated to point to local paths.")
print("Run 'python build.py' to rebuild the site using the downloaded local assets!")
