#!/usr/bin/env python3

import os
from datetime import datetime
import csv
from sys import argv
from bs4 import BeautifulSoup
import re

DEBUG = True

HELP = """
How to use:

    list_jitis file.html

"""


def read_argv():

    if len(argv) == 2:
        return argv[1]

    print("No indicated file to extact list")
    print(HELP)
    exit(1)


def read_file(path: str):
    if os.path.exists(path):
        with open(path) as file:
            return file.read()
    print(f"Not exist file: {path}")
    print(HELP)
    exit(1)


def extact_list(txt):
    html = BeautifulSoup(txt, "html.parser")
    list_people = html.find_all(attrs={"class": "display-name"})
    people = set()
    for person in list_people:

        name = person.get_text(strip=True).replace("(me)", "").replace("\n", " ")
        name = re.sub(" +", " ", name)
        people.add(name)

    return people


def save_csv(list_to_save):

    if not len(list_to_save):
        print("Nothing to save! :(")
        print(HELP)
        exit(1)

    name_csv = f'lista_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'

    with open(name_csv, mode="+w", encoding="utf-8") as list_csv:
        file_csv = csv.writer(list_csv)
        file_csv.writerow(["Nombre"])
        count = 0
        for p in list_to_save:
            file_csv.writerow([p])
            count += 1

    print(f"{count} names")
    print(f"File savef as: {name_csv}")


def main():
    file_name = read_argv()
    txt = read_file(file_name)
    people = extact_list(txt)
    save_csv(people)


if __name__ == "__main__":
    main()
