# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from models import *
import curses
from curses import wrapper


# stdscr is the main curses terminal window -- render all headings on this window
# stats_win_descriptor will be the windows to display user stats

def display_messages(player: Player, dungeon: Dungeon, messages: dict, icons: dict, stdscr):
    for key, value in messages.items():
        stdscr.addstr(value[0], value[1], value[2])
    for key, value in icons.items():
        stdscr.addstr(value[0], value[1], value[2])

def main_loop(stdscr):
    stdscr.clear()
    stdscr.refresh()

    #player_win = curses.newwin(40, 40, 0, 0)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)  # red (1) on white (7)
    RED_WHITE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_WHITE = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_BLACK = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_BLACK = curses.color_pair(4)

    player = Player()
    dungeon = Dungeon()
    messages = {
        "title": [1, 2, f"{player.name}, you are on {dungeon.player_depth(player)[0] - dungeon.player_depth(player)[1]} of the Dungeon"],
        "health": [3, 2, f"Health Points: {player.health}"],
        "torches": [3, 30, f"Torches remaining: {4- len(player.torches)}"],
        "scrolls": [7, 30, f"Scrolls found: {len(player.loot.scrolls)}"],
        "treasure": [10, 30, "Treasure found: "],
        "hoards": [13, 30, "Hoards found:"],
        "dungeon": [25, 2, "You are at the entrance to a deep, dark cave!"],
        "input": [26, 1, f"{player.name}, enter 'd' to descend, or 'x' to exit."]
    }

    icons = {
        "health": [4, 2, ' '.join([str(i) for i in dungeon.deck.health_cards[-1::-1]])],
        "torches": [4, 30, f"{' '.join(player.torches)}"],
        "scrolls": [8, 30, f"{' '.join(player.loot.scrolls)}"],
        "treasure": [11, 30, f"{' '.join(player.loot.treasure)}"],
        "hoards": [13, 30, f"{' '.join(player.loot.hoards)}"]
    }

    stdscr.clear()
    # player_win.clear()
    stdscr.refresh()
    # player_win.refresh()

    display_messages(player, dungeon, messages, icons, stdscr)
    # for key, value in messages.items():
    #     stdscr.addstr(value[0], value[1], value[2])

    # stdscr.addstr(10, 20, "Hello There")
    # stdscr.addstr(20, 10, f"Hello There {chr(int('0001F0B1', base=16))} ", RED_BLACK | curses.A_BOLD)
    # # player_win.addstr(21, 10, f"Hello There {chr(int('0001F0B2', base=16))} ", RED_WHITE | curses.A_BOLD)
    # stdscr.addstr(22, 10, f"Hello There {chr(int('0001F0B3', base=16))} ", WHITE_BLACK | curses.A_BOLD)
    # # player_win.addstr(23, 10, f"Hello There {chr(int('0001F0B4', base=16))} ", curses.A_REVERSE)
    stdscr.refresh()
    #layer_win.refresh()
    stdscr.getch()


if __name__ == "__main__":
    wrapper(main_loop)
