import csv
import sys


class EAMTInconsistencyError(Exception):
    pass


def check_two_eamt(file_1, file_2):

    eamt1 = {}
    eamt2 = {}

    # get file1
    with open(file_1) as f:
        reader = csv.reader(f)
        for row in reader:
            eamt1[row[0]] = row[1]

    # check file_2
    with open(file_2) as f:
        reader = csv.reader(f)
        for row in reader:
            eamt2[row[0]] = row[1]

    return eamt1 == eamt2


if __name__ == "__main__":
    file_1 = sys.argv[1]
    file_2 = sys.argv[2]

    result = check_two_eamt(file_1, file_2)
    if not result:
        raise EAMTInconsistencyError("与えられたEAMTが一致しません．")
