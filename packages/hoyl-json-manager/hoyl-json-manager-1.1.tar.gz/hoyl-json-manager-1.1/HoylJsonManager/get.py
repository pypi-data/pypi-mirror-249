import json

def get(jsonFile):
        
    assert type(jsonFile) == str, "jsonFile must be a string"

    jsonFile += ".json" if jsonFile.endswith(".json") == False else ""

    with open(jsonFile, "r", encoding="utf-8") as json_file:

        jsonData = json.load(json_file)

        return jsonData