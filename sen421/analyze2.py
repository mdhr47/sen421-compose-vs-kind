import sys, glob
for pat in sys.argv[1:]:
    for fn in sorted(glob.glob(pat)):
        rows = [(float(a), int(b)) for a, b in (l.strip().split(",") for l in open(fn) if l.strip())]
        fails = sum(1 for _, o in rows if o == 0)
        best, start = 0.0, None
        for t, o in rows:
            if o == 0 and start is None: start = t
            if o == 1 and start is not None:
                best = max(best, t - start); start = None
        if start is not None: best = max(best, rows[-1][0] - start)
        print(f"{fn}: failed={fails}, longest outage={best:.2f}s")
