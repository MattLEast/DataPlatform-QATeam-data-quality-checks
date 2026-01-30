import json
import os
from fileinput import filename
from typing import Any, Dict, List, Union

import tkinter
from tkinter import filedialog

def selectFile():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file")
    #base_path = filedialog.askdirectory(title="Select a file")

    if file_path:
        print(file_path)
    else:
        print("No file selected")
    return file_path

def _get_json_schema_type(value: Any) -> str:
    """Maps a Python type to its corresponding JSON Schema type string."""
    py_type = type(value)

    if py_type is int:
        return "integer"
    elif py_type is float:
        return "number"
    elif py_type is bool:
        return "boolean"
    elif py_type is str:
        return "string"
    elif py_type is list:
        return "array"
    elif py_type is dict:
        return "object"
    else:
        # Fallback for nulls or other unexpected types
        return "string"


def infer_schema(data: Union[Dict, List, Any]) -> Dict:
    if isinstance(data, dict):
        properties = {}
        # Strict Rule: Assume all keys present in the sample are required.
        required_keys = list(data.keys())

        for key, value in data.items():
            schema_type = _get_json_schema_type(value)

            if schema_type == "object":
                # Recursive call for nested objects
                property_schema = infer_schema(value)
            elif schema_type == "array":
                property_schema = {"type": "array"}
                if value:
                    # Infer schema of array items based on the first element
                    property_schema["items"] = infer_schema(value[0])
                else:
                    # Default items to string if the sample array is empty
                    property_schema["items"] = {"type": "string"}
            else:
                # Primitive types
                property_schema = {"type": schema_type}


            properties[key] = property_schema

        return {
            "type": "object",
            "properties": properties,
            "required": required_keys,
            # Strict Rule: Prevents inclusion of properties not listed in the schema
            "additionalProperties": False
        }

    elif isinstance(data, list):
        # Arrays are handled recursively above; this is a fallback for top-level list
        if data:
            # Infer the item schema based on the first element
            return infer_schema(data[0])
        else:
            return {"type": "object"}  # Default to object if list is empty

    else:
        # Primitive types (should be handled within the dict loop)
        return {"type": _get_json_schema_type(data)}


def generate_and_print_schema(file_path: str, schemaName):
    try:
        # Ensure path is relative to the project root structure
        script_dir = os.path.dirname(__file__)
        full_path = os.path.join(script_dir, file_path)

        with open(full_path, 'r') as f:
            sample_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: JSON file not found at {full_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON file at {file_path}")
        return

    data_to_infer = sample_data
    if isinstance(sample_data, list) and sample_data:
        # If the input is a list of objects, we infer the schema for the item object
        print(
            "Note: Input is an array. Inferring schema for the first item (object) only to match the desired format structure.")
        data_to_infer = sample_data[0]
    elif isinstance(sample_data, list):
        print("Warning: Input array is empty. Generating empty object schema.")
        data_to_infer = {}

    # Infer the schema
    generated_schema = infer_schema(data_to_infer)

    # print("-" * 50)
    # print(f"Generated Schema (Strict Format) from {file_path}:\n")
    # print(json.dumps(generated_schema, indent=2))
    # print("-" * 50)

    #print("-" * 50)
    #schemaName = input("Please add schema name")
    if schemaName.split(".")[-1] == "json":
        fileName = schemaName
    else:
        fileName= schemaName +".json"
    print(f"Generated Schema (Strict Format) from {file_path}:\n")
    newSchema = json.dumps(generated_schema, indent=2)
    print(fileName)
    with open(fileName, "w") as f:
        f.write(newSchema)

    # print("-" * 50)


if __name__ == "__main__":
    jsonFile = selectFile()
    schemaName = input("Please add schema name ")
    print(jsonFile)
    generate_and_print_schema(jsonFile, schemaName)
    print(f"Schema file {schemaName} created successfully")