from typing import List


class HailstoneCalculator:
    def __init__(self, starting_number: int) -> None:
        """
        Initializes the HailstoneCalculator.

        Parameters:
        - starting_number (int): The starting number
        for the hailstone sequence.
        """
        self.starting_number = starting_number
        self.sequence = [starting_number]

    def calculate_hailstone_sequence(self, starting_number: int = 4) -> None:
        """
        Calculates the hailstone sequence for the specified starting number.

        Parameters:
        - starting_number (int): The new starting number.
          If not provided, uses the initial starting number.

        Returns:
        - None
        """
        if starting_number is not None:
            self.starting_number = starting_number
            self.sequence = [starting_number]

        number = self.starting_number
        while number != 1:
            if number % 2 == 0:
                number //= 2
            else:
                number = 3 * number + 1
            self.sequence.append(number)

    def get_number_of_steps(self) -> int:
        """
        Gets the number of steps in the hailstone sequence.

        Returns:
        - int: The number of steps, excluding the initial number.
        """
        return len(self.sequence) - 1

    def get_steps_list(self) -> List[int]:
        """
        Gets the hailstone sequence as a list.

        Returns:
        - list: The list containing the hailstone sequence.
        """
        return self.sequence

    def generate_textual_summary(self) -> str:
        """
        Generates a textual summary of the hailstone sequence.

        Returns:
        - str: The textual summary.
        """
        summary = f"Hailstone sequence: {', '.join(map(str, self.sequence))}\n"
        summary += f"Number of steps: {self.get_number_of_steps()}\n"
        summary += f"Final number: {self.sequence[-1]}"
        return summary
