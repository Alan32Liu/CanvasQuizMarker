#! /usr/local/Cellar/python@3.8/3.8.3/bin/python3.8

import csv
# import pdb
import re
import sys

from datetime import datetime, timedelta
from pprint import PrettyPrinter
from typing import Dict, List, Tuple

assert len(sys.argv) == 2
quiz: str = sys.argv[1]
quiz_name: str = re.match(r"(Quiz\s?[0-9]{1,2}) .*", quiz).group(1)
print(quiz_name)
time_allowed: timedelta = timedelta(days=8)
earliest_attempt: datetime = datetime.today()

highest_score: int = 0
student_records: Dict[str, List[Tuple[datetime, int]]] = {}
student_scores: Dict[str, int] = {}

with open(quiz, 'r') as quiz_summary:
    records: List = list(csv.reader(quiz_summary))

    # skip the header in records[0]
    for record in records[1:]:
        name: str = record[0]
        date: datetime = datetime.strptime(record[4].split(" ")[0], "%Y-%m-%d")
        score: int = int(float(record[-1]))

        if date < earliest_attempt:
            earliest_attempt: datetime = date

        if highest_score < score:
            highest_score: int = score

        if name not in student_records:
            student_records[name]: List[Tuple[datetime, int]] = []

        student_records[name].append((date, score))

due_date: datetime = earliest_attempt + time_allowed
print(earliest_attempt, due_date, highest_score)

for student, records in student_records.items():
    score_awarded: int = 0
    for record in records:
        if record[0] > due_date:
            continue
        if record[1] > score_awarded:
            score_awarded = record[1]
    assert student not in student_scores
    # parse the name if needed
    # first_name, last_name = student.rsplit(" ", 1)
    student_scores[student]: int = score_awarded

with open(quiz_name + ".csv", 'w') as quiz_results_file:
    quiz_results_writer = csv.writer(quiz_results_file)
    quiz_results_writer.writerows(student_scores.items())

pp = PrettyPrinter(indent=4)
pp.pprint(student_scores)
