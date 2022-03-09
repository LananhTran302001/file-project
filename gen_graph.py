from EventCollection import EventCollection
from Excel import Excel
from Flow import Flow
from Event import Event

from pandas import ExcelWriter, DataFrame

excel = Excel("annotations.xlsx")

def read_usecases(usecases_file_path):
    flows = []
    events_collection = EventCollection()

    lines = []
    with open(usecases_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        if (excel.is_flow_name(line)):
            flows.append(Flow(line))
        elif (excel.is_event_name(line)):
            e = Event(excel.extract_event_name(line))
            e.set_annotations(excel.extract_annotations(line))
            
            events_collection.add_event(e)
            flows[-1].add_event(events_collection.get_event(e.name))
    
    return {'flows': flows, 'events': events_collection}


def read_flows(flows_file_path):
    flows = []
    events_collection = EventCollection()
    collected = False

    lines = []
    with open(flows_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        words = line.split()
        if (len(words) > 0 and excel.is_event_name(line)):
            flow = Flow("Flow " + str(lines.index(line)))
            flows.append(flow)
            
            for word in words:
                if (excel.is_event_name(word)):
                    e = Event(word)                  
                    if (events_collection.contain(e)):
                        collected = True
                    else:
                        collected = False
                        events_collection.add_event(e)
                    
                    flow.add_event(events_collection.get_event(e.name))

                elif ((not collected) and (excel.is_annotation("[" + word + "]"))):
                    flow.events[-1].add_annotation(word)

    return {'flows':flows, 'events':events_collection}

def read_events(events_file_path):
    events_collection = EventCollection()

    lines = []
    with open(events_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        words = line.split()
        if (len(words) > 0 and excel.is_event_name(line)):
            event = Event(excel.extract_event_name(line))
            events_collection.add_event(event)
            event = events_collection.get_event(event.name)

            for word in range(1, len(words) - 1):
                if (excel.is_event_name(word)):  
                    events_collection.add_event(Event(word))
                    e = events_collection.get_event(word)
                    event.add_next_event(e)

                elif (excel.is_annotation("[" + word + "]")):
                    event.add_annotation(word)

    return {'events':events_collection}

def flows_to_txt(flows, txt_file_path):
    with open(txt_file_path, mode="w", encoding="utf-8") as writer:
        for flow in flows:
            writer.write(str(flow))
            writer.write("\n")

def events_to_txt(events_collection, txt_file_path):
    with open(txt_file_path, mode="w", encoding="utf-8") as writer:
        for e in events_collection.events:
            writer.write(str(e))
            writer.write("\n")

def flows_to_excel(flows_file_path, excel_file_path):
    pass

def increase_length(list, length):
    for i in range(len(list), length):
        list.append("")

def testcase(flow):
    # testcase input
    input_elements = []
    input_labels = []

    input_annotations = flow.get_input_annotations()
    i = 0
    while (i < len(input_annotations)):
        # Nếu annotation là input element
        if (excel.is_input_element(input_annotations[i])):
            input_elements.append(excel.get_element_meaning(input_annotations[i])) # laasy meaning 
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
        
        i = i  + 1

    # testcase output
    output_elements = []
    output_states = []
    output_labels = []

    output_annotations = flow.get_output_annotations()
    for annot in output_annotations:
        # Nếu annotation là output element
        if (excel.is_ouput_element(annot)):
            output_elements.append(excel.get_element_meaning(annot))

        # Nếu annotation là state
        elif (excel.is_state(annot)):
            output_states.append(annot.strip('#'))
        
        # Nếu không -> annotation là label
        else:
            output_labels.append(annot)

    num_of_rows = max(len(input_elements), len(input_labels), len(output_elements))
    increase_length(input_elements, num_of_rows)
    increase_length(input_labels, num_of_rows)
    increase_length(output_elements, num_of_rows)
    increase_length(output_states, num_of_rows)
    increase_length(output_labels, num_of_rows)

    return {
        'input_elements': input_elements,
        'input_labels': input_labels,
        'output_elements': output_elements,
        'output_states': output_states,
        'output_labels': output_labels
    }

def testcase_to_excel(excel_file_path, testcases):
    data = DataFrame(
        {
            'input elements': testcases['input_elements'],
            'input labels': testcases['input_labels'],
            'output elements': testcases['output_elements'],
            'output states': testcases['output_states'],
            'output labels': testcases['output_labels']
        }
    )
    print(data)
    with ExcelWriter(excel_file_path) as writer:
        data.to_excel(writer)


result = read_flows("flows.txt")
flows = result["flows"]
for f in flows:
    print (str(f))
print("-------------------------------------")
t = testcase(flows[0])
print(t)
testcase_to_excel("hello.xlsx", t)