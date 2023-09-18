from FrgSet import *


class HomeScreen:
    
    def __init__(self):
        self.running = True
        self.screen = pygame.display.set_mode((HOME_SCREEN_WIDTH, HOME_SCREEN_HEIGHT))
        pygame.display.set_caption("WorldForge")
        pygame.display.set_icon(get_image('./logo.ico'))
        self.scale = True
        self.hovered_input = None  # Initialize the hovered input field
        self.active_input = None   # Initialize the active input field
        self.input_active = False  # Initialize input activity flag to False
        self.empty_fields = False
        self.desired_tileset = None

        self.theme = THEMES["Beta-Forge"]
        self.main_color = self.theme["main"]
        self.text_theme = self.theme["text"]
        self.grid_theme = self.theme["grid"]
        self.accent_color = self.theme["accent"]
        self.secondary_color = self.theme["secondary"]

        self.worldforge_title = [                                                                                                 
            [
                "@@@  @@@  @@@   @@@@@@   @@@@@@@   @@@       @@@@@@@   @@@@@@@@   @@@@@@   @@@@@@@    @@@@@@@@  @@@@@@@@",
                "@@@  @@@  @@@  @@@@@@@@  @@@@@@@@  @@@       @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@@  @@@@@@@@",
                "@@!  @@!  @@!  @@!  @@@  @@!  @@@  @@!       @@!  @@@  @@!       @@!  @@@  @@!  @@@  !@@        @@!",
                "!@!  !@!  !@!  !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@!       !@!  @!@  !@!  @!@  !@!        !@!",
                "@!!  !!@  @!@  @!@  !@!  @!@!!@!   @!!       @!@  !@!  @!!!:!    @!@  !@!  @!@!!@!   !@! @!@!@  @!!!:!",
                "!@!  !!!  !@!  !@!  !!!  !!@!@!    !!!       !@!  !!!  !!!!!:    !@!  !!!  !!@!@!    !!! !!@!!  !!!!!:",
                "!!:  !!:  !!:  !!:  !!!  !!: :!!   !!:       !!:  !!!  !!:       !!:  !!!  !!: :!!   :!!   !!:  !!:",
                ":!:  :!:  :!:  :!:  !:!  :!:  !:!   :!:      :!:  !:!  :!:       :!:  !:!  :!:  !:!  :!:   !::  :!:",
                " :::: :: :::   ::::: ::  ::   :::   :: ::::   :::: ::   ::       ::::: ::  ::   :::   ::: ::::   :: ::::",
                "  :: :  : :     : :  :    :   : :  : :: : :  :: :  :    :         : :  :    :   : :   :: :: :   : :: ::"
            ],
            [
                "'##:::::'##::'#######::'########::'##:::::::'########::'########::'#######::'########:::'######:::'########:",
                "'##:'##: ##:'##.... ##: ##.... ##: ##::::::: ##.... ##: ##.....::'##.... ##: ##.... ##:'##... ##:: ##.....::",
                "'##: ##: ##: ##:::: ##: ##:::: ##: ##::::::: ##:::: ##: ##::::::: ##:::: ##: ##:::: ##: ##:::..::: ##:::::::",
                "'##: ##: ##: ##:::: ##: ########:: ##::::::: ##:::: ##: ######::: ##:::: ##: ########:: ##::'####: ######:::",
                "'##: ##: ##: ##:::: ##: ##.. ##::: ##::::::: ##:::: ##: ##...:::: ##:::: ##: ##.. ##::: ##::: ##:: ##...::::",
                "'##: ##: ##: ##:::: ##: ##::. ##:: ##::::::: ##:::: ##: ##::::::: ##:::: ##: ##::. ##:: ##::: ##:: ##:::::::",
                ". ###. ###::. #######:: ##:::. ##: ########: ########:: ##:::::::. #######:: ##:::. ##:. ######::: ########:",
                ":...::...::::.......:::..:::::..::........::........:::..:::::::::.......:::..:::::..:::......::::........::"
            ],
            [
                ' __     __     ______     ______     __         _____     ______   ______     ______     ______     ______    ',
                '/\ \  _ \ \   /\  __ \   /\  == \   /\ \       /\  __-.  /\  ___\ /\  __ \   /\  == \   /\  ___\   /\  ___\   ',
                '\ \ \/ ".\ \  \ \ \/\ \  \ \  __<   \ \ \____  \ \ \/\ \ \ \  __\ \ \ \/\ \  \ \  __<   \ \ \__ \  \ \  __\   ',
                ' \ \__/".~\_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \____-  \ \_\    \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ ',
                '  \/_/   \/_/   \/_____/   \/_/ /_/   \/_____/   \/____/   \/_/     \/_____/   \/_/ /_/   \/_____/   \/_____/ '
            ],
            [
                '               #   ___           !!!         _     _            ...                     #   ___           !!!                         |"|      ',
                "     )|(       #  <_*_>       `  _ _  '    o' \,=./ `o     o,*,(o o)          ###       #  <_*_>       `  _ _  '      __MMM__        _|_|_     ",
                "    (o o)      #  (o o)      -  (OXO)  -      (o o)       8(o o)(_)Ooo       (o o)      #  (o o)      -  (OXO)  -      (o o)         (o o)     ",
                "ooO--(_)--Ooo--8---(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO-(_)---Ooo----ooO--(_)--Ooo--8---(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-",
            ],
            [
                " _                       _         ______                    ",
                "(_|   |   |_/           | |    |  (_) |                      ",
                "  |   |   |   __   ,_   | |  __|     _|_  __   ,_    __,  _  ",
                "  |   |   |  /  \_/  |  |/  /  |    / | |/  \_/  |  /  | |/  ",
                "   \_/ \_/   \__/    |_/|__/\_/|_/ (_/   \__/    |_/\_/|/|__/",
                "                                                      /|     ",
                "                                                      \|     "
            ]                                                                                       
        ]
        self.chosen_title = random.choice(self.worldforge_title)
        # Initialize fonts and text inputs
        self.font = pygame.font.Font("./slkscr.ttf", 28)
        self.text_inputs = {
            "Filename": {"value": "", "rect": pygame.Rect(1000, 100, 190, 50), "field": pygame.Rect(1250, 100, 250, 50)},
            "Map Width": {"value": "", "rect": pygame.Rect(1000, 200, 190, 50), "field": pygame.Rect(1250, 200, 250, 50)},
            "Map Height": {"value": "", "rect": pygame.Rect(1000, 300, 200, 50), "field": pygame.Rect(1250, 300, 250, 50)},
            "Filepath": {"value": "", "rect": pygame.Rect(1000, 400, 200, 50), "field": pygame.Rect(1250, 400, 250, 50)},
            "Forge": {"value": "Forge", "rect": pygame.Rect(1385, 520, 110, 50), "field": pygame.Rect(0, 0, 0, 0)},
            "Open": {"value": "Open", "rect": pygame.Rect(1245, 520, 110, 50), "field": pygame.Rect(0, 0, 0, 0)},
            "Tile Size": {"value": "8", "rect": pygame.Rect(1000, 520, 152, 50), "field": pygame.Rect(1160, 520, 50, 50)},
        }

        # Initialize a list to keep track of recently opened files
        self.recently_opened_files = []
        self.image_display_rect = pygame.Rect(150, 320, 328*1.5, 392*1.5)  # Rectangle for image display
        self.image_surface = None  # Surface to display the loaded image
        self.tile_size = int(self.text_inputs['Tile Size']['value'])  # Default tile size

        # Load the list of recently opened files from the JSON file, if it exists
        self.load_recently_opened_files()

    def load_recently_opened_files(self):
        try:
            with open("rcf.forge", "r") as file:
                self.recently_opened_files = json.load(file)
                if isinstance(self.recently_opened_files, dict):
                    self.recently_opened_files = list(self.recently_opened_files.keys())
                file.close()
        except FileNotFoundError:
            # Handle the case where the JSON file doesn't exist yet
            with open("rcf.forge", "w") as file:
                data = {
                    "_--_":"_____________"
                }
                json.dump(data,file)
                file.close()

    def save_recently_opened_files(self):
        # Save the list of recently opened files to a JSON file
        if len(self.recently_opened_files) > 12:
            print('too many recents')
            self.recently_opened_files.pop()
        with open("rcf.forge", "w") as file:
            json.dump(self.recently_opened_files, file, indent=4)

    def add_to_recently_opened(self, file_path):
        # Add a recently opened file to the list, removing the oldest one if it exceeds the limit and handling duplicates
        if file_path in self.recently_opened_files:
            self.recently_opened_files.remove(file_path)
            self.recently_opened_files.insert(0, file_path)
        elif len(self.recently_opened_files) <= 12:
            self.recently_opened_files.insert(0, file_path)
        elif len(self.recently_opened_files) > 12:
            print('too many recents')
            self.recently_opened_files.pop()
            self.save_recently_opened_files()

    def draw_recently_opened_files(self):
        # Define the position and size of the recently opened files viewport
        draw_text(self.screen, './slkscr.ttf', "Recent Files", VECTOR2((1245, 660)))
        self.viewport_rect = pygame.Rect(950, 680, 580, 250)
        pygame.draw.rect(self.screen, WHITE, self.viewport_rect, 2)  # Outline the viewport
        font = pygame.font.Font("./slkscr.ttf", 16)
        
        # Render the list of recently opened files
        y = self.viewport_rect.top + 10
        for file_path in self.recently_opened_files:
            text_color = WHITE
            if self.viewport_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.Rect(950, y - 2, 560, 20).collidepoint(pygame.mouse.get_pos()):
                    text_color = (50,50,50)  # Highlight text when hovered

            text_surface = font.render(file_path, True, text_color)
            self.screen.blit(text_surface, (self.viewport_rect.left + 10, y))
            y += 20

    def draw_ascii_art(self, lines, x, y, color):
        font = pygame.font.Font(None, 24)
        
        line_height = 12  # Adjust this value to set the vertical spacing between lines
        
        for line in lines:
            for char in line:
                char_surface = font.render(char, True, color)
                self.screen.blit(char_surface, (x, y))
                x += char_surface.get_width()  # Adjust horizontal position based on the rendered character width
            
            x = 50  # Reset x position for the next line
            y += line_height  # Move to the next line with vertical spacing

    def draw_input_field(self, input_name, input_data, active_input):
        # Define the colors for text and field background
        text_color = self.text_theme
        field_background_color = self.main_color

        rect = input_data["rect"]
        field = input_data["field"]
        # Draw input field background
        pygame.draw.rect(self.screen, field_background_color, rect)
        pygame.draw.rect(self.screen, self.accent_color, rect, 2)  # Draw a border around the field

        # Check if this field is currently active
        if input_name == active_input:
            text_color = [50,50,50]  # Change text color to match the field background

        # Draw field name
        text_surface = self.font.render(input_name, True, text_color)
        text_x = rect.left + 5
        text_y = rect.top + 5
        self.screen.blit(text_surface, (text_x, text_y))

        # Draw input text
        pygame.draw.rect(self.screen, self.accent_color, field)
        text_surface = self.font.render(input_data["value"], True, self.main_color)
        text_x = field.left + 4  # Adjust this value to set the distance between the field name and input text
        text_y = field.top + 8
        self.screen.blit(text_surface, (text_x, text_y))

        # Check if the input field is being hovered or active
        if input_name == self.hovered_input or input_name == self.active_input:
            pygame.draw.rect(self.screen, self.accent_color, rect, 2)  # Add a border for hover effect
            
    def draw_hud(self):
        # Background for the HUD
        hud_height = 50
        pygame.draw.rect(self.screen, self.main_color, (0, 0, HOME_SCREEN_WIDTH, hud_height))
        pygame.draw.line(self.screen, self.accent_color, (0, hud_height), (HOME_SCREEN_WIDTH, hud_height), width=2)

        # Display current time in EST timezone in 12-hour format
        est_timezone = pytz.timezone('US/Eastern')  # Use 'US/Eastern' for EST timezone
        current_time_est = datetime.datetime.now(est_timezone)
        time_format = '%I:%M %p'  # Use %I for 12-hour format, %M for minutes, %p for AM/PM
        time_text = f"{current_time_est.strftime(time_format)}"
        draw_text(self.screen, "./slkscr.ttf", time_text, VECTOR2((1520, 25)), size=28, color=self.text_theme)

        # Display title
        draw_text(self.screen, "./slkscr.ttf", f"WorldForge v0.1.0", VECTOR2((160, 25)), size=28, color=self.text_theme)

    def draw_image_display(self):
        pygame.draw.rect(self.screen, self.accent_color, self.image_display_rect, 2)  # Outline for image display

        if self.image_surface:
            if self.scale:
                self.ratio = self.image_surface.get_width() / self.image_surface.get_height()
                if self.image_surface.get_width() <= 500 and self.image_surface.get_height() <= 500:
                    desired_height = self.image_surface.get_height() * 2
                else:
                    desired_height = self.image_surface.get_height() // 2
                desired_width = int(desired_height * self.ratio)
                self.desired_tileset = self.image_surface
                # self.desired_tileset = cut_graphics(self.image_surface, self.tile_size)
                self.image_surface = scale_images([self.image_surface], (desired_width, desired_height))[0]
                self.scale = False

                # Update the image_display_rect to fit the scaled image
                # self.image_display_rect.x -= 26
                # self.image_display_rect.y -= 96
                self.image_display_rect.size = (self.image_display_rect.size[0] + 86, self.image_display_rect.size[1] + 50)
                # self.image_display_rect.size = self.image_surface.get_size()

            draw_text(self.screen, './slkscr.ttf', "Tileset", VECTOR2(450, 280), size=50)
            draw_text(self.screen, './slkscr.ttf', "Drag and drop!", VECTOR2(450, 300), size=12)

            self.screen.blit(self.image_surface, self.image_display_rect.topleft)

            # Calculate the new tile size based on the scaled image dimensions
            if self.image_surface.get_width() <= 500 and self.image_surface.get_height() <= 500:
                scaled_tile_size = self.tile_size * 2
            else:
                scaled_tile_size = self.tile_size // 2

            # Draw a grid on top of the image with the new tile size
            for x in range(0, self.image_display_rect.width, scaled_tile_size):
                pygame.draw.line(self.screen, self.grid_theme, (self.image_display_rect.left + x, self.image_display_rect.top), (self.image_display_rect.left + x, self.image_display_rect.bottom), 1)

            for y in range(0, self.image_display_rect.height, scaled_tile_size):
                pygame.draw.line(self.screen, self.grid_theme, (self.image_display_rect.left, self.image_display_rect.top + y), (self.image_display_rect.right, self.image_display_rect.top + y), 1)
        else:
            draw_text(self.screen, './slkscr.ttf', "Tileset", VECTOR2(400, 280), size=50)
            draw_text(self.screen, './slkscr.ttf', "Drag and drop!", VECTOR2(400, 300), size=12)

    def handle_drop_event(self, file_path):
        try:
            self.image_surface = pygame.image.load(file_path)
        except pygame.error:
            print(f"Failed to load image from: {file_path}")

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.DROPFILE:
                    self.handle_drop_event(event.file)
                    self.tileset_path = event.file

            self.screen.fill(self.main_color)

            # Draw WorldForge ASCII art
            # self.draw_ascii_art(self.chosen_title, 50, 50, WHITE)

            # Draw input fields
            for input_name, input_data in self.text_inputs.items():
                # Check if the input field is being hovered
                if input_data["rect"].collidepoint(pygame.mouse.get_pos()):
                    self.hovered_input = input_name
                else:
                    self.hovered_input = None

                self.draw_input_field(input_name, input_data, self.active_input)  # Draw the input field

            if self.empty_fields:
                draw_text(self.screen, './slkscr.ttf', "All Fields Required", VECTOR2(675, 450), 16, self.text_theme)

            self.draw_hud()

            # Draw the list of recently opened files
            self.draw_recently_opened_files()

            # Draw the image display section
            self.draw_image_display()
            
            # Update Grid Tilesize on tileset display
            prev_tilesize = 8
            
            if self.text_inputs['Tile Size']['value'] and self.active_input != "Tile Size":
                self.tile_size = int(self.text_inputs['Tile Size']['value'])
            else:
                self.tile_size = prev_tilesize

            pygame.display.flip()
            clock.tick(60)

    def handle_click(self, pos):
        for input_name, input_data in self.text_inputs.items():
            if input_data["rect"].collidepoint(pos):
                self.active_input = input_name
                if input_name == "Filepath":
                    folder_path = self.open_folder_dialog()
                    if folder_path:
                        self.text_inputs["Filepath"]["value"] = folder_path
                if input_name == "Forge":
                    i = 0
                    for field in self.text_inputs.values():
                        if field['value'] not in ["Forge", "Open"] and field['value']:
                            i += 1
                    if i == len(self.text_inputs) - 2:
                        self.empty_fields = False
                        save_destination = f"{self.text_inputs['Filepath']['value']}/{self.text_inputs['Filename']['value']}.forge"
                        # Add the recently opened file to the list
                        self.add_to_recently_opened(save_destination)
                        # Save the updated list of recently opened files
                        self.save_recently_opened_files()
                        self.initialize_level_editor(self.tileset_path, self.desired_tileset, int(self.text_inputs['Tile Size']['value']), int(self.text_inputs['Map Width']['value']), int(self.text_inputs['Map Height']['value']), [], save_destination, map_name=self.text_inputs['Filename']['value'])
                    else:
                        self.empty_fields = True
                elif input_name == "Open":
                    self.open_json_file()
                return

        # If you click on a recently opened file, load it
        y = self.viewport_rect.top + 10
        for i, file_path in enumerate(self.recently_opened_files):
            if pygame.Rect(950, y - 2, 560, 20).collidepoint(pos):
                try:
                    with open(file_path, "r") as file:
                            # Load the JSON data and initialize the editor with it
                            json_data = json.load(file)
                            # tilesize = self.text_inputs['Tile Size']
                            tilesize = json_data["tilesize"]
                            tileset_path = json_data["tileset_path"]
                            map_width = json_data["width"]
                            map_height = json_data["height"]
                            offgrid = json_data["offgrid"]
                            map_name = json_data["name"]
                            save_destination = file_path  # Use the selected JSON file path
                            self.initialize_level_editor(tileset_path, self.desired_tileset, tilesize, map_width, map_height, offgrid, save_destination, map_name)
                    # Move the clicked file to the top of the recently opened list
                    recently_opened_file = self.recently_opened_files.pop(i)
                    self.recently_opened_files.insert(0, recently_opened_file)
                    # Save the updated list of recently opened files
                    self.save_recently_opened_files()
                    return
                except FileNotFoundError:
                    print(f'\nFile Not Found!\nPATH: {file_path}')
                    draw_text(self.screen, './slkscr.ttf', f'\nFile Not Found!\nPATH: {file_path}', VECTOR2(250,250), size=28)
                    self.recently_opened_files.remove(file_path)
                    self.save_recently_opened_files()
            y += 20            

        # If you click outside of all input fields, deactivate input
        self.active_input = None
        self.input_active = False
   
    def open_folder_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        folder_path = filedialog.askdirectory(title="Select Save Destination Folder")
        return folder_path
    
    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file = filedialog.askopenfile(title="Select Map File")
        if file != None:
            file_path = file.name
            return file_path
        else:
            pass

    def open_json_file(self):
        json_path = self.open_file_dialog()
        if json_path != None:
            if json_path.endswith(".forge"):
                try:
                    with open(json_path, "r") as file:
                        # Load the JSON data and initialize the editor with it
                        json_data = json.load(file)
                        tilesize = json_data["tilesize"]
                        tileset_path = json_data["tileset_path"]
                        map_width = json_data["width"]
                        map_height = json_data["height"]
                        offgrid = json_data["offgrid"]
                        map_name = json_data["name"]
                        save_destination = json_path  # Use the selected JSON file path
                        self.recently_opened_files.insert(0, json_path)
                        self.save_recently_opened_files()
                        self.initialize_level_editor(tileset_path, self.desired_tileset, tilesize, map_width, map_height, offgrid, save_destination, map_name)
                except FileNotFoundError:
                    # Handle the case where the file is not found
                    print(f"File not found: {json_path}")
            else:
                # Handle the case where the selected file is not a JSON file
                print(f"Invalid file format: {json_path}")

    def handle_key(self, key):
        if self.active_input:
            if pygame.key.name(key) == "return":
                self.active_input = None
            elif pygame.key.name(key) == "backspace":
                # Check if there's text to delete
                if self.text_inputs[self.active_input]["value"]:
                    self.text_inputs[self.active_input]["value"] = self.text_inputs[self.active_input]["value"][:-1]
            elif pygame.key.name(key).isalnum():
                # Handle alphanumeric key presses
                self.text_inputs[self.active_input]["value"] += pygame.key.name(key)

    def initialize_level_editor(self, tileset_path, tileset, tilesize, map_width, map_height, offgrid, save_destination, map_name):
        # Now, you can create an instance of your LevelEditor class with the entered parameters
        level_editor = LevelEditor(tileset_path, tileset, int(map_width), int(map_height), int(tilesize), save_destination, map_name)
        level_editor.tilemap.offgrid_tiles = offgrid
        # Add the recently opened file to the list
        self.add_to_recently_opened(save_destination)
        # Save the updated list of recently opened files
        self.save_recently_opened_files()
        level_editor.run()


