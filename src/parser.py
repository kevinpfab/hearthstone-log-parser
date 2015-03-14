
import json

class Tag:
    PLAYER_ID      = 'PLAYER_ID'
    TURN           = 'TURN'
    TURN_START     = 'TURN_START'
    RESOURCES_USED = 'RESOURCES_USED'
    RESOURCES      = 'RESOURCES'

class HearthstoneLogParser:

    def  __init__(self, file_path, card_database):
        self._file_path = file_path
        self._events = []

        self.match = Match()
        self._card_database = self._generate_card_database(card_database)

    def parse(self):
        lines = [line.strip('\n') for line in open(self._file_path)]

        for line in lines:
            if line.startswith('[Zone]'):
                self._parse_zone(line)
            elif line.startswith('[Power]'):
                self._parse_power(line)

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
                print("Spent %d mana" % turn.total_mana_used)
                print("%s mana efficiency" % str(turn.total_mana_used/turn.mana_available))

                if i > 1:
                    total_turn_time[turn.player.name] = total_turn_time[turn.player.name] + turn_time
            else:
                print("Game End")

            i = i + 1

        print("\n\n")

        for player_name, turn_time in total_turn_time.items():
            print("%s: %d" % (player_name, turn_time))

    def _parse_zone(self, line):
        pass
#        if 'processing' in line:
#            data = line.split('processing', 1)[1].strip()
#            data = self._get_dict_from_string(data)

    def _parse_power(self, line):
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

            elif data['tag'] == Tag.RESOURCES:
                self.match.current_turn.set_mana_available(int(data['value']))
            elif data['tag'] == Tag.RESOURCES_USED:
                self.match.current_turn.total_mana_used = int(data['value'])

    # {{{ _get_dict_from_string
    def _get_dict_from_string(self, s):
        d = {}

        i = 0
        resolved = False
        current_word = ""
        last_word = ""
        previous_words = []
        current_key = None
        current_value = None
        while not resolved:
            c = s[i]

            if c == '=':
                if current_key:
                    value = ' '.join(previous_words)
                    d[current_key] = value

                current_key = current_word
                current_word = ""
                previous_words = []
            elif c == ' ':
                previous_words.append(current_word)
                last_word = current_word
                current_word = ""
            elif c == '[':
                projected_string = s[(i+1):]
                j = 1
                k = 0
                projected_resolved = False
                while not projected_resolved:
                    temp_c = projected_string[k]
                    if temp_c == ']':
                        j = j - 1
                    elif temp_c == '[':
                        j = j + 1

                    k = k + 1
                    if j == 0:
                        projected_resolved = True

                inside_braces = s[(i+1):(i+k)]
                if len(inside_braces) > 0:
                    d[current_key] = self._get_dict_from_string(inside_braces)
                else:
                    d[current_key] = ""
                current_key = None

                i = i + k
            else:
                current_word = current_word + c

            i = i + 1

            if i >= len(s):
                resolved = True

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

        self.mana_available = 0
        self.current_mana = 0
        self.total_mana_used = 0

    def set_mana_available(self, mana):
        self.mana_available = mana
        self.current_mana = mana

if __name__ == '__main__':

    card_database = json.loads(open('data/cards.json').read())
    parser = HearthstoneLogParser("logs/2minions1turn.txt", card_database)

    test = parser._get_dict_from_string("id=1 changes=1 complete=False local=True localTrigger=[powerTask=[] entity=[name=Voidwalker id=29 zone=HAND zonePos=1 cardId=CS2_065 player=1] srcZoneTag=HAND srcPos=1 dstZoneTag=PLAY dstPos=1]")
    print(test)
    # parser.parse()
