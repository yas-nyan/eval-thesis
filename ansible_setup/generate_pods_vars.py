import ipaddress


pods = [1, 2]
servers = range(0, 512)


for pod in pods:
    for server in servers:
        if server >= 256:
            print(
                f"  - NAME: server{pod}-{server}\n    ROUTER_ID: 100.64.{100+pod}.{server-256}")
        else:
            print(
                f"  - NAME: server{pod}-{server}\n    ROUTER_ID: 100.64.{pod}.{server}")
