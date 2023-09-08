from utils import *
from Card import *

card_width = 400
card_height = 500
resources_folder = Path(__file__).parent / "resources"


class DesignType:
    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color


class DesignTypes:
    SharedCode = DesignType("Shared Code", "#000000")
    Security = DesignType("Security", "#FF0000")
    Frontend = DesignType("Frontend", "#00FF00")
    Backend = DesignType("Backend", "#0000FF")
    Network = DesignType("Network", "#FFFF00")
    Hardware = DesignType("Hardware", "#FF00FF")
    Firmware = DesignType("Firmware", "#00FFFF")
    App = DesignType("Application-Specific", "#FFFFFF")
    __list = [SharedCode, Security, Frontend, Backend, Network, Hardware, Firmware, App]
    __list_specialized = [Security, Frontend, Backend, Network, Hardware, Firmware]
    __list_unspecialized = [SharedCode, App]
    NumTypes = len(__list)
    NumSpecializedTypes = len(__list_specialized)
    NumUnspecializedTypes = len(__list_unspecialized)

    @staticmethod
    def get():
        return iter(DesignTypes.__list)

    @staticmethod
    def get_specialized():
        return iter(DesignTypes.__list_specialized)

    @staticmethod
    def get_unspecialized():
        return iter(DesignTypes.__list_unspecialized)


class CadenceCard(Card):
    def __init__(self, front_face: Face, back_face: Face):
        super().__init__(front_face, back_face, card_width, card_height)


class ProductPieChart(FacePieChart):
    def __init__(self,
                 shared_code_pc: int = 20,
                 security_pc: int = 10,
                 frontend_pc: int = 10,
                 backend_pc: int = 10,
                 network_pc: int = 10,
                 hardware_pc: int = 10,
                 firmware_pc: int = 10,
                 app_pc: int = 20,
                 labels: list = None,
                 ):
        super().__init__({
            DesignTypes.SharedCode.color: shared_code_pc,
            DesignTypes.Security.color: security_pc,
            DesignTypes.Frontend.color: frontend_pc,
            DesignTypes.Backend.color: backend_pc,
            DesignTypes.Network.color: network_pc,
            DesignTypes.Hardware.color: hardware_pc,
            DesignTypes.Firmware.color: firmware_pc,
            DesignTypes.App.color: app_pc,
        }, labels)


class TextOnlyCard(CadenceCard):
    def __init__(self, back: str, title: str, body: str, back_color=(255, 255, 255)):
        super().__init__(Face([(FaceSolidBackground((255, 255, 255)), 0, 0),
                               (FaceText(title, 32, (0, 0, 0)), 00, 0),
                               (FaceText(body, 20, (0, 0, 0)), 0, 75),
                               ]),
                         Face([(FaceSolidBackground(back_color), 0, 0),
                               (FaceText(back, 50, (0, 0, 0)), 0, card_height / 2), ])
                         )


class Setback(TextOnlyCard):
    def __init__(self, title: str, body: str):
        super().__init__("Learning Opportunities", title, body, (255, 0, 0))


class Upgrade(TextOnlyCard):
    def __init__(self, title: str, body: str):
        super().__init__("Acceleration Strategies", title, body, (0, 255, 255))


