import re

class Flow:
    def __init__(self, flow_name):
        self.name = flow_name
        self.events = []
    
    def equal(self, flow_name):
        n1 = re.sub('[^a-zA-Z0-9]+', '', self.name).lower()
        n2 = re.sub('[^a-zA-Z0-9]+', '', flow_name).lower()
        return n1 == n2

    def add_event(self, event):
        if (event):
            if (len(self.events) > 0):
                self.events[-1].add_next_event(event) 
            self.events.append(event)

    def get_input_annotations(self):
        annotations = []
        for i in range(len(self.events) - 1):
            for a in self.events[i].annotations:
                annotations.append(a)
        return annotations
    
    def get_output_annotations(self):
        return self.events[-1].annotations

    def get_event_index(self, event_name):
        for i in range(len(self.events)):
            if (self.events[i].name == event_name):
                return i
        return -1

    def get_event_list(self, start_event, end_event):
        a = self.get_event_index(start_event)
        b = self.get_event_index(end_event)
        if (0 <= a and a < b and b < len(self.events)):
            return self.events[a : b + 1]
        else:
            print("Error: Khong co danh sach event tu ", start_event, " den ", end_event)


    def __str__(self):
        flow_str = ""
        for event in self.events:
            flow_str = flow_str + event.name + " " + event.annotations_to_str() + " -> "
        flow_str = flow_str[0:-4]
        return flow_str
