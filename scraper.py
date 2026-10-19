import re
import urllib.request
from bs4 import BeautifulSoup

TARGET_URL = "https://xnxx.health/search/familial_relations"
DOMAIN = "https://xnxx.health"

def fetch_and_generate_m3u():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(TARGET_URL, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all('div', class_='thumb-block')

    m3u_lines = ["#EXTM3U\n"]

    for block in blocks:
        # Extract Link
        link_tag = block.find('a', href=True)
        href = link_tag['href'] if link_tag else None
        if href and href.startswith('/'):
            href = DOMAIN + href

        # Extract Title
        title = None
        if link_tag and 'title' in link_tag.attrs:
            title = link_tag['title']
        else:
            title_p = block.find('p')
            if title_p:
                title = title_p.text.strip()

        # Extract Image Thumbnail URL
        img_tag = block.find('img')
        img_src = None
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src')

        if href and title:
            logo_attr = f' tvg-logo="{img_src}"' if img_src else ''
            m3u_lines.append(f'#EXTINF:-1{logo_attr}, {title}')
            m3u_lines.append(f'{href}\n')

    # Save to playlist.m3u
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))

    print(f"Successfully updated playlist.m3u with {len(blocks)} items.")

if __name__ == "__main__":
    fetch_and_generate_m3u()
