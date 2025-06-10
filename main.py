from globs import box, json
import scene, version

class Worldforge(box.app.BOXapp):
    def __init__(self) -> None:
        if self._load_settings():
            super().__init__(
                title=f"WorldForge {version.WF_YEAR}.{version.WF_MINOR}.{version.WF_PATCH}-alpha",
                clear_color=[202, 202, 202],
                screen_size=self.settings["app"]["ws"],
                display_size=self.settings["app"]["ds"],
            )
        else: self.exit()

    def _load_settings(self) -> bool:
        self.settings = None
        with open(box.utils.rel_path("data/settings.json"), "r") as f:
            try:
                self.settings = json.load(f)
            except json.JSONDecodeError as e:
                box.BOXlogger.error("[Worldforge] failed to load app settings...")
                return False
        box.BOXlogger.debug("[Worldforge] the forge brightens...")
        return True

    def init(self) -> None:
        self.cache.load_font("slkscr", box.utils.rel_path("assets/fonts/slkscr.ttf"), 18)
        self.cache.load_surface("logo", box.utils.rel_path("assets/images/wf3/Logo.ico"))
        
        self.cache.load_surface("draw", box.utils.rel_path("assets/images/icon/Draw.png"))
        self.cache.load_surface("fill", box.utils.rel_path("assets/images/icon/Fill.png"))
        self.cache.load_surface("eraser", box.utils.rel_path("assets/images/icon/Eraser.png"))
        
        self.cache.load_animation("load-anim", box.utils.rel_path("assets/images/icon/Loading.png"), [16, 16], 11)
        self.window.mod_icon(self.cache.get_surface("logo"))
        
        self.add_scene("Editor", scene.Editor)
        self.set_scene("Editor")

    def exit(self) -> None:
        box.BOXlogger.debug("[Worldforge] the forge darkens...")

Worldforge().run()