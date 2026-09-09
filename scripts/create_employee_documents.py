import pandas as pd
import json

df=pd.read_csv(r"C:\Users\prafu\Desktop\project-hr\archive\new_HR_Employee_data.csv")

print("No of Employees loaded: ",len(df))


satisfaction_map={
    1:'Low',
    2:'Medium',
    3:'High',
    4:'Very High'
}

performance_map={
    3:'Good',
    4:'Excellent'
}

documents = []
ids = []
metadatas = []


#prints just one row with iloc we can print whichever row we want
#row=df.iloc[0]

for index, row in df.iterrows():
    document=f"""
Employee Number: {row['EmployeeNumber']}

Personal Information:
Age: {row['Age']}
Gender: {row['Gender']}
Marital Status: {row['MaritalStatus']}
Education Field: {row['EducationField']}

Employment:
Department: {row['Department']}
Job Role: {row['JobRole']}
Job Level: {row['JobLevel']}
Business Travel: {row['BusinessTravel']}

Compensation:
Monthly Income: {row['MonthlyIncome']}
Daily Income: {row['DailyRate']}
Hourly Income: {row['HourlyRate']}
Monthly Income: {row['MonthlyRate']}
Percent Salary Hike: {row['PercentSalaryHike']}%

Experience:
Total Working Years: {row['TotalWorkingYears']}
Years At Company: {row['YearsAtCompany']}
Years In Current Role: {row['YearsInCurrentRole']}
Years Since Last Promotion: {row['YearsSinceLastPromotion']}
Years With Current Manager: {row['YearsWithCurrManager']}

Performance and Satisfaction:
Performance Rating: {performance_map[row['PerformanceRating']]} ({row['PerformanceRating']}/4)
Job Satisfaction: {satisfaction_map[row['JobSatisfaction']]} ({row['JobSatisfaction']}/4)
Environment Satisfaction: {satisfaction_map[row['EnvironmentSatisfaction']]} ({row['EnvironmentSatisfaction']}/4)
Job Involvement: {satisfaction_map[row['JobInvolvement']]} ({row['JobInvolvement']}/4)
Relationship Satisfaction: {satisfaction_map[row['RelationshipSatisfaction']]} ({row['RelationshipSatisfaction']}/4)
Work Life Balance: {satisfaction_map[row['WorkLifeBalance']]} ({row['WorkLifeBalance']}/4)


Work Conditions:
Overtime: {row['OverTime']}
Training Times Last Year: {row['TrainingTimesLastYear']}
Num Companies Worked: {row['NumCompaniesWorked']}

Attrition:
Attrition: {row['Attrition']}
"""

    documents.append(document)

    ids.append(f"employee_{row['EmployeeNumber']}")

    metadata = {
            "source_type": "employee",
            "employee_number": int(row["EmployeeNumber"]),
            "department": row["Department"],
            "job_role": row["JobRole"],
            "job_level": int(row["JobLevel"]),
            "attrition": row["Attrition"],
            "overtime": row["OverTime"]
    }

    metadatas.append(metadata)


print("Documents created: ",len(documents))
print("IDS created: ",len(ids))
print("Metadata record created: ",len(metadatas))

employee_data = []

for i in range(len(documents)):
    employee_data.append({
        "id": ids[i],
        "text": documents[i],
        "metadata": metadatas[i]
    })

output_path = r"C:\Users\prafu\Desktop\project-hr\documents\employee_documents.json"

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(
        employee_data,
        file,
        indent=2,
        ensure_ascii=False
    )

print("Employee documents saved successfully.")
print("Employee records saved:", len(employee_data))
