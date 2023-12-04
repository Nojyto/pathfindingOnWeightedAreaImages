import matplotlib.pyplot as plt
import sympy
import numpy as np
import math


def line_equation_and_x_intercept(point1, point2):
    (x1, y1), (x2, y2) = point1, point2

    if x2 - x1 == 0:
        return "Vertical Line", None
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    line_eq = f"y = {m}x + {b}"
    x_intercept = -b / m if m != 0 else None
    
    return line_eq, (x_intercept, 0) if x_intercept is not None else "No x-axis intercept (Horizontal Line)"


def time_for_journey(s, m, e, v1, v2):
    def time_for_path(x1, y1, x2, y2, v):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / v
    return time_for_path(*s, *m, v1) + time_for_path(*m, *e, v2)


def binary_search_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water, tolerance=1e-6):
    lhs, rhs = x_bound
    while rhs - lhs > tolerance:
        mid = (lhs + rhs) / 2

        lhs_time = time_for_journey(start_point, (lhs, 0), end_point, speed_in_sand, speed_in_water) 
        mid_time = time_for_journey(start_point, (mid, 0), end_point, speed_in_sand, speed_in_water)
        
        if lhs_time < mid_time:
            rhs = mid
        else:
            lhs = mid

    final_middle_point = (mid, 0)
    final_total_time = time_for_journey(start_point, final_middle_point, end_point, speed_in_sand, speed_in_water)

    return final_middle_point, final_total_time


def ternary_search_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water, tolerance=1e-6):
    lhs, rhs = x_bound

    while rhs - lhs > tolerance:
        one_third = (rhs - lhs) / 3
        mid1 = lhs + one_third
        mid2 = rhs - one_third

        time_mid1 = time_for_journey(start_point, (mid1, 0), end_point, speed_in_sand, speed_in_water)
        time_mid2 = time_for_journey(start_point, (mid2, 0), end_point, speed_in_sand, speed_in_water)

        if time_mid1 < time_mid2:
            rhs = mid2
        else:
            lhs = mid1

    final_middle_point = ((lhs + rhs) / 2, 0)
    final_total_time = time_for_journey(start_point, final_middle_point, end_point, speed_in_sand, speed_in_water)

    return final_middle_point, final_total_time


def gradient_descent_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water, learning_rate=0.01, tolerance=1e-6):
    def gradient_of_time_for_journey(x, start_point, end_point, speed_in_sand, speed_in_water):
        # Partial derivative with respect to x
        dx_sand = (x - start_point[0]) / (speed_in_sand * math.sqrt((x - start_point[0])**2 + start_point[1]**2))
        dx_water = (x - end_point[0]) / (speed_in_water * math.sqrt((x - end_point[0])**2 + end_point[1]**2))
        return dx_sand + dx_water

    current_x = (x_bound[0] + x_bound[1]) / 2
    difference = tolerance + 1  # Initialize with a value greater than tolerance

    while difference > tolerance:
        gradient = gradient_of_time_for_journey(current_x, start_point, end_point, speed_in_sand, speed_in_water)
        new_x = current_x - learning_rate * gradient
        new_time = time_for_journey(start_point, (new_x, 0), end_point, speed_in_sand, speed_in_water)
        current_time = time_for_journey(start_point, (current_x, 0), end_point, speed_in_sand, speed_in_water)

        difference = abs(new_time - current_time)
        current_x = new_x

    final_middle_point = (current_x, 0)
    final_total_time = time_for_journey(start_point, final_middle_point, end_point, speed_in_sand, speed_in_water)
    
    return final_middle_point, final_total_time


def derivitive_solve_min_time(start_point, end_point, speed_in_sand, speed_in_water):
    x = sympy.symbols('x')
    tx = (sympy.sqrt(sympy.Pow(x - start_point[0], 2) + sympy.Pow(start_point[1], 2)) / speed_in_sand) + \
        (sympy.sqrt(sympy.Pow(x - end_point[0], 2) + sympy.Pow(end_point[1], 2)) / speed_in_water)
    # print(tx)
    optimal_x_solutions = sympy.solve(tx.diff(x), x)
    approx_optimal_x = [sol.evalf() for sol in optimal_x_solutions][0]
    
    final_middle_point = (approx_optimal_x, 0)
    final_total_time = time_for_journey(start_point, final_middle_point, end_point, speed_in_sand, speed_in_water)
    
    return final_middle_point, final_total_time


