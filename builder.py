import math
from math import isnan

import numpy
from sympy import sympify, symbols, lambdify, solve
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class FunctionPlotter:
    def __init__(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

    def plot(self, functions, x_ranges, ylimit):
        self.ax.clear()
        local_y_lim = []
        for function, x_range in zip(functions, x_ranges):
            try:
                x_min, x_max = map(float, x_range.split(":"))
                x = np.linspace(x_min, x_max, 100000)
                x_sym, y_sym = symbols('x y')
                if "=" in function:
                    lhs, rhs = map(sympify, function.split("="))
                    expr = lhs - rhs
                    solutions = solve(expr, y_sym)
                    color = ""
                    for sol in solutions:
                        f = lambdify(x_sym, sol, "numpy")
                        y = f(x)
                        if color == "":
                            d = self.ax.plot(x, y)
                            local_y_lim = [min(d[0].get_ydata()), max(d[0].get_ydata())]
                            color = d[0].get_color()
                        else:
                            self.ax.plot(x, y, color=color)
                    self.ax.plot(0,0,label=f"{function}", color=color)
                elif "x" in function and "y" in function:
                    solutions = solve(function, y_sym)
                    color = ""
                    for sol in solutions:
                        f = lambdify(x_sym, sol, "numpy")
                        y = f(x)
                        if color == "":
                            d = self.ax.plot(x, y)
                            local_y_lim = [min(d[0].get_ydata()), max(d[0].get_ydata())]
                            color = d[0].get_color()
                        else:
                            self.ax.plot(x, y, color=color)
                    self.ax.plot(0,0,label=f"{function}", color=color)
                else:
                    f = lambdify(x_sym, function, "numpy")
                    y = f(x)
                    d = self.ax.plot(x, y, label=f"y={function}")
                    local_y_lim = [min(d[0].get_ydata()), max(d[0].get_ydata())]
                if ylimit == "Any":
                    try:
                        self.ax.set_ylim(local_y_lim)
                    except:
                        self.ax.set_ylim([-10,10])
                else:
                    self.ax.set_ylim(map(float, ylimit.split(":")))
            except Exception as e:
                raise ValueError(f"Ошибка при построении графика: {e}")

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Графики функций")
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()
