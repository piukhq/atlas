import io
import csv


def write_to_csv(list_for_csv):
    csv_file = io.StringIO()

    fieldnames = list_for_csv[0].keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(list_for_csv)
    return csv_file.getvalue()
