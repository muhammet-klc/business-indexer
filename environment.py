""" environment.py """
import os


class Environment:
    """ environment """

    def __init__(self, required_vars):
        """
        required_vars: A list of environment variables that need to be verified.
        """
        self.required_vars = required_vars

    def verify(self):
        """
        Checks the validity of environment variables.
        Returns an error message if any required variable is missing.
        """
        missing_vars = []

        for var in self.required_vars:
            if var not in os.environ:
                missing_vars.append(var)

        if missing_vars:
            return f"Error: The following environment variables are missing: {', '.join(missing_vars)}"

        return "Environment validation successful."

    def get(self, var):
        """
        Retrieve the value of an environment variable.
        Returns None if the variable is not set.
        """
        return os.environ.get(var)

    def set(self, var, value):
        """
        Set a new environment variable.
        """
        os.environ[var] = value

    def reset(self, var):
        """
        Remove an environment variable from the environment.
        """
        if var in os.environ:
            del os.environ[var]
            return f"Environment variable {var} removed."
        return f"Environment variable {var} does not exist."
