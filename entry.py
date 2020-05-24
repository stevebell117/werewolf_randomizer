import random
import traceback

def main():
    print("Welcome! Press Enter/Return to progress through each step.")
    while True:
        try:
            player_count = int(input("Please enter the number of players: "))
            break
        except ValueError:
            print("That's not a number. Try again please.")
            continue
    while True:
        try:
            print("So we have {} players. Cool. Now, please enter in the roles you'd like to randomize, one per line:".format(player_count))
            role_input = ''
            initial_confirm = True
            is_chaos_round = False
            index = 1 # gross
            player_roles = []
            for line in iter(input, role_input):
                if initial_confirm:
                    print("\nGot it. So the roles you've given me are:")
                    initial_confirm = False
                print("Role #{}: {}".format(index, line))
                player_roles.append(line)
                index = index + 1
            if len(player_roles) != player_count:
                print("The number of roles {} entered does not match the number of players {}. Let's try this again!".format(
                    len(player_roles),
                    player_count
                ))
                continue
            confirm = input("Alright, look good? Y/n: ")
            if confirm == "" or str.upper(confirm) == "Y":
                print("Let's randomize this.")
                # Check chaos
                for role in player_roles:
                    if "/" in line:
                        is_chaos_round = True
                        print("\n***************************************************")
                        print("Chaos round detected. If it's not a chaos round, don't submit roles with '/' in them.")
                        print("***************************************************\n")
                        break
                if is_chaos_round:
                    player_roles = chaos_round(player_roles)
                number_array = list(range(1,player_count+1)) # humans hate index starting at 0
                random.shuffle(number_array)
                random.shuffle(player_roles)
                final_roles = sorted(zip(number_array, player_roles))
                print("Alright, here's the rundown:")
                for role in final_roles:
                    print(role)
                confirm = input("Look good, or do you want to do this again? Y/n: ")
                if confirm == "" or str.upper(confirm) == "Y":
                    print("Awesome, good luck!")
                    break
                print("Damn, ok. Let's go again.\n**********************************************\n")
            else:
                print("Let's try this again then...")
                continue
        except KeyboardInterrupt:
            print("\nkbye")
            break
        except:
            print("Something broke. Give Steven this info {}".format(traceback.print_exc()))
            break

def chaos_round(role_list):
    determined_roles = []
    limited_roles = {}
    index = 0
    while index < len(role_list):
        role = role_list[index]
        shuffle_roles = role.split('/')
        role_to_return = 0
        if len(shuffle_roles) > 1:
            count = role_list.count(role)
            returned_roles = role_select(shuffle_roles, count)
            for role in returned_roles:
                determined_roles.append(role.strip())
            index = index + len(returned_roles)
        else:
            determined_roles.append(shuffle_roles[role_to_return].strip())
            index = index + 1
    return determined_roles

def role_select(roles, count):
    limit, valid_limit = intTryParse(roles[-1][-1])
    selected_roles = []
    for i in range(0, count):
        selected_index = random.randint(0,count)
        if roles[selected_index] == roles[-1]:
            if valid_limit:
                selected_roles.append(roles[-1])
                roles[-1] = roles[-1].replace(str(limit), str(limit - 1))
            else:
                selected_roles.append(roles[selected_index])
                count = count - 1
                del(roles[selected_index])
        else:
            selected_roles.append(roles[selected_index])
            count = count - 1
            del(roles[selected_index])
    return selected_roles



def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


main()