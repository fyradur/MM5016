import matplotlib.pyplot as plt
import numpy as np


## Description
"""
The methods are written to output the desired function. In order to
see the solutions to all the tasks run this as a python 3 file
in a terminal.
"""


## Methods copied from lab 9


def linear_interpolation(data_set):
    """ Takes a list of data points in form of tuple coordinates, that is:
    [(x0, y0), (x1, y1) ...] and returns an apporixmated function given by
    linear interpolation.
    """
    if len(data_set) <= 1:
        raise ValueError("<linear_interpolation: not enough data points>")
        
    data_set_sorted = sorted(data_set)
    if len(data_set_sorted) == 2:
        (x0, y0), (x1, y1) = data_set_sorted
        k = (y1 - y0) / (x1 - x0)
        m = y0
        interpolated_function = lambda x: k * (x - x0) + m
        return interpolated_function
    else:
        head = data_set_sorted[:2]
        head_interval_end = head[1][0] 
        tail = data_set_sorted[1:]
        head_function = linear_interpolation(head)
        tail_function = linear_interpolation(tail)
        complete_function = lambda x:( head_function(x) if x <= head_interval_end
                                       else tail_function(x))
        return complete_function


def linear_interpolation_vector(data_set, query_points):
    """ Transforms the the query_points list from the format of 
    [x1,x2,x3...] to [f(x1), f(x2), f(x3) ...],
    where f is the linearly interpolated function from data_set.
    """
    f = linear_interpolation(data_set)
    return list(map(f,query_points))


def euler_method(derivative, initial_value, stepsize):
    """ Given that 'derivative' is a function of (x,y)
    and that the 'initial_value' is a tuple of the form
    (x0, y(x0)), this method returns a function that
    approximates y in the equation dy/dx = derivative(x,y).
    """
    step_to_goal = lambda x, goal: x+stepsize if x < goal else x - stepsize
    y_next = lambda x, y, goal: (y + stepsize * derivative(x,y) if x < goal
                                 else y - stepsize * derivative(x,y) )


    def y(x):
        x0, y0 = initial_value
        xk, yk = x0, y0
        while x0 <= xk < x or x0 >= xk > x:
            xk = step_to_goal(xk, x)
            yk = y_next(xk, yk, x)
        return yk

    
    return y


## Problem 1: analytic data of function
problem_1_analytic_function = lambda t: -1 / t
problem_1_derivative = lambda t,y: (1 / t **2) - (y / t) - y ** 2
problem_1_x_values = np.linspace(1, 2, int(1 / 0.05))
problem_1_initial_value = (1,-1)
problem_1_y_values = list(map(problem_1_analytic_function, problem_1_x_values))
problem_1_data = list(zip(problem_1_x_values, problem_1_y_values))


## Problem 1a
problem_1a_function = euler_method(problem_1_derivative, problem_1_initial_value, 0.05)
problem_1a_y = list(map(problem_1a_function, problem_1_x_values))
problem_1a_data_set = list(zip(problem_1_x_values, problem_1a_y))
problem_1a_compare = [(problem_1_analytic_function(t) -
                       problem_1a_function(t))
                      for t in problem_1_x_values]
def problem_1a():
    print("Problem 1a compared values:", problem_1a_compare)


## Problem 1b
def problem_1b():
    f_interpolated = linear_interpolation(problem_1a_data_set)
    f_analytic = problem_1_analytic_function 
    print("y(1.052) analytic:", f_analytic(1.052))
    print("y(1.052) approximated:", f_interpolated(1.052))

    print("y(1.555) analytic:", f_analytic(1.555))
    print("y(1.555) approximated:", f_interpolated(1.555))

    print("y(1.978) analytic:", f_analytic(1.978))
    print("y(1.978) approximated:", f_interpolated(1.978))


def heun_method(derivative, initial_value, stepsize):
    """ Given that 'derivative' is a function of (x,y)
    and that the 'initial_value' is a tuple of the form
    (x0, y(x0)), this method returns a function that
    approximates y using heun's method in the equation 
    dy/dx = derivative(x,y).
    """


    def y(x):
        x0, y0 = initial_value
        xk, yk = x0, y0
        while x0 <= xk < x:
            x_next = xk + stepsize 
            y_bar = yk + stepsize * derivative(xk,yk)
            y_next = yk + (stepsize / 2) * (derivative(xk, yk) +
                                            derivative(x_next, y_bar))
            xk, yk = x_next, y_next
        return yk

    
    return y


