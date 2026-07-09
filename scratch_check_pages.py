import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def inspect_browse_html():
    url = "https://arabyfont.com/browse/?orderby=downloads"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
            print("✓ HTML loaded!")
            
            # Print any h2 or h3 or div class names related to font cards
            print("Looking for headers...")
            headers_list = re.findall(r'<h[234][^>]*>.*?</h[234]>', html, re.DOTALL)
            print(f"Found {len(headers_list)} headers:")
            for h in headers_list[:15]:
                print("  ", h.strip().replace("\n", ""))
                
            # Print raw links to browse
            print("\nLooking for links to fonts...")
            links = re.findall(r'href="(https://arabyfont.com/browse/[^/"]+/)"', html)
            print(f"Found {len(links)} links:")
            for l in list(set(links))[:15]:
                print("  ", l)
                
            # Write browse html to file for analysis
            with open("browse_sample.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("\nSaved browse HTML to browse_sample.html")
            
    except Exception as e:
        print(f"✗ Failed: {e}")

inspect_browse_html()
