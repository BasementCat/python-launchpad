class BaseColor(object):
    def __init__(self, offset, count=4, invert=True, no_first=False):
        self.intensities = range(offset, offset + count)
        if invert:
            self.intensities = list(reversed(self.intensities))
        if not no_first:
            self.intensities[0], self.intensities[-1] = self.intensities[-1], self.intensities[0]

    @property
    def on(self):
        return self.intensities[-1]

    def intensity(self, value):
        if value < 1 or value > 4:
            raise ValueError()

        return self.intensities[max(1, int(value * (len(self.intensities) / 4))) - 1]


class Colors(object):
    OFF = BaseColor(0, count=1)
    WHITE = BaseColor(1, count=3, invert=False)
    RED = BaseColor(4)
    ORANGE = BaseColor(8)
    YELLOW = BaseColor(12)
    FOREST = BaseColor(16)
    GREEN = BaseColor(20)
    LIME = BaseColor(24)
    CYAN1 = BaseColor(28)
    CYAN2 = BaseColor(32)
    LTBLUE = BaseColor(36)
    MDBLUE = BaseColor(40)
    BLUE = BaseColor(44)
    PURPLE = BaseColor(48)
    LTPINK = BaseColor(52)
    PINK = BaseColor(56)


class Color(object):
    def __init__(self, color, intensity=None):
        self.color = color
        self.intensity = intensity
