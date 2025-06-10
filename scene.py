from globs import box, pg
from ui import ToolsPane, Footer, TileView

class Editor(box.scene.BOXscene):
    def __init__(self, wf) -> None:
        super().__init__(app=wf)

    def init(self):
        # SAVE STATE
        self.export_grid: bool = False

        # MAP SETTINGS
        self.map_name: str = "Map2"
        self.map_path: str = "assets/map"

        # EDITOR STATE
        self.tile_id = 0
        self.tileset_id = 0
        self.map_loaded: bool = 0
        self.map_pos: list[float] = [0.0, 0.0]

        self.interface.set_element("footer", Footer(self))
        self.interface.set_element("tools", ToolsPane(self))
        
        self.renderer.set_flag(self.renderer.flags.DEBUG_TILEMAP)

    def exit(self): pass

    def events(self):
        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement):
            self.camera.mod_viewport(-2 * self.app.events.mouse_wheel_up)
            self.camera.mod_viewport(2 * self.app.events.mouse_wheel_down)

        if self.app.events.key_pressed(box.app.BOXkeyboard.F1):
            self.tilemap.export_data(self.map_name, self.map_path)
        
        if self.app.events.key_pressed(box.app.BOXkeyboard.F2):
            self.tilemap.import_data(self.map_name, self.map_path)
            self.interface.set_element("tileview", TileView(self))

        if self.app.events.key_pressed(box.app.BOXkeyboard.F3):
            self.tilemap.export_surface(self.map_name, self.map_path, self.export_grid)

        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement) and self.app.events.mouse_held(box.app.BOXmouse.LeftClick):
            self.tilemap.set_tile("bg", box.app.BOXmouse.pos.view, self.tile_id, self.tileset_id)

        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement) and self.app.events.mouse_held(box.app.BOXmouse.RightClick):
            self.tilemap.rem_tile("bg", box.app.BOXmouse.pos.view)

    def update(self, dt: float) -> None:
        self.cache.update_animation("load-anim", dt)

    def render(self) -> None:
        for tile in self.tilemap.all_tiles("bg"):
            self.renderer.commit_surface(tile.surface, tile.pos)
