# CanvasQuizMarker
Two scripts to parse students' quiz scores and write to their grades.


## Intention
The scripts fixes the two issues with the defaut Canvas Quiz mark allocatons:
1. Incorrect scores. Canvas assumes each question in quizzes is worth 1 mark, so each quiz with N questions was allocated N marks while in practice they might be evaluated differently.
2. No time restriction. In case Canvas does not exclude the attempts after the due date.

## Parser
The first script (`parse_scores.py`) parses the quiz statistics downloaded from Canvas to produce a file that contains the number of questions answered correctly by each student before the due date of each quiz. 
In case the due date is unknown, it sets the due date to be 8 days after the earliest attempt of all students’.

## Writer
The second script (`write_scores.py`) updates the grades according to a simple rule (`QUIZ_WEIGHT` if all answers are correct or `0` if late or at least one mistake). The grades are exported from the Canvas Grades section.

To update the results, put all files in the same directory and run:
```bash
for file in Quiz*Report.csv; do ./parse_scores.py $file; done;

for file in Quiz*[^a-z].csv; do ./write_scores.py <final-grades>.csv $file; done
```
