# rinno-train
Programming exercise for Application Developer position in the Office of the Vice Chancellor for Research and Innovation at the University of Illinois Urbana-Champaign.

This CLI tool reads training records from the specified input .json file and generates three output files:

##Completed Totals
The `completed_totals.json` output file lists all training programs in alphabetical order with a count of how many people have completed that training.

###Usage
Specify the file path to the training program records JSON file.
```
python main.py -i trainings.json
python main.py --input trainings.json
```



