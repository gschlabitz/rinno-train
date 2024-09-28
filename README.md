# Rinno Train
Programming exercise for Application Developer position in the Office of the Vice Chancellor for Research and Innovation at the University of Illinois Urbana-Champaign.

This CLI tool generates three reports from the specified training records JSON file. The reports can not be generated seperately, so each command line argument
must be specified every time. Example:

```
python main.py --input trainings.json --year 2024 --expiration "10/1/2023"  "Program 1" "Program 2"
```

Using short form: 
```
python main.py -i trainings.json -y 2024 -x "10/1/2023" "Program 1" "Program 2"
```

## Report 1: Training Completion Totals
The `completion_totals.json` report lists all training programs in alphabetical order with a count of how many people have completed that training.


## Report 2: Completion By Fiscal Year
The `completion_by_year.json` report lists all employees that have completed any of the specified training programs during the specified fiscal year.

## Report 3: Expired/Expiring Training
The `expiration_by_date.json` report lists all employees that have or will have expired training programs by the specified date.
Each training program entry has a status field to indicate whether the program will expire soon (within a month) or is already expired.
