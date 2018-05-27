from collections import OrderedDict


TOP_BUTTONS = OrderedDict([
    (104, 'UP'),
    (105, 'DOWN'),
    (106, 'LEFT'),
    (107, 'RIGHT'),
    (108, 'SESSION'),
    (109, 'USER1'),
    (110, 'USER2'),
    (111, 'MIXER'),
])
RIGHT_BUTTONS = OrderedDict([
    (89, 'VOLUME'),
    (79, 'PAN'),
    (69, 'SENDA'),
    (59, 'SENDB'),
    (49, 'STOP'),
    (39, 'MUTE'),
    (29, 'SOLO'),
    (19, 'RECORDARM'),
])
TOP_BUTTONS_INV = OrderedDict(zip(TOP_BUTTONS.values(), TOP_BUTTONS.keys()))
RIGHT_BUTTONS_INV = OrderedDict(zip(RIGHT_BUTTONS.values(), RIGHT_BUTTONS.keys()))


def coord_to_note(x, y):
    return (((7 - y) * 10) + x) + 11


def note_to_coord(note):
    x = (note - 11) % 10
    y = 7 - ((note - 11) / 10)
    return x, y


def get_button(message):
    if message.type == 'control_change':
        return 'TOP', TOP_BUTTONS.get(message.control), message.value > 0
    elif message.type in ('note_on', 'note_off'):
        button = RIGHT_BUTTONS.get(message.note)
        if button:
            return 'RIGHT', button, message.velocity > 0

        return 'GRID', note_to_coord(message.note), message.velocity > 0

    return None, None, None


class ButtonGroup(list):
    def __init__(self, x1=None, y1=None, x2=None, y2=None):
        super(ButtonGroup, self).__init__()
        if x1 in ('TOP', 'RIGHT'):
            fromlist = globals()[x1 + '_BUTTONS'].values()
            if y1 is None:
                self += [(x1, v) for v in fromlist]
            else:
                try:
                    y1 = int(y1)
                    self.append((x1, fromlist[y1]))
                except (ValueError, TypeError):
                    self.append((x1, y1))

        else:
            if x1 is None: x1 = 0
            if y1 is None: y1 = 0
            if x2 is None: x2 = 7
            if y2 is None: y2 = 7
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    self.append(('GRID', (x, y)))
