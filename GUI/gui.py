import math
import tkinter as tk
from tkinter import LabelFrame, messagebox
from logic import Logic
from structures.linked_list import LinkedList


class MainCanvas:
    def __init__(self, width: int, height: int):
        self.n = 0
        self.k = 0
        self.height = height
        self.width = width
        self.list = None
        self.steps = None
        self.killed = None

        self.root = tk.Tk()
        self.root.title("Josephus")
        self.root.geometry(f"{self.width}x{self.height + 110}")
        self.root.eval('tk::PlaceWindow . center')
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height + 20, bg="white")

        top_menu = self.top_menu()
        top_menu.pack()
        self.canvas.pack()

        self.root.resizable(False, False)
        self.root.mainloop()

    def top_menu(self) -> LabelFrame:
        """creates top menu"""
        frame = tk.LabelFrame(self.root)
        frame.grid()

        n_label = tk.Label(frame, text="n: ")
        n_entry = tk.Entry(frame, width=5)
        k_label = tk.Label(frame, text="k: ")
        k_entry = tk.Entry(frame, width=5)
        reset_btn = tk.Button(frame, text="Reset", command=lambda: self.reset_command(n_entry, k_entry))
        submit_btn = tk.Button(frame, text="Submit", command=lambda: self.submit_command(n_entry, k_entry, reset_btn))

        n = n_entry.get()
        k = k_entry.get()

        n_label.grid(row=0, column=0)
        n_entry.grid(row=0, column=1)
        k_label.grid(row=0, column=2)
        k_entry.grid(row=0, column=3)
        submit_btn.grid(row=1, column=0, columnspan=10, sticky="nsew")
        reset_btn.grid(row=2, column=0, columnspan=10, sticky="nsew")
        return frame

    def draw_nodes(self, values, color):
        """draws each step on canvas"""
        # adjusting circles sizes based on the number of nodes
        if len(self.list) <= 20:
            r = 50
            radius = 200
            delay = 400
        elif len(self.list) <= 50:
            r = 30
            radius = 250
            delay = 300
        else:
            r = 20
            radius = 325
            delay = 200

        theta = -math.pi / 2
        for i in range(len(self.list)):
            x_start = (self.width / 2) + (radius * math.cos(theta)) - r / 2
            y_start = (self.height / 2) + radius * math.sin(theta)
            self.canvas.create_oval(x_start, y_start, (x_start + r), (y_start + r), fill=color)
            self.canvas.create_text(x_start + r / 2, y_start + r / 2, text=values[i])
            theta += (2 * math.pi) / len(self.list)

        self.root.update()
        self.root.after(delay)

        return self.canvas

    def show_steps(self):
        """shows every step on canvas"""
        color = "black"
        logic = Logic(self.list)
        self.steps = logic.josephus(self.k - 1, 0)
        self.killed = logic.get_killed()
        for i in range(len(self.steps)):
            self.canvas.delete("all")
            values = self.steps[i]
            self.list = LinkedList()
            self.list.add_multiple_nodes(values)
            if i == len(self.steps) - 1:
                color = "green"
            self.draw_nodes(values, color)

    def submit_command(self, n_entry: tk.Entry, k_entry: tk.Entry, reset_btn=None) -> None:
        """sets n and k variables entered by user"""
        values = []
        self.n = int(n_entry.get()) if n_entry.get() != '' else 0
        self.k = int(k_entry.get()) if k_entry.get() != '' else 0

        if self.n > 0 and self.k > 0:
            for i in range(1, int(n_entry.get()) + 1):
                values.append(i)
            self.list = LinkedList()
            self.list.add_multiple_nodes(values)
            n_entry.config(state="disabled")
            k_entry.config(state="disabled")
            reset_btn.config(state="disabled")
            self.show_steps()
            # displaying killed people's information
            killed_people = self.display_killed()
            self.root.after(1000)
            self.display_results()
            reset_btn.config(state="normal")

        else:
            messagebox.showerror(title="invalid input", message="n and k must be greater than 0")

    def reset_command(self, n_entry: tk.Entry, k_entry: tk.Entry) -> None:
        """resets n and k variables to None"""
        self.n = 0
        self.k = 0
        n_entry.config(state="normal")
        k_entry.config(state="normal")
        n_entry.delete(0, "end")
        k_entry.delete(0, "end")
        self.canvas.delete("all")

    def display_killed(self):
        """displays killed people ordered by the time they got killed"""
        result = ""
        for i in range(len(self.killed)):
            result += str(self.killed[i]) + " "
            if i % 10 == 0 and i != 0:
                result += "\n "
        return result

    def display_results(self):
        killed_people = self.display_killed()
        info_frame = tk.Tk()
        info_frame.title("Info")
        killed = tk.Label(info_frame, text=f"\nkilled people:\n{killed_people}\n")
        survived = tk.Label(info_frame, text=f"\nsurvived:\n {self.steps[-1][0]}\n")
        killed.place(relx=0.5, rely=0.25, anchor="center")
        survived.place(relx=0.5, rely=0.75, anchor="center")
        info_frame.resizable(False, False)
        info_frame.mainloop()
