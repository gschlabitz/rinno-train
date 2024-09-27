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


def is_within_fiscal_year(fiscal_year, timestamp):
    try:
        fiscal_year_start = datetime(fiscal_year-1, 7, 1)
        fiscal_year_end = datetime(fiscal_year, 6, 30)
        completion_date = datetime.strptime(timestamp, "%m/%d/%Y")
        return fiscal_year_start <= completion_date <= fiscal_year_end
    except:
        return False


def generate_completion_report_by_year(training_records, fiscal_year, training_programs):
    report = {}
    for program in training_programs:
        report[program] = []
        for record in training_records:
            if "completions" in record:
                for completion in record['completions']:
                    if "name" in completion and completion['name'] == program:
                        if is_within_fiscal_year(fiscal_year, completion['timestamp']):
                            report[program].append(record['name'])

        # sort and deduplicate aggregated people
        report[program] = sorted(list(set(report[program])))

    return report


def main():
    # TODO: add paramter parsing
    # Using hardcoded parameters for now
    input_file = 'trainings.json'
    training_program_queries = [
        "Electrical Safety for Labs",
        "X-Ray Safety",
        "Laboratory Safety Training"
    ]
    fiscal_year = 2024

    # Load training data from specified JSON file
    training_records = None
    with open(input_file, 'r') as file:
        training_records = json.load(file)

    training_programs = aggregate_training_programs(training_records)

    # Excercise 1: Count how many people have completed each training
    completion_totals = count_program_completions(
        training_programs, training_records)

    with open("completion_totals.json", 'w') as file:
        json.dump(completion_totals, file, indent=4, default=str)

    # Excercise 2: List everyone that completed a given training in a given fiscal year
    completion_report_by_year = generate_completion_report_by_year(
        training_records, fiscal_year, training_program_queries)

    with open("completion_report_by_year.json", 'w') as file:
        json.dump(completion_report_by_year, file, indent=4, default=str)


if __name__ == '__main__':
    main()
