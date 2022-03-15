from pandas import DataFrame
from project.Monitor import Excel

excel = Excel("annotations.xlsx")
excel.description()

def testcase(flow):
    # testcase input
    input_elements = []
    input_labels = []

    input_annotations = flow.get_input_annotations()
    for i in range(len(input_annotations)):
        # Nếu annotation là input element
        if (excel.is_input_element(input_annotations[i])):
            input_elements.append(input_annotations[i])
            # Nếu annotation tiếp theo là label
            if (excel.is_label(input_annotations[i + 1])):
                input_labels.append(input_annotations[i + 1].strip('#'))
                i = i + 1
            else:
                input_labels.append("")
        # Nếu annotation là label
        elif (excel.is_label(input_annotations[i])):
            input_elements.append("")
            input_labels.append(input_annotations[i])

    # testcase output
    output_elements = []
    output_state = ""
    output_label = ""

    output_annotations = flow.get_output_annotations()
    for annot in output_annotations:
        # Nếu annotation là output element
        if (excel.is_ouput_element(annot)):
            output_elements.append(annot)

        # Nếu annotation là state
        elif (excel.is_state):
            output_state = output_state + " " + annot
        
        # Nếu không -> annotation là label
        else:
            output_label = output_label + " " + annot

    return {
        'input elements': input_elements,
        'input_labels': input_labels,
        'output_elements': output_elements,
        'output_state': output_state,
        'output_label': output_label
    }


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
