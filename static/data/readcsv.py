import csv

with open('Emp_details.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    ID="114185"
    Name=""
    Location=""
    BU=""
    for row in readCSV:
        if row[0]==ID:
            Name=row[1]
            Location=row[2]
            BU=row[3]
    print(ID)
    print(Name)
    print(Location)
    print(BU)
