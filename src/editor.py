from globals import box, pg

from ui.footer import Footer
from ui.toolbar import ToolBar
from ui.tilebar import TileBar

class Editor(box.scene.BOXscene):
    def __init__(self, wf) -> None:
        super().__init__(app=wf)

    def init(self):
        # SAVE STATE
        self.export_grid: bool = False

        # MAP SETTINGS
        self.map_name: str = "Map2"
        self.map_path: str = "external/data/assets/map"

        # EDITOR STATE
        self.tile_id = 0
        self.tileset_id = 0
        self.tile_layer: str = "bg"
        
        self.map_loaded: bool = 0
        self.tilebar_loaded: bool = 0

        self.theme: dict = self.app.theme
        self.map_pos: list[float] = [0.0, 0.0]

        # SCENE CONFIG
        self.interface.set_element("footer", Footer(self))
        self.interface.set_element("tools", ToolBar(self))

        self.renderer.set_flag(self.renderer.flags.DEBUG_TILEMAP)
        self.render_range_clamp: callable = lambda v: box.utils.clamp(v, int(self.tilemap.grid_size[0] / 2), self.tilemap.grid_size[0])

    def exit(self): pass

    def events(self):
        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement):
            self.camera.mod_viewport(-2 * self.app.events.mouse_wheel_up)
            self.camera.mod_viewport(2 * self.app.events.mouse_wheel_down)

        if self.app.events.key_pressed(box.app.BOXkeyboard.F1):
            self.tilemap.export_data(self.map_name, self.map_path)
        
        if self.app.events.key_pressed(box.app.BOXkeyboard.F2):
            if self.tilemap.import_data(self.map_name, self.map_path):
                self.tilemap.grid_color = self.theme["grid-color"]
                self.map_loaded = True
            
        if self.app.events.key_pressed(box.app.BOXkeyboard.F3):
            self.tilemap.export_surface(self.map_name, self.map_path, self.export_grid)
        
        if self.app.events.key_pressed(box.app.BOXkeyboard.F5):
            self.map_loaded = False
            self.tilemap.clear()

        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement) and self.app.events.mouse_held(box.app.BOXmouse.LeftClick):
            self.tilemap.set_tile(self.tile_layer, box.app.BOXmouse.pos.view, self.tile_id, self.tileset_id)

        if not isinstance(box.app.BOXmouse.Hovering, box.resource.BOXelement) and self.app.events.mouse_held(box.app.BOXmouse.RightClick):
            self.tilemap.rem_tile(self.tile_layer, box.app.BOXmouse.pos.view)

    def update(self, dt: float) -> None:
        if self.map_loaded and not self.tilebar_loaded:
            self.interface.set_element("tilebar", TileBar(self))
            self.tilebar_loaded = 1
        elif not self.map_loaded:
            self.interface.rem_element("tilebar")
            self.tilebar_loaded = 0

        self.cache.update_animation("load-anim", dt)

    def render(self) -> None:
        box.BOXlogger.DEBUG_MODE = 0
        self.render_range = [
            int(self.tilemap.grid_size[0] / self.camera.viewport_scale[0]),
            int(self.tilemap.grid_size[1] / self.camera.viewport_scale[1])
        ]
        self.render_range = [*map(self.render_range_clamp, self.render_range)]

        # for tile in self.tilemap.all_tiles(self.tile_layer):
        for tile in self.tilemap.get_tile_region(self.tile_layer, self.render_range, self.camera.pos):
            self.renderer.commit_surface(tile.surface, tile.pos)
        box.BOXlogger.DEBUG_MODE = 1
