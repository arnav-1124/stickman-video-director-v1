import urllib.request
import json
import re
from datetime import datetime
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/ink_research/scratch_channel_videos_parsed.json", "r", encoding="utf-8") as f:
    channel_videos = json.load(f)

print(f"Checking exact upload timestamps for all {len(channel_videos)} videos...\n")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

upload_records = []

for idx, v in enumerate(channel_videos, 1):
    vid = v["videoId"]
    title = v["title"]
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
        
        # Search for datePublished or uploadDate
        m_pub = re.search(r'"publishDate":"([^"]+)"', html)
        m_upload = re.search(r'"uploadDate":"([^"]+)"', html)
        m_meta_pub = re.search(r'<meta itemprop="datePublished" content="([^"]+)">', html)
        m_meta_upload = re.search(r'<meta itemprop="uploadDate" content="([^"]+)">', html)
        
        pub_date = m_pub.group(1) if m_pub else (m_meta_pub.group(1) if m_meta_pub else "")
        upload_date = m_upload.group(1) if m_upload else (m_meta_upload.group(1) if m_meta_upload else "")
        
        # Also check playerMicroformatRenderer
        m_micro = re.search(r'"playerMicroformatRenderer":({.*?})"conversionContext"', html)
        exact_iso = pub_date or upload_date
        
        upload_records.append({
            "videoId": vid,
            "title": title,
            "publishDate": pub_date,
            "uploadDate": upload_date,
            "exact_iso": exact_iso
        })
        print(f"[{idx:02d}] {title[:40]}... -> pub: {pub_date} | up: {upload_date}")
    except Exception as e:
        print(f"[{idx:02d}] Error on {vid}: {e}")

with open("scratch/ink_research/upload_timestamps.json", "w", encoding="utf-8") as f:
    json.dump(upload_records, f, indent=2, ensure_ascii=False)

print("\nDone extracting timestamps!")
