# Rinno Train
Programming exercise for Application Developer position in the Office of the Vice Chancellor for Research and Innovation at the University of Illinois Urbana-Champaign.

This CLI tool generates three reports from the specified training records JSON file. 

## Report 1: Training Completion Totals
The `completion_totals.json` report lists all training programs in alphabetical order with a count of how many people have completed that training.

## Report 2: Completion By Fiscal Year
The `completion_by_year.json` report lists all employees that have completed any of the specified training programs during the specified fiscal year.

## Report 3: Expired/Expiring Training
The `expiration_by_date.json` report lists all employees that have or will have expired training programs by the specified date.
Each training program entry has a status field to indicate whether the program will expire soon (within a month) or is already expired.


## Report Customization
The reports can be configured via command line arguments. To see the available parameters run:

```
python main.py -h
```

To generate reports with default values (all programs as of today), run:

```
python main.py -i trainings.json
```

### Configuration Example
- report 1: can't be customized
- report 2: fiscal year 2024 and only consider the programs "Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"
- report 3: expiration date of Oct 1st, 2023

```
python main.py --input trainings.json --fiscal_year 2024 --expiration "10/1/2023" "Electrical Safety for Labs" "X-Ray Safety" "Laboratory Safety Training"
```

Same example using short form: 
```
python main.py -i trainings.json -y 2024 -x "10/1/2023" "Electrical Safety for Labs" "X-Ray Safety" "Laboratory Safety Training"
```

