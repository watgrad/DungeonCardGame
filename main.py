# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models import *
import curses
from curses import wrapper


# stdscr is the main curses terminal window -- render all headings on this window
# stats_win_descriptor will be the windows to display user stats

def display_messages(player: Player, dungeon: Dungeon, messages: dict, icons: dict, stdscr):    
    messages["title"][2] = f"{player.name}, you are on level {dungeon.player_depth(player)[0] - dungeon.player_depth(player)[1]} of the Dungeon"
    messages["health"][2] = f"Health Points: {player.health}"
    messages["torches"][2] = f"Torches remaining: {4 - len(player.torches)}"
    messages["scrolls"][2] = f"Scrolls found: {len(player.loot.scrolls)}"
    messages["treasure"][2] = f"Treasure found: {len(player.loot.treasure)} items"
    messages["hoards"][2] = f"Hoards found: {len(player.loot.hoards)}"
    #messages["dungeon"][2] = "You are at the entrance to a deep, dark cave!"
    #messages["input"][2] = f"{player.name}, enter 'd' to descend, or 'x' to exit."


    icons["health"] = [4, 2, ' '.join([str(i) for i in dungeon.deck.health_cards[-1::-1]])]
    icons["torches"] =  [4, 30, ' '.join([str(i) for i in player.torches[:]])]
    icons["scrolls"] = [7, 30, ' '.join([str(i) for i in player.loot.scrolls[:]])]
    icons["treasure"] = [10, 30, ' '.join([str(i) for i in player.loot.treasure[:]])]
    icons["hoards"] = [13, 30, ' '.join([str(i) for i in player.loot.hoards[:]])]

    stdscr.clear()
    for key, value in messages.items():
        stdscr.addstr(value[0], value[1], value[2], value[3])
    for key, value in icons.items():
        stdscr.addstr(value[0], value[1], value[2])

    row = 8
    col = 3
    contents = ""
    if dungeon.rooms:
        for room in dungeon.rooms:
            for card in room.room_contents:
                contents += card.uni_code + " "
            stdscr.addstr(row, col, contents)
            contents = ""
            row += 2

    stdscr.refresh()

