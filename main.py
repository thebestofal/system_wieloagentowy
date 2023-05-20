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
    inputs = []
    for entry in input_entries:
        inputs.append(entry.get())
    print(inputs)  # Możesz dostosować tę część kodu, aby wykorzystać wartości wprowadzone przez użytkownika


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


add_labels(frame_inputy, inputs_labels, input_entries)
add_labels(frame_good_will, good_will_labels, good_will)
add_labels(frame_starting_trust_measure, starting_trust_measure_labels, starting_trust_measure)
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
