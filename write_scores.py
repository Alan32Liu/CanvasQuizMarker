#! /usr/local/Cellar/python@3.8/3.8.3/bin/python3.8

import csv
import sys

from typing import Dict, List, Union

assert len(sys.argv) == 3

QUIZ_WEIGHT: float = 0.625
grades_file: str = sys.argv[1]
new_grades_file: str = sys.argv[1]
quiz_scores_file: str = sys.argv[2]
quiz_name = quiz_scores_file[:-4]

student_scores: Dict[str, int] = {}
old_grades: List[List[Union[str, float]]] = []
new_grades: List[List[Union[str, float]]] = []


with open(quiz_scores_file, 'r') as scores_file:
    for student, score in list(csv.reader(scores_file)):
        assert student not in student_scores
        student_scores[student]: int = score

with open(grades_file, 'r') as grades_summary:
    old_grades = list(csv.reader(grades_summary))
    quiz_index: Union[int, None] = None

    # parse the header
    for index, title in enumerate(old_grades[0]):
        assert not (quiz_index and quiz_name in title)
        if quiz_name in title:
            quiz_index = index
    assert quiz_index

    possible_points: int = int(float(old_grades[2][quiz_index]))

    # the first three rows are the same
    new_grades.extend(old_grades[0:3])

    for record in old_grades[3:]:
        name: str = record[0]
        record_score: int = int(float(record[quiz_index])) \
            if record[quiz_index] else 0
        student_score: int = int(float(student_scores.pop(name, 0)))
        assert record_score >= student_score

        record[quiz_index]: float = QUIZ_WEIGHT \
            if student_score == possible_points else 0
        new_grades.append(record)
        # print(record[quiz_index], student_score, possible_points)

print(student_scores)

# pp = PrettyPrinter(indent=4)
# pp.pprint(new_grades[:5])
# pp.pprint(old_grades[:5])

assert len(new_grades) == len(old_grades)
with open(new_grades_file, 'w') as new_grades_summary:
    grades_writer: csv.writer = csv.writer(new_grades_summary)
    grades_writer.writerows(new_grades)
