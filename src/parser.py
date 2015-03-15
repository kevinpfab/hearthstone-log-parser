
import json

from handler import create_handlers
from model import CardDatabase, Match

CREATE_GAME = 'CREATE_GAME'

class HearthstoneLogParser:

    def  __init__(self, file_path, card_json):
        self.matches = []

        self._file_path = file_path
        self._events = []

        self._card_database = CardDatabase(card_json)
        self._handlers = []


    def _create_match(self):
        self.current_match = Match()
        self.matches.append(self.current_match)

        # Reset the handlers to have new match
        self._handlers = create_handlers(self.current_match, self._card_database)

    def parse(self):
        lines = [line.strip('\n') for line in open(self._file_path)]

        for line in lines:
            if CREATE_GAME in line:
                self._create_match() # Creating a game is the only handler outside of a match
                continue

            for handler in self._handlers:
                if handler.handle(line):
                    break


        # Display Fun Stuff
        aa = 0
        for match in self.matches:
            aa = aa + 1
            print("--------\nSTART MATCH %d\n---------" % aa)

            i = 0
            total_turn_time = {
                match.get_player(1).name: 0,
                match.get_player(2).name: 0,
            }
            for turn in match.turns:
                print("Start Turn %d" % i)
                print("Current Player: %s" % turn.player.name)
                if i < len(match.turns) - 1:
                    turn_time = match.turns[i+1].start - turn.start
                    print("Turn took %d seconds" % turn_time)
                    print("Spent %d mana" % turn.total_mana_used)
                    print("%s mana efficiency" % str(turn.total_mana_used/turn.mana_available))

                    if i > 1:
                        total_turn_time[turn.player.name] = total_turn_time[turn.player.name] + turn_time
                else:
                    print("Game End")

                for card in turn.cards_played:
                    print("Played %s" % card.name)

                i = i + 1

            print("\n\n")

            for player_name, turn_time in total_turn_time.items():
                print("%s: %d" % (player_name, turn_time))

if __name__ == '__main__':

    card_json = json.loads(open('data/cards.json').read())
    #parser = HearthstoneLogParser("logs/2minions1turn.txt", card_json)
    parser = HearthstoneLogParser("logs/game2.txt", card_json)

    parser.parse()
