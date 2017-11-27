"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
"""

import json
import csv as csv

def csv_to_json(f, delimiter = ','):
    reader = csv.reader(f, delimiter=delimiter)
    csv_lines = list(reader)
    header = csv_lines[0]
    json_object = []
    for row in csv_lines[1:]:
        tmp = {}
        for item_idx, item in enumerate(row):
            if(item_idx < len(header)):
                tmp[header[item_idx]] = item
        json_object.append(tmp)
    return json.dumps(json_object)