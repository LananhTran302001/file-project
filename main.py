from EventCollection import EventCollection
from Excel import Excel
from Flow import Flow
from Event import Event
from Testcase import Testcase

from pandas import ExcelWriter, DataFrame

excel = Excel("annotations.xlsx")

def read_from_usecases(usecases_file_path):
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


def read_from_flows(flows_file_path):
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

def read_from_events(events_file_path):
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


def flow_to_testcase(index, flow):
    t = Testcase(index)

    # testcase input
    input_annotations = flow.get_input_annotations()
    i = 0
    while (i < len(input_annotations)):
        # Nếu annotation là input element
        if (excel.is_input_element(input_annotations[i])):
            input_element = excel.get_element_meaning(input_annotations[i]) # laasy meaning 
            # Nếu annotation tiếp theo là label
            if (excel.is_label(input_annotations[i + 1])):
                t.add_input(input_element=input_element, input_label=input_annotations[i + 1])
                i = i + 1
            else:
                t.add_input(input_element, "")
        # Nếu annotation là label
        elif (excel.is_label(input_annotations[i])):
            t.add_input("", input_annotations[i])        
        i = i  + 1


    # testcase output
    output_annotations = flow.get_output_annotations()
    i = 0
    while (i < len(output_annotations)):
        # Nếu annotation là state
        if (excel.is_state(output_annotations[i])):
            t.add_output_data(output_annotations[i] + " ")
        # Nếu annotation là output element
        elif (excel.is_ouput_element(output_annotations[i])):
            t.add_output_data(output_annotations[i])
        # Nếu annotation là label
        else:
            t.add_output_label(output_annotations[i])
        
        i = i + 1
    return t.dictionary()

def flows_to_excel(excel_file_path, flows):
    testcases = {
        'STT': [],
        'input element': [],
        'input label': [],
        'input data': [],
        'expected output label': [],
        'expected output data': []
    }

    for i in range(len(flows)):
        t = flow_to_testcase(i + 1, flows[i])
        testcases['STT'].extend(t['STT'])
        testcases['input element'].extend(t['input element'])
        testcases['input label'].extend(t['input label'])
        testcases['input data'].extend(t['input data'])
        testcases['expected output label'].extend(t['expected output label'])
        testcases['expected output data'].extend(t['expected output data'])
        
    data = DataFrame(testcases)
    with ExcelWriter(excel_file_path) as writer:
        data.to_excel(writer)


result = read_from_flows("flows.txt")
flows = result["flows"]
flows_to_excel("hello1.xlsx", flows)