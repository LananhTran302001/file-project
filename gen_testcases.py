from __future__ import annotations
from pandas import DataFrame
from Excel import Excel

excel = Excel("annotations.xlsx")
excel.description()
print(excel.is_element("#ti"))
print(excel.is_input_element("#tio"))

def testcase(flow):
    input_elements = []
    input_labels = []
    for event in flow.events:
        for annotation in event.annotations:
            if (excel.is_input_element(annotations)):
                input_elements.append(annotation)
            elif (excel.is_label(annotation)):
                input_labels.append(annotation.strip('#'))
            
            if (len(input_elements) - len(input_labels) > 1):
                input_labels.append("")
            elif (len(input_labels) - len(input_elements) > 1):
                input_elements.append("")


def from_flows_to_testcases(flow):

    annotations = flow
    index = []
    input_labels = flow.get_input_annotations()
    input_data = []
    expected_output_label = []
    expected_output_data = []

    data = DataFrame({
        'STT':[],
        'Input label': flow.get_input_annotations(),
        'Input data': [],
        'Expected output label': [],
        'Expected output data': flow.get_output_annotations()
    })
    data.to_excel("testcases.xlsx")
