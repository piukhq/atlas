import io
import csv


def write_to_csv(dict_for_csv):
    csv_file = io.StringIO()
    fieldnames = ['email', 'opt_out_timestamp']

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(dict_for_csv)
    return csv_file.getvalue()
