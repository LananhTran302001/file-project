class EventCollection:
    def __init__(self):
        self.events = []

    def contain(self, event):
        for e in self.events:
            if (event.name == e.name):
                return True
        return False

    def add_event(self, event):
        if (not self.contain(event)):
            self.events.append(event)

    def get_index(self, event_name):
        for e in self.events:
            if (e.name == event_name):
                return self.events.index(e)   
        return -1

    def get_event(self, event_name):
        index = self.get_index(event_name)
        if (index >= 0):
            return self.events[index]
        else:
            return None

    def remove_event(self, event_name):
        index = self.get_index(event_name)
        if (index >= 0):
            self.events.pop(index)

    def __str__(self):
        collection_str = ""
        for e in self.events:
            collection_str = collection_str + str(e)
            collection_str = collection_str + "\n"
        return collection_str
