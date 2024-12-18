import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plotter import FunctionPlotter


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Построитель графиков")
        self.geometry("800x600")

        # Создаем фреймы для левой и правой части окна
        self.left_frame = tk.Frame(self)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Элементы управления в левом фрейме
        self.function_label = tk.Label(self.left_frame, text="Функция:")
        self.function_label.pack(anchor="w")

        self.function_input = tk.Entry(self.left_frame)
        self.function_input.insert(0, "sin(x)")
        self.function_input.pack(fill=tk.X)

        self.x_range_label = tk.Label(self.left_frame, text="Диапазон x:")
        self.x_range_label.pack(anchor="w")

        self.x_range_input = tk.Entry(self.left_frame)
        self.x_range_input.insert(0, "-10:10")
        self.x_range_input.pack(fill=tk.X)

        self.plot_button = tk.Button(self.left_frame, text="Построить график", command=self.plot_function)
        self.plot_button.pack(fill=tk.X, pady=5)

        self.add_plot_button = tk.Button(self.left_frame, text="Добавить график", command=self.add_plot)
        self.add_plot_button.pack(fill=tk.X, pady=5)

        self.remove_plot_button = tk.Button(self.left_frame, text="Удалить график", command=self.remove_plot)
        self.remove_plot_button.pack(fill=tk.X, pady=5)

        # Создание объекта графика в правом фрейме
        self.plotter = FunctionPlotter()
        self.canvas = FigureCanvasTkAgg(self.plotter.figure, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Переменные для хранения графиков
        self.functions = []
        self.x_ranges = []

    def plot_function(self):
        function = self.function_input.get()
        x_range = self.x_range_input.get()

        if function and x_range:
            # try:
                self.functions = [function]
                self.x_ranges = [x_range]
                self.plotter.plot(self.functions, self.x_ranges)
                self.plotter.figure.tight_layout()
                self.canvas.draw()
            # except Exception as e:
                # messagebox.showerror("Ошибка", f"Ошибка: {e}")

    def add_plot(self):
        function = self.function_input.get()
        x_range = self.x_range_input.get()

        if function and x_range:
            # try:
                self.functions.append(function)
                self.x_ranges.append(x_range)
                self.plotter.plot(self.functions, self.x_ranges)
                self.plotter.figure.tight_layout()
                self.canvas.draw()
            # except Exception as e:
            #     messagebox.showerror("Ошибка", f"Ошибка: {e}")

    def remove_plot(self):
        if self.functions:
            items = [f"{i + 1}: {func}" for i, func in enumerate(self.functions)]
            item = tk.simpledialog.askstring("Удалить график", "Выберите график для удаления:\n" + "\n".join(items))
            if item:
                index = int(item.split(":")[0]) - 1
                self.functions.pop(index)
                self.x_ranges.pop(index)
                self.plotter.plot(self.functions, self.x_ranges)
                self.plotter.figure.tight_layout()
                self.canvas.draw()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
