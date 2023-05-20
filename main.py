import sys
from tkinter import *
import tkinter as tk


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


# start programu TODO dodać reszte inputów
def get_inputs():
    inputs = []
    for entry in input_entries:
        inputs.append(entry.get())
    print(inputs)  # Możesz dostosować tę część kodu, aby wykorzystać wartości wprowadzone przez użytkownika


root = tk.Tk()
root.title("System wieloagentowy")

# grupy
inputs_group = tk.LabelFrame(root, text="Input")
inputs_group.pack()

good_will_group = tk.LabelFrame(root, text="Good will")
good_will_group.pack()

starting_trust_measure_group = tk.LabelFrame(root, text="Starting trust measure")
starting_trust_measure_group.pack()

options_group = tk.LabelFrame(root, text="Options")
options_group.pack()

actions_group = tk.LabelFrame(root, text="Actions")
actions_group.pack()

# tablice ze zczytanymi wartościami
input_entries = []
good_will = []
starting_trust_measure = []
options = []
actions = []

# nazwy pól
inputs_labels = ["Cykle", "Agenci", "s-Agents", "kmin", "kmax", "dystrybuantaA", "dystrybuantaG"]
good_will_labels = ["x", "y", "z"]
starting_trust_measure_labels = ["V_0 trust"]


def add_labels(group, labels_list, input_arr):
    for l in labels_list:
        label = tk.Label(group, text=l)
        label.pack()
        entry = tk.Entry(group)
        entry.pack()
        input_arr.append(entry)


add_labels(inputs_group, inputs_labels, input_entries)
add_labels(good_will_group, good_will_labels, good_will)
add_labels(starting_trust_measure_group, starting_trust_measure_labels, starting_trust_measure)
# add_radiobuttons()
# add_button()

# start programu
button = tk.Button(actions_group, text="Pobierz dane", command=get_inputs)
button.pack()

# przekierowanie konsoli na aplikację
text_widget = tk.Text(root)
text_widget.pack()
console_redirector = ConsoleRedirector(text_widget)
sys.stdout = console_redirector

root.mainloop()
