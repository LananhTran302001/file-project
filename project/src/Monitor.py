import re
from pandas import read_excel, ExcelFile

from src.myconstants import EXCEL_FILE_PATH
from src.myconstants import ELEMENT_SHEET, ELEMENT_COLUMN, ELEMENT_MEANING_COLUMN, ELEMENT_HTML_COLUMN
from src.myconstants import ANNOTATION_SHEET, ANNOTATION_COLUMN
from src.myconstants import STATE_SHEET, STATE_COLUMN
from src.myconstants import FLOW_SHEET, FLOW_COLUMN
from src.myconstants import EVENT_SHEET, EVENT_COLUMN

class Monitor:
    def __init__(self):
        self.file_path = EXCEL_FILE_PATH
        with ExcelFile(self.file_path) as reader:
            self.elements = read_excel(reader, sheet_name=ELEMENT_SHEET).astype("string").loc[:,[ELEMENT_COLUMN, ELEMENT_MEANING_COLUMN, ELEMENT_HTML_COLUMN]]
            self.states = read_excel(reader, sheet_name=STATE_SHEET).astype("string").loc[:,STATE_COLUMN].to_list()
            self.annotations = read_excel(reader, sheet_name=ANNOTATION_SHEET).astype("string").loc[:,ANNOTATION_COLUMN].to_list()
            self.flows = read_excel(reader, sheet_name=FLOW_SHEET).astype("string").loc[:,FLOW_COLUMN].to_list()
            self.events = read_excel(reader, sheet_name=EVENT_SHEET).astype("string").loc[:,EVENT_COLUMN].to_list()

            self.elements = self.elements.applymap(lambda x: str(x).lower().strip(), na_action='ignore')
            self.states = [i.lower().strip() for i in self.states]
            self.annotations = [i.lower().strip() for i in self.annotations]
            self.flows = [i.lower().strip() for i in self.flows]
            self.events = [i.lower().strip() for i in self.events]

    def description(self):
        print(self.file_path)
        print(self.elements)
        print(self.states)
        print(self.flows)
        print(self.events)
        print(self.annotations)

    def is_annotation(self, str):
        current_anno_regex = self.annotations[0]
        return re.match(current_anno_regex, str)
    
    def is_element(self, annot):
        return (self.elements[ELEMENT_COLUMN].str.contains(annot).any())

    def get_element(self, element_annot):
        return self.elements.loc[self.elements[ELEMENT_COLUMN] == element_annot]

    def get_element_meaning(self, element_annot):
        return self.get_element(element_annot)[ELEMENT_MEANING_COLUMN].values[0]

    def get_element_html(self, element_annot):
        return self.get_element(element_annot)[ELEMENT_HTML_COLUMN].values[0]

    def is_input_element(self, element_annot):
        if (self.is_element(element_annot)):
            element_meaning = self.get_element_meaning(element_annot)
            if ("input" in element_meaning):
                return True
            elif ("output" in element_meaning):
                return False
            else:
                return True
    
    def is_ouput_element(self, element_annot):
        if (self.is_element(element_annot)):
            element_meaning = self.get_element_meaning(element_annot)
            if ("output" in element_meaning):
                return True
            elif ("input" in element_meaning):
                return False
            else:
                return True

    def is_state(self, annot):
        return (annot in self.states)

    def is_label(self, annot):
        return ((not self.is_element(annot)) and (not self.is_state(annot)))

    def is_event_name(self, str):
        current_event_regex = self.events[0]
        return re.match(current_event_regex, str)
    
    def is_flow_name(self, str):
        str = str.lower().strip()
        for f in self.flows:
            if (str.startswith(f)):
                return True
        return False

    def extract_event_name(self, line):
        line = line.lower().strip()
        current_event_regex = self.events[0]
        event_name_in_line = re.findall(current_event_regex, line, flags=re.IGNORECASE)
        return event_name_in_line[0]

    def extract_annotations(self, line):
        line = line.lower().strip()
        current_anno_regex = self.annotations[0]
        annotations_in_line = re.findall(current_anno_regex, line, flags=re.IGNORECASE)
        annotations_in_line = ["".join(x) for x in annotations_in_line]
        annotations_in_line = [annotation[1:-1].strip() for annotation in annotations_in_line]
        return annotations_in_line