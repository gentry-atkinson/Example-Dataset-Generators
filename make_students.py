# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 9 July, 2024

### Change the CUR_YEAR value as you rerun this ###

import pandas as pd
import random
from numpy import count_nonzero, mean

NUM_STUDENTS = 50000
NUM_ADVISORS = 7
WITH_NOISE = True
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

with open("first_names.txt") as f:
    FIRST_NAMES = f.readlines()

with open("last_names.txt") as f:
    LAST_NAMES = f.readlines()

ADVISORS = []
for _ in range(NUM_ADVISORS):
    ADVISORS.append(random.choice(FIRST_NAMES).strip() + ' ' + random.choice(LAST_NAMES).strip())

if __name__ == '__main__':
    print(f"Generating a dataset of {NUM_STUDENTS} random students")
    print(f"Possible first names: {len(FIRST_NAMES)}\nPossible last names: {len(LAST_NAMES)}")

    # Making fake names
    names = []
    for _ in range(NUM_STUDENTS):
        names.append(random.choice(LAST_NAMES).strip() + ', ' + random.choice(FIRST_NAMES).strip())
    
    # Making fake GPAs
    overall_gpas = [random.gauss(3.0, 0.4) for _ in range(NUM_STUDENTS)]
    major_gpas = [gpa + random.gauss(-0.2, 0.1) for gpa in overall_gpas]

    # Making fake birthdays
    b_days = []
    for i in range(NUM_STUDENTS):
        b_month = random.choice(list(MONTHS.keys()))
        b_year = CUR_YEAR - int(random.gauss(21, 2))
        b_days.append(str(random.randint(1, MONTHS[b_month])) + ' ' + b_month + ', ' + str(b_year))

        # TREND- older students have higher GPAs
        age = CUR_YEAR - b_year
        overall_gpas[i] += random.gauss((age-18)*0.01, 0.1)
        major_gpas[i] += random.gauss((age-18)*0.01, 0.1)

    # Making majors
    majors = [random.choice(MAJORS) for _ in range(NUM_STUDENTS)]
    minors = []
    for major in majors:
        if random.randint(1, 100) <= 70:
            minors.append("None")
        else:
            minor = random.choice(MAJORS)
            while minor == major:
                minor = random.choice(MAJORS)
            minors.append(minor)
    for i, minor in enumerate(minors):
        # TREND- GPAs are lower for students that have a minor
        if minor != "None":
            overall_gpas[i] -= 0.1
            major_gpas[i] -= 0.2

    # Making advisors
    advisors = []
    for major in majors:
        advisors.append(ADVISORS[int(MAJORS.index(major) / len(MAJORS) * NUM_ADVISORS)])

    # Making academic standing
    standings = []
    for i in range(NUM_STUDENTS):
        if random.randint(1, 100) <= 8:
            standings.append("Financial Hold")
        elif overall_gpas[i] < 2.5:
            standings.append("Academic Probation")
        elif major_gpas[i] < 2.5:
            standings.append("Academic Warning")
        else:
            standings.append("Good Standing")
    

    # Making club lists
    clubs = []
    for gpa in overall_gpas:
        # TREND- students with higher GPAs join more clubs
        if gpa > 3.8:
            clubs.append(random.sample(CLUBS, random.randint(0,4)))
        elif gpa > 3.0:
            clubs.append(random.sample(CLUBS, random.randint(0,3)))
        elif gpa > 2.5:
            clubs.append(random.sample(CLUBS, random.randint(0,2)))
        else:
            clubs.append(random.sample(CLUBS, random.randint(0,1)))

    # Sanity checking and rounding GPAs
    for i, gpa in enumerate(overall_gpas):
        if gpa > 4.0:
            overall_gpas[i] = 4.00
        else:
            overall_gpas[i] = round(gpa, 2)

    for i, gpa in enumerate(major_gpas):
        if gpa > 4.0:
            major_gpas[i] = 4.00
        else:
            major_gpas[i] = round(gpa, 2)
    
    # Adding Noise
    if WITH_NOISE:
        # NOISE- some students are 124 years old
        for i in [random.randint(0, NUM_STUDENTS-1) for _ in range(NUM_STUDENTS//5000)]:
            b_days[i] = "01 Jan, 1900"

        # NOISE- unreasonably high major specific gpas with an error in standing
        for i in [random.randint(0, NUM_STUDENTS-1) for _ in range(NUM_STUDENTS//5000)]:
            major_gpas[i] *= 10
            standings[i] = "**ERROR**"

        # NOISE- some students have a single club entered in their list multiple times
        for i in [random.randint(0, NUM_STUDENTS-1) for _ in range(NUM_STUDENTS//5000)]:
            club = random.choice(CLUBS)
            clubs[i] = [club for __ in range(6)]

        # NUISANCE- the names of some advisors are all caps
        for i in [random.randint(0, NUM_STUDENTS-1) for _ in range(NUM_STUDENTS//5000)]:
            advisors[i] = advisors[i].upper()

        # NOISE- NaN entered for some overall GPAs
        for i in [random.randint(0, NUM_STUDENTS-1) for _ in range(NUM_STUDENTS//5000)]:
            overall_gpas[i] = float('nan')

    # Summary
    print(f"Number of students in good standing: {standings.count('Good Standing')}")
    print(f"Number of students in fin hold: {standings.count('Financial Hold')}")
    print(f"Number of students in ac prob: {standings.count('Academic Probation')}")
    print(f"Number of students in ac warning: {standings.count('Academic Warning')}")
    print(f"Number of students in UNK: {standings.count('**ERROR**')}")
    print(f"Mean overall gpa: {mean(overall_gpas)}")
    print(f"Mean major gpa: {mean(major_gpas)}")
    print(f"Max overall gpa: {max(overall_gpas)}")
    print(f"Max major gpa: {max(major_gpas)}")
    
    # Convert to DF and write to JSON
    table = pd.DataFrame.from_dict({
        "Name": names,
        "Date of Birth": b_days,
        "Major": majors,
        "Minor": minors,
        "Advisor" : advisors,
        "Overall GPA": overall_gpas,
        "Major-Specific GPA": major_gpas,
        "Academic Standing": standings,
        "Club Participation": clubs
    })

    print(table[['Name', 'Overall GPA', 'Major-Specific GPA', 'Date of Birth']].head(10))
    table.to_json("Student Database.json")