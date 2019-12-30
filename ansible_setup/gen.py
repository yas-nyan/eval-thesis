

for br_i in range(1, 31):
    ipv4 = f"202.0.73.{50+br_i}"
    ipv6 = f"2001:200:0:8831:cafe::{50+br_i}"
    hostname = f"br{str(br_i).zfill(2)}"
    print(f"{hostname} ansible_host={ipv4} ROUTER_ID={ipv4}")
