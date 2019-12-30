from jinja2 import Template, Environment, FileSystemLoader
hosts = range(1, 61)
pods = range(1, 3)

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('pod.yml.j2')


for pod in pods:
    data = {
        "servers": []
    }
    for host in hosts:
        data["servers"].append(
            {
                "router_id": f"202.0.73.{128 + host - 1 + (pod-1) * 60}",
                "name": f"server{str(pod).zfill(2)}-{str(host).zfill(2)}"
            }
        )
        template = env.get_template('pod.yml.j2')
        rendered = template.render(data)
        with open(f"pod{pod}.yml", "w") as f:
            f.write(rendered)
