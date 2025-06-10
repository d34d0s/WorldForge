from globals import box, json
import editor, version

class Worldforge(box.app.BOXapp):
    def __init__(self) -> None:
        if self._load_settings():
            super().__init__(
                title=f"WorldForge {version.WF_YEAR}.{version.WF_MINOR}.{version.WF_PATCH}-alpha",
                clear_color=self.theme["clear-color"],
                screen_size=self.settings["app"]["ws"],
                display_size=self.settings["app"]["ds"],
            )
        else: self.exit()

    @box.utils.BOXprofile
    def _load_settings(self) -> bool:
        self.theme: dict = None
        self.settings: dict = None
        with open(box.utils.rel_path("external/data/settings.json"), "r") as settings:
            try:
                # load settings
                self.settings = json.load(settings)
            
                # load theme
                with open(box.utils.rel_path(f"external/data/themes/{self.settings['app']['theme']}.json"), "r") as theme:
                    self.theme = json.load(theme)
            except json.JSONDecodeError as e:
                box.BOXlogger.error("[Worldforge] failed to load app settings...")
                return False
        box.BOXlogger.debug("[Worldforge] the forge brightens...")
        return True

    @box.utils.BOXprofile
    def init(self) -> None:
        self.cache.load_font("slkscr", box.utils.rel_path("external/data/assets/fonts/slkscr.ttf"), 18)
        self.cache.load_surface("logo", box.utils.rel_path("external/data/assets/images/wf3/Logo.ico"))
        
        self.cache.load_surface("draw", box.utils.rel_path("external/data/assets/images/icon/Draw.png"))
        self.cache.load_surface("fill", box.utils.rel_path("external/data/assets/images/icon/Fill.png"))
        self.cache.load_surface("eraser", box.utils.rel_path("external/data/assets/images/icon/Eraser.png"))
        
        self.cache.load_animation("load-anim", box.utils.rel_path("external/data/assets/images/icon/Loading.png"), [16, 16], 11)
        self.window.mod_icon(self.cache.get_surface("logo"))
        
        self.add_scene("editor", editor.Editor)
        self.set_scene("editor")

    def exit(self) -> None:
        box.BOXlogger.debug("[Worldforge] the forge darkens...")

Worldforge().run()