class LevelEditor:

    def __init__(self, tileset_path, tileset, map_width, map_height, tilesize, save_destination, map_name):
        self.running = True
        self.get_editor_settings()
        self.setup_pygame(map_width, map_height, tilesize)
        pygame.display.set_icon(get_image('./logo.ico'))
        self.mouse_position = (0, 0)
        self.movement = [False, False, False, False]
        self.map_name = map_name
        self.map_path = save_destination
        self.map_width = int(map_width)
        self.map_height = int(map_height)
        self.edit_area_width = 0
        self.edit_area_height = 0
        self.setup_assets(tileset=tileset, tileset_path=tileset_path, tilesize=tilesize)
        self.tilesize = tilesize
        self.tileset_path = tileset_path
        self.tile_group = 0
        self.tile_id = 0
        self.tilemap = Tilemap(map_name, self, self.assets, tile_size=int(tilesize))
        
        try:
            self.load(self.map_path)
        except:
            print('no map')

        self.scroll = [0, 0]
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True
        self.show_grid = False
        self.show_tiles = False
        self.fill = False
        self.tile_slot_size = tilesize
        self.dragging_tile = False
        self.dragging_start_pos = None
        self.middle_mouse_dragging = False
        self.middle_mouse_drag_start = None

        # List to keep track of tile placements for undo
        self.last_state = None
        self.old_tile = []
        self.old_tile_ids = []
        self.default_redo = []
        self.tile_check = []
        self.redo_history = []
        self.undo_history = [self.tilemap.tilemap.copy()]
        self.fill_undo_history = []

        # variables to track current level size
        self.current_level_x = 0
        self.current_level_y = 0

        # hud settings
        self.hud_font_size = 24

        # Tile view pane settings
        self.tileset_viewport = {
            "x": 0,
            "y": 0,
            "scroll_speed": 50,  # Adjust the scroll speed as needed
        }
        self.tile_view_x = 0  # Adjust the x-coordinate as needed.
        self.tile_view_y = 0
        
        if get_image(self.tileset_path).get_width() <= 100 and get_image(self.tileset_path).get_height() <= 100:
            self.tile_view_width = 180  # Adjust the width as needed.
            self.tile_size_scale = 4.0  # Controls the size of individual tiles within the viewport
        else:
            self.tile_view_width = 450  # Adjust the width as needed.
            self.tile_size_scale = 1.0  # Controls the size of individual tiles within the viewport
        
        self.tile_view_height = self.screen.get_size()[1]
        self.tileset_scale = 1.0  # Controls the scale of the entire tileset viewport
        self.tile_view_min = False
        self.tile_view_max = False

        # Dropdown menu settings
        self.dropdown_open = False
        self.dropdown_items = ["Home", "Save", "Export\n  PNG", "Exit"]
        self.dropdown_item_height = 80
        self.dropdown_rect = None

        # zoom
        self.zoom = 1
        self.zoom_step = 1
        self.zoom_max = 8.0
        self.zoom_min = 0.5

        # cooldowns
        self.undoing = False
        self.redoing = False
        self.cooldowns = {
            'undo': 0,
            'redo': 0
        }

    def get_editor_settings(self):
        with open('./settings.json', 'r') as configfile:
            settings = json.load(configfile)
        
        self.scroll_speed = settings['scroll speed']

    def setup_pygame(self,map_width, map_height, tilesize):
        pygame.display.set_caption('WORLDFORGE')
        self.screen = pygame.display.set_mode((EDITOR_SCREEN_SIZE), pygame.SCALED)
        self.scaled_screen = PYSURFACE((EDITOR_SCREEN_WIDTH/4, EDITOR_SCREEN_HEIGHT/4))
        self.edit_sheet = PYSURFACE((map_width * tilesize, map_height * tilesize))
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock()

    def setup_assets(self, tileset, tileset_path, tilesize):
        if isinstance(tileset, type(None)):
            self.assets = {
                'tileset': cut_graphics(get_image(tileset_path), tilesize)
            }
            tile_list = list(self.assets)
            self.tile_list = tile_list
        else:
            self.assets = {
                'tileset': cut_graphics(tileset, tilesize)
            }
            tile_list = list(self.assets)
            self.tile_list = tile_list
            return tile_list

    def handle_mouse_wheel(self, event):
        # Check if the mouse wheel was scrolled up or down
        if event.button == 4 and self.show_tiles and not self.tile_view_min:  # Mouse wheel up
            self.tileset_viewport["y"] += self.tileset_viewport["scroll_speed"]
        elif event.button == 5 and self.show_tiles and not self.tile_view_max:  # Mouse wheel down
            self.tileset_viewport["y"] -= self.tileset_viewport["scroll_speed"]

        if event.button == 4 and not self.show_tiles:  # Mouse wheel up
            if self.zoom + self.zoom_step <= self.zoom_max:
                self.zoom += self.zoom_step
            else:
                pass
            
        elif event.button == 5 and not self.show_tiles:  # Mouse wheel down
            if self.zoom - self.zoom_step >= self.zoom_min:
                self.zoom -= self.zoom_step
            else:
                pass

    def draw_fps(self):
        fpsCounter = int(self.clock.get_fps())
        draw_text(self.screen, f"fps: {fpsCounter}", [660, 25], font=FONT, size=32, color=[255, 255, 255])

    def export_as_png(self):
        self.tilemap.export_as_png(self.map_path.removesuffix(f"/{self.map_name}.forge"))

    def undo(self):
        if len(self.undo_history) > 0:
            print('undoing...')
            self.last_state = self.tilemap.tilemap.copy()
            # # Save the current tilemap state for redo
            self.redo_history.append(self.tilemap.tilemap.copy())
            # # Restore the previous state
            old_state = self.undo_history.pop()
            self.tilemap.tilemap = old_state

            if len(self.old_tile_ids) > 0 and len(self.old_tile) > 0:
                for tile_id in self.old_tile_ids:
                    self.old_tile_ids.pop()
                    old_tile = self.old_tile.pop()
                    if self.tilemap.tilemap[f"{old_tile['position'][0]};{old_tile['position'][1]}"]['id'] != tile_id:
                        self.tilemap.tilemap[f"{old_tile['position'][0]};{old_tile['position'][1]}"]['id'] = tile_id
            else:
                pass

    def redo(self):
        if len(self.redo_history) > 0:
            print('redoing...')
            # Save the current tilemap state for undo
            self.copy_undo_state()
            # Restore the next state (if available) for redo
            self.tilemap.tilemap = self.redo_history.pop()

    def fill_empty_space(self, start_pos):
        # Check if the selected tile is already filled or out of bounds
        if self.tilemap.tilemap.get(str(start_pos), None) is not None:
            return

        # Define a stack for the flood fill algorithm
        stack = [start_pos]

        # Get the active tile information
        active_tile_type = self.tile_list[self.tile_group]
        active_tile_id = self.tile_id

        while stack:
            x, y = stack.pop()

            # Check if the tile is within the edit area bounds
            if (
                0 <= x < self.edit_area_width
                and 0 <= y < self.edit_area_height
            ):
                # Check if the tile is empty and can be filled
                if self.tilemap.tilemap.get(f"{x};{y}", None) is None:
                    # Place the active tile in the current position
                    self.tilemap.tilemap[f"{x};{y}"] = {
                        'tileset': self.tile_list[self.tile_group],
                        "id": active_tile_id,
                        "position": (x, y)
                    }

                    # Check if a tile was drawn over or empty
                    placed_tile = {
                        'tileset': self.tile_list[self.tile_group],
                        "id": self.tile_id,
                        "position": (
                            self.mouse_position[0] + self.scroll[0],
                            self.mouse_position[1] + self.scroll[1],
                        ),
                    }
                    self.tile_check.append(placed_tile['position'])

                    # Add adjacent tiles to the stack for processing
                    stack.append((x + 1, y))
                    stack.append((x - 1, y))
                    stack.append((x, y + 1))
                    stack.append((x, y - 1))

    def fill_bucket(self):
        if self.ongrid and self.fill:
            # Check if the current tile is empty
            if self.tilemap.tilemap.get(str(self.selected_tile_pos), None) is None:
                # Fill empty space around the clicked position
                self.fill_empty_space(self.selected_tile_pos)
        self.clicking = False

    def updates(self):
        self.mouse_position = pygame.mouse.get_pos()
        self.mouse_position = (self.mouse_position[0] / self.zoom, self.mouse_position[1] / self.zoom)
        self.selected_tile_pos = (int(self.mouse_position[0] + self.scroll[0]) // self.tilemap.tile_size, int(self.mouse_position[1] + self.scroll[1]) // self.tilemap.tile_size)
        
        # Adjust camera to stay within the edit area bounds and one tile further
        level_width = (self.edit_area_width + 1) * self.tilemap.tile_size
        level_height = (self.edit_area_height + 1) * self.tilemap.tile_size
        max_scroll_x = max(level_width - self.screen.get_width(), 0)
        max_scroll_y = max(level_height - self.screen.get_height(), 0)
        self.scroll[0] = min(max(self.scroll[0], 0), max_scroll_x)
        self.scroll[1] = min(max(self.scroll[1], 0), max_scroll_y)

    def draw_tile_selection_pane(self, surface: PYSURFACE):
        self.mouse_position = (self.mouse_position[0] * self.zoom, self.mouse_position[1] * self.zoom)
        # Calculate the position and size of the scaled tile view pane.
        scaled_tile_view_rect = pygame.Rect(
            self.tile_view_x,
            self.tile_view_y,
            self.tile_view_width * self.tileset_scale,  # Apply tileset scale
            self.tile_view_height * self.tileset_scale,  # Apply tileset scale
        )
        pygame.draw.rect(surface, [0, 0, 0], scaled_tile_view_rect)

        # Calculate the number of tiles per row in the pane.
        tile_slot_size_with_scale = self.tile_slot_size * self.tile_size_scale + 8
        tiles_per_row = max(1, int(self.tile_view_width / tile_slot_size_with_scale))

        # Calculate the starting position for the first tile taking into account the viewport position.
        start_x = self.tile_view_x + 16 * self.tileset_scale
        start_y = self.tile_view_y + 48 * self.tileset_scale - self.tileset_viewport["y"]

        # Constrain the tileset view scroll
        def min_scroll():
            if start_y <= -self.tile_view_height - get_image(self.tileset_path).get_height() - get_image(self.tileset_path).get_width():
                self.tile_view_min = True
            else:
                self.tile_view_min = False
            return -self.tile_view_height - get_image(self.tileset_path).get_height() - get_image(self.tileset_path).get_width()
        def max_scroll():
            # if start_y >= -len(self.tile_list):
            if start_y >= self.tile_view_height - 952:
                self.tile_view_max = True
            else:
                self.tile_view_max = False
            # return -len(self.tile_list)
            return self.tile_view_height - 952

        start_y = clamp(start_y, min_scroll(), max_scroll())

        # print(self.tile_view_min, "min", " | ", self.tile_view_max, "max")

        tile_index = 0
        for tile_type_index, tile_type in enumerate(self.tile_list):
            for tile_id_index, tile_id in enumerate(self.assets[tile_type]):
                tile_image = tile_id
                tile_rect = pygame.Rect(
                    start_x + tile_slot_size_with_scale * (tile_index % tiles_per_row),
                    start_y + tile_slot_size_with_scale * (tile_index // tiles_per_row),
                    self.tile_slot_size * self.tile_size_scale,  # Apply tile size scale
                    self.tile_slot_size * self.tile_size_scale,  # Apply tile size scale
                )

                # Check if the tile is within the visible area of the scaled tile view pane.
                if tile_rect.colliderect(scaled_tile_view_rect):
                    # Draw the scaled tile image.
                    scaled_tile_image = pygame.transform.scale(
                        tile_image,
                        (int(tile_image.get_width() * self.tile_size_scale), int(tile_image.get_height() * self.tile_size_scale)),
                    )
                    surface.blit(scaled_tile_image, tile_rect.topleft)

                    # Check if the mouse is over a tile.
                    if tile_rect.collidepoint(self.mouse_position):
                        # Highlight the selected tile.
                        pygame.draw.rect(surface, (255, 255, 255), tile_rect, 1)

                        # Handle tile selection when clicked.
                        if self.clicking:
                            self.tile_group = tile_type_index
                            self.tile_id = tile_id_index
                    else:
                        pygame.draw.rect(surface, (20, 20, 20), tile_rect, 1)

                tile_index += 1

    def draw_hud(self, surface:PYSURFACE):
        # Background for the HUD
        hud_height = 50
        pygame.draw.rect(surface, (0, 0, 0), (0, 0, self.screen_size[0], hud_height))

        # Display current time in EST timezone in 12-hour format
        est_timezone = pytz.timezone('US/Eastern')  # Use 'US/Eastern' for EST timezone
        current_time_est = datetime.datetime.now(est_timezone)
        time_format = '%I:%M %p'  # Use %I for 12-hour format, %M for minutes, %p for AM/PM
        time_text = f"{current_time_est.strftime(time_format)}"
        draw_text(surface, "./slkscr.ttf", time_text, VECTOR2((1520, 25)), size=self.hud_font_size, color=[255, 255, 255])

        # Display map dimensions
        map_dimensions = f"{self.map_width * self.tilemap.tile_size}px | {self.map_height * self.tilemap.tile_size}px"
        draw_text(surface, "./slkscr.ttf", map_dimensions, VECTOR2((125, 25)), size=self.hud_font_size, color=[255,255,255])

        # Display snap to grid status
        stg_status = f"STG:{self.ongrid}"
        draw_text(surface, "./slkscr.ttf", stg_status, VECTOR2((1000, 25)), size=self.hud_font_size, color=[255,255,255])
        
        # Display grid view status
        if self.show_grid:
            grid_view = "Grid:On"
        else:            
            grid_view = "Grid:Off"
        draw_text(surface, "./slkscr.ttf", grid_view, VECTOR2((1135, 25)), size=self.hud_font_size, color=[255,255,255])
       
        # Display fill bucket status
        draw_text(surface, "./slkscr.ttf", f"Fill:{self.fill}", VECTOR2((1280, 25)), size=self.hud_font_size, color=[255,255,255])

        # Load and display your logo
        logo = scale_images([pygame.image.load("./logo.png")], (128, 128))[0]
        logo.set_alpha(100)
        surface.blit(logo, (EDITOR_SCREEN_WIDTH - 120, EDITOR_SCREEN_HEIGHT - 140))

    def draw_dropdown_menu(self):
        if self.dropdown_open:
            # Calculate the dropdown menu position
            dropdown_x = 1405
            dropdown_y = 370 - (len(self.dropdown_items) * self.dropdown_item_height)
            dropdown_width = 180

            # Create the dropdown menu rectangle
            self.dropdown_rect = pygame.Rect(dropdown_x + 15, dropdown_y, dropdown_width, len(self.dropdown_items) * self.dropdown_item_height)

            # Draw the dropdown menu background
            pygame.draw.rect(self.screen, (0, 0, 0), self.dropdown_rect)

            for i, item in enumerate(self.dropdown_items):
                item_rect = pygame.Rect(
                    dropdown_x + 15,
                    dropdown_y + i * self.dropdown_item_height,
                    dropdown_width,
                    self.dropdown_item_height,
                )

                # Check if the mouse is over the item
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if item_rect.collidepoint(mouse_x, mouse_y):
                    # Change item's color when hovered
                    item_color = (100, 100, 100)  # Background color when hovered
                    text_color = (255, 255, 255)  # Text color when hovered
                else:
                    item_color = (255, 255, 255)  # Default background color
                    text_color = (255,255,255)  # Default text color

                pygame.draw.rect(self.screen, item_color, item_rect, 1)

                # Calculate text position for center alignment
                text_x = item_rect.centerx
                text_y = item_rect.centery - 2

                draw_text(
                    self.screen,
                    "./slkscr.ttf",
                    item,
                    VECTOR2((text_x, text_y)),
                    size=28,
                    color=text_color,  # Use the calculated text color
                )

            # Check for item clicks
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.dropdown_rect.collidepoint(mouse_x, mouse_y):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            clicked_item_index = (mouse_y - dropdown_y) // self.dropdown_item_height
                            if 0 <= clicked_item_index < len(self.dropdown_items):
                                clicked_item = self.dropdown_items[clicked_item_index]
                                
                                if clicked_item == "Home":
                                    self.switch_to_home_screen()
                                elif clicked_item == "Export\n  PNG":
                                    self.export_as_png()
                                elif clicked_item == "Save":
                                    self.save(self.map_path)
                                elif clicked_item == "Exit":
                                    print('Forging save...\n')
                                    if self.save(self.map_path):
                                        print('Save Forged...')
                                    pygame.quit()
                                    sys.exit()

    def copy_undo_state(self):
        self.undo_history.append(self.tilemap.tilemap.copy())

    def render(self, surface: PYSURFACE):
        # fill background of editor area
        surface.fill([80, 80, 80])

        # update scroll/"camera" value to move the level
        self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
        self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

        # Show grid
        if self.show_grid:
            for x in range(-int(self.scroll[0]) % self.tilemap.tile_size, surface.get_width(), self.tilemap.tile_size):
                pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, surface.get_height()))
            for y in range(-int(self.scroll[1]) % self.tilemap.tile_size, surface.get_height(), self.tilemap.tile_size):
                pygame.draw.line(surface, (255, 255, 255), (0, y), (surface.get_width(), y))

        # Grid Highlighting
        if self.ongrid:
            # Calculate the position and size of the selected grid square.
            selected_grid_rect = pygame.Rect(
                self.selected_tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                self.selected_tile_pos[1] * self.tilemap.tile_size - self.scroll[1],
                self.tilemap.tile_size,
                self.tilemap.tile_size,
            )

            # Highlight the selected grid square with an outline.
            pygame.draw.rect(surface, (250, 50, 50), selected_grid_rect, 1)

        # draw tiles to tilemap
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.clicking and self.ongrid and self.show_tiles and not mouse_x < self.tile_view_width:
            tile_location = str(self.selected_tile_pos[0]) + ";" + str(self.selected_tile_pos[1])
            if tile_location not in self.tilemap.tilemap:
                placed_tile = {
                    'tileset': self.tile_list[self.tile_group],
                    "id": self.tile_id,
                    "position": (
                        self.mouse_position[0] + self.scroll[0],
                        self.mouse_position[1] + self.scroll[1],
                    ),
                }
                self.tile_check.append(placed_tile['position'])
                self.copy_undo_state()
                self.tilemap.tilemap[tile_location] = {'tileset': self.tile_list[self.tile_group], 'id': self.tile_id, 'position': self.selected_tile_pos}
            
            elif tile_location in self.tilemap.tilemap and self.tilemap.tilemap[tile_location]['id'] != self.tile_id:
                self.copy_undo_state()
                self.tilemap.tilemap[tile_location] = {'tileset': self.tile_list[self.tile_group], 'id': self.tile_id, 'position': self.selected_tile_pos}

        elif self.clicking and self.ongrid and not self.show_tiles:
            tile_location = str(self.selected_tile_pos[0]) + ";" + str(self.selected_tile_pos[1])
            if tile_location not in self.tilemap.tilemap:
                placed_tile = {
                    'tileset': self.tile_list[self.tile_group],
                    "id": self.tile_id,
                    "position": (
                        self.mouse_position[0] + self.scroll[0],
                        self.mouse_position[1] + self.scroll[1],
                    ),
                }
                self.tile_check.append(placed_tile['position'])
                self.copy_undo_state()
                self.tilemap.tilemap[tile_location] = {'tileset': self.tile_list[self.tile_group], 'id': self.tile_id, 'position': self.selected_tile_pos}
            
            elif tile_location in self.tilemap.tilemap and self.tilemap.tilemap[tile_location]['id'] != self.tile_id:
                self.copy_undo_state()
                self.tilemap.tilemap[tile_location] = {'tileset': self.tile_list[self.tile_group], 'id': self.tile_id, 'position': self.selected_tile_pos}
            
        # delete tiles from tilemap
        if self.right_clicking:
            tile_location = str(self.selected_tile_pos[0]) + ";" + str(self.selected_tile_pos[1])
            if tile_location in self.tilemap.tilemap:
                self.copy_undo_state()
                del self.tilemap.tilemap[tile_location]
            for tile in self.tilemap.offgrid_tiles.copy():
                tile_image = self.assets[tile['tileset']][tile['id']]
                tile_rect = pygame.Rect( (tile['position'][0] - self.scroll[0], tile['position'][1] - self.scroll[1]), (tile_image.get_width(), tile_image.get_height()) )
                if tile_rect.collidepoint(self.mouse_position):
                    self.copy_undo_state()
                    self.tilemap.offgrid_tiles.remove(tile)

        # render the current selected tile hud
        current_tile_image = self.assets[f'tileset'][self.tile_id].copy()
        current_tile_image.set_alpha(185)

        # render the tilemap
        self.tilemap.render(surf=surface, offset=render_scroll)
        
        # render the next tile to be placed
        if self.ongrid:
            surface.blit(current_tile_image, (self.selected_tile_pos[0] * self.tilemap.tile_size - self.scroll[0], self.selected_tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
        else:
            surface.blit(current_tile_image, self.mouse_position)

        # Scale display for zoom and blit
        self.scaled_screen = PYSURFACE((EDITOR_SCREEN_WIDTH/self.zoom, EDITOR_SCREEN_HEIGHT/self.zoom))
        self.screen.blit(SCALE(surface, EDITOR_SCREEN_SIZE), (0,0))

        # Call the method to draw the tile selection pane.
        if self.show_tiles:
            self.draw_tile_selection_pane(surface=self.screen)

        # Call the method to draw the HUD.
        self.draw_hud(self.screen)

        # Call the method do draw the dropdown.
        self.draw_dropdown_menu()

    def send_frame(self):
        pygame.display.update()
        self.dt = self.clock.tick(144) / 1000.0

    def save(self, path):
        try:
            with open(path, 'w') as savefile:
                json.dump({'tilemap': self.tilemap.tilemap, 'name': self.map_name, 'tileset_path': self.tileset_path, 'tilesize': self.tilemap.tile_size, 'width': self.map_width, 'height': self.map_height, 'offgrid': self.tilemap.offgrid_tiles}, savefile, indent=4)
                savefile.close()
            return True
        except FileNotFoundError:
            os.mkdir(path.removesuffix(f'\{self.map_name}.forge'))
            with open(path, 'w') as savefile:
                json.dump({'tilemap': self.tilemap.tilemap, 'name': self.map_name, 'tileset_path': self.tileset_path, 'tilesize': self.tilemap.tile_size, 'width': self.map_width, 'height': self.map_height, 'offgrid': self.tilemap.offgrid_tiles}, savefile, indent=4)
                savefile.close()
            print("Save Auto-Forged...")
            return True

    def load(self, path):
        with open(path, 'r') as savefile:
            map_data = json.load(savefile)

        self.tilemap.tilemap = map_data['tilemap']
        self.tile_size = map_data['tilesize']
        self.offgrid_tiles = map_data['offgrid']

    def switch_to_home_screen(self):
        self.save(self.map_path)
        self.running = False
        HomeScreen().run()
        print('switch to home screen')

    def run(self):
        self.edit_area_width = self.map_width
        self.edit_area_height = self.map_height
        
        while self.running:
            self.updates()
            self.render(self.scaled_screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 4:  # Mouse wheel up
                        self.handle_mouse_wheel(event)
                    elif event.button == 5:  # Mouse wheel down
                        self.handle_mouse_wheel(event)

                    if event.button == editor_controls['place tile']:
                        # Handle the click
                        self.clicking = True

                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'tileset': self.tile_list[self.tile_group], 'id': self.tile_id, 'position': (self.mouse_position[0] + self.scroll[0], self.mouse_position[1] + self.scroll[1])})
                            self.clicking = False

                        if self.fill:
                            self.fill_undo_history.append(
                                self.tilemap.tilemap.copy()
                            )
                            self.fill_bucket()

                        # print(self.selected_tile_pos, 'tile just placed')

                    # Handle tile dragging
                    if event.button == editor_controls['place tile'] and self.ongrid:
                        self.dragging_tile = True
                        self.dragging_start_pos = self.selected_tile_pos

                    elif event.button == 2:  # Middle mouse button
                        self.middle_mouse_dragging = True
                        self.middle_mouse_drag_start = pygame.mouse.get_pos()

                    elif event.button == editor_controls['del tile']:
                        self.right_clicking = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == editor_controls['place tile']:
                        self.clicking = False
                    # Handle tile dragging
                    elif event.button == editor_controls['place tile'] and self.ongrid:
                        self.dragging_tile = False
                        self.dragging_start_pos = None
                    elif event.button == editor_controls['del tile']:
                        self.right_clicking = False
                    
                    elif event.button == 2:  # Middle mouse button
                        self.middle_mouse_dragging = False
                        self.middle_mouse_drag_start = None
                
                if event.type == KEYDOWN:
                    if event.key == editor_controls['menu']:
                        self.dropdown_open = not self.dropdown_open
                    elif event.key == editor_controls['fill']:
                        self.fill = not self.fill
                    elif event.key == editor_controls['show tiles']:
                        self.show_tiles = not self.show_tiles
                    elif event.key == editor_controls['show grid']:
                        self.show_grid = not self.show_grid
                    elif event.key == editor_controls['move left']:
                        self.movement[0] = self.scroll_speed
                    elif event.key == editor_controls['move right']:
                        self.movement[1] = self.scroll_speed
                    elif event.key == editor_controls['move up']:
                        self.movement[2] = self.scroll_speed
                    elif event.key == editor_controls['move down']:
                        self.movement[3] = self.scroll_speed
                    elif event.key == editor_controls['toggle grid']:
                        self.ongrid = not self.ongrid
                    elif event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_F1:
                        self.save(self.map_path)
                    elif event.key == pygame.K_t:
                        self.tilemap.auto_tile()

                if event.type == KEYUP:
                    if event.key == editor_controls['move left']:
                        self.movement[0] = False
                    if event.key == editor_controls['move right']:
                        self.movement[1] = False
                    if event.key == editor_controls['move up']:
                        self.movement[2] = False
                    if event.key == editor_controls['move down']:
                        self.movement[3] = False

            # Handle middle mouse button drag to pan the map
            if self.middle_mouse_dragging:
                current_mouse_pos = pygame.mouse.get_pos()
                if self.middle_mouse_drag_start:
                    delta_x = current_mouse_pos[0] - self.middle_mouse_drag_start[0]
                    delta_y = current_mouse_pos[1] - self.middle_mouse_drag_start[1]
                    self.scroll[0] -= delta_x
                    self.scroll[1] -= delta_y
                    self.middle_mouse_drag_start = current_mouse_pos

            keys = pygame.key.get_pressed()

            # undo 
            if keys[pygame.K_z] and pygame.key.get_mods() & pygame.KMOD_CTRL and not self.cooldowns['undo']:
                print('undo')
                self.cooldowns['undo'] = UNDO_CD
                self.undo()
                self.undoing = not self.undoing
            
            # redo
            if keys[pygame.K_y] and pygame.key.get_mods() & pygame.KMOD_CTRL and not self.cooldowns['redo']:
                print('redo')
                self.cooldowns['redo'] = UNDO_CD
                self.redo()
                self.redoing = not self.redoing

            # cooldowns
            if self.undoing:
                self.cooldowns['undo'] -= self.dt
            if self.redoing:
                self.cooldowns['redo'] -= self.dt

            if self.cooldowns['undo'] <= 0:
                self.cooldowns['undo'] = 0
                self.undoing = False
            if self.cooldowns['redo'] <= 0:
                self.cooldowns['redo'] = 0
                self.redoing = False

            # reset variables
            if self.clicking and self.tilemap.tilemap != self.last_state and len(self.redo_history) > 0:
                self.redo_history = []

            # debug
            # print("undo's", len(self.undo_history), "|", "redo's", len(self.redo_history), "|", "old tiles", len(self.old_tile), "|", "old tile id's", len(self.old_tile_ids))
            # print(self.cooldowns)

            self.send_frame()


HomeScreen().run()