class TestSuite:
    """
    Parent class to define and run test cases with.
    """
    def __init__(self):
        self.results = {}

    def _get_test_cases(self) -> list:
        """
        Get all test cases defined in the child class.

        Returns
        -------
        list:
            All the test cases defined in the child class.
            Returns an empty list when the parent class is used directly.
        """
        # Get all child class attributes.
        child = self
        child_all = dir(self)
        child_attributes = list(self.__dict__.keys())

        # Get all parent class methods.
        parent = self.__class__.__base__
        parent_methods = dir(parent)

        # Get child methods which are not in parent class.
        tests = [test for test in child_all if test not in parent_methods]
        tests = [test for test in tests if test not in child_attributes]

        # Return empty list when parent class is used directly.
        if self.__class__.__base__ == object:
            tests = []

        return [getattr(child, test) for test in tests]

    def _run_test_suite_method(self, method: callable) -> bool:
        """
        Run a test suite method.

        Parameters
        ----------
        method: callable
            The test suite method to be run.

        Returns
        -------
        bool:
            True: the test suite method succeeded.
            False: the test suite method failed.
        """
        name = method.__name__
        success = False
        message = None

        try:
            method()
            success = True
        except Exception as error:
            message = str(error)

        self.results[name] = [success, message]
        return success

    def _run_test_case(self, test_case: callable) -> bool:
        """
        Run a test case method including its setup and teardown.

        Parameters
        ----------
        test_case: callable
            The test case method to be run.

        Returns
        -------
        bool:
            True: the test case, including its setup and teardown, succeeded.
            False: either the test case, its setup, or its teardown failed.
        """
        name_case = test_case.__name__
        name_setup = self.set_up_test_case.__name__
        name_teardown = self.tear_down_test_case.__name__

        # Return False when test case setup fails.
        if not self._run_test_suite_method(method=self.set_up_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_setup)
            return False

        # Run test case.
        success = self._run_test_suite_method(method=test_case)

        # Return False when test case teardown fails.
        if not self._run_test_suite_method(method=self.tear_down_test_case):
            # Replace test case setup key with test case method key in results.
            self.results[name_case] = self.results.pop(name_teardown)
            return False

        return success

    def run_test_suite(self) -> bool:
        """
        Run the entire test suite including its setups and teardowns.

        Returns
        -------
        bool:
            True: all test suite methods succeeded.
            False: some test suite methods failed.
        """
        # Reset results.
        self.results = {}

        # Return False when test suite setup fails.
        if not self._run_test_suite_method(method=self.set_up_test_suite):
            return False

        # Run all test cases.
        success = True
        tests = self._get_test_cases()

        for test in tests:
            if not self._run_test_case(test_case=test):
                success = False

        # Return False when test suite teardown fails.
        if not self._run_test_suite_method(method=self.tear_down_test_suite):
            return False

        # Return result of all test cases.
        return success

    def set_up_test_suite(self):
        """
        Editable placeholder for the test suite setup.
        """

    def tear_down_test_suite(self):
        """
        Editable placeholder for the test suite teardown.
        """

    def set_up_test_case(self):
        """
        Editable placeholder for the test case setup.
        """

    def tear_down_test_case(self):
        """
        Editable placeholder for the test case setup.
        """


def assert_equal(calc: any, true: any) -> None:
    """
    Assert if two variables are equal.
    Supported variable types: bool, str, int, float, list, tuple, dict.

    Parameters
    ----------
    calc: any
        Calculated or predicted variable value.
    true: any
        True or expected variable value.
    """
    if calc != true:
        raise AssertionError(f"calculated value {calc} is not equal to true value {true}")


def assert_not_equal(calc: any, true: any) -> None:
    """
    Assert if two variables are not equal.
    Supported variable types: bool, str, int, float, list, tuple, dict.

    Parameters
    ----------
    calc: any
        Calculated or predicted variable value.
    true: any
        True or expected variable value.
    """
    if calc == true:
        raise AssertionError(f"calculated value {calc} is equal to true value {true}")


def assert_almost_equal(calc: any, true: any, margin: float, relative: bool = True) -> None:
    """
    Assert if two variables are almost equal within a given margin.
    Supported variable types: int, float, list(int, float), tuple(int, float).

    Parameters
    ----------
    calc: any
        Calculated or predicted variable value.
    true: any
        True or expected variable value.
    margin: float
        Allowed margin for the comparison.
        The true value is used as a reference.
    relative: bool
        The margin is a fraction of the reference value when True (relative),
        or the margin is used directly when False (absolute).
    """
    def _check_elements(calc_ele, true_ele):
        # Check if elements are numeric.
        try:
            float(calc_ele) and float(true_ele)
        except ValueError:
            raise AssertionError("margin not supported for non-numeric variables")

        # Calculate allowed margin.
        allowed = true_ele * margin if relative else margin
        # Lower boundary of allowed element value.
        lower = (calc_ele + allowed) - true_ele < 0
        # Upper boundary of allowed element value.
        upper = (true_ele + allowed) - calc_ele < 0
        # Iterables are not equal when element value lies outside boundaries.
        if lower or upper:
            raise AssertionError(f"calculated value {calc} is not close to true value {true}")

    # Check if variables are iterable.
    if "__iter__" in dir(calc) and "__iter__" in dir(true):
        # Check if lengths match.
        if len(calc) != len(true):
            raise AssertionError("calculated variable is not the same size as true variable")
        # Check each element if so.
        else:
            for i in range(len(calc)):
                _check_elements(calc_ele=calc[i], true_ele=true[i])

    # Check if either variable is iterable.
    elif "__iter__" in dir(calc) or "__iter__" in dir(true):
        raise AssertionError(f"iterable and non-iterable variable are asserted")

    # Perform single comparison if neither.
    else:
        _check_elements(calc_ele=calc, true_ele=true)


def assert_true(expr: any) -> None:
    """
    Assert if an expression is True.

    Parameters
    ----------
    expr: any
        Any expression which can be reduced to a boolean (e.g. non-empty list, operator).
    """
    if not expr:
        raise AssertionError(f"calculated variable or statement {expr} is not True")


def assert_false(expr: any) -> None:
    """
    Assert if an expression is False.

    Parameters
    ----------
    expr: any
        Any expression which can be reduced to a boolean (e.g. empty list, operator).
    """
    if expr:
        raise AssertionError(f"calculated variable or statement {expr} is not False")


def assert_raises(action: callable, expected: any,
                  args: tuple = None, kwargs: dict = None) -> None:
    """
    Assert if executing a callable raises an error.

    Parameters
    ----------
    action: callable
        Callable to be executed.
    expected: any
        Expected error to be raised.
    args: tuple
        Arguments for the callable, if any.
    kwargs: dict
        Keyword arguments for the callable, if any.
    """
    args = () if args is None else args
    kwargs = {} if kwargs is None else kwargs
    message = "no error is raised"

    try:
        action(*args, **kwargs)
    except Exception as error:
        if not isinstance(error, expected):
            message = f"raised error is not {expected}: {type(error)} {error}"
        else:
            message = None

    if message is not None:
        raise AssertionError(message)
