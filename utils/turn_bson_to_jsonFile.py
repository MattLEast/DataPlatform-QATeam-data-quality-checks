import json, re
from pathlib import Path
import base64
from functions.helper_functions import selectGame, BsonReader
from functions.helper_functions import Filelister

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8')  # Try to decode as UTF-8
            except UnicodeDecodeError:
                return base64.b64encode(obj).decode('utf-8')  # Fallback to base64 encoding
        return super().default(obj)


def turn_bson_to_jsonFile(jsonFileName):
    # Select the BSON file
    filePath = selectGame("file")  # Assuming selectGame() returns the path to the BSON file
    bsonFile = BsonReader(filePath)

    # Read the BSON data
    bdata = bsonFile.read()

    # Prepare the output directory
    dst = Path("../resources/jsonFiles")
    dst.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

    # Create the JSON file name
    fileName = f"{jsonFileName}.json"
    dstFileName = dst / fileName  # Save the JSON file directly in the destination

    # Convert BSON data to JSON string using the custom encoder
    json_str = json.dumps(bdata, indent=4, cls=CustomJSONEncoder)

    # Write the JSON string to a file

    with open(dstFileName, "w") as f:
        f.write(json_str)


def turn_bson_to_jsonFiles(gameDetails, dataType):
    # Select the BSON file
    filePath = selectGame()  # Assuming selectGame() returns the path to the BSON file
    files =Filelister(filePath)
    fileList = files.list_files()
    for file in fileList:
        fileName = Path(filePath, file)
        bson_reader = BsonReader(fileName)
        bdata = bson_reader.read()
        keyData = bdata[0]
        dstPath = Path("../resources/jsonFiles/fromBson")
        dst = dstPath / gameDetails / dataType
        dst.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        n = file.split(".")[0]
        fileName = f"{n}.json"
        dstFileName = dst / fileName  # Save the JSON file directly in the destination
        print(dstFileName)
        json_str = json.dumps(bdata, indent=4, cls=CustomJSONEncoder)
        with open(dstFileName, "w") as f:
            f.write(json_str)


if __name__ == "__main__":
    gameDetails = "BSONS_0022500283"
    dataType = "tracking"
    newJsonFile = turn_bson_to_jsonFiles(gameDetails, dataType)