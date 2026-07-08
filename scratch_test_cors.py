import urllib.request

def test_cors():
    url = "https://arabyfont.com/wp-content/uploads/2026/05/a-mitra-2014-1.ttf"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Origin': 'https://saudi-logos.vercel.app'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            print("✓ Font fetched successfully!")
            print(f"Status: {r.status}")
            print("\nResponse Headers:")
            for name, val in r.getheaders():
                print(f"  {name}: {val}")
    except Exception as e:
        print(f"✗ Failed: {e}")

test_cors()
