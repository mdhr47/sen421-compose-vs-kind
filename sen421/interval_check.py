import glob, statistics as s
for f in sorted(glob.glob("*.csv")):
    t = [float(l.split(",")[0]) for l in open(f) if l.strip() and l[0].isdigit()]
    d = [b - a for a, b in zip(t, t[1:])]
    if d: print(f"{f}: {len(t)} rows, median gap {s.median(d):.3f} s")
