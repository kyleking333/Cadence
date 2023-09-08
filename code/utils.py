class Color:
    colors_english = [
        "black",
        "red",
        "green",
        "blue",
        "yellow",
        "magenta",
        "cyan",
        "white"
    ]
    colors_hex = [
        "#000000",
        "#FF0000",
        "#00FF00",
        "#0000FF",
        "#FFFF00",
        "#FF00FF",
        "#00FFFF",
        "#FFFFFF",
    ]
    colors_tuple = [
        (0, 0, 0),
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (255, 255, 255),
    ]

    fgs = [
        "white",  # "black",
        "white",
        "black",
        "white",
        "black",
        "white",
        "black",
        "black",  # "white"
    ]

    @staticmethod
    def __hex_to_index(hex_str: str):
        return Color.colors_hex.index(hex_str)

    @staticmethod
    def __tup_to_index(tup: (int, int, int)):
        return Color.colors_tuple.index(tup)

    @staticmethod
    def __english_to_index(english: str):
        return Color.colors_english.index(english)

    @staticmethod
    def __to_index(val):
        if isinstance(val, str):
            if val[0] == "#":
                return Color.__hex_to_index(val)
            else:
                return Color.__english_to_index(val)
        else:
            return Color.__tup_to_index(val)

    @staticmethod
    def as_tuple(val):
        return Color.colors_tuple[Color.__to_index(val)]

    @staticmethod
    def as_english(val):
        return Color.colors_english[Color.__to_index(val)]

    @staticmethod
    def as_hex(val):
        return Color.colors_hex[Color.__to_index(val)]

    @staticmethod
    def choose_fg_for_bg(val):
        return Color.fgs[Color.__to_index(val)]
