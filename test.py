def print_solution(perm):
    print(" ".join(perm))

def is_valid(perm):
    # In this example, any arrangement is considered valid
    return True

def arrange_boys_girl_seats(perm, choices):
    if len(perm) == len(choices):
        # All positions are filled, print the solution
        print_solution(perm)
        return

    for person in choices:
        # Skip arrangements where the girl is not in the middle
        if person == 'Girl' and len(perm) != len(choices) // 2:
            continue

        # Add the person to the current arrangement
        perm.append(person)

        # Check if the current arrangement is valid
        if is_valid(perm):
            # Recur to fill the next position
            arrange_boys_girl_seats(perm, choices)

        # Backtrack: Remove the person and try other possibilities
        perm.pop()

# Example usage:
boys_and_girl = ['Boy1', 'Girl', 'Boy2']
arrange_boys_girl_seats([], boys_and_girl)
