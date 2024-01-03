
def linear(t: float):
    return t


def ease_in_out_quad(x: float):
    if x < 0.5:
        return 2 * x * x
    else:
        return 1 - (-2 * x + 2) ** 2 / 2


def ease_in_out_back(x: float):
    c1 = 1.70158
    c2 = c1 * 1.525

    if x < 0.5:
        return (((2 * x) ** 2) * ((c2 + 1) * 2 * x - c2)) / 2
    else:
        return (((2 * x - 2) ** 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2


def ease_in_back(x: float):
    c1 = 1.70158
    c3 = c1 + 2
    return c3 * x * x * x - c1 * x * x
