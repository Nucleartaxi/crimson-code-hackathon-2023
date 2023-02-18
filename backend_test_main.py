from backend import Backend

b = Backend()
while True:
    print("enter int to press index|H|")
    user_input = input(": ").strip()
    if user_input.isdigit():
        b.pressed_index(int(user_input))
    elif user_input == "H":
        b._previous_folder_list()
        b.previous_directory()
    
    print("left pane: " + str(b.previous_folder_list))
    print("center pane: " + str(b.current_folder_list))
    print("right pane: " + str(b.right_pane_list))
