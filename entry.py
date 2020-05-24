import random
import traceback
import re
import time

def main():
    print("Welcome! Press Enter/Return to progress through each step.")
    while True:
        try:
            print("Please enter in the roles you'd like to randomize, one per line:")
            role_input = ''
            is_chaos_round = False
            index = 1 # gross
            player_roles = []
            for line in iter(input, role_input):
                player_roles.append(line)
                index = index + 1
            player_count = len(player_roles)
            confirm = input("Got it! We have {} players this round. Sound good? Y/n: ".format(player_count))
            if confirm == "" or str.upper(confirm) == "Y":
                print("Let's randomize this.")
                start = time.time()
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
                    drunk_found = False
                    while not drunk_found:
                        drunk_index = random.randint(0, len(player_roles)-1)
                        if "Drunk" in player_roles[drunk_index]:
                            continue
                        player_roles[drunk_index] = player_roles[drunk_index] + " | Drunk"
                        drunk_found = True
                number_array = list(range(1,player_count+1)) # humans hate index starting at 0
                random.shuffle(number_array)
                random.shuffle(player_roles)
                final_roles = sorted(zip(number_array, player_roles))
                end = time.time()
                print("Alright, here's the rundown:")
                for role in final_roles:
                    print(role)
                print("Good Luck! (This took {} seconds to randomize)".format(end - start))
                break
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
            if valid_limit and limit > 0:
                selected_roles.append(re.sub(r'x.', '', roles[-1]))
                roles[-1] = roles[-1].replace(str(limit), str(limit - 1))
            elif valid_limit and limit == 0:
                del(roles[-1])
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