import csv

with open('Emp_details.csv','a') as csvfile:
    ID="114185"
    Name="RAMU"
    Location="MUMBAI"
    BU="FS"
    newemp=ID+","+Name+","+Location+","+BU
    csvfile.write(newemp+"\n")
