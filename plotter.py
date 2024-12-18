from sympy import sympify, symbols, lambdify, solve
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FunctionPlotter:
    def __init__(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

    def plot(self, functions, x_ranges):
        self.ax.clear()
        for function, x_range in zip(functions, x_ranges):
            try:
                x_min, x_max = map(float, x_range.split(":"))
                x = np.linspace(x_min, x_max, 100000)
                x_sym, y_sym = symbols('x y')
                if "=" in function:
                    lhs, rhs = map(sympify, function.split("="))
                    expr = lhs - rhs
                    solutions = solve(expr, y_sym)
                    for sol in solutions:
                        f = lambdify(x_sym, sol, "numpy")
                        y = f(x)
                        self.ax.plot(x, y)
                    self.ax.plot(0,0,label=f"{function}")
                elif "x" in function and "y" in function:
                    solutions = solve(function, y_sym)
                    for sol in solutions:
                        print(sol)
                        f = lambdify(x_sym, sol, "numpy")
                        y = f(x)
                        self.ax.plot(x, y)
                    self.ax.plot(0, 0, label=f"{function}")
                else:
                    f = lambdify(x_sym, function, "numpy")
                    y = f(x)
                    self.ax.plot(x, y, label=f"y={function}")
            except Exception as e:
                raise ValueError(f"Ошибка при построении графика: {e}")

        # Настройки графика
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Графики функций")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
