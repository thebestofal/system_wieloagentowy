from tkinter import *
import tkinter as tk
import system


class ConsoleRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass


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


# framy lewo
frame_inputy = tk.LabelFrame(frame, text="Inputs")
frame_inputy.pack(side=tk.LEFT, padx=5, pady=5)

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
inputs_labels = {"Cykle": 30, "Agenci": 500, "sAgenci": 50, "kmin": 50, "kmax": 100, "expoA": 10, "expoG": 10}
good_will_labels = {"x": 0.8, "y": 0.8, "z": 0.8}
starting_trust_measure_labels = {"V_0": 1.0}


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


def clear_canvas(canvas):
    canvas.get_tk_widget().destroy()


# start programu
button = tk.Button(frame, text="Start", command= lambda: [get_inputs, system.start_simulation(input_entries)])
button.pack(side=tk.BOTTOM, padx=10, pady=10)

root.mainloop()