## Problem 1c
problem_1c_function = heun_method(problem_1_derivative, problem_1_initial_value, 0.05)
problem_1c_y = list(map(problem_1c_function, problem_1_x_values))
problem_1c_data_set = list(zip(problem_1_x_values, problem_1c_y))
problem_1c_compare = [(problem_1_analytic_function(t) -
                       problem_1c_function(t))
                      for t in problem_1_x_values]
def problem_1c():
    print("Problem 1a compared values:", problem_1c_compare)


## Problem 1d
def problem_1d():
    f_interpolated = linear_interpolation(problem_1c_data_set)
    f_analytic = problem_1_analytic_function 
    print("y(1.052) analytic:", f_analytic(1.052))
    print("y(1.052) approximated:", f_interpolated(1.052))

    print("y(1.555) analytic:", f_analytic(1.555))
    print("y(1.555) approximated:", f_interpolated(1.555))

    print("y(1.978) analytic:", f_analytic(1.978))
    print("y(1.978) approximated:", f_interpolated(1.978))


def runge_kutta_method(derivative, initial_value, stepsize):
    """ Given that 'derivative' is a function of (x,y)
    and that the 'initial_value' is a tuple of the form
    (x0, y(x0)), this method returns a function that
    approximates y using runge kutta method in the equation 
    dy/dx = derivative(x,y).
    """


    def y(x):
        x0, y0 = initial_value
        xk, yk = x0, y0
        while x0 <= xk < x:
            k1 = derivative(xk,yk)
            k2 = derivative(xk + stepsize / 2, yk + stepsize * k1 / 2)
            k3 = derivative(xk + stepsize / 2, yk + stepsize * k2 / 2)
            k4 = derivative(xk + stepsize, yk + stepsize * k3)
            x_next = xk + stepsize 
            y_next = yk + (1/6) * stepsize * (k1 + 2 * k2 + 2 * k3 + k4)
            xk, yk = x_next, y_next
        return yk

    
    return y


## Problem 1e
problem_1e_function = runge_kutta_method(problem_1_derivative,
                                         problem_1_initial_value, 0.05)
problem_1e_y = list(map(problem_1e_function, problem_1_x_values))
problem_1e_data_set = list(zip(problem_1_x_values, problem_1e_y))
problem_1e_compare = [(problem_1_analytic_function(t) -
                       problem_1e_function(t))
                      for t in problem_1_x_values]
def problem_1e():
    print("Problem 1e compared values:", problem_1e_compare)


## Problem 1f
def problem_1f():
    f_interpolated = linear_interpolation(problem_1e_data_set)
    f_analytic = problem_1_analytic_function 
    print("y(1.052) analytic:", f_analytic(1.052))
    print("y(1.052) approximated:", f_interpolated(1.052))

    print("y(1.555) analytic:", f_analytic(1.555))
    print("y(1.555) approximated:", f_interpolated(1.555))

    print("y(1.978) analytic:", f_analytic(1.978))
    print("y(1.978) approximated:", f_interpolated(1.978))


## Problem 1: display graphs
def problem_1_display():
   # a = linear_interpolation(problem_1a_data_set)
   # problem_1a_interpolated_y = list(map(a, problem_1_x_values))
   # c = linear_interpolation(problem_1c_data_set)
   # problem_1c_interpolated_y = list(map(c, problem_1_x_values))
   # e = linear_interpolation(problem_1e_data_set)
   # problem_1e_interpolated_y = list(map(e, problem_1_x_values))
    
    plt.plot(problem_1_x_values, problem_1_y_values, label="Analytical")
    plt.plot(problem_1_x_values, problem_1a_y, label="Euler's method")
    #plt.plot(problem_1_x_values, problem_1a_interpolated_y,
    #         label="Euler's method interpolated")
    plt.plot(problem_1_x_values, problem_1c_y, label="Heun's method")
    #plt.plot(problem_1_x_values, problem_1c_interpolated_y,
    #         label="Heun's method interpolated")
    plt.plot(problem_1_x_values, problem_1e_y, label="Runge-Kutta method")
    #plt.plot(problem_1_x_values, problem_1e_interpolated_y,
    #         label="Runge-Kutta method interpolated")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()


## Problem 2: analytic data of function
problem_2_stepsize = 0.1
problem_2_analytic_function = lambda x: 2 + 2 * x + x ** 2 - np.exp(x)
problem_2_derivative = lambda x,y: y - x ** 2
problem_2_x_values = np.linspace(0, 3.3, int(3.3 / 0.1))
problem_2_initial_value = (0,1)
problem_2_y_values = list(map(problem_2_analytic_function, problem_2_x_values))
problem_2_data = list(zip(problem_2_x_values, problem_2_y_values))

