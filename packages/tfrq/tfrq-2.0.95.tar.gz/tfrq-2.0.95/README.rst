tfrq - an easy way to parallelize processing a function
=======================================================

`tfrq on github! <https://github.com/masterFoad/tfrq>`_

Stop waiting for your code to finish, start using tfrq - the effortless solution for parallelizing your functions and supercharging your performance!

This library provides an easy way to parallelize the execution of a
function in python using the concurrent.futures library. It allows you
to run multiple instances of a function simultaneously, making your code
run faster and more efficiently. It also provides a simple API for
managing the process, allowing you to cancel or wait for the completion
of a task. With this library, you can easily take advantage of the power
of parallel processing in python.

Here’s an example of how you can use the library to parallelize the
execution of the ``print`` function:

Example 1:
==========

::

   from tfrq import tfrq
   params = ["Hello", "World", "!"]
   func = print
   tfrq(func=func, params=params, num_cores=3)

Example 2:
==========

::

   input_list = [[1, 2], [3, 4], [5, 5], [6, 7]]
   list_of_results_for_all_pairs = tfrq(sum, input_list)
   print(list_of_results_for_all_pairs)  # [[3], [7], [10], [13]] -- result for each pair ordered.

This code will call the ``sum`` function in parallel with the given
parameters and use all cores, so it will print the given parameters in
parallel.

Example 3 - using the config parameter:
=======================================

::

        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs = tfrq(sum, input_list)
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.

        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs = tfrq(sum, input_list, config={"print_errors": True})
        # unsupported operand type(s) for +: 'int' and 'str'
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.

        input_list = [[1, 2], [3, 4], [5, 5], [6, str(7) + '1']]  # error in final input
        list_of_results_for_all_pairs, errors = tfrq(sum, input_list,
                                                     config={"print_errors": True, "return_errors": True})
        # unsupported operand type(s) for +: 'int' and 'str'
        print(list_of_results_for_all_pairs)  # [[3], [7], [10], []] -- result for each pair ordered.
        print(errors)  # [[], [], [], [TypeError("unsupported operand type(s) for +: 'int' and 'str'")]]

Example 4 - operator to apply on parameters:
=============================================

::

        operator=None  -> func(args)
        operator="*"   -> func(*args)
        operator="**"  -> func(**args)

        params = ["Hello", "World", "!"]
        func = print
        tfrq(func=func, params=params, num_cores=3, operator="*")
        # H e l l o
        # !
        # W o r l d ---- notice now it is func(*args) - that is causing the spaces.

        params = ["Hello", "World", "!"]
        func = print
        tfrq(func=func, params=params, num_cores=3)
        # Hello
        # World
        # !

default config:
===============

::

    config = {"return_errors": False, "print_errors": True}


tfrq is an arabic word meaning “To Split”, which is the purpose of this
simple method, to split the work of a single function into multiple
processes as easy as possible.