def main_loop(stdscr):
    stdscr.clear()
    
    # CHECK is the terminal the correct size?
    y, x = stdscr.getmaxyx()
    while y < 40 or x < 40:
        stdscr.addstr(2, 2, "Resize screen \nto 40 x 25!")
        stdscr.refresh()
        resize = curses.is_term_resized(y, x)
        if resize is True:
            y, x = stdscr.getmaxyx()
            stdscr.clear()
            curses.resizeterm(y, x)
            stdscr.refresh()

    stdscr.addstr(10, 10, "Welcome to the dungeon!", curses.A_BOLD | curses.A_STANDOUT)
    stdscr.addstr(11, 10, "Press any key to begin!")
    stdscr.refresh()

    # Set a color palate
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)  # red (1) on white (7)
    RED_WHITE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_WHITE = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_BLACK = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    YELLOW_BLACK = curses.color_pair(5)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
    BLUE_BLACK = curses.color_pair(6)
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_BLACK = curses.color_pair(7)

    # create the player and dungeon objects
    player = Player()
    dungeon = Dungeon()

    # prepare the messages dictionary for game play
    messages = {
        "title": [1, 2,
                  f"{player.name}, you are on level {dungeon.player_depth(player)[0] - dungeon.player_depth(player)[1]} of the Dungeon",
                  curses.A_BOLD],
        "health": [3, 2, f"Health Points: {player.health}", RED_BLACK | curses.A_BOLD],
        "torches": [3, 30, f"Torches remaining: {4 - len(player.torches)}", YELLOW_BLACK | curses.A_BOLD],
        "scrolls": [6, 30, f"Scrolls found: ", BLUE_BLACK | curses.A_BOLD],
        "treasure": [9, 30, "Treasure found:", GREEN_BLACK | curses.A_BOLD],
        "hoards": [12, 30, "Hoards found:", GREEN_BLACK | curses.A_BOLD],
        "dungeon": [25, 2, "You are at the entrance to a deep, dark cave!", curses.COLOR_WHITE],
        "description": [27, 2, "You are at the entrance to a deep, dark dungeon!", curses.COLOR_WHITE],
        "input": [29, 2, f"{player.name}, enter 'd' to descend, or 'x' to exit.", curses.COLOR_WHITE]
    }

    icons = {
        "health": [4, 2, ' '.join([str(i) for i in dungeon.deck.health_cards[-1::-1]])],
        "torches": [4, 30, ' '.join([str(i) for i in player.torches[:]])],
        "scrolls": [7, 30, ' '.join([str(i) for i in player.loot.scrolls[:]])],
        "treasure": [10, 30, ' '.join([str(i) for i in player.loot.treasure[:]])],
        "hoards": [13, 30, ' '.join([str(i) for i in player.loot.hoards[:]])]
    }

    # wait for keypress and then set to 100 to generate the first room  TODO: add logic to end game if x is pressed?
    key_press = stdscr.getch()
    key_press = 100

    while player.health > 0:

        if key_press == 263 or key_press == 27: # Backspace or esc
            quit()

        if key_press == 100 or key_press == 68:   # 'd' or 'D' keypress
            messages["dungeon"][2] = f"You {player.direction} the dungeon!"
            dungeon.rooms.append(Room(dungeon, player))
            dungeon.rooms[-1].set_up_room()
            if dungeon.rooms[-1].event.value <=0 and dungeon.rooms[-1].devine_intervention == True:
                messages['input'][2] = "The Godess has blessed you, disarming a trap!"
                dungeon.rooms[-1].process_room(player, messages)
            messages['input'][2] = "Press 'd' to delve deeper or 'x' to leave the dungeon."
            messages['description'][2] = f"{dungeon.rooms[-1].description}"

        if dungeon.rooms[-1].event.value > 0:
            # if the room event is a trap:
            if dungeon.rooms[-1].event.suit == Suits.DIAMOND:
                messages['dungeon'][2] = f"You come to a {dungeon.rooms[-1].name}."
                messages['input'][2] = "Draw a card [c] to disarm the trap!"
                if player.loot.scrolls_contains(Suits.DIAMOND):
                    message['input'][2] = "Draw a card [c] or use the Disarm Traps scroll[s]."
                display_messages(player, dungeon, messages, icons, stdscr)
                stdscr.refresh()
                choice = stdscr.getch()
                # 'c' == 99 or 67;  's' == 115 or 83
                if (choice == 115 or choice == 83) and player.loot.scrolls_contains(Suits.DIAMOND):
                    dungeon.rooms[-1].event.value = 0
                    # TODO: get rid of the used scroll!
                    messages[input][2] = ""
                    messages["description"][2] = "The scroll worked, the trap is disarmed!\n"
                    
                if choice == 99 or choice == 67:
                    dungeon.rooms[-1].draw_card(player)
                    if dungeon.rooms[-1].devine_intervention == True:
                        messages['input'][2] = "The goddess has blessed you with a devine intervention - the trap is disarmed!\n Press any key."
                        stdscr.refresh()
                        choice = stdscr.getch()
                    if dungeon.rooms[-1].room_contents[-1].value == 1:  #card is torch
                        message['input'] += "You used a torch!\n"
                        player.torches.append(dungeon.rooms[-1].room_contents.pop())
                    if dungeon.rooms[-1].event.value <= 0 and dungeon.rooms[-1].devine_intervention == False:
                        if dungeon.rooms[-1].devine_intervention != True:
                            messages['input'][2] += "You've disarmed the trap!\n"
                    elif dungeon.rooms[-1].event.value <= 0 and dungeon.rooms[-1].devine_intervention == True:    
                        messages['input'][2] = "The goddess has saved you - the trap is disarmed!\n"
                        dungeon.rooms[-1].event.value = 0
                    else:
                        messages['input'][2] = f"You failed to disarm the trap! You took {dungeon.rooms[-1].event.value} damage!"
                        player.health -= dungeon.rooms[-1].event.value
                        for i in range(dungeon.rooms[-1].event.value):
                            dungeon.deck.health_cards.pop(0)
                        if player.health < 1:
                            messages['dungeon'][2] = "You Died!"
                if dungeon.rooms[-1].event.value <= 0:
                    dungeon.rooms[-1].process_room(player, messages)
                messages['input'][2] += "\nPress a key to go on..."


            if dungeon.rooms[-1].event.suit == Suits.CLUB:
                messages['dungeon'][2] = f"You come to a {dungeon.rooms[-1].name}."

                #outcome = engine.resolve_door(dungeon, player)

            if dungeon.rooms[-1].event.suit == Suits.SPADE:
                messages['dungeon'][2] = f"You come to a {dungeon.rooms[-1].name}."

                #outcome = engine.resolve_monster(dungeon, player

        # X OR x == 88 OR 120
        display_messages(player, dungeon, messages, icons, stdscr)
        stdscr.refresh()
        key_press = stdscr.getch()

if __name__ == "__main__":
    wrapper(main_loop)
