"""
Converts notes from one application to another
"""


import json
import re
from typing import List
from nanoid import generate
from datetime import datetime
import re
import argparse
from abc import ABC, abstractmethod
import itertools
import sys
import time
import threading


# cli args
parser = argparse.ArgumentParser(
    description="Convert notes from one application format to another."
)
parser.add_argument(
    "-i",
    "--inputfile",
    type=str,
    help="The source backup file (e.g. Logseq JSON export)",
)
parser.add_argument("-o", "--outputfile", type=str, help="The desired output filename")
parser.add_argument(
    "-p",
    "--profile",
    type=str,
    help="The converter profile to use",
    choices=["logseqtoroam"],
    default="logseqtoroam",
)
parser.add_argument(
    "-m",
    "--metadatafile",
    type=str,
    help="The path to the metadata file",
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
METADATA_FILEPATH = args.metadatafile
CONVERTER_PROFILE = args.profile


class Metadata:
    def __init__(self, name: str, kind: str, path: str, link: str):
        self.name = name
        self.kind = kind
        self.path = path
        self.link = link

    @classmethod
    def from_json(cls, data: dict) -> "Metadata":
        name = data.get("name")
        kind = data.get("type")
        path = data.get("path")
        link = data.get("markdownLink")
        return cls(name, kind, path, link)


class Identifiers:
    """Stores Logseq IDs mapped to Roam UIDs"""

    def __init__(
        self,
        uids: dict = {},
        dates: dict = {},
        blocks: dict = {},
        metadata: List[Metadata] = [],
    ):
        self.uids = uids
        self.dates = dates
        self.blocks = blocks
        md: dict[str, Metadata] = {}
        for m in metadata:
            md[m.name] = m
        self.metadata = md

        self.img_md_regex = re.compile("(!\[.*)({.*})")

    def uid(self, logseq_id: str) -> str:
        """Constructs a UID from a Logseq ID"""
        uid = self.uids.setdefault(logseq_id, generate(size=9))
        return uid

    def add_date(self, original_date: str, new_date: str):
        self.dates[original_date] = new_date

    def update_references(self, content: str) -> str:
        """Replaces Logseq IDs in the given string with Roam IDs"""
        if not content:
            return content

        months = {
            "Jan": "January",
            "Feb": "February",
            "Mar": "March",
            "Apr": "April",
            "Jun": "June",
            "Jul": "July",
            "Aug": "August",
            "Sep": "September",
            "Oct": "October",
            "Nov": "November",
            "Dec": "December",
        }
        months_regex = "(" + "|".join(months.keys()) + ")"
        day_regex = r"(\b\d{1,2})"
        months_pattern = months_regex + " " + day_regex

        def replace_with_long_month(match):
            short_month = match.group(1)
            day = match.group(2)
            long_month = months[short_month]
            return f"{long_month} {day}"

        content = re.sub(months_pattern, replace_with_long_month, content)

        for id, uid in self.uids.items():
            if id in content:
                content = content.replace(id, uid)

        for original_date, new_date in self.dates.items():
            if original_date in content:
                content = content.replace(original_date, new_date)
        return content

    def update_metadata(self, content: str) -> str:
        """Replaces links and other information from the given metadata file"""

        # remove image metadata
        match = self.img_md_regex.search(content)
        if match:
            content = content.replace(match.group(2), "")

        for name, md in self.metadata.items():
            if name in content:
                escaped_name = re.escape(name)
                regex = f"!\\[.*{escaped_name}\\)"
                content = re.sub(
                    regex,
                    md.link,
                    content,
                )
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


def get_ordinal_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        return "th"
    else:
        return ["st", "nd", "rd"][day % 10 - 1]


def fix_date(content):
    if not content:
        return content

    try:
        # Remove ordinal suffixes before parsing
        no_ordinal_str = re.sub(
            r"(1st|2nd|3rd|\dth)", lambda x: x.group()[0:-2], content
        )

        # Parse the date without the ordinal suffix
        date_obj = datetime.strptime(no_ordinal_str, "%b %d, %Y")

        # Determine the ordinal suffix for the day
        ordinal_suffix = get_ordinal_suffix(date_obj.day)

        # Convert the date object back to a string with the full month name and include ordinal suffix
        full_month_date_string = date_obj.strftime(
            f"%B {date_obj.day}{ordinal_suffix}, %Y"
        )

        return full_month_date_string
    except:
        # title is not a date
        return content


class RoamBlock:
    def __init__(self, uid: str, title: str, string: str, children: List["RoamBlock"]):
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

        title = fix_date(block.page_name)
        if title != block.page_name:
            # date has been changed
            db.add_date(block.page_name, title)

        string = fix_date(block.content)
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

    def update_metadata(self, db: Identifiers):
        """
        Updates any metadata in the block to use the new metadata
        """
        self.string = db.update_metadata(self.string)
        for child in self.children:
            child.update_metadata(db)

    def _format_content(self, string: str) -> str:
        # used to find markers that should be converted to a TODO state in Roam
        todo_regex = r"(NOW|LATER|TODO|DOING|WAITING|WAIT|CANCELED|CANCELLED|STARTED|IN-PROGRESS)"

        # regex for finding markers that should be converted to a DONE state in Roam
        done_regex = r"DONE"

        # remove logbook info
        logbook_regex = r":LOGBOOK:.*:END:"
        string = re.sub(logbook_regex, "", string, flags=re.DOTALL)

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


class Converter(ABC):
    """Converts notes from one application to another"""

    @abstractmethod
    def read(self, input_path: str) -> any:
        pass

    @abstractmethod
    def convert(self, source: any) -> any:
        pass

    @abstractmethod
    def write(self, output_path: str):
        pass


class LogseqToRoam(Converter):
    def __init__(self, metadata_file: str = None):
        metadata: List[Metadata] = []
        if metadata_file:
            try:
                data = json.load(open(metadata_file))
                metadata = [Metadata.from_json(raw_md) for raw_md in data]
            except FileNotFoundError:
                print(
                    f"Metadata file not found at {metadata_file}. Are you sure that's right?"
                )
                exit(1)
        self.db = Identifiers(metadata=metadata)

    def read(self, input_path: str) -> any:
        try:
            return json.load(open(input_path))
        except FileNotFoundError:
            print(f"File not found at {input_path}. Are you sure that's right?")
            exit(1)

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
            block.update_metadata(self.db)

        roam_json = [block.to_dict() for block in roam_blocks]
        return roam_json


class Spinner(threading.Thread):
    def __init__(self, message="Loading..."):
        super().__init__()
        self.message = message
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            for char in itertools.cycle("|/-\\"):
                if self._stop_event.is_set():
                    break
                status = f"\r{self.message} {char}"
                sys.stdout.write(status)
                sys.stdout.flush()
                time.sleep(0.1)

    def stop(self):
        self._stop_event.set()


def main():
    converters = {
        "logseqtoroam": LogseqToRoam,
    }

    print(f"\nConverting notes using the profile '{CONVERTER_PROFILE}'.\n")

    spinner = Spinner(message="This might take a minute...")
    spinner.start()

    converter = converters.get(CONVERTER_PROFILE)(metadata_file=METADATA_FILEPATH)
    raw_data = converter.read(INPUT_FILEPATH)
    converter.write(OUTPUT_FILEPATH, converter.convert(raw_data))

    spinner.stop()
    spinner.join()
    print("\n\n\nDone!\n")


if __name__ == "__main__":
    main()
