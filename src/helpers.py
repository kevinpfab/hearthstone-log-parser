
class Helpers(object):

    # {{{ get_dict_from_string
    @staticmethod
    def get_dict_from_string(s):
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
                    d[current_key] = Helpers.get_dict_from_string(inside_braces)
                else:
                    d[current_key] = ""
                current_key = None

                i = i + k
            else:
                current_word = current_word + c

            i = i + 1

            if i >= len(s):
                d[current_key] = (' '.join(previous_words + [current_word]))
                resolved = True

        return d
    # }}}
