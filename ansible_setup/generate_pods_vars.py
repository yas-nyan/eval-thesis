import yaml
import ipaddress
import sys

ROUTER_NETWORK = ipaddress.ip_network("100.64.0.0/20")
PODS_PATH = ["./host_vars/pod1.yml", "./host_vars/pod2.yml"]


def modify_group_all_ver(count, path="./group_vars/all.yml"):
    obj = {}
    with open(path, "r") as f:
        obj = yaml.load(f, Loader=yaml.SafeLoader)
    obj["SERVER_COUNT"] = count

    with open(path, "w") as f:
        yaml.dump(obj, f, encoding='utf8')


def create_server_config(pod_name, index, router_address):
    return {
        "NAME": f"{pod_name}-{index}",
        "ROUTER_ID": str(router_address)
    }


def generate_config(count, router_network=ROUTER_NETWORK, pods_path=PODS_PATH):

    hosts = list(ROUTER_NETWORK.hosts())

    pods = []
    # 全体変数の書き換え
    modify_group_all_ver(count)
    # podsの各変数を書き換え
    for index, path in enumerate(pods_path):
        with open(path) as f:
            obj = yaml.load(f, Loader=yaml.SafeLoader)
            obj["SERVERS"] = []
        pods.append({
            "name": f"pod{index+1}",
            "data": obj,
            "path": path
        })

    for i in range(count):
        pod = pods[i % len(pods)]
        pod["data"]["SERVERS"].append(
            create_server_config(pod["name"], i, hosts[i]))

    # 書き出し
    for pod in pods:
        with open(pod["path"], "w") as f:
            yaml.dump(pod["data"], f, encoding='utf8')


if __name__ == "__main__":
    count = int(sys.argv[1])
    generate_config(count)
