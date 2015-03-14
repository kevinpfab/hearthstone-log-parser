
from helpers import Helpers

class BaseHandler(object):

    def __init__(self, match, database):
        self._match = match
        self._database = database

        self.base_tag = None
        self.method = self._method()
        self.tags = self._tags()

    # Handlers can stop execution of later handlers by returning True in their _execute overrides
    def handle(self, line):
        handled = False
        if self._can_handle(line):
            data = self._parse(line)
            try:
                handled = self._execute(data['method'], data['data'])
            except Exception as e:
                print(self.__class__.__name__)
                print(line)
                raise e

        return handled

    def _can_handle(self, s):
        if self.method:
            starts = "%s %s" % (self.base_tag, self.method)
        else:
            starts = self.base_tag

        if not s.startswith(starts):
            return False

        return self._check_tags(s)

    def _check_tags(self, s):
        valid = True
        for tag in self.tags:
            if not tag in s:
                valid = False
                break

        return valid

    def _parse(self, s):
        d = {}

        base_tag_len = len(self.base_tag) + 2
        no_base_tag = s[base_tag_len:]

        parts = no_base_tag.split('-', 1)

        d['method'] = parts[0].strip()
        d['data'] = Helpers.get_dict_from_string(parts[1].strip())

        return d

    def _method(self):
        return None

    def _tags(self):
        return []

    def _execute(self, s):
        pass
