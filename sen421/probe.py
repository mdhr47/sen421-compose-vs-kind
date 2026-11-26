import time, sys, urllib.request
url, out = sys.argv[1], sys.argv[2]
with open(out, "w") as f:
    while True:
        t = time.time()
        try:
            urllib.request.urlopen(url, timeout=0.5).read()
            ok = 1
        except Exception:
            ok = 0
        f.write(f"{t:.3f},{ok}\n")
        f.flush()
        time.sleep(0.1)
