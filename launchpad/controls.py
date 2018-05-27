from collections import OrderedDict

from buttons import ButtonGroup
from colors import Color


class Control(object):
    def __init__(self, lp, *buttons):
        self.lp = lp
        self.buttons = buttons

    def dispatch(self, type_, button, value):
        for check_type, check_button in self.buttons:
            if type_ == check_type and button == check_button:
                self._dispatch(type_, button, value)

    def render(self):
        pass

    def _dispatch(self, type_, button, value):
        raise NotImplementedError()

    def set_color(self, type_, button, color):
        if type_ == 'GRID':
            self.lp.set_color(button[0], button[1], color.color, intensity=color.intensity)
        else:
            self.lp.set_color(type_, button, color.color, intensity=color.intensity)


class Momentary(Control):
    def __init__(self, lp, on_color, off_color, callback, *buttons):
        super(Momentary, self).__init__(lp, *buttons)
        self.on_color = on_color
        self.off_color = off_color
        self.callback = callback

    def render(self):
        for type_, button in self.buttons:
            self.set_color(type_, button, self.off_color)

    def _dispatch(self, type_, button, value):
        if value:
            self.set_color(type_, button, self.on_color)
        else:
            self.set_color(type_, button, self.off_color)
        self.callback(type_, button, value)


class Toggle(Control):
    def __init__(self, lp, states, colors, callback, *buttons):
        super(Toggle, self).__init__(lp, *buttons)
        self.states = states
        self.colors = colors
        self.callback = callback
        self.button_states = {b: 0 for b in self.buttons}

    def render(self):
        for type_, button in self.buttons:
            self.set_color(type_, button, self.colors[self.button_states[(type_, button)]])

    def _dispatch(self, type_, button, value):
        if value:
            self.button_states[(type_, button)] += 1
            if self.button_states[(type_, button)] + 1 > self.states:
                self.button_states[(type_, button)] = 0
            self.set_color(type_, button, self.colors[self.button_states[(type_, button)]])
            self.callback(type_, button, self.button_states[(type_, button)])


class Slider(Control):
    O_HZ = 1
    O_VT = 2

    def __init__(self, lp, position, orientation, off_color, on_colors, callback):
        self.position = position
        self.orientation = orientation
        self.off_color = off_color
        self.on_colors = on_colors
        self.callback = callback

        if isinstance(self.on_colors, Color):
            self.on_colors = OrderedDict([(i, self.on_colors) for i in range(8)])
        elif isinstance(self.on_colors, list):
            self.on_colors = OrderedDict([(i, self.on_colors[int(i / len(self.on_colors))]) for i in range(8)])
        else:
            self.on_colors = OrderedDict(self.on_colors.items())

        if self.orientation == self.O_HZ:
            buttons = ButtonGroup(0, self.position, 7, self.position)
        elif self.orientation == self.O_VT:
            buttons = ButtonGroup(self.position, 0, self.position, 7)

        self.value = 0

        super(Slider, self).__init__(lp, *buttons)

    def render(self):
        if self.orientation == self.O_HZ:
            on = 0, self.value + 1
            off = self.value + 1, 8
        else:
            on = 7 - self.value, 8
            off = 0, 7 - self.value

        for i in range(*on):
            if self.orientation == self.O_VT:
                color_i = 7 - i
            else:
                color_i = i
            self.set_color(self.buttons[i][0], self.buttons[i][1], self.on_colors[color_i])
        for i in range(*off):
            self.set_color(self.buttons[i][0], self.buttons[i][1], self.off_color)

    def _dispatch(self, type_, button, value):
        if value:
            if self.orientation == self.O_HZ:
                self.value = button[0]
            else:
                self.value = 7 - button[1]

            self.render()
            self.callback(type_, button, self.value)