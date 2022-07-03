from pandas import ExcelWriter, DataFrame

from src.EventCollection import EventCollection
from src.Monitor import Monitor
from src.Flow import Flow
from src.Event import Event
from src.Testcase import Testcase
from src.myconstants import HTML_FILE_PATH, HTML_REPLACE_TAG

# Monitor là biến lưu các quy tắc của annotation: regex, định nghĩa, html,..
monitor = Monitor()



# YÊU CẦU 1
# ---------------------------------------------------------------------------------
# Đọc file usecases --> trả về các flows & events
# Basic flow:
# 1. [#ti][#button]
# 2. abc..
def read_usecases_txt(usecases_file_path):
    flows = []
    events_collection = EventCollection()

    lines = []
    with open(usecases_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        
        if (monitor.is_flow_name(line)):
            flows.append(Flow(line))
        
        elif (monitor.is_event_list(line)):
            start, end, flow_name = monitor.extract_event_list(line)
            print(start)
            print(end)
            print(flow_name)
            
            for f in flows:
                print(f.name)
                if (f.equal(flow_name)):
                    break              
            events = f.get_event_list(start, end)
            
            for e in events:
                flows[-1].add_event(events_collection.get_event(e.name)) 

        elif (monitor.is_event_name(line)):
            e = Event(monitor.extract_event_name(line))
            e.set_annotations(monitor.extract_annotations(line))
            
            events_collection.add_event(e)
            flows[-1].add_event(events_collection.get_event(e.name)) 
    
    return {'flows': flows, 'events': events_collection}


# Đọc file flows --> trả về các flows và events
# 1. [#ti] -> 2.[#yes][#button] ->..
# 1. [#ti] -> 2a.[#no][#button] ->..
def read_flows_txt(flows_file_path):
    flows = []
    events_collection = EventCollection()
    collected = False

    lines = []
    with open(flows_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        words = line.split()
        if (len(words) > 0 and monitor.is_event_name(line)):
            flow = Flow("Flow " + str(lines.index(line)))
            flows.append(flow)
            
            for word in words:
                if (monitor.is_event_name(word)):
                    e = Event(word)                  
                    if (events_collection.contain(e)):
                        collected = True
                    else:
                        collected = False
                        events_collection.add_event(e)
                    
                    flow.add_event(events_collection.get_event(e.name))

                elif ((not collected) and (monitor.is_annotation("[" + word + "]"))):
                    flow.events[-1].add_annotation(word)

    return {'flows':flows, 'events':events_collection}


# Đọc file events --> trả về các events
# 1. [#ti] 2. 2a.
# 2. [#yes][#button]
# 2a. [#no][#button]
def read_events_txt(events_file_path):
    events_collection = EventCollection()

    lines = []
    with open(events_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        words = line.split()
        if (len(words) > 0 and monitor.is_event_name(line)):
            event = Event(monitor.extract_event_name(line))
            events_collection.add_event(event)
            event = events_collection.get_event(event.name)

            for word in range(1, len(words) - 1):
                if (monitor.is_event_name(word)):  
                    events_collection.add_event(Event(word))
                    e = events_collection.get_event(word)
                    event.add_next_event(e)

                elif (monitor.is_annotation("[" + word + "]")):
                    event.add_annotation(word)

    return {'events':events_collection}


# Viết các flows vào file txt: xuất file flows
def flows_to_txt(flows, txt_file_path):
    with open(txt_file_path, mode="w", encoding="utf-8") as writer:
        for flow in flows:
            writer.write(str(flow))
            writer.write("\n")

# Viết các events vào file txt: xuất file events
def events_to_txt(events_collection, txt_file_path):
    with open(txt_file_path, mode="w", encoding="utf-8") as writer:
        for e in events_collection.events:
            writer.write(str(e))
            writer.write("\n")




# YÊU CẦU 2
# ---------------------------------------------------------------------------------
# Sinh testcase từ 1 flow
def flow_to_testcase(index, flow):
    t = Testcase(index)

    # testcase input
    input_annotations = flow.get_input_annotations()
    i = 0
    while (i < len(input_annotations)):
        # Nếu annotation là input element
        if (monitor.is_input_element(input_annotations[i])):
            input_element = monitor.get_element_meaning(input_annotations[i]) # laasy meaning 
            # Nếu annotation tiếp theo là label
            if (monitor.is_label(input_annotations[i + 1])):
                t.add_input(input_element=input_element, input_label=input_annotations[i + 1].strip("#"))
                i = i + 1
            else:
                t.add_input(input_element, "")
        # Nếu annotation là label
        elif (monitor.is_label(input_annotations[i])):
            t.add_input("", input_annotations[i].strip("#"))        
        i = i  + 1


    # testcase output
    output_annotations = flow.get_output_annotations()
    i = 0
    while (i < len(output_annotations)):
        # Nếu annotation là state
        if (monitor.is_state(output_annotations[i])):
            t.add_output_state(output_annotations[i].strip("#"))
        # Nếu annotation là output element
        elif (monitor.is_ouput_element(output_annotations[i])):
            t.add_output_element(monitor.get_element_meaning(output_annotations[i]))
        # Nếu annotation là label
        else:
            t.add_output_label(output_annotations[i].strip("#"))
        
        i = i + 1
    return t.dictionary()

# Sinh và viết các testcase vào file excel: yêu cầu 2
def flows_to_excel(flows, excel_file_path):
    testcases = {
        'STT': [],
        'input element': [],
        'input label': [],
        'input data': [],
        'expected output element': [],
        'expected output label': [],
        'expected output state': []
    }

    for i in range(len(flows)):
        t = flow_to_testcase(i + 1, flows[i])
        testcases['STT'].extend(t['STT'])
        testcases['input element'].extend(t['input element'])
        testcases['input label'].extend(t['input label'])
        testcases['input data'].extend(t['input data'])
        testcases['expected output label'].extend(t['expected output label'])
        testcases['expected output element'].extend(t['expected output element'])
        testcases['expected output state'].extend(t['expected output state'])
        
    data = DataFrame(testcases)
    with ExcelWriter(excel_file_path) as writer:
        data.to_excel(writer)




# YÊU CẦU 3
# ---------------------------------------------------------------------------------
# sinh string html từ 1 cặp label-element lấy từ testcase
def to_html(label, element_annot):
    html_label = ""
    html_element = ""

    if (element_annot):
        open_html = monitor.get_element_o_html(element_annot)
        close_html = monitor.get_element_c_html(element_annot)
        if (len(close_html)):
            return '\t' + open_html + label + close_html + '\n'
        else:
            html_element = open_html

    if (label):
        html_label = "<label>" + label + "</label>"
    
    return '\t' + html_label + '\n' + '\t' + html_element + '\n'


# Sinh file template UI html cho 1 flow
def flow_to_html(flow, html_file_path):
    html = ''
    testcase = flow_to_testcase(0, flow)

    for i in range(len(testcase['input element'])):
        html = html + to_html(testcase['input label'][i], testcase['input element'][i])
    
    lines = []
    with open(HTML_FILE_PATH, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    # Write the file out again
    with open(html_file_path, mode="w", encoding="utf-8") as writer:
        for line in lines:
            line = line.replace(HTML_REPLACE_TAG, html)
            writer.write(line)
