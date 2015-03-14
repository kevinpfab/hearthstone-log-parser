
import json

class Tag:
    PLAYER_ID   = 'PLAYER_ID'
    TURN        = 'TURN'
    TURN_START  = 'TURN_START'

class HearthstoneLogParser:

    def  __init__(self, file_path, card_database):
        self._file_path = file_path
        self._events = []

        self.match = Match()
        self._card_database = self._generate_card_database(card_database)

    def parse(self):
        lines = [line.strip('\n') for line in open(self._file_path)]

        for line in lines:
            if line.startswith('[Zone]') or line.startswith('[Power]'):
                self._parse_line(line)

        i = 0
        total_turn_time = {
            self.match.get_player(1).name: 0,
            self.match.get_player(2).name: 0,
        }
        for turn in self.match.turns:
            print("Start Turn %d" % i)
            print("Current Player: %s" % turn.player.name)
            if i < len(self.match.turns) - 1:
                turn_time = self.match.turns[i+1].start - turn.start
                print("Turn took %d seconds" % turn_time)

                if i > 1:
                    total_turn_time[turn.player.name] = total_turn_time[turn.player.name] + turn_time
            else:
                print("Game End")

            i = i + 1

        print("\n\n")

        for player_name, turn_time in total_turn_time.items():
            print("%s: %d" % (player_name, turn_time))


    def _parse_line(self, line):
        # Tag Changes are useful for discovering turns and players
        if 'TAG_CHANGE' in line:
            tag_change = line.split('TAG_CHANGE', 1)[1].strip()
            data = self._get_dict_from_string(tag_change)

            # Create Players - happens at start of game
            if data['tag'] == Tag.PLAYER_ID:
                new_player = Player(data['value'], data['Entity'])
                self.match.set_player(new_player)

            elif data['tag'] == Tag.TURN:
                new_turn = Turn(data['value'])
                self.match.turns.append(new_turn)

            elif data['tag'] == Tag.TURN_START:
                self.match.current_turn.player = self.match.get_player_by_name(data['Entity'])
                self.match.current_turn.start = int(data['value'])

    # {{{ _get_dict_from_string
    def _get_dict_from_string(self, s):
        d = {}

        last_char = s[-1]
        pairs = s.count('=')
        split_on_equals = s.split('=')

        current_key = split_on_equals.pop(0)

        if last_char != '=':
            last_value = split_on_equals.pop()
        else:
            last_value = None

        current_value = None
        for string in split_on_equals:
            items = string.split(' ')
            next_key = items.pop()
            current_value = ' ' .join(items)

            d[current_key] = current_value
            current_key = next_key

        d[current_key] = last_value

        return d

    # }}}



#        card_id = ''
#        if 'cardId=' in line:
#            parts = line.split('cardId=', 1)
#            card_id = parts[1].split(' ', 1)[0]
#
#        card = self._get_card(card_id)
#
#        return card['name'] if card else ""

    def _generate_card_database(self, db):
        card_database = {}

        for set_name, card_array in db.items():
            for card in card_array:
                card['set_name'] = set_name
                card_database[card['id']] = card

        return card_database

    def _get_card(self, card_id):
        return self._card_database.get(card_id)

class Match:

    def __init__(self):
        self._players = {}
        self.turns = []

    def set_player(self, player):
        self._players[player.id] = player

    def get_player(self, player_id):
        return self._players[str(player_id)]

    def get_player_by_name(self, name):
        for player in self._players.values():
            if player.name == name:
                return player

    def get_turn(self, turn_number):
        return self.turns[int(turn_number)]

    @property
    def current_turn(self):
        return self.turns[-1]

class Player:

    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name

class Turn:

    def __init__(self, number, player=None, start=None):
        self.number = number
        self.player = player
        self.start = start

if __name__ == '__main__':

    card_database = json.loads(open('data/cards.json').read())
    parser = HearthstoneLogParser("logs/game2.txt", card_database)

    parser.parse()
