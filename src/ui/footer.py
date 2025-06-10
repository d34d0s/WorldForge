from globals import box, pytz, datetime

class FooterClock(box.resource.BOXlabel):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            scene.cache.get_font("slkscr"),
            text=f"{datetime.today().astimezone(pytz.timezone("US/Eastern")).strftime("%I:%M %p")}",
            text_pos = [4, 0],
            size=[100, 16],
            flags=box.resource.BOXelement.flags.SHOW_TEXT
        )
        self.pos = [8, 32]
        self.color = scene.theme["base-color"]
        self.text_color = scene.theme["text-color"]
        self.border_color = scene.theme["border-color"]
        self.set_flag(self.flags.SHOW_BORDER)

    def on_hover(self):
        self.border_color = self.scene.theme["hover-color"]

    def on_unhover(self):
        self.border_color = self.scene.theme["border-color"]

    def on_update(self, events):
        self.text = f"{datetime.today().astimezone(pytz.timezone("US/Eastern")).strftime("%I:%M %p")}"

class FooterTileSize(box.resource.BOXlabel):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            scene.cache.get_font("slkscr"),
            text=f"{scene.tilemap.tile_size[0]}x{scene.tilemap.tile_size[1]}",
            text_pos = [4, 0],
            size=[140, 16],
            flags=box.resource.BOXelement.flags.SHOW_TEXT
        )
        self.pos = [8, 52]
        self.color = scene.theme["base-color"]
        self.text_color = scene.theme["text-color"]
        self.border_color = scene.theme["border-color"]
        self.set_flag(self.flags.SHOW_BORDER)
    
    def on_hover(self):
        self.border_color = self.scene.theme["hover-color"]

    def on_unhover(self):
        self.border_color = self.scene.theme["border-color"]

    def on_update(self, events):
        self.text = f"{self.scene.tilemap.tile_size[0]}x{self.scene.tilemap.tile_size[1]}"

class FooterMapSize(box.resource.BOXlabel):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            scene.cache.get_font("slkscr"),
            text=f"{scene.tilemap.grid_size_raw[0]}x{scene.tilemap.grid_size_raw[1]}",
            text_pos = [4, 0],
            size=[140, 16],
            flags=box.resource.BOXelement.flags.SHOW_TEXT
        )
        self.pos = [8, 72]
        self.color = scene.theme["base-color"]
        self.text_color = scene.theme["text-color"]
        self.border_color = scene.theme["border-color"]
        self.set_flag(self.flags.SHOW_BORDER)
    
    def on_hover(self):
        self.border_color = self.scene.theme["hover-color"]

    def on_unhover(self):
        self.border_color = self.scene.theme["border-color"]
        
    def on_update(self, events):
        self.text = f"{self.scene.tilemap.grid_size_raw[0]}x{self.scene.tilemap.grid_size_raw[1]}"

class Footer(box.resource.BOXlabel):
    def __init__(self, scene) -> None:
        super().__init__(
            scene.cache.get_font("slkscr"),
            text="WorldForge",
            text_pos=[8, 8],
            size=[scene.app.window.screen_size[0], 100],
            flags=box.resource.BOXelement.flags.SHOW_TEXT
        )
        self.sections: int = 5

        self.color = scene.theme["base-color"]
        self.text_color = scene.theme["text-color"]
        self.border_color = scene.theme["border-color"]
        self.pos = [0, scene.app.window.screen_size[1]-100]

        self.set_flag(self.flags.SHOW_BORDER)

        # section 1 | forge info
        self.set_element("clock", FooterClock(scene))
        self.set_element("tilesize", FooterTileSize(scene))
        self.set_element("mapsize", FooterMapSize(scene))

        # section 2 | map info

    # def on_render(self, surface):
    #     for i in range(1, self.sections+1):
    #         box.utils.draw_line(
    #             width=2,
    #             surface=surface,
    #             color=[0, 255, 0],
    #             start=[i * self.get_element("mapsize").size[0] + 16, 0],
    #             end=[i * self.get_element("mapsize").size[0] + 16, 100]
    #         )
 