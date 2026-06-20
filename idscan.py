# Enumerate all result ids for a keyword search on the archive site. Runs on CI runner.
# Source stays CJK-free: keyword is url-encoded.
import re, time
import requests

KW = "%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8"   # url-encoded search keyword
PAGES = 28                                     # 1..27 (1-based), a bit of headroom
S = requests.Session()
S.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) GF/2.1"})

ids = []
for page in range(1, PAGES):
    html = ""
    for _ in range(4):
        try:
            html = S.get(f"https://www.digital.archives.go.jp/search?kw={KW}&page={page}", timeout=40).text
            break
        except Exception:
            time.sleep(3)
    found = re.findall(r"/(item|file)/(\d+)", html)
    ids += found
    print(f"page {page}: +{len(found)} (cum {len(ids)})", flush=True)
    time.sleep(1)

seen, out = set(), []
for typ, i in ids:
    if i not in seen:
        seen.add(i); out.append((typ, i))
print(f"unique ids: {len(out)}", flush=True)
with open("worklist.csv", "w", encoding="utf-8") as f:
    f.write("type,id\n")
    for typ, i in out:
        f.write(f"{typ},{i}\n")
print("worklist.csv written", flush=True)
