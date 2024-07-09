# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 9 July, 2024

import pandas as pd
import random

NUM_STUDENTS = 50000
MONTHS = {'Jan':31, 'Feb':28, 'Mar':31, 
          'Apr':30, 'May':31, 'Jun':30, 
          'Jul':31, 'Aug':31, 'Sep':30,
          'Oct':31, 'Nov':30, 'Dec':31}
CUR_YEAR = 2024
CLUBS = ["Investment Club", "Accounting Club", "AI Club",
         "Alliance of Indigenous Scholars", "Alpha Psi Omega",
         "Ballet Folklorico", "Board Game Club", 
         "Black Student Alliance", "Cheer", "CS Club", 
         "First Generation Scholars", "Forensic Association",
         "Happy Feet", "Hilltop Productions", "i4",
         "International Student Association", "March for Our Lives",
         "Math Club", "MUSE", "Muslim Student Association", 
         "Phi Delta Alpha", "Physics Club", "PRIDE", "Rowing Club",
         "Bird Watching Club", "Women in STEM"]
MAJORS = ["Accounting", "Mathematics", "Acting", "Nursing", "Finance",
          "Pre-Dental", "Chemistry", "French", "Criminal Justice",
          "Computer Science", "Pre-Medical", "Global Studies",
          "Psychology", "History", "Spanish", "Social Work", "Digital Media",
          "Theater Arts", "Kinesiology", "Marketing", "Video Game Dev."]

with open("Example-Dataset-Generators/first_names.txt") as f:
    FIRST_NAMES = f.readlines()

with open("Example-Dataset-Generators/last_names.txt") as f:
    LAST_NAMES = f.readlines()

if __name__ == '__main__':
    print(f"Generating a dataset of {NUM_STUDENTS} random students")
    print(f"Possible first names: {len(FIRST_NAMES)}\nPossible last names: {len(LAST_NAMES)}")

    # Making fake names
    names = []
    for _ in range(NUM_STUDENTS):
        names.append(random.choice(LAST_NAMES).strip() + ', ' + random.choice(FIRST_NAMES).strip())
    
    # Making fake birthdays
    b_days = []
    for _ in range(NUM_STUDENTS):
        b_month = random.choice(list(MONTHS.keys()))
        b_year = CUR_YEAR - int(random.gauss(21, 2))
        b_days.append(str(random.randint(1, MONTHS[b_month])) + ' ' + b_month + ', ' + str(b_year))
    
    # Making fake GPAs
    overall_gpas = [round(random.gauss(3.0, 0.4), 2) for _ in range(NUM_STUDENTS)]
    major_gpas = [round(gpa + random.gauss(-0.2, 0.1), 2) for gpa in overall_gpas]

    # Making academic standing
    standings = []
    for i in range(NUM_STUDENTS):
        if random.randint(1, 100) <= 8:
            standings.append("Financial Hold")
        elif overall_gpas[i] < 2.5:
            standings.append("Academic Probation")
        elif major_gpas[i] < 2.5:
            standings.append("Insuff. Major GPA")
        else:
            standings.append("Good Standing")
    







        
