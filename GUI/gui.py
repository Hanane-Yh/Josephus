import math
import tkinter as tk
from tkinter import LabelFrame, messagebox
from logic import Logic
from structures.linked_list import LinkedList


class MainCanvas:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.list = None
        self.steps = None
        self.killed = None
        self.n = 0
        self.k = 0

        self.root = tk.Tk()
        self.root.title("Josephus Visualizer")
        self.root.geometry(f"{self.width}x{self.height + 110}")
        self.root.eval('tk::PlaceWindow . center')

        self.top_menu().pack()

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height + 20, bg="white")
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

        n_label.grid(row=0, column=0)
        n_entry.grid(row=0, column=1)
        k_label.grid(row=0, column=2)
        k_entry.grid(row=0, column=3)
        submit_btn.grid(row=1, column=0, columnspan=10, sticky="nsew")
        reset_btn.grid(row=2, column=0, columnspan=10, sticky="nsew")
        return frame

    def draw_nodes(self, values: list, color: str, counter: int) -> tk.Canvas:
        """draws each step on canvas"""

        # adjusting circles sizes based on the number of nodes
        if len(self.list) <= 20:
            r = 50
            radius = 200
            delay = 350
        elif len(self.list) <= 50:
            r = 30
            radius = 250
            delay = 200
        else:
            r = 20
            radius = 325
            delay = 150

        # draws alive people on the canvas
        theta = -math.pi / 2
        for i in range(len(self.list)):
            x_start = (self.width / 2) + (radius * math.cos(theta)) - r / 2
            y_start = (self.height / 2) + radius * math.sin(theta)
            self.canvas.create_oval(x_start, y_start, (x_start + r), (y_start + r), fill=color)
            self.canvas.create_text(x_start + r / 2, y_start + r / 2, text=values[i], fill="white")
            theta += (2 * math.pi) / len(self.list)

        # reporting each step
        label = tk.Label(self.canvas)
        label.place(x=25, y=25)
        if counter < len(self.killed):
            label.config(text="killed:")
            self.canvas.create_text(90, 37, text=self.killed[counter], fill="black", font='Arial, 20')
        else:
            label.config(text="alive")
            self.canvas.create_text(90, 37, text=self.steps[-1][0], fill="black", font='Arial, 20')

        self.root.update()
        self.root.after(delay)
        return self.canvas

    def show_steps(self) -> None:
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
            self.draw_nodes(values, color, counter=i)

    def submit_command(self, n_entry: tk.Entry, k_entry: tk.Entry, reset_btn=None) -> None:
        """sets n and k variables entered by user"""
        values = []
        self.n = int(n_entry.get()) if n_entry.get() != '' else 0
        self.k = int(k_entry.get()) if k_entry.get() != '' else 0

        if self.n > 1 and self.k > 0:
            for i in range(1, int(n_entry.get()) + 1):
                values.append(i)
            self.list = LinkedList()
            self.list.add_multiple_nodes(values)
            n_entry.config(state="disabled")
            k_entry.config(state="disabled")
            reset_btn.config(state="disabled")
            self.show_steps()
            reset_btn.config(state="normal")

            # displaying killed people's information
            self.display_killed()
            self.root.after(500)
            self.display_results()

        else:
            messagebox.showerror(title="invalid input", message="n and k must be non negative values")

    def reset_command(self, n_entry: tk.Entry, k_entry: tk.Entry) -> None:
        """resets n and k variables to None"""
        self.n = 0
        self.k = 0
        n_entry.config(state="normal")
        k_entry.config(state="normal")
        n_entry.delete(0, "end")
        k_entry.delete(0, "end")
        self.canvas.delete("all")

    def display_killed(self) -> str:
        """displays killed people ordered by the time they got killed"""
        result = ""
        for i in range(len(self.killed)):
            result += str(self.killed[i]) + " "
            if i % 10 == 0 and i != 0:
                result += "\n "
        return result

    def display_results(self) -> None:
        """opens a new window to show final results"""
        killed_people = self.display_killed()

        info_frame = tk.Tk()
        info_frame.title("Info")
        info_frame.eval('tk::PlaceWindow . center')
        info_frame.geometry("250x400")

        killed = tk.Label(info_frame, text=f"\ndead people:\n{killed_people}\n")
        survived = tk.Label(info_frame, text=f"\nsurvived:\n {self.steps[-1][0]}")
        killed.place(relx=0.5, rely=0.25, anchor="center")
        survived.place(relx=0.5, rely=0.75, anchor="center")

        info_frame.mainloop()