class EngineerCard(CadenceCard):
    def __init__(self, name: str, level: int, salary: int, type: DesignType):
        def as_roman_numeral(lvl):
            if lvl == 1:
                return "I"
            if lvl == 2:
                return "II"
            if lvl == 3:
                return "III"
            if lvl == 4:
                return "IV"
            if lvl == 5:
                return "V"
        super().__init__(front_face=Face([
            (FaceSolidBackground((255, 255, 255)), 0, 0),
            (FaceText(name, 32, (0, 0, 0), bg=type.color), 0, 0),
            # (FaceText(type.name, 32, Color.choose_fg_for_bg(type.color), bg=type.color), 0, card_height / 2),
            # (FaceText(f"Engineer {as_roman_numeral(level)}", 32, (0, 0, 0)), 0, card_height-32),
            (FaceIcon(resources_folder / "nerdy_glasses.png", card_width // 4, card_height // 4), 10, 50),
            (FaceText(f"{type.name}\nEngineer {as_roman_numeral(level)}", 32, Color.choose_fg_for_bg(type.color), bg=type.color), 0, card_height - 32*2),
            (FaceText(f"${salary/1000:3.1f}k/wk", 32, (0, 0, 0)), card_width - 160, card_height - 32),
        ]), back_face=Face([
            (FaceSolidBackground((255, 255, 0)), 0, 0),
            (FaceText("Engineer", 32, (0, 0, 0)), 0, 0),
        ]))


class ProductCard(CadenceCard):
    def __init__(self, title: str,
                 funding: int,
                 total_complexity: int,
                 shared_code_pc: int,
                 security_pc: int,
                 frontend_pc: int,
                 backend_pc: int,
                 network_pc: int,
                 hardware_pc: int,
                 firmware_pc: int,
                 app_pc: int,
                 labels: list = None
                 ):
        super().__init__(Face([(FaceSolidBackground((255, 255, 255)), 0, 0),
                               (FaceText(title, 32, (0, 0, 0)), 0, 0),
                               (ProductPieChart(shared_code_pc, security_pc, frontend_pc, backend_pc, network_pc, hardware_pc, firmware_pc, app_pc, labels), 0, 50),
                               (FaceText(f"TOT={total_complexity}", 32, (0, 0, 0)), 0, card_height - 32),
                               (FaceText(f"${funding/1000:4.1f}k/wk", 32, (0, 0, 0)), card_width - 180, card_height - 32),
                               ]),
                         Face([(FaceSolidBackground((0, 255, 255)), 0, 0),
                               (FaceText("Product", 50, (0, 0, 0)), 0, card_height / 2), ])
                         )


class FeatureFace(Face):
    def __init__(self, type: DesignType, complexity: int, priority: int, title: str, subtitle: str = None):
        img_height = card_height // 4
        items = [
            (FaceSolidBackground((255, 255, 255)), 0, 0),
            (FaceText(title, 32, Color.choose_fg_for_bg(type.color), bg=type.color), 0, 0),
            (FaceIcon(resources_folder / "blocks.png", card_width // 4, img_height), 0, card_height - 32 - img_height),
            (FaceText(f"P{priority}", 32, (0, 0, 0)), 0, card_height - 32),
            (FaceText(f"{complexity} days", 32, (0, 0, 0)), card_width - 160, card_height - 32),
        ]
        if subtitle:
            items.append((FaceText(subtitle, 20, Color.choose_fg_for_bg(type.color), bg=type.color), 0, 32*2))  # allow for 2 line title
        super().__init__(items)


class TestBugFace(Face):
    def __init__(self, type: DesignType, complexity: int, priority: int, test_title: str, bug_title: str):
        border_offset_each = 4
        img_height = card_height // 4
        super().__init__([
            (FaceSolidBackground((255, 255, 255)), 0, 0),
            (FaceText(test_title, 32, Color.choose_fg_for_bg(type.color), bg=type.color), 0, 0),
            (FaceText(f"{complexity} days", 32, (0, 0, 0)), card_width - 160, card_height/2 - 32 - border_offset_each),
            (FaceText(f"P{priority}", 32, (0, 0, 0)), 0, card_height/2 - 32 - 2),
            (FaceIcon(resources_folder / "test_icon.png", card_width//4, card_height//4), 10, card_height//2 - 32 - border_offset_each - img_height),
            (FaceSolidLine((0, card_height//2), (card_width, card_height//2), width=border_offset_each*2), 0, 0),
            (FaceIcon(resources_folder / "bug_icon.png", card_width//4, card_height//4, 180), -10, -(card_height//2 - 32 - border_offset_each - img_height)),
            (FaceText(bug_title, 32, Color.choose_fg_for_bg(type.color), bg=type.color, angle_degrees=180), 0, 0),
            (FaceText(f"{complexity} days", 32, (0, 0, 0), angle_degrees=180), -(card_width - 160), -(card_height/2 - 32 - border_offset_each)),
            (FaceText(f"P{priority}", 32, (0, 0, 0), angle_degrees=180), 0, -(card_height/2 - 32 - border_offset_each)),
        ])


class TicketCard(CadenceCard):
    def __init__(self, type: DesignType, complexity: int, priority: int, feature_title: str, test_title: str, bug_title: str, subtitle: str = None):
        super().__init__(front_face=FeatureFace(type, complexity, priority, feature_title, subtitle),
                         back_face=TestBugFace(type, complexity, priority, test_title, bug_title))
