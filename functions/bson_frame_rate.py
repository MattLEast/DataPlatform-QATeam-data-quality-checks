# from dataclasses import dataclass
# from typing import Iterable, List, Sequence
from helper_functions import Filelister, BsonReader, JsonReader
from pathlib import Path
from openapi_schema_validator import validate

import json
import os

import bson

DEFAULT_FPS = 50
DEFAULT_TOLERANCE_US = 10




class BsonFrameRate:
    def __init__(self, filePath=None, bsonType=None):
        self.homeDir = Path(__file__).parent
        self.basePath = self.homeDir / ".." / "resources" / "jsonFiles" / "fromBson"
        self.fullPath = self.basePath / filePath / bsonType
        fileLister = Filelister(self.fullPath)
        self.listFiles = fileLister.list_files()

    # def readBsonFiles(self, jsonFIleName):
    #
    #     for f in self.listFiles:
    #         fileName = Path(self.fullPath, f)
    #         bson_reader = BsonReader(fileName)
    #         bdata = bson_reader.read()
    #         keyData = bdata[0]


    def schemaValidation(self, schemaFile):

        jsonRader = JsonReader(schemaFile)
        readSchema = jsonRader.read_json()
        for f in self.listFiles:
            fileName = Path(self.fullPath, f)
            jsonReader = JsonReader(fileName)
            jdata = jsonReader.read_json()
            #prop = jdata.get("personFrameData").get('people')[0].get('jointIds')
            #print(type(prop))
            validate(jdata, readSchema)
            # try:
            #     validate(jdata, schemaFile)
            #     print("Good")
            # except:
            #     pass








frameRate =BsonFrameRate("BSONS_0022500283", "tracking")
#readBson = frameRate.readBsonFiles("basketBallTracking")
schemaPath = Path("../resources/schema/BasketballTracking_schema.json")
frameRate.schemaValidation(schemaPath)

    #
    # def updateBson(obj, base_path):
    #     parent_path = os.path.dirname(base_path)
    #     newDirectoryName = input("please add new directory name")
    #     destination = os.path.join(parent_path, newDirectoryName)
    #     os.makedirs(destination, exist_ok=True)
    #     isMaster_input = input("Please enter isMaster <True/False>")
    #     isMaster = bool(isMaster_input)
    #     for i in obj:
    #         fileName = base_path + "\\" + i
    #         destinationFileName = destination + "\\" + i
    #         bson_reader = BsonReader(fileName)
    #         bdata = bson_reader.read()
    #         keyData = bdata[0]
    #         keyData.update({"isMaster": isMaster})
    #         newBson = bson.encode(keyData)
    #         print(newBson)
    #         with open(destinationFileName, 'wb') as f:
    #             f.write(newBson)

# def _iter_bson_docs(paths: Iterable[str]):
#     for path in paths:
#         with open(path, "rb") as handle:
#             for doc in bson.decode_file_iter(handle):
#                 print(doc)
#                 yield doc
#
#
# def _extract_timestamp_us(doc: dict) -> int:
#     try:
#         return int(doc["bsondata"]["time"])
#     except (KeyError, TypeError, ValueError) as exc:
#         raise AssertionError(f"Missing/invalid bsondata.time in {doc}") from exc
#
#
# @dataclass
# class BsonFrameRateTest:
#     paths: Sequence[str]
#     fps: int = DEFAULT_FPS
#     tolerance_us: int = DEFAULT_TOLERANCE_US
#
#     def _frame_interval_us(self) -> int:
#         return int(1_000_000 / self.fps)
#
#     def _collect_timestamps(self) -> List[int]:
#         timestamps: List[int] = []
#         for doc in _iter_bson_docs(self.paths):
#             timestamps.append(_extract_timestamp_us(doc))
#         return timestamps
#
#     def run(self) -> None:
#         timestamps = self._collect_timestamps()
#         assert timestamps, "No BSON messages found; cannot validate frame cadence."
#
#         # Ensure non-decreasing order (revisions may repeat timestamps).
#         for previous, current in zip(timestamps, timestamps[1:]):
#             assert current >= previous, "Timestamps are out of order."
#
#         # Collapse revisions: keep first occurrence of each timestamp in sequence.
#         seen = set()
#         unique_timestamps: List[int] = []
#         for ts in timestamps:
#             if ts in seen:
#                 continue
#             seen.add(ts)
#             unique_timestamps.append(ts)
#
#         start_ts = unique_timestamps[0]
#         interval_us = self._frame_interval_us()
#         for index, ts in enumerate(unique_timestamps[1:], start=1):
#             expected_ts = start_ts + interval_us * index
#             delta = abs(ts - expected_ts)
#             assert (
#                 delta <= self.tolerance_us
#             ), f"Frame gap detected at index {index}: expected {expected_ts}, got {ts}"
#
#
# def test_saved_bson_has_no_frame_gaps():
#     # Keep this simple for pytest, configure via the class for custom callers.
#     tester = BsonFrameRateTest(
#         paths=[basePath],
#         fps=DEFAULT_FPS,
#         tolerance_us=DEFAULT_TOLERANCE_US,
#     )
#     tester.run()
#
#
# test = test_saved_bson_has_no_frame_gaps()