import tkinter as tk
from tkinter import messagebox

from PIL.ImageOps import expand
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import FunctionPlotter

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.entry_count = 1
        self.current_x_range = "-10:10"
        self.current_y_range = "Any"
        self.show_ranges = tk.BooleanVar()
        self.title("GraphMate")

        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Элементы управления в левом фрейме
        self.function_label = tk.Label(self.left_frame, text="Функция:")
        self.function_label.pack(anchor="w")

        self.entry_frame = tk.Frame(self.left_frame)
        self.entry_frame.pack()
        func =  tk.Entry(self.entry_frame)
        func.bind('<Return>', lambda event: self.add_function(func.get(), func))
        func.insert(self.entry_count, "")
        func.pack(fill=tk.X, pady=10)

        checkbox = tk.Checkbutton(self.left_frame, text="Изменить диапазоны", variable=self.show_ranges, command=self.toggle_entry)
        checkbox.pack(pady=10)

        self.x_range_label = tk.Label(self.left_frame, text="Диапазон x:")

        self.x_range_input = tk.Entry(self.left_frame)
        self.x_range_input.insert(0, self.current_x_range)
        self.x_range_input.bind("<Return>", lambda event: self.update_ranges(self.x_range_input.get(), self.current_y_range))

        self.y_range_label = tk.Label(self.left_frame, text="Диапазон y:")

        self.y_range_input = tk.Entry(self.left_frame)
        self.y_range_input.insert(0, "Any")
        self.y_range_input.bind("<Return>", lambda event: self.update_ranges(self.current_x_range, self.y_range_input.get()))

        self.plotter = FunctionPlotter()
        self.canvas = FigureCanvasTkAgg(self.plotter.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.functions = []
        self.entries = []
        self.x_ranges = [self.current_x_range]

    def update_ranges(self, x_range, y_range):
        self.current_x_range = x_range
        self.x_ranges = [x_range] * len(self.functions)
        self.current_y_range = y_range
        self.render()

    def add_function(self, function, entry):
        if function:
            if entry in self.entries:
                self.functions.pop(self.entries.index(entry))
                self.entries.remove(entry)
            self.functions.append(function)
            self.entries.append(entry)
            self.x_ranges = [self.current_x_range] * len(self.functions)
            self.render()
            if len(self.functions) == self.entry_count:
                self.entry_count += 1
                func = tk.Entry(self.entry_frame)
                func.bind('<Return>', lambda event: self.add_function(func.get(), func))
                func.insert(self.entry_count, "")
                func.pack(fill=tk.X, pady=10)
        else:
            if self.entry_count > 1:
                if entry in self.entries:
                    self.functions.pop(self.entries.index(entry))
                    self.entries.remove(entry)
                self.entry_count -= 1
                entry.destroy()
                self.render()

    def toggle_entry(self):
        if self.show_ranges.get():
            self.x_range_label.pack(anchor="w")
            self.x_range_input.pack(fill=tk.X)
            self.y_range_label.pack(anchor="w")
            self.y_range_input.pack(fill=tk.X)
        else:
            self.x_range_input.pack_forget()
            self.y_range_input.pack_forget()
            self.x_range_label.pack_forget()
            self.y_range_label.pack_forget()

    def render(self):
        try:
            self.plotter.plot(self.functions, self.x_ranges, self.current_y_range)
            self.plotter.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка: {e}")

    def remove_plot(self):
        if self.functions:
            items = [f"{i + 1}: {func}" for i, func in enumerate(self.functions)]
            item = tk.simpledialog.askstring("Удалить график", "Выберите график для удаления:\n" + "\n".join(items))
            if item:
                index = int(item.split(":")[0]) - 1
                self.functions.pop(index)
                self.x_ranges.pop(index)
                self.plotter.plot(self.functions, self.x_ranges, self.current_y_range)
                self.plotter.figure.tight_layout()
                self.canvas.draw()

    def remove_all_plots(self):
        if self.functions:
            self.functions = []
            self.x_ranges = []
            self.plotter.plot(self.functions, self.x_ranges, )
            self.plotter.figure.tight_layout()
            self.canvas.draw()