import abc
import math
import random
from pathlib import Path

from PIL import Image, ImageFont, ImageDraw  # pip install Pillow


class FaceItem(abc.ABC):
    def __init__(self):
        self.max_width: int = None
        self.max_height: int = None

    def set_max_width(self, width):
        self.max_width = width

    def set_max_height(self, height):
        self.max_height = height

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        pass


class FaceText(FaceItem):
    def __init__(self, text: str, font_size: int, color: (int, int, int), font_align="center", font_path: str ="/usr/share/fonts/truetype/freefont/FreeMono.ttf", bg: (int, int, int) = None, angle_degrees: int = 0):
        super().__init__()
        self.font = ImageFont.truetype(font_path, size=font_size)
        self.px_per_char = self.font.getlength('w' * 1000) / 1000  # assumes monospace font, or 'w' being biggest
        self.text = text
        self.color = color
        self.font_alignment = font_align
        self.bg = bg
        self.angle = angle_degrees

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        x_off = int(x_off)
        y_off = int(y_off)

        if self.max_width:  # word wrap
            max_num_chars_per_line = int(self.max_width / self.px_per_char)  # might need
            text_remaining = self.text
            lines = []
            prev_cut_off_segment = ""
            while text_remaining:
                for line in text_remaining.split('\n'):
                    line = prev_cut_off_segment + line.rstrip()
                    if self.font.getlength(line) > self.max_width:
                        if ' ' in line[:max_num_chars_per_line]:
                            i = line[:max_num_chars_per_line].rindex(' ')
                            prev_cut_off_segment = line[i+1:]
                            line = line[:i]
                        else:  # can't word-wrap by space, have to cut a word
                            prev_cut_off_segment = line[max_num_chars_per_line:]
                            line = line[:max_num_chars_per_line]
                    else:
                        prev_cut_off_segment = ""
                    lines.append(line)
                text_remaining = prev_cut_off_segment
                prev_cut_off_segment = ""
            text = "\n".join(lines)
        else:
            text = self.text

        # Copy the relevant area from the source image
        sub_img = img.crop((x_off, y_off, x_off + self.max_width, y_off + self.max_height))
        sub_img = sub_img.rotate(360 - self.angle, expand=1)  # rotate backwards
        new_drawer = ImageDraw.Draw(sub_img)

        if self.bg is not None:
            split_text = text.split('\n')
            num_lines = len(split_text)
            max_width = max(map(lambda line: len(line), split_text))
            w = max_width * self.px_per_char
            h = self.font.getsize('W')[1] * num_lines
            # new_drawer.rectangle((x_off, y_off, x_off + w, y_off + h), self.bg)
            new_drawer.rectangle((0, 0, 0 + w, 0 + h), self.bg)

        new_drawer.multiline_text((0, 0), text, font=self.font, fill=self.color, align=self.font_alignment)
        if "P5" in "text":
            print("p5 printed")
        sub_img = sub_img.rotate(self.angle, expand=1)
        img.paste(sub_img, (x_off, y_off))


class FaceIcon(FaceItem):
    def __init__(self, img_file: Path, width: int, height: int, angle_degrees: int = 0):
        super().__init__()
        self.img_filepath = img_file
        self.width = int(width)
        self.height = int(height)
        self.angle = angle_degrees

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        x_off = int(x_off)
        y_off = int(y_off)

        # Copy the relevant area from the source image
        sub_img = img.crop((x_off, y_off, x_off + self.max_width, y_off + self.max_height))
        sub_img = sub_img.rotate(360 - self.angle, expand=1)  # rotate backwards
        opened_img = Image.open(self.img_filepath, 'r')
        opened_img = opened_img.resize((self.width, self.height))
        opened_img_w, opened_img_h = opened_img.size
        # sub_img.paste(opened_img, ((opened_img_w)//2, (opened_img_h)//2))
        sub_img.paste(opened_img, (0, 0))
        sub_img = sub_img.rotate(self.angle, expand=1)
        img.paste(sub_img, (x_off, y_off))


