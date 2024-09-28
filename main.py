import json
from datetime import datetime, timedelta


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


def date_from_string(date_string):
    try:
        return datetime.strptime(date_string, "%m/%d/%Y")
    except:
        return None


def is_within_fiscal_year(fiscal_year, timestamp):
    fiscal_year_start = datetime(fiscal_year-1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)
    completion_date = date_from_string(timestamp)

    return fiscal_year_start <= completion_date <= fiscal_year_end


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


def index_expired_programs(completions, expiration_date, expires_in_days=0):
    most_recent_expired = {}
    for completion in completions:
        program = completion.get('name')
        if not program:
            continue

        expiration = date_from_string(completion.get('expires'))
        if not expiration:
            continue

        delta = expiration - expiration_date
        is_expired = delta.days < 0 and expires_in_days == 0
        expires_soon = expires_in_days > 0 and delta.days >= 0 and delta.days <= expires_in_days
        if is_expired or expires_soon:
            if program in most_recent_expired:
                most_recent = date_from_string(most_recent_expired[program])
                if expiration > most_recent:
                    most_recent_expired[program] = completion['expires']
            else:
                most_recent_expired[program] = completion['expires']

    return most_recent_expired


def generate_expiration_report_by_date(training_records, expiration):
    expiration_date = date_from_string(expiration)
    report = []
    for record in training_records:
        if "completions" not in record:
            continue

        entry = {'name': record['name']}

        expired_programs = index_expired_programs(
            record['completions'], expiration_date)
        programs_expiring_next_month = index_expired_programs(
            record['completions'], expiration_date, 30)

        programs = []
        for program in expired_programs:
            programs.append({
                'name': program,
                'expiration': expired_programs[program],
                'status': 'expired'
            })

        for program in programs_expiring_next_month:
            programs.append({
                'name': program,
                'expiration': programs_expiring_next_month[program],
                'status': 'expires soon'
            })

        if programs:
            report.append({
                'name': record['name'],
                'expired_training': programs
            })

    return sorted(report, key=lambda x: x['name'])


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
    expiration_date = "10/1/2023"

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

    # Excercise 2: List everyone that completed a given training
    # in a given fiscal year
    completion_report_by_year = generate_completion_report_by_year(
        training_records, fiscal_year, training_program_queries)

    with open("completion_report_by_year.json", 'w') as file:
        json.dump(completion_report_by_year, file, indent=4, default=str)

    # Excercise 3: List everyone whose training has expired or will expire
    # within a month of a given date.
    expiration_report_by_date = generate_expiration_report_by_date(
        training_records, expiration_date)

    with open("expiration_report_by_date.json", 'w') as file:
        json.dump(expiration_report_by_date, file, indent=4, default=str)


if __name__ == '__main__':
    main()
