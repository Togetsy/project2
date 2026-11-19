import json
from pathlib import Path
from repositories import animal_repository
import xml.etree.ElementTree as ET
import yaml

def export_json():
    data = animal_repository.get_all_for_export()

    Path("out").mkdir(exist_ok=True)

    with open("out/data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

import csv

def export_csv():
    data = animal_repository.get_all_for_export()

    Path("out").mkdir(exist_ok=True)

    with open("out/data.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "id", "name", "species", "sex",
                "age", "status", "owner"
            ]
        )

        writer.writeheader()

        for animal in data:
            row = animal.copy()
            row["owner"] = (
                json.dumps(animal["owner"], ensure_ascii=False)
                if animal["owner"] else ""
            )
            writer.writerow(row)

def export_xml():
    data = animal_repository.get_all_for_export()

    Path("out").mkdir(exist_ok=True)

    root = ET.Element("animals")

    for animal in data:
        animal_element = ET.SubElement(root, "animal")

        for key, value in animal.items():
            if key == "owner":
                owner = ET.SubElement(animal_element, "owner")

                if value:
                    for owner_key, owner_value in value.items():
                        ET.SubElement(owner, owner_key).text = str(owner_value)
            else:
                ET.SubElement(animal_element, key).text = (
                    str(value) if value is not None else ""
                )

    tree = ET.ElementTree(root)
    ET.indent(tree, space="    ")

    tree.write("out/data.xml", encoding="utf-8", xml_declaration=True)

def export_yaml():
    data = animal_repository.get_all_for_export()

    Path("out").mkdir(exist_ok=True)

    with open("out/data.yaml", "w", encoding="utf-8") as file:
        yaml.safe_dump(
            data,
            file,
            allow_unicode=True,
            sort_keys=False
        )

def export_all():
    export_json()
    export_csv()
    export_xml()
    export_yaml()

    print("Все файлы успешно экспортированы!")