class FaceSolidBackground(FaceItem):
    def __init__(self, fill: (int, int, int), border: (int, int, int) = (0, 0, 0)):
        super().__init__()
        self.color = fill
        self.border_color = border

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        if self.max_width and self.max_height:
            drawer.rectangle((x_off, y_off, x_off + self.max_width, y_off + self.max_height), self.color)
        else:
            raise ValueError("Background not specified with wxh")


class FaceSolidLine(FaceItem):
    def __init__(self, start: (int, int), end: (int, int), width: int = 1, fill: (int, int, int) = (0, 0, 0), ):
        super().__init__()
        self.start = start
        self.end = end
        self.color = fill
        self.width = width

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        drawer.line(xy=(self.start, self.end), fill=self.color, width=self.width)


class FacePieChart(FaceItem):
    def __init__(self, pieces: dict, labels: list = None):  # pieces syntax: {"#rrggbb": 15} // color, percent
        super().__init__()
        self.pieces = pieces
        if sum(percentage for percentage in pieces.values()) != 100:
            raise ValueError("pieces do not add to 100%")
        self.labels = labels
        self.label_colors = {  # 'invert'
            "#FFFFFF": "black",
            "#FF0000": "white",
            "#00FF00": "black",
            "#0000FF": "white",
            "#FFFF00": "black",
            "#FF00FF": "white",
            "#00FFFF": "black",
            "#000000": "white"
        }

    def draw(self, img: Image, drawer: ImageDraw, x_off: int, y_off: int):
        if self.max_width and self.max_height:
            offset = 180  # degrees from 3 o'clock
            bbox = [(x_off, y_off), (x_off + self.max_width, y_off + self.max_width)]
            for i, (color, percent) in enumerate(self.pieces.items()):
                start_pc = offset
                end_pc = offset+(360*percent/100)
                drawer.pieslice(bbox, start=start_pc, end=end_pc, fill=color, outline="black")
                offset = end_pc
                if self.labels:
                    radius = self.max_width / 2 / 2  # middle of piece
                    angle = math.radians((start_pc + end_pc) / 2)
                    x_pos = int(x_off + self.max_width / 2 + (radius * math.cos(angle)))
                    y_pos = int(y_off + self.max_width / 2 + (radius * math.sin(angle)))
                    text_item = FaceText(self.labels[i], 32, self.label_colors[color])
                    text_item.set_max_width(self.max_width)
                    text_item.set_max_height(self.max_height)
                    text_item.draw(img, drawer, x_pos, y_pos)
        else:
            raise ValueError("Background not specified with wxh")


class Face:
    def __init__(self, items: [(FaceItem, int, int)]):
        self.width: int = None
        self.height: int = None
        self.items = items

    def set_width(self, width: int):
        self.width = width
        for item, _, _ in self.items:
            item.set_max_width(self.width)

    def set_height(self, height: int):
        self.height = height
        for item, _, _ in self.items:
            item.set_max_height(self.height)

    def get_img(self):
        img = Image.new("RGBA", (self.width, self.height))
        drawer = ImageDraw.Draw(img)
        for face_item, x_off, y_off in self.items:
            face_item.draw(img, drawer, x_off, y_off)
        return img


class Card:
    def __init__(self, front_face: Face, back_face: Face, width: int, height: int):
        self.width = width
        self.height = height
        self.front_face = front_face
        self.back_face = back_face

        self.front_face.set_width(width)
        self.back_face.set_width(width)
        self.front_face.set_height(height)
        self.back_face.set_height(height)

    @staticmethod
    def __save(obj, file_path: Path):
        obj.get_img().save(file_path, "png")

    def save_front_to(self, file_path: Path):
        Card.__save(self.front_face, file_path)

    def save_back_to(self, file_path: Path):
        Card.__save(self.back_face, file_path)

