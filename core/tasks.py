import csv
from django.conf import settings
from faker import Faker
from DummyCSV.celery import app



@app.task
def csv_create_task(dataset_id):
    from core.models import DataSetModel,ColumnModel,TableModel
    fake = Faker()

    dataset = DataSetModel.objects.filter(id=dataset_id).first()
    if not dataset:
        return
    schema = TableModel.objects.filter(id=dataset.schema_id).first()
    columns = ColumnModel.objects.filter(table=schema.id).order_by("order").values()
    delimeter = schema.column_separator
    quotechar = schema.string_character
    row_number = dataset.rows
    header = []
    all_rows = []
    for column in columns:
        header.append(column["name"])

    for row in range(row_number):
        raw_row = []
        for column in columns:
            column_type = column["column_type"]
            if column_type == ColumnModel.FULL_NAME:
                data = fake.name()
            elif column_type == ColumnModel.JOB:
                data = fake.job()
            elif column_type == ColumnModel.EMAIL:
                data = fake.email()
            elif column_type == ColumnModel.DOMAIN_NAME:
                data = fake.domain_name()
            elif column_type == ColumnModel.PHONE_NUMBER:
                data = fake.phone()
            elif column_type == ColumnModel.COMPANY_NAME:
                data = fake.company()
            elif column_type == ColumnModel.TEXT:
                data = fake.sentences(
                    nb=fake.random_int(
                        min=column["range_from"] or 1,
                        max=column["range_to"] or 10
                    )
                )
                data =" ".join(data)

            elif column_type == ColumnModel.INTEGER:
                data = fake.random_int(
                    min=column["range_from"] or 0,
                    max=column["range_to"] or 99999
                )
            elif column_type == ColumnModel.ADDRESS:
                data = fake.address()
            elif column_type == ColumnModel.DATE:
                data = fake.date()
            else:
                data = None
            raw_row.append(data)
        all_rows.append(raw_row)
        print(all_rows)

    with open(f'{settings.MEDIA_ROOT}schema_{schema.id}dataset_{dataset_id}.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimeter, quotechar=quotechar, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(all_rows)
        dataset.status = dataset.Status.READY
        dataset.save()