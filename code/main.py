# TODO: decide how bug-chances are determined
# > How about a choice when writing the test:
#   > FAST: 5+/6 roll bugrate -- takes 50% time --> 1/3 * x + 2/3 (10+x) == 12 --> x/3 + 20/3 + 2x/3 == x + 20/3 == 12 -> x = 12 - 20/3 = 5.333
#   > NORMAL: 4+/6 roll bugrate -- takes 60% time
#   > THOROUGH: 0+/6 bugrate -- takes 100% time
# -- to ignore rounding, have this needed_roll / 6 ratio be determined by the total complexity of the ticket:
# i.e. a 16-day ticket could have 0+/6 --> 16 days, 3+/6 --> 10 days, 6+/6 --> 8 days

from collections import namedtuple

from CadenceCard import *

if __name__ == '__main__':
    # Controls
    start_engineer_team_levels = [1, 3, 5]
    avg_engineer_team_levels = [1, 2, 3, 4, 5]
    avg_num_rounds = 8  # scales game time
    max_num_players = 6

    class Engineer:
        _effectiveness_by_level = {  # num 'days of work' per week
            1: 5,
            2: 6,
            3: 7,
            4: 8,
            5: 9
        }
        _salary_by_level = {  # dollars per week
            1: 2000,
            2: 2500,
            3: 3000,
            4: 3500,
            5: 4000
        }

        def __init__(self, level, design_type: DesignType = None):
            self.level = level
            self.effectiveness = Engineer._effectiveness_by_level[level]
            self.salary = Engineer._salary_by_level[level]
            self.design_type = design_type

    engineers = []
    for design_type in DesignTypes.get_specialized():
        for lvl in range(1, 6):
            engineers.append(Engineer(lvl, design_type))

    def get_eng_name():
        first_names = [
        "Penrod",
        "Jarman",
        "Gabrio",
        "Paco",
        "Herrmann",
        "Plat",
        "Kelvin",
        "Eleasar",
        "Norm",
        "Ursinus",
        "Rigby",
        "Amerigo",
        "Jadyn",
        "Marlon",
        "Pasquale",
        "Merrick",
        "Rosanna",
        "Clarinda",
        "Dorika",
        "Joya",
        "Eloisee",
        "Blythe",
        "Eglantine",
        "Rosellina",
        "Tatum",
        "Tayte",
        "Druilla",
        "Merlyn",
        "Harvine",
        "Meyla",
        "Manette",
        "Loveleen",
        ]
        last_names = [
            "Johan",
            "Samir",
            "Audric",
            "Fynn",
            "Bozo",
            "Baldric",
            "Valdimar",
            "Milton",
            "Raffaello",
            "Caden",
            "Carrington",
            "Shamar",
            "Edwin",
            "Seid",
            "Derrall",
            "Fielding",
            "Maurina",
            "Norberta",
            "Welda",
            "Catherine",
            "Narcisse",
            "Amaya",
            "Jeanetta",
            "Jacky",
            "Louise",
            "Lexie",
            "Andie",
            "Janina",
            "Brynn",
            "Dea",
            "Clemance",
            "Sylke",
        ]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    starter_engineer_team = [Engineer(lvl) for lvl in start_engineer_team_levels]
    avg_engineer_team = [Engineer(lvl) for lvl in avg_engineer_team_levels]
    avg_engineer_team_effectiveness = sum(map(lambda e: e.effectiveness, avg_engineer_team))
    avg_engineer_team_cost = sum(map(lambda e: e.salary, avg_engineer_team))
    avg_complexity_per_product = avg_num_rounds * avg_engineer_team_effectiveness

    class Product:
        def __init__(self, industry: str, complexity_ratio: float, category_percentages: list):
            self.industry = industry
            self.complexity_ratio = complexity_ratio
            self.category_percentages = category_percentages  # leave these pre-rounded
            total_complexity = self.complexity_ratio * avg_complexity_per_product  # not yet rounded
            self.complexity_by_category = map(lambda p: int(total_complexity * p / 100), self.category_percentages)
            self.complexity_by_category = [int(c) for c in self.complexity_by_category]  # floor each
            self.total_complexity = sum(self.complexity_by_category)  # rounded complexity score
            # print(f"{industry} complexity rounded from {total_complexity} to {self.total_complexity}")
            funding = avg_engineer_team_cost * complexity_ratio  # not yet rounded
            self.funding = int(funding/500)*500 + (500 if funding % 500 >= 250 else 0)
            # print(f"{industry} funding rounded from {funding} to {self.funding}")

        def get_total_complexity(self):
            return self.total_complexity

        def get_categorized_complexity(self):
            return self.complexity_by_category

    products = [  # shared_code, hw, fw, net, sec, back, front, app
        Product("Medical", 1.25, [20, 10, 20, 0, 15, 0, 15, 20]),
        Product("Military", 1.25, [20, 15, 10, 15, 20, 0, 0, 20]),
        Product("Construction", 1, [20, 20, 10, 0, 10, 10, 10, 20]),
        Product("Entertainment", .875, [20, 0, 10, 15, 0, 15, 20, 20]),
        Product("Agriculture", .75, [20, 15, 20, 0, 0, 15, 10, 20]),
        Product("Manufacturing", 1, [20, 20, 15, 10, 0, 15, 0, 20]),
        Product("Cloud", 1.125, [20, 0, 0, 15, 15, 15, 15, 20]),
        Product("Business", 1.125, [20, 0, 0, 15, 15, 15, 15, 20]),
        Product("Education", .75, [20, 0, 15, 15, 10, 0, 20, 20]),
        Product("IoT", .875, [20, 20, 0, 15, 15, 10, 0, 20]),
    ]

    # how many tix do I need to generate, and at what complexities?
    max_complexity_per_product = max(map(lambda p: p.total_complexity, products))
    complexity_needed_in_deck_including_app_shared_code = max_complexity_per_product * max_num_players

    app_complexity_needed = math.ceil(complexity_needed_in_deck_including_app_shared_code * .2)
    shared_code_complexity_needed = app_complexity_needed
    complexity_needed_in_deck = complexity_needed_in_deck_including_app_shared_code - app_complexity_needed - shared_code_complexity_needed
    print(f"complexity needed={complexity_needed_in_deck_including_app_shared_code}, app and shared code tickets each are 20% of that number ({app_complexity_needed}), leaving us with {complexity_needed_in_deck}")

    avg_complexity_per_round = avg_complexity_per_product / avg_num_rounds
    avg_complexity_per_ticket = avg_complexity_per_round / len(avg_engineer_team) * 1.5  # assume half of eng's are spec
    ticket_complexity_range = round(avg_complexity_per_ticket * .5), round(avg_complexity_per_ticket * 1.5)

    # print(f"remaining tickets should be in the range of {ticket_complexity_range} complexity")
    num_ticket_complexities = ticket_complexity_range[1]-ticket_complexity_range[0]+1
    ticket_distribution = [0]*num_ticket_complexities
    complexity_distributed = 0
    while complexity_distributed < complexity_needed_in_deck:
        for i in range(num_ticket_complexities):
            index = num_ticket_complexities - 1 - i
            compl = ticket_complexity_range[1] - i
            ticket_distribution[index] += 1
            complexity_distributed += compl
            if complexity_distributed >= complexity_needed_in_deck:
                break
    print("minimum ticket distribution:", ticket_distribution)
    if ticket_distribution[-1] % DesignTypes.NumSpecializedTypes == 0:
        num_tickets_per_complexity_in_deck = ticket_distribution[-1]
    else:  # round up
        num_tickets_per_complexity_in_deck = ticket_distribution[-1] // DesignTypes.NumSpecializedTypes * DesignTypes.NumSpecializedTypes + DesignTypes.NumSpecializedTypes

    print(f"So, ticket complexity will be in (inclusive) range of {ticket_complexity_range}.\n"
          f"App and Shared code tickets will be already allocated by product (not drafted), but will still fit in these bins.\n"
          f"The draft deck will have {num_tickets_per_complexity_in_deck} cards of each complexity value, which "
          f"splits to {int(num_tickets_per_complexity_in_deck / DesignTypes.NumSpecializedTypes)} copies of each specialization.")

    app_deck_by_product = {}
    shared_code_deck_by_product = {}
    for product in products:
        complexity_needed = product.get_categorized_complexity()[0]  # shared code complexity
        ticket_distribution = [0]*num_ticket_complexities
        complexity_distributed = 0
        while complexity_distributed < complexity_needed:
            for i in range(num_ticket_complexities):
                index = num_ticket_complexities - 1 - i
                compl = ticket_complexity_range[1] - i
                ticket_distribution[index] += 1
                complexity_distributed += compl
                if complexity_distributed >= complexity_needed:
                    break
        shared_code_deck_by_product[product.industry] = ticket_distribution
        app_deck_by_product[product.industry] = ticket_distribution

    class Feature:
        def __init__(self, type: DesignType, complexity: int, title: str, priority: int):
            self.design_type = type
            self.complexity = complexity
            self.title = title
            self.priority = priority

    class Test:
        def __init__(self, type: DesignType, complexity: int, title: str, priority: int):
            self.design_type = type
            self.complexity = complexity
            self.title = title
            self.priority = priority

    class Bug:
        def __init__(self, type: DesignType, complexity: int, title: str, priority: int):
            self.design_type = type
            self.complexity = complexity
            self.title = title
            self.priority = priority

    class Ticket:
        Titles = namedtuple("TicketStrings", ["feature", "test", "bug"])

        def __init__(self, type: DesignType, complexity: int, feature_title: str, test_title: str, bug_title: str):
            priority = Ticket.calc_ticket_priority(complexity, ticket_complexity_range[0], ticket_complexity_range[1])
            self.feature = Feature(type, complexity, feature_title, priority)
            self.test = Test(type, complexity, test_title, priority)
            self.bug = Bug(type, complexity, bug_title, priority)

        @staticmethod
        def calc_ticket_priority(complexity, min_complexity, max_complexity):
            num_complexity_values = max_complexity - min_complexity + 1
            priority_bin_size = num_complexity_values / 5  # 5 priorities
            return math.floor((complexity - min_complexity) / priority_bin_size) + 1

    app_features = [
        Ticket.Titles(feature="Retry Logic", test="Task Failed Successfully?", bug="Off-by-1? Classic"),
        Ticket.Titles(feature="U.I.? E.Z.", test="\"Are you there?\"", bug="All Data Deleted."),
        Ticket.Titles(feature="*sigh* Yet Another State Machine", test="A or B and C?", bug="\"It's Infinite-Looped\""),
        Ticket.Titles(feature="Backwards Compatibility", test="Loading v1.0.2", bug="Math Error"),
        Ticket.Titles(feature="Same Models, New Relationships", test="Old Tests", bug="New Problems"),
    ]

    shared_code_features = [
        Ticket.Titles(feature="Cross-Platform Support", test="...Linux?", bug="We 'forgot' about Linux"),
        Ticket.Titles(feature="Deprecated? I'm Not Switching", test="The Test of Time", bug="Something Somewhere Updated"),
        Ticket.Titles(feature="There's a Python package for that", test="import exoticpkg", bug="ImportError: Someone broke this"),
        Ticket.Titles(feature="Open.* Is Free!", test="Unique Use Case", bug="Undefined Behavior"),
        Ticket.Titles(feature="C.O.T.S. Tools", test="Can it do X?", bug="Shoot we need X"),
    ]

    hw_features = [  # in order of complexity
        Ticket.Titles(feature="Test Points", test="Debugging Something Else", bug="Floating Connection?"),
        Ticket.Titles(feature="Flyback Diodes", test="Alright, Give 'er!", bug="Magic Smoke Released!"),
        Ticket.Titles(feature="Interfacing Logic Families", test="Testing Truth Tables", bug="Logic Levels with Illogical Levels!"),
        Ticket.Titles(feature="Smaller!", test="Routing Puzzles", bug="Hollo Werld! (Crosstalk)"),
        Ticket.Titles(feature="No, Even Smaller!", test="D.R.C. Still Passing?", bug="Some (New) Assembly Required"),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
    ]

    fw_features = [  # in order of complexity
        Ticket.Titles(feature="Debug Prints", test="\"Hello World!\"", bug="*crickets*"),
        Ticket.Titles(feature="Support Multiple Products", test="Build Product Z", bug="3,266 Warnings, 134 Errors."),
        Ticket.Titles(feature="Another Chip, Another Register Interface", test="Scratchpad Written", bug="Why is it always 0xFF?!"),
        Ticket.Titles(feature="Interrupt Handler", test="Data Updated?", bug="Protect ya Check"),
        Ticket.Titles(feature="Polymorphism is C?", test="Edge-Case Params", bug="SegFault: Core Dumped"),
        Ticket.Titles(feature="Bit Bangin'", test="Peripheral Roll Call!", bug="No-Baud-y's Responding?"),
        Ticket.Titles(feature="P.O.S.T.", test="You DROPPED it???", bug="Wait, it PASSED?!"),
        Ticket.Titles(feature="Data Structures: Harder, Better, Faster, Stronger", test="Add, Move, Query", bug="*((void*)0)"),
        Ticket.Titles(feature="Big Oh-No-Tation", test="Worst-Case Runtime", bug="Faster by Hand"),
        Ticket.Titles(feature="Factory Patterns: Never out of style", test="Generate, Generate, Generate, Generate", bug="Stack Overflow"),
        Ticket.Titles(feature="Thread", test="Produce to Consume!", bug="Watchdog Timeout"),
        Ticket.Titles(feature="You Sure You NEED a Network?", test="<Ping>", bug="<Exception: Timeout>"),
    ]

    network_features = [
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
    ]

    security_features = [
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
    ]

    frontend_features = [
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
    ]

    backend_features = [
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
        Ticket.Titles(feature="", test="", bug=""),
    ]

    specialized_feature_ticket_titles = {
        DesignTypes.Hardware: hw_features,
        DesignTypes.Firmware: fw_features,
        DesignTypes.Security: security_features,
        DesignTypes.Network: network_features,
        DesignTypes.Frontend: frontend_features,
        DesignTypes.Backend: backend_features,
    }

    unspecialized_feature_ticket_titles = {
        DesignTypes.App: app_features,
        DesignTypes.SharedCode: shared_code_features,
    }

    setbacks = {
        "End of Life?!": "One of your engineers is busy for 2 weeks, (only 1 week for a Hardware specialist)",
        "Pen-Tested, Pen-Approved!": "One of your engineers is busy for 2 weeks, (only 1 week for a Security specialist)",
        "New Subsystem, Who Dis?": "One of your engineers is busy for 2 weeks, (only 1 week for a Firmware specialist)",
        "Cloud Nein!": "One of your engineers is busy for 2 weeks, (only 1 week for a Network specialist)",
        "I Just Work Here, Man": "One of your engineers is busy for 2 weeks, (only 1 week for a Front-End specialist)",
        "'Unique Index', Huh?": "One of your engineers is busy for 2 weeks, (only 1 week for a Back-End specialist)",
        "Awww, a Puppy!": "Your lowest-ranking engineer loses 3 effectiveness for the next 2 weeks",
        "Internal Audit": "All engineers must work on tickets this week",
        "New Regulations?!": "Your lowest-ranking engineer is busy generating new documentation this week",
        "User Study Flop": "Draw the top card of the Design Deck and add it to your Feature Tickets Queue",
        "Who Rebased Develop?": "Re-add the last ticket you resolved to it's previous Queue",
        "Race Condition": "The ticket with the most time left gains an additional 2 weeks",
        "Board Meeting": "Your highest-ranking engineer is busy this week",
        "Hawaii Bay-bee!": "The player to your left chooses one of your engineers to go on holiday this week",
        "Poached!": "Your most mid-ranking engineer will be poached unless you choose to Counter-Offer",
        "False Passes": "Add 1 week of additional work to the 2 tickets with the least time remaining",
        "Funny Money": "VC funding is reduced by 1k this week",
        "New Management": "Swap the tickets actively being worked on by the highest and lowest level engineers.",
        "In Too Deep": "The engineer assigned to the ticket with the most remaining time loses 3 effectiveness this week, and cannot be moved until the ticket is resolved",
        "Sidetracked": "The player to your right reassigns one of your engineers who are working on a ticket to a new one",
        "No Coffee?!": "Your engineers lose 1 effectiveness this week.",
    }

    upgrades = {
        "New CAD, Shiny!": "Hardware tickets require 4 days less effort.",
        "All of the Dev Boards!": "Firmware tickets require 4 days less effort.",
        "Yet Another Certification?": "Security tickets require 4 days less effort.",
        "New OS Just Dropped!": "Front-End tickets require 4 days less effort.",
        "All My Homies Hate Javascript": "Back-End tickets require 4 days less effort.",
        "HTTP, meet S": "Network tickets require 4 days less effort.",
        "Gantt Chart": "Whenever you encounter a setback, you may choose to blindly take the top of the Setback deck instead.",
        "Debugger": "Apply this card to a ticket slot in the staging area. Engineers working in this slot gain +2 effectiveness",
        "Nap Pods": "Engineers will give 2 weeks notice before leaving if poached",
        "Can't Reproduce": "Keep this card. Use at any time to Resolve a Priority 2 or lower Bug Ticket.",
        "Stack Overflow": "Keep this card. Use at any time to Resolve a Priority 2 or lower Feature Ticket",
        "Ramp Up Investment": "Your lowest-ranking engineers operate with +1 effectiveness",
        "Sales Training": "When an engineer presents at a conference, they may also act as if they are in the Labor Market",
        "Intern Program": "Rank I engineers can be hired for .5k less",
        "Integration Testing": "Application-Specific tickets of Priority 4 get automatically resolved",
        "Unit Testing": "Application-Specific tickets of Priority 5 get automatically resolved",
        "Architecture Document Revision": "Your engineers may give or receive any type of Knowledge at a conference",
        "Interface Document Revision": "Engineers working on a ticket they are not specialists in gain +1 effectiveness.",
        "Requirements Document Revision": "Test Ticket durations are reduced by 1 day",
        "FMEA Document Revision": "Keep this card: Use it to discard one setup card you encounter",
        "Test Plan Document Revision": "Bug Ticket durations are reduced by 1 day",
        "Work Instruction Document Revision": "New engineers reduce ramp-up time by 1 week",
        "Standard Operation Procedure Document Revision": "New engineers reduce ramp-up time by 1 week",
    }

    # -------------------------------------------------------------------------
    # Save Images
    # -------------------------------------------------------------------------

    def title_to_filename(title: str):
        file_id = ""
        for c in title:
            if c.isalnum():
                file_id += c
            elif c.isspace():
                file_id += '_'
        return file_id

    image_folder = Path(__file__).parent / "images"
    image_folder.mkdir(exist_ok=True)

    setbacks_folder = image_folder / "setbacks"
    setbacks_folder.mkdir(exist_ok=True)

    upgrades_folder = image_folder / "upgrades"
    upgrades_folder.mkdir(exist_ok=True)

    products_folder = image_folder / "products"
    products_folder.mkdir(exist_ok=True)

    engineers_folder = image_folder / "engineers"
    engineers_folder.mkdir(exist_ok=True)

    tickets_folder = image_folder / "tickets"
    tickets_folder.mkdir(exist_ok=True)
    # make ticket subfolders
    for design_type in DesignTypes.get_unspecialized():
        (tickets_folder / design_type.name).mkdir(exist_ok=True)
        for product in products:
            (tickets_folder / design_type.name / product.industry).mkdir(exist_ok=True)
    for design_type in DesignTypes.get_specialized():
        (tickets_folder / design_type.name).mkdir(exist_ok=True)

    for title, desc in setbacks.items():
        setback = Setback(title, desc)
        file_id = title_to_filename(title)
        setback.save_front_to(setbacks_folder / f"{file_id}_front.png")
        setback.save_back_to(setbacks_folder / f"{file_id}_back.png")

    for title, desc in upgrades.items():
        upgrade = Upgrade(title, desc)
        file_id = title_to_filename(title)
        upgrade.save_front_to(upgrades_folder / f"{file_id}_front.png")
        upgrade.save_back_to(upgrades_folder / f"{file_id}_back.png")

    for product in products:
        file_id = title_to_filename(product.industry)
        product = ProductCard(product.industry,
                              product.funding,
                              product.total_complexity,
                              *product.category_percentages,
                              labels=list(map(str, product.get_categorized_complexity())))
        product.save_front_to(products_folder / f"{file_id}_front.png")
        product.save_back_to(products_folder / f"{file_id}_back.png")

    for engineer in engineers:
        file_id = title_to_filename(f"{engineer.design_type.name}_Engineer_{engineer.level}")
        eng = EngineerCard(get_eng_name(), engineer.level, engineer.salary, engineer.design_type)
        eng.save_front_to(engineers_folder / f"{file_id}_front.png")
        eng.save_back_to(engineers_folder / f"{file_id}_back.png")

    # Main deck
    for design_type, ticket_titles in specialized_feature_ticket_titles.items():
        num_cards_needed = num_tickets_per_complexity_in_deck * num_ticket_complexities
        num_titles_available = len(ticket_titles)
        cards_filled = 0
        while cards_filled < num_cards_needed:
            for complexity in range(ticket_complexity_range[1], ticket_complexity_range[0]-1, -1):
                titles = ticket_titles[ticket_complexity_range[1] - complexity]
                ticket = Ticket(design_type, complexity, *titles)
                file_id = title_to_filename(f"{design_type.name}_{ticket.feature.complexity}")
                ticket_card = TicketCard(design_type, complexity, ticket.test.priority, *titles)
                ticket_card.save_front_to(tickets_folder / design_type.name / f"{file_id}_front.png")
                ticket_card.save_back_to(tickets_folder / design_type.name / f"{file_id}_back.png")

                cards_filled += 1
                if cards_filled >= num_cards_needed:
                    break

    # App / Shared Code -- specific per industry
    for design_type, ticket_titles in unspecialized_feature_ticket_titles.items():
        for product in products:
            num_cards_needed = sum(shared_code_deck_by_product[product.industry])
            num_tickets_available = len(ticket_titles)
            cards_filled = 0
            while cards_filled < num_cards_needed:
                for complexity in range(ticket_complexity_range[1], ticket_complexity_range[0] - 1, -1):
                    titles = ticket_titles[ticket_complexity_range[1] - complexity]
                    ticket = Ticket(design_type, complexity, *titles)
                    file_id = title_to_filename(f"{design_type.name}_{ticket.feature.complexity}")
                    ticket_card = TicketCard(design_type, complexity, ticket.test.priority, *titles, subtitle=product.industry)
                    ticket_card.save_front_to(tickets_folder / design_type.name / product.industry / f"{file_id}_front.png")
                    ticket_card.save_back_to(tickets_folder / design_type.name / product.industry / f"{file_id}_back.png")
                    cards_filled += 1
                    if cards_filled >= num_cards_needed:
                        break
