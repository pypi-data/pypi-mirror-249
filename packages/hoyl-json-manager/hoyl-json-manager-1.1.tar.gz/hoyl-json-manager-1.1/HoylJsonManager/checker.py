import json

def checker(jsonFile, jsonSchema):

    assert type(jsonFile) == str, "jsonFile must be a string"
    assert type(jsonSchema) == dict, "jsonSchema must be a dictionary"

    jsonFile += ".json" if jsonFile.endswith(".json") == False else ""

    strangeKeys = {
        "missing": [],
        "extra": [],
        "wrongType": []
    }

    with open(jsonFile) as json_file:

        jsonData = json.load(json_file)
        
        for key in jsonData:
            if (key not in jsonSchema):
                strangeKeys["extra"].append(key)
            elif (type(jsonData[key]) != jsonSchema[key]):
                strangeKeys["wrongType"].append(key)

        [ strangeKeys["missing"].append(key) for key in jsonSchema if key not in jsonData ]
        
        return strangeKeys
