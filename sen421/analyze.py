import sys
rows = [l.strip().split(",") for l in open(sys.argv[1]) if l.strip()]
rows = [(float(t), int(o)) for t, o in rows]
fails = [t for t, o in rows if o == 0]
if not fails:
    print("no failures seen")
else:
    nxt = [t for t, o in rows if t > fails[-1] and o == 1]
    end = nxt[0] if nxt else fails[-1]
    print(f"failed probes: {len(fails)}, downtime: {end - fails[0]:.2f} s")