if __name__ == "__main__":
    x_bound = (0, 10)
    y_bound = (-10, 10)

    speed_in_sand = 6
    speed_in_water = 2
    start_point = (2, -8)
    end_point = (8, 4)


    mp_middle_point = ((start_point[0] + end_point[0]) / 2, 0)
    mp_min_total_time = time_for_journey(start_point, mp_middle_point, end_point, speed_in_sand, speed_in_water)
    bs_middle_point, bs_min_total_time = binary_search_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water)
    ts_middle_point, ts_min_total_time = ternary_search_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water)
    gd_middle_point, gd_min_total_time = gradient_descent_min_time(start_point, end_point, x_bound, speed_in_sand, speed_in_water)
    ds_middle_point, ds_min_total_time = derivitive_solve_min_time(start_point, end_point, speed_in_sand, speed_in_water)
    _, sl_middle_point = line_equation_and_x_intercept(start_point, end_point)
    sl_min_total_time = time_for_journey(start_point, sl_middle_point, end_point, speed_in_sand, speed_in_water)
    
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

    # Plotting the points
    ax.plot(*start_point,  'go', label='Start Point')
    ax.plot(*end_point,    'ro', label='End Point')
    ax.plot(*ds_middle_point, 'bo', label='Middle Point')
    
    # Annotating the points
    ax.annotate(f'Start Point {start_point}', (start_point[0], start_point[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate(f'End Point {end_point}', (end_point[0], end_point[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate(f'Middle Point {mp_middle_point}', (mp_middle_point[0], mp_middle_point[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate(f'Optimal Middle Point ({ds_middle_point[0]:.4f}, {ds_middle_point[1]})', (ds_middle_point[0], ds_middle_point[1]), textcoords="offset points", xytext=(0,-15), ha='center')

    # Connecting paths
    ax.plot([start_point[0], mp_middle_point[0], end_point[0]], 
            [start_point[1], mp_middle_point[1], end_point[1]], 
            'y--', label=f'Mid Point path - {mp_min_total_time:.4f}')
    ax.plot([start_point[0], sl_middle_point[0], end_point[0]], 
            [start_point[1], sl_middle_point[1], end_point[1]], 
            'y--', label=f'Straight line path - {sl_min_total_time:.4f}')
    ax.plot([start_point[0], bs_middle_point[0], end_point[0]], 
            [start_point[1], bs_middle_point[1], end_point[1]], 
            'b--', label=f'Binary search path - {bs_min_total_time:.4f}')
    ax.plot([start_point[0], ts_middle_point[0] - 0.01, end_point[0]], 
            [start_point[1], ts_middle_point[1], end_point[1]], 
            'c--', label=f'Ternary search path - {ts_min_total_time:.4f}')
    ax.plot([start_point[0], gd_middle_point[0], end_point[0]], 
            [start_point[1], gd_middle_point[1], end_point[1]], 
            'k--', label=f'Gradiant descent path - {gd_min_total_time:.4f}')
    ax.plot([start_point[0], ds_middle_point[0], end_point[0]], 
            [start_point[1], ds_middle_point[1], end_point[1]], 
            'm--', label=f'Derivitive solution path - {ds_min_total_time:.4f}')
    
 
    # Fill area under and above the x-axis (Ox)
    x = np.linspace(*x_bound)
    ax.fill_between(x, 0, y_bound[1], facecolor='blue', alpha=0.3, interpolate=True)
    ax.fill_between(x, y_bound[0], 0, facecolor='orange', alpha=0.3, interpolate=True)

    # Write speed in coresponding terrains
    plt.text(0.9, 0.95, f'Speed in water: {speed_in_water}',
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes)
    plt.text(0.9, 0.05, f'Speed in sand: {speed_in_sand}',
     horizontalalignment='center',
     verticalalignment='center',
     transform = ax.transAxes)
    
    # Set settings
    plt.xlim(x_bound)
    plt.ylim(y_bound)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Graph with approximate solutions and endpoints')
    plt.legend()
    plt.show()