import json
from datetime import datetime, timezone, timedelta
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load extracted timestamps
with open("scratch/ink_research/upload_timestamps.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Total videos analyzed: {len(records)}\n")

parsed_entries = []

for r in records:
    iso_str = r.get("uploadDate") or r.get("publishDate") or r.get("exact_iso")
    title = r.get("title", "")
    vid = r.get("videoId", "")
    
    if not iso_str:
        continue
    
    # Try parsing various ISO formats
    dt = None
    try:
        # Standard fromisoformat handles +00:00, Z, etc. in Python 3.11+
        cleaned_iso = iso_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned_iso)
    except Exception as e:
        # Might be just YYYY-MM-DD
        try:
            dt = datetime.strptime(iso_str[:10], "%Y-%m-%d")
        except Exception:
            pass
            
    parsed_entries.append({
        "videoId": vid,
        "title": title,
        "raw": iso_str,
        "datetime": dt
    })

# Filter entries with valid datetime
valid_entries = [e for e in parsed_entries if e["datetime"] is not None]
has_time = any(e["datetime"].hour != 0 or e["datetime"].minute != 0 for e in valid_entries)

# Convert all to UTC, IST (UTC+5:30), EST (UTC-4:00/UTC-5:00)
ist_tz = timezone(timedelta(hours=5, minutes=30))
est_tz = timezone(timedelta(hours=-4)) # EDT / US Eastern

summary = []
days_count = {}
hours_ist = {}
hours_utc = {}

for e in valid_entries:
    dt = e["datetime"]
    if dt.tzinfo is None:
        # If naive, assume UTC or check raw string
        dt = dt.replace(tzinfo=timezone.utc)
    
    dt_utc = dt.astimezone(timezone.utc)
    dt_ist = dt.astimezone(ist_tz)
    dt_est = dt.astimezone(est_tz)
    
    day_name = dt_ist.strftime("%A")
    hour_ist_val = dt_ist.hour
    hour_utc_val = dt_utc.hour
    
    days_count[day_name] = days_count.get(day_name, 0) + 1
    hours_ist[hour_ist_val] = hours_ist.get(hour_ist_val, 0) + 1
    hours_utc[hour_utc_val] = hours_utc.get(hour_utc_val, 0) + 1
    
    summary.append({
        "title": e["title"],
        "videoId": e["videoId"],
        "raw": e["raw"],
        "utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC (%A)"),
        "ist": dt_ist.strftime("%Y-%m-%d %I:%M %p IST (%A)"),
        "est": dt_est.strftime("%Y-%m-%d %I:%M %p EST (%A)"),
        "day": day_name,
        "hour_ist": hour_ist_val
    })

print("=== INDIVIDUAL VIDEO PUBLISH DATES & TIMES ===")
for s in summary:
    print(f"- {s['title'][:45]}")
    print(f"  Raw: {s['raw']}")
    print(f"  IST: {s['ist']} | US EST: {s['est']}")

print("\n=== DAY OF WEEK FREQUENCY (IST / UTC) ===")
for d, c in sorted(days_count.items(), key=lambda x: -x[1]):
    print(f"  {d:10s}: {c} videos ({c/len(valid_entries)*100:.1f}%)")

print("\n=== UPLOAD HOUR FREQUENCY (IST) ===")
for h, c in sorted(hours_ist.items()):
    am_pm = f"{h%12 if h%12!=0 else 12}:00 {'AM' if h < 12 else 'PM'}"
    print(f"  {am_pm:10s} (Hour {h:02d}): {c} videos")

# Calculate upload cadence (gap between videos)
valid_entries_sorted = sorted(valid_entries, key=lambda x: x["datetime"])
gaps = []
for i in range(1, len(valid_entries_sorted)):
    gap = (valid_entries_sorted[i]["datetime"] - valid_entries_sorted[i-1]["datetime"]).total_seconds() / 86400.0
    gaps.append(gap)

if gaps:
    avg_gap = sum(gaps) / len(gaps)
    min_gap = min(gaps)
    max_gap = max(gaps)
    print(f"\n=== UPLOAD CADENCE / INTERVAL ===")
    print(f"  Average interval between uploads: {avg_gap:.1f} days")
    print(f"  Min interval: {min_gap:.1f} days | Max interval: {max_gap:.1f} days")
