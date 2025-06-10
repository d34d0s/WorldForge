from globs import box, pytz, pg
from datetime import datetime

class Tile(box.resource.BOXlabel):
    def __init__(self, key, id, scene, icon, size, font) -> None:
        self.id: int = id
        self.scene = scene
        self.key: str = key
        super().__init__(
            icon=icon,
            size=size,
            font=font
        )
        print(self.icon)

    def on_click(self):
        self.scene.tile_id = self.id
    
    def on_hover(self):
        self.border_color = pg.Surface.get_at(self.icon, [0, 0])
    
    def on_unhover(self):
        self.border_color = [0, 0, 0]

class TileView(box.resource.BOXscrollview):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            speed=scene.tilemap.tile_size[0]//8,
            size=[96, 256],
            color=[100, 100, 100],
            border_color=[255, 0, 0],
            wrap_x=96/scene.tilemap.tile_size[0],
            wrap_y=256/scene.tilemap.tile_size[1],
            pos=[0, scene.app.window.screen_size[1]/2.8],
        )

        # size of viewport tiles, not editor size
        self.tileset_id: int = self.scene.tileset_id
        self.tile_count: int = len(scene.tilemap.tilesets[self.tileset_id][1])
        self.tile_size: list[int] = [*map(lambda t: t* 2 if t < 16 else t, scene.tilemap.tile_size)]
        self.tiles: int = [pg.transform.scale(tile, self.tile_size) for tile in scene.tilemap.tilesets[self.tileset_id][1]]
    
        self.load_tiles()

    def load_tiles(self, tileset_id: int=0) -> None:
        self.tileset_id = tileset_id
        self.tiles = self.scene.tilemap.tilesets[self.tileset_id][1]
        self.tile_count = len(self.scene.tilemap.tilesets[self.tileset_id][1])
        self.tile_size = [*map(lambda t: t* 2 if t < 16 else t, self.scene.tilemap.tile_size)]
        self.tiles = [pg.transform.scale(tile, self.tile_size) for tile in self.scene.tilemap.tilesets[self.tileset_id][1]]

        for i, t in enumerate(self.tiles):
            key = f"tile{i}"
            self.set_element(key, Tile(
                id=i,
                key=key,
                scene=self.scene,
                icon=self.tiles[i],
                size=self.tile_size,
                font=self.scene.cache.get_font("slkscr")
            ))


class ToolButton(box.resource.BOXelement):
    def __init__(self, scene, _type: str, pos: list[int]) -> None:
        self.scene = scene
        super().__init__(
            pos=pos[:],
            color=[50, 50, 50],
            size=[18*3.5, 16],
            border_color = [0, 0, 0]
        )

        self._type = _type
        self.icon_pos = [18, 0]

        if self._type.lower() == "draw":
            self.tile_id = 2
        if self._type.lower() == "eraser":
            self.tile_id = 0
        if self._type.lower() == "fill":
            self.tile_id = 3

    def on_hover(self) -> None:
        if self.scene.tile_id == self.tile_id:
            self.border_color = [0, 255, 0]
        else:
            self.border_color= [255, 0, 0]

    def on_unhover(self) -> None:
        self.border_color = [0, 0, 0]

    def on_click(self) -> None:
        self.border_color = [0, 255, 0]
        self.scene.tile_id = self.tile_id

    def on_render(self, surface):
        surface.blit(self.scene.cache.get_surface(self._type), self.icon_pos)
        
class ToolsPane(box.resource.BOXlabel):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            scene.cache.get_font("slkscr"),
            text="tools",
            size=[96, 256],
            text_pos=[14, 0],
            flags=box.resource.BOXelement.flags.SHOW_TEXT
        )
        
        self.pos=[scene.app.window.screen_size[0]-96, scene.app.window.screen_size[1]/2.8]
        self.color= [100, 100, 100]

        self.border_size = [2, 2]
        self.border_color = [0, 0, 0]

        self.set_element("red-btn", ToolButton(scene, "draw", [16, 32]))
        self.set_element("green-btn", ToolButton(scene, "eraser", [16, 64]))
        self.set_element("blue-btn", ToolButton(scene, "fill", [16, 96]))


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
        self.color = [255, 255, 255]
        self.set_flag(self.flags.SHOW_BORDER)

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
        self.color = [255, 255, 255]
        self.set_flag(self.flags.SHOW_BORDER)
    
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
        self.color = [255, 255, 255]
        self.set_flag(self.flags.SHOW_BORDER)

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
        self.color = [100, 100, 100]
        self.pos = [0, scene.app.window.screen_size[1]-100]

        self.set_flag(self.flags.SHOW_BORDER)
        self.set_element("clock", FooterClock(scene))
        self.set_element("tilesize", FooterTileSize(scene))
        self.set_element("mapsize", FooterMapSize(scene))

 