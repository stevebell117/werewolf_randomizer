import random
import traceback
import re
import time

def main():
    print("Welcome!")
    try:
        print("Please enter in the roles you'd like to randomize, one player/potential role per line:")
        role_input = ''
        is_chaos_round = False
        player_roles = []
        # Get the roles that the user inputs
        for line in iter(input, role_input):
            player_roles.append(line)
        # Get the number of players based on lines entered
        player_count = len(player_roles)
        print("Got it! We have {} players this round. Randomizing.".format(player_count))
        start = time.time()
        # Check chaos
        for role in player_roles:
            if "/" in line:
                is_chaos_round = True
                break
        if is_chaos_round:
            player_roles = chaos_round(player_roles)
        # Get a human readable list of player numbers, from 1 to player_count + 1 (0-14 becomes 1-15).
        number_array = list(range(1, player_count + 1))
        random.shuffle(number_array)
        random.shuffle(player_roles)
        # The numbers and roles are shuffled. Join them and sort by Player number.
        final_roles = sorted(zip(number_array, player_roles))
        end = time.time()
        print("Here's the rundown:")
        for role in final_roles:
            print(role)
        print("Good Luck! (This took {} seconds to randomize)".format(end - start))
    except KeyboardInterrupt:
        print("\nkbye")
    except:
        print("Something broke. Give Steven this info {}".format(traceback.print_exc()))


def chaos_round(role_list, drunk_enabled=True):
    determined_roles = []
    index = 0
    while index < len(role_list):
        # Grab the role string
        role_string = role_list[index]
        # Split the role string by all possibilities on the line. x / y / z becomes [x, y, z]
        shuffle_roles = role_string.split('/')
        role_to_return = 0
        if len(shuffle_roles) > 1:
            # We need to count how many times this particular string is possible.
            # For example, if we have x / y / z twice, it means that
            # once we pick z, then the next selection will be between x / y.
            count = role_list.count(role_string)
            returned_roles = role_select(shuffle_roles, count)
            for role in returned_roles:
                determined_roles.append(role.strip())
            # We've handled the duplicate lines, let's move on
            index = index + len(returned_roles)
        else:
            # If there is only one role, no need to do work and we can just add it in
            determined_roles.append(shuffle_roles[role_to_return].strip())
            index = index + 1
    while drunk_enabled:
        drunk_index = random.randint(0, len(determined_roles)-1)
        # At the moment, if the role has the word Drunk in it, it can't be drunk.
        # It makes sense when you look at the input...
        if "Drunk" in determined_roles[drunk_index]:
            continue
        determined_roles[drunk_index] = determined_roles[drunk_index] + " | Drunk"
        break
    return determined_roles


def role_select(roles, count):
    # Limit in this regard is if we have a role like x / y / z x2
    # This means that if we were to pick z, we can still pick it a second time
    # If we didn't pick z, then the next time would be between z and whatever is remaining.
    # This also prevents the randomizing being x / y / z / z.
    limit, valid_limit = intTryParse(roles[-1][-1])
    selected_roles = []
    for _ in range(0, count):
        # Select one of the roles
        selected_index = random.randint(0, count)
        # As of now, the role with potential duplicates is always the last one so we check that
        if roles[selected_index] == roles[-1]:
            if valid_limit and limit > 0:
                # If we still have the ability to select this role, let's do it and decrement the value on it.
                # For example, x / y / z x2 will become x / y / z x1
                selected_roles.append(re.sub(r'x.', '', roles[-1]))
                if limit - 1 == 0:
                    # This means we've already selected the maximum from this role, so let's remove it entirely.
                    del(roles[-1])
                    continue
                roles[-1] = roles[-1].replace(str(limit), str(limit - 1))
                continue
            else:
                # Only one of the items can exist, nothing special needs to be done.
                selected_roles.append(roles[selected_index])
                del(roles[selected_index])
        else:
            # Select the role and remove it from future consideration.
            selected_roles.append(roles[selected_index])
            del(roles[selected_index])
        count = count - 1
    return selected_roles


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


main()
