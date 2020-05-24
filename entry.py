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
            print("Something broke. Give Steven this info".format(traceback.print_exc()))
            break

main()