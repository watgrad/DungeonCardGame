# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models import *
import curses
from curses import wrapper


# stdscr is the main curses terminal window -- render all headings on this window
# stats_win_descriptor will be the windows to display user stats

def display_messages(player: Player, dungeon: Dungeon, messages: dict, icons: dict, stdscr):
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
    
    messages["title"] =  [1, 2,
                  f"{player.name}, you are on level {dungeon.player_depth(player)[0] - dungeon.player_depth(player)[1]} of the Dungeon",
                  curses.A_BOLD]
    messages["health"] = [3, 2, f"Health Points: {player.health}", RED_BLACK | curses.A_BOLD]
    messages["torches"] = [3, 30, f"Torches remaining: {4 - len(player.torches)}", YELLOW_BLACK | curses.A_BOLD]
    messages["scrolls"] = [6, 30, f"Scrolls found: ", BLUE_BLACK | curses.A_BOLD]
    messages["treasure"] = [9, 30, "Treasure found:", GREEN_BLACK | curses.A_BOLD]
    messages["hoards"] = [12, 30, "Hoards found:", GREEN_BLACK | curses.A_BOLD]
    messages["dungeon"] = [25, 2, "You are at the entrance to a deep, dark cave!", curses.COLOR_WHITE]
    messages["input"] = [26, 1, f"{player.name}, enter 'd' to descend, or 'x' to exit.", curses.COLOR_WHITE]


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
    stdscr.refresh()

def main_loop(stdscr):
    stdscr.clear()
    stdscr.addstr(10, 10, "Welcome to the dungeon!", curses.A_BOLD | curses.A_STANDOUT)
    stdscr.addstr(11, 10, "Press any key to begin!")
    stdscr.refresh()

    # player_win = curses.newwin(40, 40, 0, 0)

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

    player = Player()
    dungeon = Dungeon()
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
        "input": [26, 1, f"{player.name}, enter 'd' to descend, or 'x' to exit.", curses.COLOR_WHITE]
    }

    icons = {
        "health": [4, 2, ' '.join([str(i) for i in dungeon.deck.health_cards[-1::-1]])],
        "torches": [4, 30, ' '.join([str(i) for i in player.torches[:]])],
        "scrolls": [7, 30, ' '.join([str(i) for i in player.loot.scrolls[:]])],
        "treasure": [10, 30, ' '.join([str(i) for i in player.loot.treasure[:]])],
        "hoards": [13, 30, ' '.join([str(i) for i in player.loot.hoards[:]])]
    }
    key_press = stdscr.getch()
    key_press = 100

    while player.health > 0:

        display_messages(player, dungeon, messages, icons, stdscr)
        # printing ideas:
        # stdscr.addstr(22, 10, f"Hello There {chr(int('0001F0B3', base=16))} ", WHITE_BLACK | curses.A_BOLD)
        # stdscr.addstr(30, 1, str(key_press))

        if key_press == 263 or key_press == 27: # Backspace or esc
            quit()
        #
        if key_press == 100 or key_press == 68:   # 'd' or 'D' keypress
            messages["dungeon"] = [25, 2, f"You {player.direction} the dungeon!", curses.COLOR_WHITE]
            dungeon.rooms.append(Room(dungeon, player))
            dungeon.rooms[-1].set_up_room()
            messages['input'] = [26, 1, f"{dungeon.rooms[-1].description}", curses.COLOR_WHITE]


        # X OR x == 88 OR 120
        key_press = stdscr.getch()

if __name__ == "__main__":
    wrapper(main_loop)
