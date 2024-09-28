# Rinno Train
Programming exercise for Application Developer position in the Office of the Vice Chancellor for Research and Innovation at the University of Illinois Urbana-Champaign.

This CLI tool reads training records from the specified input .json file and generates three output files:

## Exercise 1: Completed Totals
The `completed_totals.json` output file lists all training programs in alphabetical order with a count of how many people have completed that training.

###Usage
Specify the file path to the training program records JSON file.
```
python main.py -i trainings.json
python main.py --input trainings.json
```


## Exercise 2: People That Completed Within Fiscal Year
The `completion_report_by_year.json` output file lists all persons that have completed any of the specified training programs during the specified fiscal year.

###Usage
Specify the file path to the training program records JSON file.
Specify the fiscal year.
List training programs by name and in quotes as positional parameters.

```
python main.py -i trainings.json -y 2024 "Program 1" "Program 2"
python main.py --input trainings.json --year 2024 "Program 1" "Program 2"
```

## Exercise 3: People That Have Expired/Expiring Training Programs
The `expiration_report_by_date.json` output file lists all persons that have or will have expired training programs by the specified date.
Each training program entry has a status field to indicate wether the program will expire soon (within a month) or is already expired.

###Usage
Specify the file path to the training program records JSON file.
Specify the expiration date quotes using the format "m/d/Y", e.g. 10/1/2024.

```
python main.py -i trainings.json -x "10/1/2023"
python main.py --input trainings.json -expiration "10/1/2023"
```
