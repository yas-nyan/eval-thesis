import ipaddress


pods = [1, 2]
servers = range(0, 256)


for pod in pods:
    for server in servers:
        print(
            f"  - NAME: server{pod}-{server}\n    ROUTER-ID: 100.64.{pod}.{server}")