problem_2_init_orbit_x = [-0.8 ,-0.9 ,0]
problem_2_init_orbit_y = list(map(problem_2_analytic_function,
                                  problem_2_init_orbit_x))
problem_2_init_orbit = list(zip(problem_2_init_orbit_x, problem_2_init_orbit_y))


## Problem 2: runge kutta
problem_2_runge_kutta = runge_kutta_method(problem_2_derivative,
                                           problem_2_initial_value,
                                           problem_2_stepsize)


## Problem 2: Adams-Bashforth
def bashforth_method(derivative, initial_value_orbit, stepsize):
    """ Given that 'derivative' is a function of (x,y) and that the 'initial_value' is a tuple of the form
    (x0, y(x0)), this method returns a function that
    approximates y using the Adams-Bashforth method in the equation 
    dy/dx = derivative(x,y).
    """


    def y(x):
        orbit = initial_value_orbit.copy()
        while 0 <= orbit[-1][0] < x:
            (x0,y0), (x1,y1) = orbit[-2:]
            x_next = x1 + stepsize 
            y_next = (y1 + (3/2) * stepsize * derivative(x1,y1)
                      - (1/2) * stepsize * derivative(x0,y0))
            orbit.append((x_next, y_next))
            
        return orbit[-1][1]

    
    return y

## To get the adams-Bashforth method:
problem_2_bashforth = bashforth_method(problem_2_derivative,
                                             problem_2_init_orbit,
                                             problem_2_stepsize)


## Problem 2: Adams-Moulton
def moulton_method(derivative, initial_value_orbit, stepsize):
    """ Given that 'derivative' is a function of (x,y) and that the 'initial_value' is a tuple of the form
    (x0, y(x0)), this method returns a function that
    approximates y using the Adams-Moulton method in the equation 
    dy/dx = derivative(x,y).
    """


    def y(x):
        orbit = initial_value_orbit.copy()
        while 0 <= orbit[-1][0] < x:
            (x0,y0), (x1,y1) = orbit[-2:]
            euler = euler_method(derivative, (x1,y1), stepsize)
            x_next = x1 + stepsize 
            y_next_approx = euler(x_next)
            
            y_next = (y1 + stepsize * ( (5/12) * derivative(x_next, y_next_approx)
                                        + (2/3) * derivative(x1,y1)
                                        - (1/12) * derivative(x0, y0)))
            orbit.append((x_next, y_next))
            
        return orbit[-1][1]

    
    return y

## To get the Adams-Moulton method:
#f = trapezoidal_method( problem_2_derivative ,problem_2_init_orbit, problem_2_stepsize)
problem_2_moulton = moulton_method(problem_2_derivative,
                                   problem_2_init_orbit,
                                   problem_2_stepsize)


## Problem 1: display graphs
def problem_2_display():
    y_runge_kutta = list(map(problem_2_runge_kutta, problem_2_x_values))
    y_bashforth = list(map(problem_2_bashforth ,problem_2_x_values))
    y_moulton = list(map(problem_2_moulton ,problem_2_x_values))
    
    plt.plot(problem_2_x_values, problem_2_y_values, label="Analytical")
    plt.plot(problem_2_x_values, y_runge_kutta, label="Runge-Kutta")
    plt.plot(problem_2_x_values, y_bashforth, label="Adams Bashforth")
    plt.plot(problem_2_x_values, y_moulton, label="Adam Moulton method")

    plt.xlabel("x")
    plt.ylabel("y")

    plt.legend()
    plt.show()


def main():
    while True:
        print("At any point, type 'exit', to exit")
        message =(
""" 
To display solutions to '1a', '1b', '1c', '1d', '1e' or '1f'
simply type in the string. To display a graph of all subroutines in task 1,
type 'display 1'. To display the graph for task 2, type 'display 2'. 
""")
        user_input = input(message)
        if user_input == "1a":
            problem_1a()
        elif user_input == "1b":
            problem_1b()
        elif user_input == "1c":
            problem_1c()
        elif user_input == "1d":
            problem_1d()
        elif user_input == "1e":
            problem_1e()
        elif user_input == "1f":
            problem_1f()
        elif user_input == "display 1":
            problem_1_display()
        elif user_input == "display 2":
            problem_2_display()
        elif user_input == "exit":
            break
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()
