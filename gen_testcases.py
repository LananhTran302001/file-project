from __future__ import annotations
from pandas import DataFrame
from gen_graph import read_flows
from Excel import Excel

excel = Excel("annotations.xlsx")

def testcase(flow):
    for event in flow.events:
        for annotation in event.annotations:
            if (excel.is_element(annotations)):
                pass


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

result = read_flows("flows.txt")
flows = result["flows"]
from_flows_to_testcases(flows[0])