import subprocess
from subprocess import PIPE
from multiprocessing import Pool
import time
import datetime


def isUP(target, timeout=100):
    proc = subprocess.run(
        f"fping {target} -t {timeout}", shell=True, stdout=PIPE, stderr=PIPE)

    return proc.returncode == 0


def allUP(targets, timeout=100):
    proc = subprocess.run(
        f"fping -t {timeout} -A {' '.join(targets)}",  shell=True)
    return proc.returncode == 0


def mesure(profile):
    # 無限に試して終了時間を測る
    start_time = time.time()
    end_time = None
    mesure_type = profile["type"]
    targets = profile["targets"]
    timeout = profile["timeout"]

    while True:
        res = allUP(targets, timeout=timeout)
        if res:
            end_time = time.time()
            break

    return {
        "result": end_time - start_time,
        "type": mesure_type
    }


if __name__ == "__main__":
    ### v6とv4で同時にpingを試して，v6が出来てからv4が終わるまでを計測する．####
    start_date = datetime.datetime.now()

    # 各podごとのサービスアドレス群(v6はprefixが違うので)
    targets_v4_pod1 = [f"202.0.73.{128+i}" for i in range(60)]
    targets_v4_pod2 = [f"202.0.73.{188+i}" for i in range(60)]
    targets_v6_pod1 = [
        f"2001:200:0:8831:1::{v4_addr}" for v4_addr in targets_v4_pod1]
    targets_v6_pod2 = [
        f"2001:200:0:8831:2::{v4_addr}" for v4_addr in targets_v4_pod2]

    # まとめたサービスアドレス群
    targets_v4 = targets_v4_pod1 + targets_v4_pod2
    targets_v6 = targets_v6_pod1 + targets_v6_pod2

    profile_v4 = {
        "type": "ipv4",
        "targets": targets_v4,
        "timeout": 100
    }

    profile_v6 = {
        "type": "ipv6",
        "targets": targets_v6,
        "timeout": 100
    }

    profiles = [profile_v4, profile_v6]
    all_result = []
    with Pool(2) as pool:
        for result in pool.imap_unordered(mesure, profiles):
            # 全部揃うまで終了扱いにはならない
            all_result.append(result)

    ipv4_result = None
    ipv6_result = None
    # 結果をprintする．入っている順番はわからない．
    for result in all_result:
        if result["type"] == "ipv4":
            ipv4_result = result["result"]
        elif result["type"] == "ipv6":
            ipv6_result = result["result"]
        else:
            raise(ValueError(f"Mesure Type is not valid. {result['type']}"))

    end_date = datetime.datetime.now()
    print("----------------------【FINISHED】--------------------------")
    print(f"start: {str(start_date)}")
    print(f"end: {str(end_date)}")
    print(f"duration: {end_date - start_date}")

    if ipv4_result and ipv6_result:
        print("-----duration result(UNIX TIME seconds)-----")
        print(
            f"ipv4: {ipv4_result}\nipv6: {ipv6_result}\nTimeLag:{abs(ipv4_result - ipv6_result)}")
