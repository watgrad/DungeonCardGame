from enum import Enum
import random


# enumerate the Suits class to support program logic
class Suits(Enum):
    CLUB = 0
    SPADE = 1
    HEART = 2
    DIAMOND = 3


# card properties include the suit from Suits class, numeric value, face (val+Suit name), image location
class Card:
    suit: Suits = None
    value: int = None
    face: str = None
    uni_code: str = None  # stores unicode glyph

    def __init__(self, suit, value, face):
        code_suit = {Suits.CLUB: 'D', Suits.SPADE: 'A', Suits.HEART: 'B', Suits.DIAMOND: 'C'}
        code_value = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5",
                      6: "6", 7: "7", 8: "8", 9: "9", 10: "A", 11: "B", 12: "D", 13: "E"}
        self.suit = suit
        self.value = value
        self.face = face
        self.uni_code = chr(int("0001F0" + code_suit[self.suit] + code_value[self.value], base=16))

    def __str__(self):
        return self.uni_code


# construction of the deck starts as a collection of cards in a list cards[]
# the deck is broken further into health_cards[]  that are all hearts value 2-10
# and the remaining dungeon_cards[] used for game play
class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suits:
            for value in range(1, 14):
                face = str(value) + suit.name
                self.cards.append(Card(suit, value, face))

        self.health_cards = []
        self.dungeon_cards = []

        # prepare the health_cards and dungeon_card sets
        for card in self.cards:
            if card.suit == Suits.HEART and 1 < card.value <= 10:
                self.health_cards.append(card)
            else:
                self.dungeon_cards.append(card)

        # randomize dungeon_cards, order health cards
        random.shuffle(self.dungeon_cards)
        self.health_cards = self.health_cards[::-1]

    # create a deal method for dungeon_cards to use in game play
    def deal(self):
        if self.length() > 0:
            return self.dungeon_cards.pop(0)
        elif self.length() <= 0:
            print("You've run out of cards!")
            print("You died of starvation in the dungeon!!  :(")
            quit()

    # create a method to determine how many cards are left
    def length(self):
        return len(self.dungeon_cards)


# Hand class us used to manage rooms within the dungeon
class Hand:
    def __init__(self, kind: str):
        self.cards = []
        self.kind = kind

    def add(self, card: Card):
        self.cards.append(card)

    def get(self, ind: int):
        return self.cards.pop(ind)

    def show(self):
        # list the cards in the hand for display
        return self.cards[-1]


# the Treasures class is used to gather the player's loot from each dungeon room
# treasues in hoards, and skills separated from other diamonds
class Treasures:
    def __init__(self) -> None:
        self.hoards = []
        self.treasure = []
        self.scrolls = []

    # check to see if the player has a certain skill in their hand
    def scrolls_contains(self, card: Card):
        if card in self.scrolls:
            return True

        return False


class Player:
    scroll_effects: dict = {"11CLUB": "Open All Doors", "11SPADE": "Incinerate", "11DIAMOND": "Disarm All Traps",
                            "11HEART": "Heal"}

    def __init__(self):
        self.health: int = 10
        self.name: str = "Explorer"
        self.loot: Treasures = Treasures()
        self.living: bool = True  # maybe not needed?
        self.death: str = ""  # Cause of death if not False, the string should contain the cause of death
        self.torches: list = []  # collection of used torches (ace cards as used)
        self.direction: str = "decend into"  # players direction in the game alternate is "ascend from"

    def check_torches(self):  # check to see if all torches are used
        return len(self.torches)

    def calculate_treasure(self):  # script to calculate treasure value
        total: int = 0
        for i in self.loot.treasure:
            total += i.value
        total += len(self.loot.hoards) * 10
        total += len(self.loot.scrolls) * 10

        return total

    def list_scrolls(self):  # method to list all the player's current stats
        scrolls = []
        for card in self.loot.scrolls:
            scrolls += f"{card} "
        return f"You found the scrolls {scrolls}"

    def list_treasure(self):
        hoards = 0
        treasure = 0
        for card in self.loot.hoards:
            hoards += card.value
        for card in self.loot.treasure:
            treasure += card.value

        return f"You've found {treasure} in gold and {len(self.loot.hoards)} King's hoards worth {hoards} in gold so far!"


