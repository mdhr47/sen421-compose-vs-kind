import statistics as s
data = {
 "Compose crash recovery (s)": [0.89,0.84,0.85,0.89,0.87],
 "K8s crash recovery (s)": [1.12,1.77,1.93,2.44,1.27],
 "Compose update, failed probes": [5,4,4,3,3],
 "Compose update, longest outage (s)": [2.22,1.03,0.94,0.82,0.82],
 "K8s update, failed probes": [0,0,4,9,7],
 "K8s update, longest outage (s)": [0,0,3.37,9.13,3.48],
 "K8s tuned update, failed probes": [0,0,0,0,0],
}
for k, v in data.items():
    print(f"{k}: mean={s.mean(v):.2f} sd={s.stdev(v):.2f} median={s.median(v):.2f} min={min(v)} max={max(v)}")
