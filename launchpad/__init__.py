import fnmatch

import mido

from buttons import (
    TOP_BUTTONS,
    RIGHT_BUTTONS,
    TOP_BUTTONS_INV,
    RIGHT_BUTTONS_INV,
    get_button,
    coord_to_note,
)
from colors import Colors


class Page(object):
    def __init__(self, lp, include_top, include_right, *controls):
        self.lp = lp
        self.include_top = include_top
        self.include_right = include_right
        self.controls = controls

    def render(self):
        self.lp.reset(reset_top=self.include_top, reset_right=self.include_right)
        for control in self.controls:
            control.render()

    def dispatch(self, type_, button, value):
        for control in self.controls:
            control.dispatch(type_, button, value)


class Launchpad(object):
    @classmethod
    def list_devices(self):
        inputs = set(mido.get_input_names())
        outputs = inputs & set(mido.get_output_names())
        return [d for d in outputs if fnmatch.fnmatch(d, '*Launchpad*')]

    def __init__(self, device=None, page=None):
        device = device or self.list_devices()[0]
        self.inp = mido.open_input(device)
        self.outp = mido.open_output(device)
        self.pages = []
        self.reset()

    def reset(self, reset_top=True, reset_right=True):
        if reset_top:
            for y in TOP_BUTTONS.values():
                self.set_color('TOP', y, Colors.OFF)
        if reset_right:
            for y in RIGHT_BUTTONS.values():
                self.set_color('RIGHT', y, Colors.OFF)
        for x in range(8):
            for y in range(8):
                self.set_color(x, y, Colors.OFF)

    def set_color(self, x, y, color, intensity=None):
        if intensity == None:
            color = color.on
        else:
            color = color.intensity(intensity)
        if x == 'TOP':
            button = TOP_BUTTONS_INV[y]
            self.outp.send(mido.Message('control_change', channel=0, control=button, value=color))
        elif x == 'RIGHT':
            button = RIGHT_BUTTONS_INV[y]
            self.outp.send(mido.Message('note_on', channel=0, note=button, velocity=color))
        else:
            self.outp.send(mido.Message('note_on', channel=0, note=coord_to_note(x, y), velocity=color))

    def poll(self):
        for message in self.inp.iter_pending():
            type_, button, value = get_button(message)
            for page in reversed(self.pages):
                if type_ == 'TOP' and page.include_top:
                    page.dispatch(type_, button, value)
                    break
                elif type_ == 'RIGHT' and page.include_right:
                    page.dispatch(type_, button, value)
                    break
                else:
                    page.dispatch(type_, button, value)
                    break

    def push_page(self, page):
        self.pages.append(page)
        self.pages[-1].render()

    def pop_page(self):
        self.pages.pop()
        if self.pages:
            self.pages[-1].render()
        else:
            self.reset()
