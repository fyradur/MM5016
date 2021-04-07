import math
## Description

# The solution to task 1 will be the functions find_root_newton and
# find_root_secant.

# The solution to task 2 will be displayed by running this program in a terminal.
# The discussion of the dependence of initial values will be in the report.

## Iterate function
def iterate(function, root_approximates, tolerance, next_values_function,
            iteration=0, max_iterations=100, debug=False):
    """ Approximates a root x for the equation function(x) = 0,
    by applying the next_values_function on the list root_approximates 
    until tolerance is met on the last element of the list, in that
    case that last element is returned. If debug is True, then a tuple of
    that mentioned value and the iteration is returned. An error is raised 
    if iteration exceeds max_iterations.
    """
    # The root_approximates list will usually be (always, in the context of
    # this asignment) updated by calculating a new value based on all
    # the values in the root_approximates list, and then appending that new value,
    # and deleting the first element in root_approximates.
    # So the last element in root_approximates will be the most recent estimate of
    # the root. In the case of Newton's method, the root_approximates list
    # will just be a single value surrounded by a list.
    newest_root_approximate = root_approximates[-1]
    satisfies_tolerance = abs(function(newest_root_approximate)) <= tolerance
    if iteration > max_iterations:
        raise RecursionError("<iterate: maximum ammount of iterations reached>")
    elif satisfies_tolerance and debug:
        return newest_root_approximate, iteration
    elif satisfies_tolerance and not debug:
        return newest_root_approximate
    else:
        next_values = next_values_function(root_approximates)
        return iterate(function, next_values, tolerance, next_values_function,
                       iteration+1, max_iterations, debug)

## Newtons's method
# The next values function for Newton's method just takes a list of size
# one and returns a list of size one.
def newton_next_values_function(function, derivative_of_function):
    """ The next_values function for Newton's method. """
    f, f_prim = function, derivative_of_function
    next_value_function = lambda x: x - (f(x) / f_prim(x))
    return lambda guess_roots: [ next_value_function(guess_roots[0]) ]


def find_root_newton(function, function_derivative, root_approximate,
                     tolerance=0.00001,
                     debug=False):
    """ Solve the root x for the equation function(x) = 0 using
    Newton's method, where root_approximate is an approximation of
    the root.
    """
    root_approximates = [root_approximate]
    next_values_function = newton_next_values_function(function,
                                                       function_derivative)
    return iterate(function, root_approximates, tolerance, next_values_function,
                   debug=debug)

## Secant method
def secant_next_values_function(function):
    """ The next_values_function for the Secant method. """
    f = function
    next_value_function = lambda x0, x : x - f(x) * (x0 - x) / ( f(x0) - f(x) ) 
    # As mentioned in the comments for iterate, this updates function
    # updates root_approximates by calculating the new approximate root,
    # appending it, and deleting the first element of the list.
    return lambda root_approximates: [root_approximates[1],
                                      next_value_function(root_approximates[0],
                                                          root_approximates[1])]


def find_root_secant(function, root_approximates,
                     tolerance=0.00001, debug=False):
    """ Solve the root x for the equation function(x) = 0 using
    the secant method, where root_approximates is a list of 2 approximates
    of the root.
    """
    next_values_function = secant_next_values_function(function)
    return iterate(function, root_approximates, tolerance, next_values_function,
                   debug=debug)

## The following functions are for task 2.
def function1(x):
    """ Equation (1) has zero on the right hand side so we let the left hand
    side be the function.
    """
    return x**4 - 5 * x**3 + 9 * x + 3


def function1_derivative(x):
    """ The derivative to function1 with respect to x. """
    return 4 * x**3 - 15 * x**2 + 9

def function2(x):
    """ If we substract exp(x) on each side of equation (2), we get zero on
    the right hand side, so we let the left hand side be the function.
    """
    return 2 * x**2 + 5 - math.exp(x)


def function2_derivative(x):
    """ The derivative of function2. """
    return 4 * x - math.exp(x)

def test_newton(function, function_derivative):
    """ Prints the result of approximating a root x in the equation 
    function(x) = 0, using Newton's method, with initial value
    ranging from 0 to 10.
    """
    for init_value in range(10):
        solution, iterations = find_root_newton(function, function_derivative,
                                                init_value, debug=True)
        print("Found solution: x =", solution, ", in", iterations, "iterations")

def test_secant(function, boundary):
    """ Prints the result of approximating a root x in the equation 
    function(x) = 0, using the Secant method, with initial values being the
    boundary.
    """
    solution, iterations = find_root_secant(function, boundary,
                                            debug=True)
    print("Found solution: x =", solution, ", in", iterations, "iterations")

def main():
    """ Asks the user to choose an equation and what method to use in order
    to find a root, and an appropiate result will be output.
    """
    print("At any point write 'exit' to exit.")
    loop = True
    while loop:
        message = ("Choose one of the following tasks:\n"
                   "Find a root to x^4-5x^3+9x+3=0 using Newton's method. (1)\n"
                   "Find a root to x^4-5x^3+9x+3=0 using the Secant method. (2)\n"
                   "Find a root to 2x^2 + 5 = e^x using Newton's method. (3)\n"
                   "Find a root to 2x^2 + 5 = e^x using the Secant method. (4)\n")
        case = input(message)
        if case == 'exit':
            print("The program will now terminate.")
            loop = False
        elif case == '1':
            test_newton(function1, function1_derivative)
        elif case == '2':
            test_secant(function1, [4,6])
        elif case == '3':
            test_newton(function2, function2_derivative)
        elif case == '4':
            test_secant(function2, [3,4])
        else:
            print("Not a valid input.")
            

if __name__ == "__main__":
    main()
