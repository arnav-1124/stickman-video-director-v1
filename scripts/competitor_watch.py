import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import csv
import datetime
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# Tracked competitor channels and their YouTube Channel IDs
COMPETITORS = {
    "Day One Films": "UCUWG17RpxXBZ4avKIqPX6CQ",
    "Ink Explainer": "UCpgrEMx8diLrw7YNQ6r3uUw"
}

def fetch_rss_feed(channel_id):
    """Fetches public RSS XML feed for a YouTube channel ID (zero API key required)."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        print(f"  [Warning] Could not fetch RSS for {channel_id}: {e}")
        return None

def parse_rss_entries(xml_data, channel_name):
    """Parses video entries from YouTube RSS feed."""
    if not xml_data:
        return []
    
    root = ET.fromstring(xml_data)
    ns = {
        'atom': 'http://www.w3.org/2005/Atom',
        'yt': 'http://www.youtube.com/xml/schemas/2015',
        'media': 'http://search.yahoo.com/mrss/'
    }
    
    entries = []
    for entry in root.findall('atom:entry', ns):
        video_id = entry.find('yt:videoId', ns)
        title = entry.find('atom:title', ns)
        published = entry.find('atom:published', ns)
        
        v_id = video_id.text if video_id is not None else ""
        v_title = title.text if title is not None else ""
        v_pub = published.text if published is not None else ""
        
        media_group = entry.find('media:group', ns)
        thumb_url = ""
        if media_group is not None:
            thumb = media_group.find('media:thumbnail', ns)
            if thumb is not None:
                thumb_url = thumb.attrib.get('url', '')

        entries.append({
            "channel": channel_name,
            "video_id": v_id,
            "title": v_title,
            "published": v_pub,
            "thumbnail_url": thumb_url,
            "watch_url": f"https://www.youtube.com/watch?v={v_id}",
            "pulled_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })
    return entries

def main():
    print("=" * 60)
    print("  📺 COMPETITOR WATCH — RSS Catalog Pull")
    print("=" * 60)
    
    output_dir = Path("assets/analytics/competitor_catalog")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "latest_competitor_videos.csv"
    
    all_videos = []
    for name, cid in COMPETITORS.items():
        print(f"\nPulling latest uploads for: {name} ({cid})...")
        data = fetch_rss_feed(cid)
        if data:
            vids = parse_rss_entries(data, name)
            print(f"  ✓ Found {len(vids)} recent upload(s).")
            all_videos.extend(vids)
            
    if all_videos:
        fieldnames = ["channel", "video_id", "title", "published", "thumbnail_url", "watch_url", "pulled_at"]
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_videos)
        print(f"\n[SUCCESS] Saved {len(all_videos)} competitor videos to:\n  {csv_file}")
    else:
        print("\nNo entries fetched.")

if __name__ == "__main__":
    main()
