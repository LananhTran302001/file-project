from EventCollection import EventCollection
from Excel import Excel
from Flow import Flow
from Event import Event

excel = Excel("annotations.xlsx")

def use_cases_to_flows(use_cases_file_path, flows_file_path):
    flows = []
    events_collection = EventCollection()

    lines = []
    with open(use_cases_file_path, mode="r", encoding="utf-8") as reader:
        lines = reader.readlines()

    for line in lines:
        if (excel.is_flow_name(line)):
            flows.append(Flow(line))
        elif (excel.is_event_name(line)):
            e = Event(excel.extract_event_name(line))
            e.set_annotations(excel.extract_annotations(line))
            
            events_collection.add_event(e)
            flows[-1].add_event(events_collection.get_event(e.name))
    
    with open(flows_file_path, mode="w", encoding="utf-8") as writer:
        for flow in flows:
            writer.write(str(flow))
            writer.write("\n")

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

def flows_to_excel(flows_file_path, excel_file_path):
    pass

result = read_flows("flows.txt")
print(result["events"])