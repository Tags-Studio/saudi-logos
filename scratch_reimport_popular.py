import os
import json
import urllib.request
import re
import concurrent.futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_best_font_url(slug, urls):
    if not urls:
        return None
    clean_slug = re.sub(r'[^a-zA-Z]', '', slug.lower())
    best_url = None
    best_score = -1
    
    for url in urls:
        filename = url.split('/')[-1].lower()
        clean_filename = re.sub(r'[^a-zA-Z]', '', filename.split('.')[0])
        score = 0
        if clean_slug in clean_filename or clean_filename in clean_slug:
            score = 100 + len(clean_filename)
        else:
            score = len(os.path.commonprefix([clean_slug, clean_filename]))
        if score > best_score:
            best_score = score
            best_url = url
    if best_url is None:
        best_url = urls[0]
    return best_url

def scrape_popular_slugs(max_pages=30):
    print("Scraping popular slugs from HTML browse pages...")
    slugs = []
    
    def fetch_page_slugs(page):
        url = f"https://arabyfont.com/browse/page/{page}/?orderby=downloads"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                html = r.read().decode("utf-8")
                # Extract slugs from <h3 class="af-font-card__name"> <a href=".../browse/SLUG/">
                page_slugs = re.findall(r'<h3 class="af-font-card__name">\s*<a href="https://arabyfont.com/browse/([^/"]+)/"', html)
                return page_slugs
        except Exception as e:
            print(f"⚠️ Page {page} failed to fetch: {e}")
            return []

    # Fetch pages in parallel for speed!
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_page_slugs, p) for p in range(1, max_pages + 1)]
        for fut in concurrent.futures.as_completed(futures):
            slugs.extend(fut.result())
            
    # Remove duplicates preserving order
    seen = set()
    unique_slugs = [x for x in slugs if not (x in seen or seen.add(x))]
    
    # Filter out common pages or garbage slugs
    unique_slugs = [s for s in unique_slugs if s not in ["page", "browse", "font_category"]]
    print(f"✓ Scraped {len(unique_slugs)} unique popular slugs.")
    return unique_slugs

def fetch_api_metadata(slugs, categories_map):
    print("\nFetching metadata from WP API in batches...")
    fonts_metadata = []
    
    # Query in batches of 20 to avoid URL length limitations
    batch_size = 20
    batches = [slugs[i:i + batch_size] for i in range(0, len(slugs), batch_size)]
    
    def fetch_batch(batch):
        slugs_str = ",".join(batch)
        url = f"https://arabyfont.com/wp-json/wp/v2/font?slug={slugs_str}&per_page=50"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode("utf-8"))
                batch_results = []
                for item in data:
                    title = item.get("title", {}).get("rendered", "")
                    slug = item.get("slug", "")
                    link = item.get("link", "")
                    cat_ids = item.get("font_category", [])
                    
                    # Map category ID to name
                    cat_name = "غير مصنف"
                    if cat_ids:
                        for cid in cat_ids:
                            name = categories_map.get(str(cid))
                            if name:
                                cat_name = name
                                break
                                
                    batch_results.append({
                        "id": item.get("id"),
                        "name": title,
                        "slug": slug,
                        "category": cat_name,
                        "link": link
                    })
                return batch_results
        except Exception as e:
            print(f"⚠️ Batch query failed for slugs ({batch[0]}...): {e}")
            return []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_batch, b) for b in batches]
        for fut in concurrent.futures.as_completed(futures):
            fonts_metadata.extend(fut.result())
            
    print(f"✓ Fetched metadata for {len(fonts_metadata)} fonts.")
    return fonts_metadata

def download_font_file(font, output_dir):
    slug = font["slug"]
    link = font["link"]
    req = urllib.request.Request(link, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            html = response.read().decode("utf-8")
            urls = re.findall(r"https://arabyfont.com/wp-content/uploads/[^\s'\"]+\.(?:ttf|otf)", html)
            if urls:
                best_url = get_best_font_url(slug, list(set(urls)))
                if best_url:
                    # Determine extension
                    ext = ".otf" if best_url.endswith(".otf") else ".ttf"
                    filename = f"{slug}{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Perform download if not already downloaded
                    if not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                        req_dl = urllib.request.Request(best_url, headers=headers)
                        with urllib.request.urlopen(req_dl, timeout=15) as r_dl:
                            data = r_dl.read()
                            if len(data) > 1000:
                                with open(filepath, "wb") as f_dl:
                                    f_dl.write(data)
                                    
                    font["font_url"] = f"/assets/fonts/arabyfont/{filename}"
                    # Remove temp link field
                    if "link" in font:
                        del font["link"]
                    return font
    except Exception as e:
        print(f"✗ Failed download for {font['name']}: {e}")
    return None

def main():
    # 1. Fetch category names
    print("Fetching categories mapping...")
    cat_url = "https://arabyfont.com/wp-json/wp/v2/font_category?per_page=100"
    req = urllib.request.Request(cat_url, headers=headers)
    categories_map = {}
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode("utf-8"))
            categories_map = {str(item["id"]): item["name"] for item in data}
    except Exception as e:
        print(f"✗ Failed to fetch categories: {e}")
        return
        
    # 2. Scrape the most popular font slugs
    # We will query up to 35 pages of ordering by downloads to fetch the top 350 most popular fonts!
    popular_slugs = scrape_popular_slugs(max_pages=35)
    if not popular_slugs:
        print("✗ No slugs scraped!")
        return
        
    # 3. Query WP API for metadata
    fonts_metadata = fetch_api_metadata(popular_slugs, categories_map)
    if not fonts_metadata:
        print("✗ No metadata fetched!")
        return
        
    # 4. Download and configure files in parallel
    output_dir = "public/assets/fonts/arabyfont"
    os.makedirs(output_dir, exist_ok=True)
    
    final_fonts = []
    print("\nDownloading popular font files locally in parallel...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_font_file, font, output_dir) for font in fonts_metadata]
        for fut in concurrent.futures.as_completed(futures):
            res = fut.result()
            if res:
                final_fonts.append(res)
                print(f"✓ Imported: {res['name']} [{res['category']}]")
                
    print(f"\n✓ Completed! Successfully imported {len(final_fonts)} popular fonts locally.")
    
    # 5. Save database
    db_path = "src/data/fonts.json"
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(final_fonts, f, indent=2, ensure_ascii=False)
    print(f"✓ Saved database of popular fonts to {db_path}.")

if __name__ == "__main__":
    main()
