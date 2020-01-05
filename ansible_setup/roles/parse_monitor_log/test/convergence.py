import pandas as pd
from datetime import datetime
import sys

hosts = [f"br{str(i).zfill(2)}" for i in range(1, 31)]
#filepaths = [ f"backup/deploy_test/{host}.csv" for host in hosts]
#filepaths = [ f"backup/docker_512_minus1/{host}.csv" for host in hosts]
filepaths = [
    f"./backup/monitor/{host}.csv" for host in hosts]


def clean_and_addheader(filepath):
    new_lines = []
    with open(filepath) as f:
        lines = f.readlines()
        started_time = float(lines[0].strip().split(",")[0])
        for line in lines:
            striped_words = line.strip().split(",")
            if len(striped_words) != 3:
                continue
            try:
                this_time = round(float(striped_words[0]), 1)  # 小数点第一位で四捨五入
            except:
                continue  # 時間以外のものが混ざるなら殺す
            striped_words[0] = this_time
            striped_words[1] = int(striped_words[1])
            striped_words[2] = int(striped_words[2])
            new_lines.append(striped_words)
    return new_lines


def calc_convergence(merged_df, completed_count):
    hosts = [f"br{str(i).zfill(2)}" for i in range(1, 31)]
    coluｍns_j = [f"{host}_jool" for host in hosts]
    query_text = ""
    for index, column in enumerate(columns_j):
        if index == 0:
            pass
        else:
            query_text += " & "
        query_text += f"{column} == {completed_count}"

    convergenced_time = merged_df.query(query_text).head(1).index

    return convergenced_time - merged_df.head(1).index


if __name__ == "__main__":

    # get args
    COMPLETE_EAMT_COUNT = sys.argv[1]
    # get docker started/stopped time
    docker_log_path = "./backup/pod/docker-log.txt"
    standard_time = 0
    with open(docker_log_path, "r") as f:
        standard_time = int(f.read().strip())

    dfs = []
    # キレイにしてpandasに挿入
    for index, filepath in enumerate(filepaths):
        host = hosts[index]
        df = pd.DataFrame(clean_and_addheader(filepath), columns=[
            "time", f"{host}_gobgp", f"{host}_jool"])
        selected = df.query(f"time >= {standard_time} ")
        selected["time"] = selected["time"] - standard_time
        selected.set_index("time")
        dfs.append(selected)

    merged = pd.concat(dfs, sort=True)
    # merged["time"] = pd.to_datetime(merged['time'].astype(float), unit='s')
    merged = merged.sort_values("time")
    merged = merged.fillna(method='ffill')
    merged = merged.reset_index(drop=True)
    merged = merged.groupby('time').mean()

    convergenced_time = calc_convergence(merged, COMPLETE_EAMT_COUNT)

    print(convergenced_time[0])
