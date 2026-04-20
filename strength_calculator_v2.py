print("Workout Logger + 1RM Calculator (v2)")

MAX_REPS = 15


def epley_1rm(weight: float, reps: int) -> float:
    """Estimate 1RM using the Epley formula."""
    return weight * (1 + reps / 30)


def get_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def cap_reps(reps: int) -> int:
    if reps > MAX_REPS:
        print(f"Reps capped at {MAX_REPS} for formula accuracy.")
        return MAX_REPS
    return reps


def log_session():
    workout_type = input("\nWorkout type (push/pull/legs/core/etc): ").strip().lower()
    lift_name = input("Lift name (bench, row, OHP, etc): ").strip().lower()

    planned_sets = get_int("How many sets do you plan to log? ")
    if planned_sets <= 0:
        print("Sets must be greater than 0.")
        return

    # Each set stored as: {"set": i, "weight": w, "reps": r, "one_rm": x}
    sets = []

    for i in range(1, planned_sets + 1):
        print(f"\nSet {i}/{planned_sets}")
        weight = get_float("  Weight: ")
        reps = get_int("  Reps: ")

        if reps <= 0:
            print("  Reps must be > 0. Re-do this set.")
            # redo the same set number
            continue

        reps = cap_reps(reps)

        one_rm = epley_1rm(weight, reps)
        sets.append({"set": i, "weight": weight, "reps": reps, "one_rm": one_rm})

        print(f"  Estimated 1RM: {one_rm:.2f}")

    if not sets:
        print("\nNo sets logged.")
        return

    best = max(sets, key=lambda s: s["one_rm"])
    total_volume = sum(s["weight"] * s["reps"] for s in sets)

    print("\n--- Session Summary ---")
    print(f"Workout type: {workout_type}")
    print(f"Lift: {lift_name}")
    print(f"Sets logged: {len(sets)}")
    print(f"Best set (by est 1RM): {best['weight']} x {best['reps']}  ->  {best['one_rm']:.2f}")
    print(f"Total volume (weight x reps): {total_volume:.0f}")


def main():
    while True:
        print("\nMenu:")
        print("1) Log a workout session")
        print("0) Quit")

        choice = input("Selection: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        elif choice == "1":
            log_session()
        else:
            print("Invalid selection. Choose 1 or 0.")


main()