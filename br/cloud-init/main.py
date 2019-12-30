from jinja2 import Template, Environment, FileSystemLoader
import subprocess
import pathlib
import sys


env = Environment(loader=FileSystemLoader('./templates'))
BR_MIN = 1
BR_MAX = 30


def generate_network_yml(ipv4="202.0.73.51/25", ipv6=f"2001:200:0:8831:cafe::51/64", gateway4="202.0.73.1", gateway6="2001:200:0:8831::1"):
    network = {
        "ipv4": ipv4,
        "ipv6": ipv6,
        "gateway4": gateway4,
        "gateway6": gateway6,
        "nameservers": [
            "2404:6800:4004:810::200e",
            "8.8.8.8"
        ]
    }
    netowork_template = env.get_template('network.yml.j2')
    rendered_network = netowork_template.render(network)

    return str(rendered_network)


def generate_meta_data(hostname):
    seed = {
        "hostname": hostname,
        "instance_id": hostname
    }
    meta_template = env.get_template('meta-data.j2')
    rendered_meta_data = meta_template.render(seed)

    return str(rendered_meta_data)


def generate_user_data(initial_pw):
    seed = {
        "initial_pw": initial_pw
    }
    user_template = env.get_template('user-data.j2')
    rendered_user_data = user_template.render(seed)

    return str(rendered_user_data)


def gen_br_iso(br_i):
    ipv4 = f"202.0.73.{50+br_i}/25"
    ipv6 = f"2001:200:0:8831:cafe::{50+br_i}/64"
    hostname = f"br{str(br_i).zfill(2)}"

    rendered_meta_data = generate_meta_data(hostname)
    rendered_network = generate_network_yml(ipv4=ipv4, ipv6=ipv6)
    rendered_user_data = generate_user_data(initial_pw="PASSWORD")  # deleted
    p_dir = pathlib.Path(f'./tmp/{hostname}')
    build_dir = pathlib.Path(f"./build")
    if not p_dir.exists():
        p_dir.mkdir(parents=True)

    with open(f"{str(p_dir)}/network.yml", "w") as f:
        f.write(rendered_network)
    with open(f"{str(p_dir)}/meta-data", "w") as f:
        f.write(rendered_meta_data)
    with open(f"{str(p_dir)}/user-data", "w") as f:
        f.write(rendered_user_data)

    BUILD_CMD = ["docker", "run", "--rm", "-v", f"{p_dir.resolve()}:/workdir", "-v", f"{build_dir.resolve()}:/build",
                 "cloud-utils:latest", "cloud-localds", "-N", "network.yml", f"/build/{hostname}.iso", "user-data", "meta-data"]

    proc = subprocess.run(
        BUILD_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        print(f"ERROR: hostname->{hostname}")
        print(proc.stderr.decode("utf-8"))
        return False
    else:
        print(f"BUILD SUCCESS: {hostname}")
        return True


if __name__ == "__main__":
    br_range = range(BR_MIN, BR_MAX+1)
    for br_i in br_range:
        if not gen_br_iso(br_i):
            sys.exit(1)
