"""
    Filename: lite_unit_test.py
    Author: Hung Tran
    Purpose: To ease the unit testing and debugging work.
    Usage: 
    <1>: For in-script testing
        1. Import this module.
        2. Use UTEST_INSTANCE provided by the module or
            create a new UnitTest
        3. Add all tests with UnitTest.add_test()
        4. After adding all of the test cases, UnitTest.execute()
    <2>: For writing assignment checker (Advanced):
        1. Import this module.
        2. In the checker, use try_import.
        3. Write test_cases with return value of try_import as the
            imported module. Example: try_import("merge.py").
        3. Encapsulate all test cases and execute() of that module in
            if(try_import is not None)

    Potential improvement:
        + Concurrent queue for task scheduling and asynchronous
            unit tests.
        + Accounting for ANY output in a set
        + Better error reflections (tracebacks, exceptions)
        + Timeout (to come with asynchronous tests)
        + Solve lists as f_arg is unhashable.
        + Make exception prints more visible.
"""
import importlib

def try_import(module_path):
    """ Try import module_path and return the module. Returns None
         and prints exception error if import cannot be accomplished.
         
        Argument: module_path is string that is absolute or relative
                        path of the module we want to import

        Returns: module or None
    """
    try:
        return importlib.import_module(module_path)            
    except Exception as e:
        exception_str = "Could not import \"{}\". Error: {}; {}"\
            .format(module_path, e.__doc__, e)
        print(exception_str)
        return None

class UnitTest:
    """ A class that helps compare output of a function given an input.
        Uses a dict to traverse through function calls and arguments.
        Does not break any test in case an exception is thrown and prints
        out exceptions.
        
        Notes: add_test() for every possible tests before execute()
        
        Variables: in2out is dict of func_arg-tuple(func,string)
                   total is int of total tests added
                   passed is int of total tests passed
    """
    def __init__(self):
        self.in2out = dict()
        self.total = 0
        self.passed = 0
    def add_test(self,func, f_arg, expected_str_out):
        """
            Adds the test to in2out dict without executing it.
            Converts expected_str_out to str if necessary.

            Arguments:
                func is function pointer (pass by name without ())
                f_arg is function argument
                expected_str_out is the expected string output
                    from func(f_arg).
            
            Pre-condition:
                func is func ptr of any kind
                f_arg must be hashable (for variadic arg, make
                    a tuple because tuple is hashable and is accepted
                    by variadic arg).
                expected_str_out must be str or any type with
                    __str__()
            
            Post-condition:
                self.in2out[f_arg] is assigned the set of
                    func and expected_str_out
                self.total += 1
        """
        # Ensures expected_str_out is actually type str
        # This also allows lazy typing and unsure in str notation
        # of the resulting obj
        if type(expected_str_out) is not str:
            expected_str_out = str(expected_str_out)
        func_1_arg = func
        if func.__code__.co_argcount >1:
            # Transform it to variadic func
            func_1_arg = lambda args: func(*args)
        value_set = (func_1_arg, expected_str_out)
        self.in2out[f_arg] = value_set
        self.total += 1
    def execute(self):
        """
            Executes everything in self.in2out, catches
            every exception in theory and write to stdout.
            Prints out the number of tests passed.
            Expect printing <lambda> function instead
            of the correct name for multi-arg funcs
        """
        FUNC = 0
        OUT = 1
        # TODO: Can do this multi-threadedly
        for func_arg, func_out_pair in self.in2out.items():
            try:
                func, exp_out = func_out_pair[FUNC],func_out_pair[OUT]
                # Get str_out by executing func and type cast to str
                str_out = str(func(func_arg))
                if str_out == exp_out:
                    self.passed += 1
                    print("Passed {}({}).".format(func.__name__,func_arg))
                else:
                    print("Output mismatched: \"{}\" vs \"{}\"".format\
                          (str_out, exp_out))            
            except Exception as e:
                # Catch all exceptions in theory
                print("Failed to execute {}({})."\
                       .format(func.__name__,func_arg))
                exception_str = "Error: {}. {}".format(e.__doc__, e)
                # Should be better to print in stderr
                print(exception_str)
            finally:
                # Add a new line to make it easier to 
                # distinguish between
                # tests
                print()
        # Print out results
        print("Passed {}/{}".format(self.passed, self.total))

# Quick and dirty static singleton
# Might not work correctly if python has singly-inclusion
# like #pragma once in C++ headers
UTEST_INSTANCE = UnitTest()

# Example usage
if __name__ == "__main__":   
    def test_func(inp):
        if type(inp) is str:
            raise ZeroDivisionError
        return 2

    UTEST_INSTANCE.add_test(test_func, 5, "2")
    UTEST_INSTANCE.add_test(test_func, "2", "2")
    UTEST_INSTANCE.add_test(test_func, 1, 1)
    # Expecting: 1/3 with one ZeroDivisionError err msg

    #Tests that test for VA-func transformation
    def test_func_2_args(arg1, arg2):
        return "{}_;_{}".format(arg1, arg2)
    
    def division(arg1, arg2):
        return arg1/arg2

    UTEST_INSTANCE.add_test(test_func_2_args,(12, 34),\
       test_func_2_args(12,34))  #Correct
    UTEST_INSTANCE.add_test(division, (5,2), "2.5")  #Correct
    # Expecting another ZeroDivisionError err msg.
    UTEST_INSTANCE.add_test(division, (1, 0), "inf")  #Err
    # Total should be 3/6
    UTEST_INSTANCE.execute()
    
