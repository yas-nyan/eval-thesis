import sys
import ipaddress


def write_injector_csv(count):
    lines = []
    for i in range(count):
        origin = i + 1
        ipv4 = ipaddress.IPv4Network(origin)
        ipv6 = ipaddress.IPv6Network(f"2001:db8:ffff:ffff::{origin}")

        lines.append(f"{str(ipv6)},{str(ipv4)}")

    with open(f"./injector_{count}.csv", "w") as f:
        for line in lines:
            f.write(f"{line}\n")


if __name__ == "__main__":
    count = int(sys.argv[1])

    write_injector_csv(count)
