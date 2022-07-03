import os

fileDir = os.path.dirname(os.path.realpath('__file__'))

# relative paths to project directory
EXCEL_FILE_PATH = os.path.join(fileDir, "resources/annotations.xlsx")
HTML_FILE_PATH = os.path.join(fileDir, "resources/templateHTML.html")

INPUT_FOLDER_PATH = "../input/"
OUTPUT_FOLDER_PATH = "../output/"

ANNOTATION_SHEET = "annotations"
ANNOTATION_COLUMN = "annotation"

ELEMENT_SHEET = "elements"
ELEMENT_COLUMN = "annotation"
ELEMENT_MEANING_COLUMN = "meaning"
ELEMENT_HTML_O_COLUMN = "html-open"
ELEMENT_HTML_C_COLUMN = "html-close"

STATE_SHEET = "states"
STATE_COLUMN = "annotation"
FLOW_SHEET = "flows"
FLOW_COLUMN = "flow"
EVENT_SHEET = "events"
EVENT_COLUMN = "event"
EVENT_LIST_SHEET = "event_list"
EVENT_LIST_COLUMN = "list of events"

HTML_REPLACE_TAG = "[#content]"
