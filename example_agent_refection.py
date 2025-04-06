import random

class ReflectiveAgent:
    """
    A simple reflective agent that attempts to reach a target value through iterative refinement.
    """
    def __init__(self, target_value, max_iterations=10, tolerance=0.05, initial_value=None):
        """
        Initializes the reflective agent.

        Args:
            target_value (float): The value the agent is trying to achieve.
            max_iterations (int, optional): The maximum number of iterations the agent will run. Defaults to 10.
            tolerance (float, optional): The acceptable error margin. Defaults to 0.05.
            initial_value (float, optional): The starting value for the agent. If None, a random value between 0 and 1 is used.
        """
        self.target_value = target_value
        # Ensure max_iterations is at least 1
        self.max_iterations = max(1, int(max_iterations))
        self.tolerance = tolerance
        if initial_value is None:
            self.current_value = random.uniform(0, 1)  # Initial random guess
        else:
            self.current_value = initial_value
        self.iterations = 0
        self.memory = []  # Store past values and errors as (value, error) tuples

    def generate_output(self):
        """
        Simulates the agent generating an output or taking an action.
        In a real-world scenario, this could involve complex calculations,
        interaction with an environment, or using a language model.
        This simple example adds a small random change to the current value.

        Returns:
            float: The new output value.
        """
        # Add a small random change, but keep it within the 0 to 1 range
        self.current_value = self.current_value + random.uniform(-0.2, 0.2)
        self.current_value = max(0, min(1, self.current_value))
        return self.current_value

    def evaluate_output(self):
        """
        Evaluates the agent's current output by comparing it to the target value.
        Calculates the absolute error.

        Returns:
            float: The error (absolute difference between current value and target value).
        """
        error = abs(self.current_value - self.target_value)
        self.memory.append((self.current_value, error))  # Store the value and error
        return error

    def reflect(self):
        """
        Implements a basic reflection mechanism.  This version looks at the two
        previous steps and tries to avoid going in the wrong direction.
        More advanced reflection could involve:
            - Analyzing the entire history in self.memory.
            - Using a model to predict better adjustments.
            - Considering the context of the task.
        """
        if len(self.memory) > 1:
            previous_value, previous_error = self.memory[-2]
            current_error = self.memory[-1][1]

            if current_error > previous_error:
                # Error increased: Try going back to the previous value.
                self.current_value = previous_value
                print("   Reflecting: Error increased, reverting to previous value.")
            else:
                # Error decreased (or stayed the same): Keep the new value.
                print("   Reflecting: Error decreased, keeping current value.")
        elif len(self.memory) == 1:
             print("   Reflecting: First iteration, no previous state to compare.")
        else:
            print("   Reflecting: No memory yet.")

    def iterate(self):
        """
        Runs the agent through multiple iterations of generating output,
        evaluating it, and reflecting on the result.

        Returns:
            float: The final output value after all iterations, or the value at the
                   iteration where the target was reached within tolerance.
        """
        print(f"Starting agent iterations (max {self.max_iterations}, tolerance {self.tolerance})...")
        while self.iterations < self.max_iterations:
            self.iterations += 1
            print(f"\n--- Iteration {self.iterations} ---")
            output = self.generate_output()
            error = self.evaluate_output()

            print(f"   Generated output: {output:.4f}, Error: {error:.4f}")

            if error <= self.tolerance:
                print(f"   Target value {self.target_value:.4f} reached within tolerance after {self.iterations} iterations.")
                print(f"   Result: {self.current_value:.4f}")
                return self.current_value

            self.reflect()  # Reflect and adjust for the next iteration

        print(f"\nMaximum iterations ({self.max_iterations}) reached. Target value {self.target_value:.4f} not reached within tolerance.")
        print(f"Final result: {self.current_value:.4f}")
        return self.current_value


if __name__ == "__main__":
    # Example usage:
    target_value = 0.65
    agent = ReflectiveAgent(target_value, max_iterations=15, tolerance=0.02, initial_value=0.2)
    final_result = agent.iterate()

    print(f"\nAgent finished with final value: {final_result:.4f}")
