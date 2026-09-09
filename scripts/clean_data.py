import pandas as pd

df = pd.read_csv(r"C:\Users\prafu\Desktop\project-hr\archive\HR_Employee_Data.csv")


print("Shape: ",df.shape)

print("\n Columns: ")
print(df.columns.tolist())

print("Duplicate employee numbers: ")
print(df["EmployeeNumber"].duplicated().sum())

print("Missing values: ")
print(df.isnull().sum())

print("Departments: ")
print(df["Department"].unique())

print("Job roles: ")
print(df["JobRole"].unique())

print("Attrition: ")
print(df["Attrition"].unique())

print("Overtime: ")
print(df["OverTime"].unique())

print("data types: ")
print(df.dtypes)

#checking which columns are constant
const_columns=df.columns[df.nunique()== 1]

print("Constant Column: ")
print(const_columns.tolist())

print(df["EmployeeCount"].unique())
print(df["Over18"].unique())
print(df["StandardHours"].unique())

df=df.drop(columns=["EmployeeCount","Over18","StandardHours"])

print("new shape: ",df.shape)
print("new columns: ",df.columns.tolist())


#checking if there is any invalid values by checking from min to max values
print("\nChecking numeric ranges:")

print("Age:", df["Age"].min(), "-", df["Age"].max())
print("Monthly Income:", df["MonthlyIncome"].min(), "-", df["MonthlyIncome"].max())
print("Total Working Years:", df["TotalWorkingYears"].min(), "-", df["TotalWorkingYears"].max())
print("Years At Company:", df["YearsAtCompany"].min(), "-", df["YearsAtCompany"].max())
print("Years In Current Role:", df["YearsInCurrentRole"].min(), "-", df["YearsInCurrentRole"].max())
print("Years Since Last Promotion:", df["YearsSinceLastPromotion"].min(), "-", df["YearsSinceLastPromotion"].max())
print("Years With Current Manager:", df["YearsWithCurrManager"].min(), "-", df["YearsWithCurrManager"].max())


# values will range from 1 to 4 where 1 means least satisfied and 4 means most satisfied. We need to mostly know the job satisfaction where higher means better
print("\nSatisfaction and rating values:")

print("Environment Satisfaction:", df["EnvironmentSatisfaction"].unique())
print("Job Satisfaction:", df["JobSatisfaction"].unique())
print("Job Involvement:", df["JobInvolvement"].unique())
print("Performance Rating:", df["PerformanceRating"].unique())
print("Relationship Satisfaction:", df["RelationshipSatisfaction"].unique())
print("Work Life Balance:", df["WorkLifeBalance"].unique())

print("\nChecking experience consistency:")

invalid_years = df[
    (df["YearsAtCompany"] > df["TotalWorkingYears"]) |
    (df["YearsInCurrentRole"] > df["YearsAtCompany"]) |
    (df["YearsSinceLastPromotion"] > df["YearsAtCompany"]) |
    (df["YearsWithCurrManager"] > df["YearsAtCompany"])
]

print("Potentially inconsistent records:", len(invalid_years))


output_path = r"C:\Users\prafu\Desktop\project-hr\archive\new_HR_Employee_data.csv"

df.to_csv(output_path, index=False)

print("Cleaned dataset has been saved successfully...")
print("Final Shape of the database is: ",df.shape)