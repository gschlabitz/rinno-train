import json
from datetime import datetime


def aggregate_training_programs(completion_record):
    names = set()
    for record in completion_record:
        if "completions" in record:
            for completion in record['completions']:
                if "name" in completion:
                    names.add(completion['name'])

    return sorted(list(names))


def has_completed_training_program(program_name, completion_records):
    for completion in completion_records:
        if "name" in completion and completion['name'] == program_name:
            return True
    return False


def count_program_completions(training_programs, training_records):
    totals = {}
    for program in training_programs:
        totals[program] = 0
        for record in training_records:
            if "completions" in record:
                if has_completed_training_program(program, record['completions']):
                    totals[program] += 1
    return totals


def main():
    # TODO: add paramter parsing
    # Using hardcoded parameters for now
    input_file = 'trainings.json'
    training_records = None

    # Load training data from specified JSON file
    with open(input_file, 'r') as file:
        training_records = json.load(file)

    training_programs = aggregate_training_programs(training_records)
    completion_totals = count_program_completions(
        training_programs, training_records)

    # Save completion totals as an ordered dictionary in JSON format
    with open("completion_totals.json", 'w') as file:
        json.dump(completion_totals, file, indent=4, default=str)


if __name__ == '__main__':
    main()
