from src.hailstone_calculator.calculator import HailstoneCalculator


def main() -> None:
    """
    Main function to interact with the user
    and display hailstone sequence results.

    Returns:
    - None
    """
    while True:
        starting_number = int(
            input(
                "Enter the starting number for hailstone sequence \
                (or type 'exit' to quit): "
            )
        )

        if starting_number == "exit":
            print("Exiting the program.")
            break

        # Create an instance of HailstoneCalculator
        hailstone_calculator = HailstoneCalculator(starting_number)

        # Calculate the hailstone sequence
        hailstone_calculator.calculate_hailstone_sequence()

        # Display results
        print("\nResults:")
        print(f"Number of steps: {hailstone_calculator.get_number_of_steps()}")
        print(f"List of steps: {hailstone_calculator.get_steps_list()}")
        print(hailstone_calculator.generate_textual_summary())


if __name__ == "__main__":
    main()
