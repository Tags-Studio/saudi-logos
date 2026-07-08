import os
import json
import urllib.request
import concurrent.futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_single_font(font, output_dir):
    name = font.get("name", "")
    slug = font.get("slug", "")
    url = font.get("font_url", "")
    
    if not url:
        return None
        
    ext = ".ttf"
    if ".otf" in url.lower():
        ext = ".otf"
        
    filename = f"{slug}{ext}"
    filepath = os.path.join(output_dir, filename)
    
    # If already downloaded, return updated entry
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        font["font_url"] = f"/assets/fonts/arabyfont/{filename}"
        return font
        
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            if len(data) > 1000: # Ensure it is a valid file, not an error page
                with open(filepath, "wb") as f:
                    f.write(data)
                font["font_url"] = f"/assets/fonts/arabyfont/{filename}"
                print(f"✓ Downloaded: {name} ({filename}) - {len(data)/1024:.1f} KB")
                return font
            else:
                print(f"✗ Empty file for: {name}")
    except Exception as e:
        print(f"✗ Failed to download '{name}' from {url}: {e}")
        
    return None

def main():
    db_path = "src/data/fonts.json"
    if not os.path.exists(db_path):
        print("✗ Database src/data/fonts.json not found!")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        fonts = json.load(f)
        
    print(f"Loaded {len(fonts)} fonts from database.")
    
    output_dir = "public/assets/fonts/arabyfont"
    os.makedirs(output_dir, exist_ok=True)
    
    updated_fonts = []
    failed_count = 0
    
    print("Downloading fonts in parallel (max 12 workers)...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(download_single_font, font, output_dir) for font in fonts]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            if res:
                updated_fonts.append(res)
            else:
                failed_count += 1
                
    print(f"\n✓ Completed downloading! Success: {len(updated_fonts)}, Failed: {failed_count}")
    
    # Save the updated database with local paths
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(updated_fonts, f, indent=2, ensure_ascii=False)
    print("✓ Saved updated database with local font paths.")

if __name__ == "__main__":
    main()
