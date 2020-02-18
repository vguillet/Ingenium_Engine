
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import sys

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '7/02/2020'

##################################################################################################################


class ML_tools:
    @staticmethod
    def throttle(current_step, nb_steps, max_value, min_value=1., decay_function=0):
        """
        Throttle a value according to the instance in the run time.

        The following decay functions settings can be used:
                0 - Fixed value (no decay, returns max value)

                1 - Linear decay

                2 - Logarithmic decay (in development)

        :param current_step: Current step
        :param nb_steps: Total number of step in the run
        :param max_value: Max allowed value
        :param min_value: Min allowed value
        :param decay_function: Decay function setting
        :return: Throttled value
        """
        from math import log10

        # -- Exit program if incorrect settings used
        if decay_function > 2:
            print("Invalid throttle decay function reference")
            sys.exit()

        inverse = False
        if max_value < min_value:
            inverse = True

        # TODO: add decay functions (log/exponential etc...)
        if current_step <= nb_steps:
            if decay_function == 0:  # Fixed value
                return max_value

            if decay_function == 1:  # Linear decay
                if inverse:
                    throttled_value = max_value + (min_value - max_value) / nb_steps * current_step
                    if throttled_value >= min_value:
                        throttled_value = min_value
                else:
                    throttled_value = max_value - (max_value - min_value) / nb_steps * current_step
                    if throttled_value <= min_value:
                        throttled_value = min_value

            # TODO: Complete log decay
            elif decay_function == 2:  # Logarithmic decay
                throttled_value = max_value + log10(-(current_step - nb_steps))

            else:
                throttled_value = max_value

        else:
            throttled_value = min_value

        return throttled_value
