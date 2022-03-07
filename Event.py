from EventCollection import EventCollection

class Event:
    def __init__(self, event_name):
        self.name = event_name
        self.annotations = []
        self.next = EventCollection()

    def set_annotations(self, annotations):
        self.annotations = annotations

    def add_annotation(self, str):
        self.annotations.append(str)
    
    def add_next_event(self, event):
        self.next.add_event(event)
    
    def annotations_to_str(self):
        anno_str = ""
        for a in self.annotations:
            anno_str = anno_str + a + " "
        return anno_str

    def next_to_str(self):
        next_str = ""
        for e in self.next.events:
            next_str = next_str + e.name + " "
        return next_str
    

    def __str__(self):
        return (self.name + " " + self.annotations_to_str() + " " + self.next_to_str())

    pass

