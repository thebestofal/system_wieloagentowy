import sys
from tkinter import *
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
    inputs = {}
    for key, value in input_entries.items():
        inputs[key] = value.get()
    print(inputs)

root = tk.Tk()
root.title("System wieloagentowy")

# framy główne
frame = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame.pack(side=tk.LEFT, padx=10, pady=10)

frame_right = tk.Frame(root, borderwidth=2, relief=tk.GROOVE)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

# framy lewo
frame_inputy = tk.LabelFrame(frame, text="Inputs")
frame_inputy.pack(padx=5, pady=5)

frame_good_will = tk.LabelFrame(frame, text="Good will")
frame_good_will.pack(padx=5, pady=5)

frame_starting_trust_measure = tk.LabelFrame(frame, text="Starting trust measure")
frame_starting_trust_measure.pack(padx=5, pady=5)

# grupy
options_group = tk.LabelFrame(root, text="Options")
options_group.pack(side=tk.LEFT, padx=10, pady=10)


# tablice ze zczytanymi wartościami
input_entries = {}

# nazwy pól
inputs_labels = {"Cykle": 30, "Agenci": 500, "s-Agents": 50, "kmin": 50, "kmax": 100, "expoA": 10, "expoG": 10}
good_will_labels = {"x": 0.8, "y": 0.8, "z": 0.8}
starting_trust_measure_labels = {"V_0 trust": 1.0}


# def add_labels2(group, labels_list):
#     for l in labels_list:
#         label = tk.Label(group, text=l)
#         label.pack()
#         entry = tk.Entry(group)
#         entry.pack()


def add_labels(group, param_list, entries):
    for key, value in param_list.items():
        label = tk.Label(group, text=key)
        label.pack()
        entry = Entry(group)
        entry.insert(0, value)
        entry.pack()
        entries[key] = entry


add_labels(frame_inputy, inputs_labels, input_entries)
add_labels(frame_good_will, good_will_labels, input_entries)
add_labels(frame_starting_trust_measure, starting_trust_measure_labels, input_entries)
# add_radiobuttons()

# start programu
button = tk.Button(frame, text="Start", command=get_inputs)
button.pack(side=tk.BOTTOM, padx=10, pady=10)

# przekierowanie konsoli na aplikację
text_widget = tk.Text(frame_right)
text_widget.pack(side=tk.BOTTOM, padx=10, pady=10)
console_redirector = ConsoleRedirector(text_widget)
sys.stdout = console_redirector

# wykres
canvas = FigureCanvasTkAgg(None, master=frame_right)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()
