class Testcase:
    def __init__(self, index):
        self.index = []
        self.index.append(index)
        self.input_elements = []
        self.input_labels = []
        self.output_states = []
        self.output_labels = []
        self.output_elements = []

    def add_input(self, input_element, input_label):
        if (input_element):
            self.input_elements.append(input_element)
        else:
            self.input_elements.append("")

        if (input_label):
            self.input_labels.append(input_label)
        else:
            self.input_labels.append("")

    def add_output(self, output_element, output_state, output_label):
        if (output_label):
            self.output_labels.append(output_label)
        if (output_state):
            self.output_states.append(output_state)
        if (output_element):
            self.output_elements.append(output_element)

    def add_output_element(self, output_element):
        self.output_elements.append(output_element)

    def add_output_label(self, output_label):
        self.output_labels.append(output_label)

    def add_output_state(self, output_state):
        self.output_states.append(output_state)

    def increase_to_length(self, list, length):
        for i in range(len(list), length):
            list.append("")

    def dictionary(self):
        num_of_rows = max(len(self.input_elements), len(self.input_labels), len(self.output_labels), len(self.output_states), len(self.output_elements))
        self.increase_to_length(self.index, num_of_rows)
        self.increase_to_length(self.input_elements, num_of_rows)
        self.increase_to_length(self.input_labels, num_of_rows)
        self.increase_to_length(self.output_labels, num_of_rows)
        self.increase_to_length(self.output_elements, num_of_rows)
        self.increase_to_length(self.output_states, num_of_rows)

        input_data = []
        self.increase_to_length(input_data, num_of_rows)
        
        return {
            'STT': self.index,
            'input element': self.input_elements,
            'input label': self.input_labels,
            'input data': input_data,
            'expected output label': self.output_labels,
            'expected output element': self.output_elements,
            'expected output state': self.output_states
        }
