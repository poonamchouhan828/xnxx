import time
import urllib.request
from bs4 import BeautifulSoup

# Domain change hone par sirf yahan update karein:
BASE_DOMAIN = "https://xnxx.health"

# Jiske data fetch karne hain un sabhi categories ke path:
CATEGORIES = [
    "/search/familial_relations",
    "/search/wife",
    "/search/indian",
    "/search/teen",
    "/search/big_cock",
    "/search/gangbang",
    "/search/cheating",
    "/search/latina",
    "/search/cuckold",
    "/search/exotic",
    "/search/stepdaughter",
    "/search/doctor"
]

def fetch_category_items(path):
    url = f"{BASE_DOMAIN}{path}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    items = []
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return items

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all('div', class_='thumb-block')

    for block in blocks:
        # Extract Link
        link_tag = block.find('a', href=True)
        href = link_tag['href'] if link_tag else None
        if href and href.startswith('/'):
            href = BASE_DOMAIN + href

        # Extract Title
        title = None
        if link_tag and 'title' in link_tag.attrs:
            title = link_tag['title']
        else:
            title_p = block.find('p')
            if title_p:
                title = title_p.text.strip()

        # Extract Thumbnail Image
        img_tag = block.find('img')
        img_src = None
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src')

        if href and title:
            items.append({
                'title': title,
                'href': href,
                'img': img_src
            })

    return items

def main():
    m3u_lines = ["#EXTM3U\n"]
    total_videos = 0

    for path in CATEGORIES:
        print(f"Fetching: {BASE_DOMAIN}{path}")
        videos = fetch_category_items(path)
        
        for vid in videos:
            logo_attr = f' tvg-logo="{vid["img"]}"' if vid['img'] else ''
            # group-title="🔞adult+" yahan add kiya gaya hai
            m3u_lines.append(f'#EXTINF:-1 group-title="🔞adult"{logo_attr}, {vid["title"]}')
            m3u_lines.append(f'{vid["href"]}\n')
            total_videos += 1
        
        # Server par jyada load na pade isliye 1 sec delay
        time.sleep(1)

    # Output M3U File Save
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"\nDone! Total {total_videos} videos saved to playlist.m3u")

if __name__ == "__main__":
    main()
