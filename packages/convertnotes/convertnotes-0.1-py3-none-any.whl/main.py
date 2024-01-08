"""
Converts notes from one application to another
"""

import json
import re
from typing import List, Dict
from nanoid import generate
from datetime import datetime
import re
import argparse
from abc import ABC, abstractmethod

# cli args
parser = argparse.ArgumentParser(description="Convert Logseq JSON to Roam JSON.")
parser.add_argument("-i", "--inputfile", type=str, help="The Logseq JSON file")
parser.add_argument("-o", "--outputfile", type=str, help="The desired Roam JSON file")
parser.add_argument(
    "-p",
    "--profile",
    type=str,
    help="The converter profile to use",
    choices=["logseqtoroam"],
)
args = parser.parse_args()
if not args.inputfile:
    print(f"Must provide Logseq input JSON file")
    exit(1)
if not args.outputfile:
    print(f"Must provide Roam ouput JSON file")
    exit(1)
if not args.profile:
    print(f"Must provide converter profile")
    exit(1)

INPUT_FILEPATH = args.inputfile
OUTPUT_FILEPATH = args.outputfile
CONVERTER_PROFILE = args.profile


class Identifiers:
    """Stores Logseq IDs mapped to Roam UIDs"""

    def __init__(self, uids: dict = {}, blocks: dict = {}):
        self.uids = uids
        self.blocks = blocks

    def uid(self, logseq_id: str) -> str:
        """Constructs a UID from a Logseq ID"""
        uid = self.uids.setdefault(logseq_id, generate(size=9))
        return uid

    def update_references(self, content: str) -> str:
        """Replaces Logseq IDs in the given string with Roam IDs"""
        for id, uid in self.uids.items():
            if id in content:
                content = content.replace(id, uid)
        return content


class LogseqBlock:
    def __init__(
        self,
        id: str,
        page_name: str,
        properties: dict,
        format: str,
        content: str,
        children: List,
    ):
        self.id = id
        self.page_name = page_name
        self.properties = properties
        self.format = format
        self.content = content
        self.children = children

    @classmethod
    def from_json(cls, raw_block: dict) -> "LogseqBlock":
        id = raw_block.get("id", None)
        page_name = raw_block.get("page-name", None)
        properties = raw_block.get("properties", None)
        format = raw_block.get("format", None)
        content = raw_block.get("content", "")
        children = []
        for child in raw_block.get("children", []):
            child_block = LogseqBlock.from_json(child)
            children.append(child_block)
        return cls(id, page_name, properties, format, content, children)


class RoamBlock:
    def __init__(self, uid: str, title: str, string: str, children: List):
        self.uid = uid
        self.title = title
        self.string = string
        self.children = children

    def to_dict(self) -> dict:
        obj = {"uid": self.uid}
        if self.title:
            obj["title"] = self.title
        if self.string:
            obj["string"] = self.string
        if len(self.children) > 0:
            obj["children"] = [child.to_dict() for child in self.children]
        return obj

    @classmethod
    def from_logseq(cls, block: LogseqBlock, db: Identifiers) -> "RoamBlock":
        uid = db.uid(block.id)
        title = cls._format_title(cls, block.page_name)

        string = block.content
        if string:
            string = cls._format_content(cls, string)

        # convert logseq properties to roam attributes
        if (
            (not block.page_name or block.page_name == "")
            and (not string or string == "")
            and (block.properties != None and len(block.properties) == 1)
        ):
            for k, v in block.properties.items():
                value = None
                if isinstance(v, str):
                    value = v
                elif isinstance(v, list):
                    value = v[0]
                else:
                    continue
                string = f"{k.strip().lstrip()}:: {value}"

        children = [RoamBlock.from_logseq(child, db) for child in block.children]
        return cls(uid, title, string, children)

    def update_references(self, db: Identifiers):
        """
        Updates any Logseq IDs contained in the block to use the new Roam IDs
        """
        self.string = db.update_references(self.string)
        for child in self.children:
            child.update_references(db)

    def _format_content(self, string: str) -> str:
        # used to find markers that should be converted to a TODO state in Roam
        todo_regex = r"(NOW|LATER|TODO|DOING|WAITING|WAIT|CANCELED|CANCELLED|STARTED|IN-PROGRESS)"

        # regex for finding markers that should be converted to a DONE state in Roam
        done_regex = r"DONE"

        # reformatting
        string = string.replace("{{embed ", "{{embed: ")
        string = string.replace("{{video ", "{{[[video]]: ")
        string = re.sub(todo_regex, "{{[[TODO]]}}", string)
        string = re.sub(done_regex, "{{[[DONE]]}}", string)
        # fix json export bug
        string = string.replace("\ncollapsed:: true", "")
        # cleanup
        string = string.lstrip()
        return string

    def _get_ordinal_suffix(self, day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1]

    def _format_title(self, title):
        try:
            # Remove ordinal suffixes before parsing
            no_ordinal_str = re.sub(
                r"(1st|2nd|3rd|\dth)", lambda x: x.group()[0:-2], title
            )

            # Parse the date without the ordinal suffix
            date_obj = datetime.strptime(no_ordinal_str, "%b %d, %Y")

            # Determine the ordinal suffix for the day
            ordinal_suffix = self._get_ordinal_suffix(date_obj.day)

            # Convert the date object back to a string with the full month name and include ordinal suffix
            full_month_date_string = date_obj.strftime(
                f"%B {date_obj.day}{ordinal_suffix}, %Y"
            )

            return full_month_date_string
        except:
            # title is not a date
            return title


class Converter(ABC):
    """Converts notes from one application to another"""

    @abstractmethod
    def read(self, input_path) -> any:
        pass

    @abstractmethod
    def convert(self, source: any) -> any:
        pass

    @abstractmethod
    def write(self, output_path):
        pass


class LogseqToRoam(Converter):
    def __init__(self):
        self.db = Identifiers()

    def read(self, input_path: str) -> any:
        return json.load(open(input_path))

    def write(self, output_path: str, data: any) -> any:
        with open(output_path, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def convert(self, logseq_json: any) -> any:
        logseq_blocks = []
        for raw_block in logseq_json["blocks"]:
            block = LogseqBlock.from_json(raw_block)
            if block.page_name == "Contents":
                continue
            logseq_blocks.append(block)

        # convert logseq pages to roam pages
        # these do not have updated block references
        roam_blocks = [RoamBlock.from_logseq(block, self.db) for block in logseq_blocks]

        # update all block refs using the new block ids
        # once all blocks have been imported
        for block in roam_blocks:
            block.update_references(self.db)

        roam_json = [block.to_dict() for block in roam_blocks]
        return roam_json


converters = {
    "logseqtoroam": LogseqToRoam,
}

converter = converters.get(CONVERTER_PROFILE)()
raw_data = converter.read(INPUT_FILEPATH)
converter.write(OUTPUT_FILEPATH, converter.convert(raw_data))
