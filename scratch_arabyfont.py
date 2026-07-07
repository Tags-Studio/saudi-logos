import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def test_multiple_fonts():
    # Load font categories mapping
    try:
        with open("font_categories.json", "r", encoding="utf-8") as f:
            categories_map = json.load(f)
    except:
        categories_map = {}
        
    url = "https://arabyfont.com/wp-json/wp/v2/font?per_page=5"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            fonts = json.loads(r.read().decode("utf-8"))
            print(f"✓ Loaded {len(fonts)} font posts!")
            
            for index, font in enumerate(fonts):
                title = font.get("title", {}).get("rendered", "")
                link = font.get("link", "")
                cat_ids = font.get("font_category", [])
                
                # Get category names
                cat_names = [categories_map.get(str(cid), str(cid)) for cid in cat_ids]
                
                print(f"\nFont {index+1}: {title}")
                print(f"  Link: {link}")
                print(f"  Categories: {cat_names}")
                
                # Fetch webpage to extract .ttf link
                req_page = urllib.request.Request(link, headers=headers)
                try:
                    with urllib.request.urlopen(req_page, timeout=10) as r_page:
                        html = r_page.read().decode("utf-8")
                        ttf_urls = re.findall(r"https://arabyfont.com/wp-content/uploads/[^\s'\"]+\.(?:ttf|otf)", html)
                        if ttf_urls:
                            print(f"  ✓ Extracted TTF/OTF links: {list(set(ttf_urls))}")
                        else:
                            print("  ✗ No font file links extracted from HTML!")
                except Exception as e_page:
                    print(f"  ✗ Failed to fetch webpage: {e_page}")
    except Exception as e:
        print(f"✗ Failed: {e}")

test_multiple_fonts()
