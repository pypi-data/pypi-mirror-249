import json, os

def checker(jsonFile, jsonSchema):

    assert type(jsonFile) == str, "jsonFile must be a string."
    assert os.path.isfile(jsonFile), "jsonFile must be a file."

    if (type(jsonSchema) == str):

        assert os.path.isfile(jsonSchema), "jsonSchema must be a file."

        with open(jsonSchema) as json_file:
            jsonSchema = json.load(json_file)

            for item in jsonSchema.values():
                assert item in [ "int", "float", "bool", "str", "list", "dict" ], "jsonSchema must be a valid schema."

            jsonSchema = { key: eval(value) for key, value in jsonSchema.items() }
            
    else:
        assert type(jsonSchema) == dict, "jsonSchema must be a dictionary."

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
