#!/usr/local/bin/python3

import csv
import sys
import ipaddress


class EAMTInconsistencyError(Exception):
    pass


def convert_row_to_eamt_dict(rows):
    eamt = {}

    for row in rows:
        ipv6 = ipaddress.ip_network(row[0])
        ipv4 = ipaddress.ip_network(row[1])

        eamt[str(ipv6)] = ipv4

    return eamt


def check_two_eamt(file_1, file_2):

    eamt1 = {}
    eamt2 = {}

    # get file1
    with open(file_1) as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        eamt1 = convert_row_to_eamt_dict(rows)

    # get file1
    with open(file_2) as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        eamt2 = convert_row_to_eamt_dict(rows)

    return eamt1 == eamt2


if __name__ == "__main__":
    file_1 = sys.argv[1]
    file_2 = sys.argv[2]

    result = check_two_eamt(file_1, file_2)
    if not result:
        raise EAMTInconsistencyError("与えられたEAMTが一致しません．")
