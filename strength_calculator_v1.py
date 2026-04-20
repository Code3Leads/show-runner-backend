# 1RM Calculator using Epley's formula
print("Welcome to the 1RM Calculator!")
MAX_REPS = 15
def epley_1rm(weight: float, reps: int) -> float:
    """Estimate 1RM using Epley's formula."""
    return weight * (1 + reps /30)
def get_float(prompt: str) -> float:
    """safely get a float from user."""
    while True:
        try: 
            return float(input(prompt))
        except ValueError:
            print(" Invalid input. Please enter a number.")
def get_int(promt: str) -> int:
    """safely get an integer from the user."""
    while True:
        try:
            return int(input(promt))
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            
def get_training_percent() -> float:
    """Get a training max percentage like 85,90, etc."""
    while True:
        pct = get_float("Enter training max percentage (e.g., 85 for 85%): ")
        if 50 <= pct <= 100:
            return pct / 100
        print("Please enter a percentage between 50 and 100.")
def one_rep_max_flow():
    weight = get_float("Enter the weight lifted (or 0 to quit): ")
    if weight == 0:
        print("Exiting the calculator. Goodbye!")
        return
    reps = get_int("Enter the number of reps: ")
    if reps <= 0:
        print("Reps must be greater than 0.")
        print("Maybe try lowering the weight next set?")
        return
    if reps > MAX_REPS:
        print(f"Reps capped at {MAX_REPS} for formula accuracy.")
        reps = MAX_REPS
    pct = get_training_percent()
    one_rm = epley_1rm(weight, reps)
    tm = one_rm * pct
    print(f"\nEstimate 1RM: {one_rm:.2f} lbs")
    print(f"Training Max ({pct*100:.0f}%): {tm:.2f} lbs\n")
    return 
def main():
    while True:
        print("\nChoose and option:")
        print("1) Estimate 1RM (Epley)")
        print("2) Estimate 1RM + Training Max (choose percentage)")
        print("0) Quit")
        Choice = input("Selection: ").strip()
        if Choice == "0":
            print("Pussying out. Goodbye!")
            break
        elif Choice  == "1":
            keep_going = one_rep_max_flow()
            if not keep_going:
                print("Nice work. Goodbye!")
                break
        elif Choice == "2":
            keep_going = one_rep_max_flow()
            if not keep_going:
                print("Awesome. Goodbye!")
                break
        else:
            print("Invalid. Please choose 1, 2, or 0.")
main()