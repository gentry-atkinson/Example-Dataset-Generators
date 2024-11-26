# Author: Gentry Atkinson (gatkins0@stedwards.edu)
# Organization: St. Edwards Universtiy
# Date: 26 November, 2024

import random
import numpy as np
import pandas as pd

WITH_NOISE = True

NUM_EMPLOYEES = 75000
COLA = 0.04
MAX_VACATION_DAYS = 32
MAX_REVIEW_SCORE = 5.
MISSING_DEPTS = 0.2

MEAN_SALARIES_BY_DEPARTMENT = {
    "Human Resources" : 60000,
    "It" : 58000,
    "Accounting" : 64000,
    "Legal" : 110000,
    "Product Engineering" : 87000,
    "Quality Assurance" : 82000,
    "Operations" : 53000,
    "Customer Service" : 37000,
    "Sales" : 66000,
    "Manufactoring" : 42000
}

EDUCATION_BY_DEPARTMENT = {
    "Human Resources" : 'BBA',
    "IT" : 'BS',
    "Accounting" : 'MS',
    "Legal" : 'JD',
    "Product Engineering" : 'MS',
    "Quality Assurance" : 'BA',
    "Operations" : 'BS',
    "Customer Service" : 'BA',
    "Sales" : 'BBA',
    "Manufactoring" : 'High School/ GED'
}

ABBREVIATIONS_BY_DEPARTMENT = {
    "Human Resources" : 'HR',
    "IT" : 'IT',
    "Accounting" : 'AC',
    "Legal" : 'LG',
    "Product Engineering" : 'PE',
    "Quality Assurance" : 'QA',
    "Operations" : 'OP',
    "Customer Service" : 'CS',
    "Sales" : 'SL',
    "Manufactoring" : 'MN'
}

DEGREES = ['AAS', 'AA', 'BA', 'BS', 'MA', 'MS', 'MBA', 'PhD', 'JD', 'MEd', 'BBA', 'High School/ GED']

GENDER_CHOICES = ['Male', 'Female', 'Other/ Did Not Specify']

LOCATIONS = ['Austin, TX', 'Seattle, WA', 'San Diego, CA']

Locations = []

# Columns: employee id, age, years employment, most recent annual review, 
#   highest annual review, lowest annual review, salary, department, 
#   accumulated vacation days, job title, location, w2 witholding, married?, 
#   coded job title, gender

if __name__ == '__main__':
    employee_ids = [None] * NUM_EMPLOYEES
    ages = [None] * NUM_EMPLOYEES
    marrieds = [None] * NUM_EMPLOYEES
    genders = [None] * NUM_EMPLOYEES
    years = [None] * NUM_EMPLOYEES
    most_recent_reviews = [None] * NUM_EMPLOYEES
    highest_reviews = [None] * NUM_EMPLOYEES
    lowest_reviews = [None] * NUM_EMPLOYEES
    accumulated_vacations = [None] * NUM_EMPLOYEES
    locations = [None] * NUM_EMPLOYEES
    withholdings = [None] * NUM_EMPLOYEES
    job_titles = [None] * NUM_EMPLOYEES
    departments = [None] * NUM_EMPLOYEES

    for i in range(NUM_EMPLOYEES):
        dept = random.choices(
            list(MEAN_SALARIES_BY_DEPARTMENT.keys()), 
            weights=[0.05, 0.1, 0.05, 0.02, 0.2, 0.05, 0.1, 0.15, 0.12, 0.16],
            k=1
        )

        id = 'EMP' + str(random.randint(100_000_000, 999_999_999)) + random.choice(['d', 't', 'l', 'k'])
        age = random.randint(18, 68)
        year = min(random.randint(1, 35), age-18)
        gender = random.choices(
            GENDER_CHOICES,
            weights = [0.45, 0.45, 0.1],
            k=1
        )