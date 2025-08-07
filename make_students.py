# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 9 July, 2024

### Change the CUR_YEAR value as you rerun this ###

import pandas as pd
import random
import numpy as np
import seaborn as sbn
from matplotlib import pyplot as plt

DEBUG = False

NUM_STUDENTS = 50000
NUM_ADVISORS = 7
WITH_NOISE = True
MONTHS = {'Jan':31, 'Feb':28, 'Mar':31, 
          'Apr':30, 'May':31, 'Jun':30, 
          'Jul':31, 'Aug':31, 'Sep':30,
          'Oct':31, 'Nov':30, 'Dec':31}
CUR_YEAR = 2025
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

def generate_skewed_integers_transform(size, power, min_val=0, max_val=100):
    """
    Generates skewed integers by transforming a uniform distribution.

    Args:
        size (int): The number of integers to generate.
        power (float): The power to raise the uniform values to.
                       >1 for left-skew, <1 (but >0) for right-skew.
        min_val (int): The minimum value of the desired range.
        max_val (int): The maximum value of the desired range.

    Returns:
        numpy.ndarray: An array of skewed integers.
    """
    uniform_data = np.random.rand(size)
    transformed_data = uniform_data**power
    scaled_data = min_val + transformed_data * (max_val - min_val)
    integers = np.round(scaled_data).astype(int)
    return integers

if __name__ == '__main__':
    print(f"Generating a dataset of {NUM_STUDENTS} random students")
    print(f"Possible first names: {len(FIRST_NAMES)}\nPossible last names: {len(LAST_NAMES)}")

    # Making fake names
    names = []
    for _ in range(NUM_STUDENTS):
        names.append(random.choice(LAST_NAMES).strip() + ', ' + random.choice(FIRST_NAMES).strip())
    
    # Making fake GPAs
    overall_gpas = [random.gauss(3.0, 0.2) for _ in range(NUM_STUDENTS)]
    major_gpas = [gpa + random.gauss(-0.2, 0.075) for gpa in overall_gpas]

    # Making fake birthdays
    ages = generate_skewed_integers_transform(NUM_STUDENTS, power=3.5, min_val=18, max_val=35)
    b_days = []
    for i in range(NUM_STUDENTS):
        age = ages[i]
        b_month = random.choice(list(MONTHS.keys()))
        b_year = CUR_YEAR - age
        b_days.append(str(random.randint(1, MONTHS[b_month])) + ' ' + b_month + ', ' + str(b_year))

        # TREND- older students have higher GPAs
        overall_gpas[i] += random.gauss((age-18)*0.1, 0.1)
        major_gpas[i] += random.gauss((age-18)*0.1, 0.1)

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
            overall_gpas[i] -= 0.2
            major_gpas[i] -= 0.3

    # Making advisors
    advisors = []
    for major in majors:
        advisors.append(ADVISORS[int(MAJORS.index(major) / len(MAJORS) * NUM_ADVISORS)])

    # Making academic standing
    standings = []
    for i in range(NUM_STUDENTS):
        if overall_gpas[i] < 2.5:
            standings.append("Academic Probation")
        elif major_gpas[i] < 2.5:
            standings.append("Academic Warning")
        elif random.randint(1, 100) <= 8:
            standings.append("Financial Hold")
        else:
            standings.append("Good Standing")
    

    # Making club lists
    clubs = []
    for gpa in overall_gpas:
        # TREND- students with higher GPAs join more clubs
        if gpa > 3.8:
            clubs.append(random.sample(CLUBS, random.randint(1,5)))
        elif gpa > 3.0:
            clubs.append(random.sample(CLUBS, random.randint(1,3)))
        elif gpa > 2.5:
            clubs.append(random.sample(CLUBS, random.randint(0,2)))
        else:
            clubs.append(random.sample(CLUBS, random.randint(0,1)))

    # Making student IDs
    stud_ids = []
    for i, name in enumerate(names):
        s_id = random.choice(['G', 'D', 'T'])
        s_id += str(random.randint(10, 99))
        s_id += name[0].upper()
        s_id += f"{ADVISORS.index(advisors[i]):02d}"
        s_id += b_days[i][-4:]
        s_id += f"{MAJORS.index(majors[i]):02d}"
        assert len(s_id) == 12, "Bad len of student id"
        stud_ids.append(s_id)

    #Making Net IDs
    # net_ids = []
    # for name in names:
    #     n_id = name[0:3]
    #     n_id += name.split(',')

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
    print(f"Mean overall gpa: {np.mean(overall_gpas)}")
    print(f"Mean major gpa: {np.mean(major_gpas)}")
    print(f"Max overall gpa: {max(overall_gpas)}")
    print(f"Max major gpa: {max(major_gpas)}")
    
    # Convert to DF and write to JSON
    table = pd.DataFrame.from_dict({
        "Name": names,
        "Student ID" : stud_ids,
        "Date of Birth": b_days,
        "Major": majors,
        "Minor": minors,
        "Advisor" : advisors,
        "Overall GPA": overall_gpas,
        "Major-Specific GPA": major_gpas,
        "Academic Standing": standings,
        "Club Participation": clubs
    })

    if DEBUG:
        table['Age'] = ages

    print(table[['Name', 'Overall GPA', 'Major-Specific GPA', 'Date of Birth']].head(10))
    table.to_json("Student Database.json")
    table.to_excel("Student Database.xlsx")

    if DEBUG:
        print('DEBUG- show age/gpa plot')
        print(table['Age'].value_counts().sort_index())
        sbn.scatterplot(data=table, x='Age', y='Overall GPA')
        plt.show()