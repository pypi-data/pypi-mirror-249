import json

def update(jsonFile, key, value):

    assert type(jsonFile) == str, "jsonFile must be a string"
    assert type(key) == str, "key must be a string"
    assert type(value) == str, "value must be a string"

    jsonFile += ".json" if jsonFile.endswith(".json") == False else ""

    with open(jsonFile, "r", encoding="utf-8") as json_file:
            
            jsonData = json.load(json_file)
    
            if key not in jsonData:
                return False
            
            jsonData[key] = value
    
            with open(jsonFile, "w", encoding="utf-8") as json_file:
                json.dump(jsonData, json_file, indent=4)
    
            return True