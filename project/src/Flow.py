from __future__ import annotations
from project.src.Event import Event

class Flow:
    def __init__(self, flow_name):
        self.name = flow_name
        self.events = []
    
    def add_event(self, event):
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

    def __str__(self):
        flow_str = ""
        for event in self.events:
            flow_str = flow_str + event.name + " " + event.annotations_to_str() + " -> "
        flow_str = flow_str[0:-4]
        return flow_str