class Dungeon:
    def __init__(self):
        self.rooms: list = []  # a list of the rooms visited - as Room objects
        self.deck = Deck()  # the deck of cards for gameplay

    # determine the depth the player has gotten to
    def player_depth(self, player: Player) -> tuple:
        down: int = 0
        up: int = 0
        if self.rooms:
            for room in self.rooms:
                if room.direction == "decend into":
                    down += 1
                    # if down == 8:   # there must be a limit on how deep a player can go
                    #     player.direction = "ascend from"
                    #     print("You've reached the bottom of the dungeon, you must turn around!")
                if room.direction == "ascend from":
                    up += 1
            return down, up
        else:
            return 0, 0


class Room:
    def __init__(self, dungeon: Dungeon, player: Player):
        self.room_contents: list = [] # list of played cards from dungeon deck
        self.devine_intervention: bool = False # if Q is present in room
        self.event: Card = None # What monster, barrier or trap was uncovered in deck
        self.description: str = ""
        self.name: str = ""
        self.direction: str = ""
        self.dungeon = dungeon # where played cards come from
        self.player = player # results impact the player

    def set_up_room(self):
        self.direction = self.player.direction
        self.room_contents.append(self.dungeon.deck.deal())  # get the first card for the room

        while self.room_contents[-1].value > 10 or self.room_contents[-1].value == 1:
            # make sure the last card is not a torch, skill, devine blessing, or hoard
            self.room_contents.append(self.dungeon.deck.deal())

        self.event = self.room_contents[-1]  # set reference to 'monster' for as the event to track health and messages

        for card in self.room_contents:  # scan the current  room hand so far for special cards
            if card.value == 1:
                self.player.torches.append(card)
                self.player.check_torches()
                if not self.player.living:
                    print(self.player.death)  # TODO: Handle death -- call an endgame routine?
                    return False
                else:
                    print("You used a torch!")

            if card.value == 12:  # if there is a queen in the hand mark devine_intervention true (player wins round)
                self.devine_intervention = True
                self.event.value = 0  # set event health to 0 to mark pass of round

        self.description = self.event_message(self.event)[1]
        self.name = self.event_message(self.event)[0]

    def draw_card(self):
        # TODO: when you draw a card, return a standard tuple with consistent values:
        # devine blessing, torches used, damage done, remaining events health  -- this may be impacted by the room?
        self.room_contents.append(self.dungeon.deck.deal())

        while self.room_contents[-1].value == 1 or self.room_contents[-1].value > 10:
            self.room_contents.append(self.dungeon.deck.deal())

            if self.room_contents[-1].face == ("12" + self.event.suit.name):  # Calculate this based on the event suit
                self.event.value = 0
                self.devine_intervention = True
                return

        self.event.value -= self.room_contents[-1].value
        # print(f"you did {self.room_contents[-1].value} damage!!!")
        # TODO: rather than do this here, just return and let the calling function send messages
        return

    def process_room(self, player: Player):
        message = ""
        for card in self.room_contents:
            if card.value == 13:
                player.loot.hoards.append(card)
                message += f"You found one of the King's Hoards! {card.face}\n"
            if card.suit == Suits.DIAMOND and (11 > card.value > 1):
                player.loot.treasure.append(card)
                message += f"You found a treasure {card.face}\n"
            if card.value == 11:
                player.loot.scrolls.append(card)
                message += f"You found the scroll {player.loot.scrolls[card.face]}!\n"
        return message

    def event_message(self, card: Card):
        # This function looks up appropriate messages for the different dungeon events.
        diamond_events = {
            "1DIAMOND": ["torch", "Your torch burned out!!"],
            "2DIAMOND": ["trip wire", "There is a simple trap on the floor..."],
            "3DIAMOND": ["wooden door", "There is a simple trap on the door..."],
            "4DIAMOND": ["wooden door", "There is a simple trap on the door..."],
            "5DIAMOND": ["wooden door", "This door seems suspicious, is there a trap?"],
            "6DIAMOND": ["dead fall", "A dead fall blocks the passage."],
            "7DIAMOND": ["wooden chest", "The chest has a complex lock."],
            "8DIAMOND": ["wooden chest", "The chest has a complex lock."],
            "9DIAMOND": ["golden chest", "You see an ornate chest on a dais in the middle of the room"],
            "10DIAMOND": ["alter", "There is an alter at the front of the room!"],
            "11DIAMOND": ["Disarm Traps scroll", "You used the 'Disarm Traps' scroll!"],
            "12DIAMOND": ["Blessing", "The goddess has granted you a divine favour!!!"],
            "13DIAMOND": ["HOARD of treasure", "You've found one of the King's hoards!!! So much treasure!!!"]
        }

        club_events = {
            "1DIAMOND": ["torch", "Your torch burned out!!"],
            "2CLUB": ["jambed door", "The door is stuck!"],
            "3CLUB": ["jambed door", "The door is stuck!"],
            "4CLUB": ["blocked door", "The pile of debris is blocking the door..."],
            "5CLUB": ["blocked door", "The pile of debris is blocking the door..."],
            "6CLUB": ["blocked door", "The pile of debris is blocking the door..."],
            "7CLUB": ["barred door", "The door is blocked from the inside! Try kicking it!"],
            "8CLUB": ["barred door", "The door is blocked from the inside! Try kicking it!"],
            "9CLUB": ["barred door", "The door is blocked from the inside! Try kicking it!"],
            "10CLUB": ["locked door", "The door is locked, can you break it open?"],
            "11DIAMOND": ["Open All Doors scroll", "You used the 'Open All Doors' scroll!"],
            "12DIAMOND": ["Blessing", "The goddess has granted you a divine favour!!!"],
            "13DIAMOND": ["HOARD of treasure", "You've found one of the King's hoards!!! So much treasure!!!"]
        }

        spade_events = {
            "1DIAMOND": ["torch", "Your torch burned out!!"],
            "2SPADE": ["darkmantle",
                       "A Darkmantle falls from the cavern roof, its thin, hook-lined tentacles grasp at you!"],
            "3SPADE": ["gelantinous cube",
                       "A Gelatinous Cube inches toward you, a partially digested skeleton seems to dance and quiver inside..."],
            "4SPADE": ["violet fungus",
                       "Violet Fungus confronts you, a bed of roots writhes on the ground and tentacles slither out of fissures in its pointed cap!"],
            "5SPADE": ["seru",
                       "You hear the sound of flapping wings! An angry hiss accompanies the appearance of a flying snake-like Seru!"],
            "6SPADE": ["shadow rat swarm",
                       "A Shadow Rat Swarm attacks! The squirming and squeaky mass of rats with rotting flesh, torn and matted fur, and reddish blazing eyes moves toward you!"],
            "7SPADE": ["orphane",
                       "Out of the mist an Orphne appears - pale skin and dark features frame this starkly beautiful creature, which is surrounded by a palpable aura of death."],
            "8SPADE": ["rat king",
                       "You are attacked by a Rat King! Squeaks and chittering cries rise from this tangle of diseased rats with their tails knotted together."],
            "9SPADE": ["dracolisk",
                       "A Dracolisk turns toward you as you enter the room! This six-legged dragon flaps its massive wings as it lowers its head to glare at you with hideous glowing eyes."],
            "10SPADE": ["lurker",
                        "What looks at first like a stalactite unfurls into a shape like a manta ray and a Lurker sails silently downward with his rasp-like mouth wide."],
            "11DIAMOND": ["instant Kill scroll", "You used the 'INSTANT KILL' scroll!"],
            "12DIAMOND": ["Blessing", "The goddess has granted you a divine favour!!!"],
            "13DIAMOND": ["HOARD of treasure", "You've found one of the King's hoards!!! So much treasure!!!"]
        }

        if card.suit == Suits.DIAMOND:
            return diamond_events.get(card.face)

        if card.suit == Suits.SPADE:
            return spade_events.get(card.face)

        if card.suit == Suits.CLUB:
            return club_events.get(card.face)
#
# player = Player()
# dungeon = Dungeon()
#
# dungeon.rooms.append(Room(dungeon, player))
# dungeon.rooms[-1].set_up_room()
# print()
# a = ""
# for i in dungeon.deck.health_cards[-1::-1]:
#     a += i.uni_code
# print(' '.join([str(i) for i in dungeon.deck.health_cards[-1::-1]]))
# print(a)
