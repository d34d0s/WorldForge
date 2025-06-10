from globals import box, pg

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

        self.color = scene.theme["base-color"]
        self.text_color = scene.theme["text-color"]
        self.border_color = scene.theme["border-color"]

    def on_click(self):
        self.scene.tile_id = self.id
        self.border_color = self.scene.theme["select-color"]
    
    def on_hover(self):
        if self.scene.tile_id == self.id:
            self.border_color = self.scene.theme["select-color"]
        else:
            self.border_color= self.scene.theme["deselect-color"]
    
    def on_unhover(self):
        self.border_color = self.scene.theme["border-color"]

class TileBar(box.resource.BOXscrollview):
    def __init__(self, scene) -> None:
        self.scene = scene
        super().__init__(
            speed=scene.tilemap.tile_size[0]//8,
            size=[96, 256],
            wrap_x=96/scene.tilemap.tile_size[0],
            wrap_y=256/scene.tilemap.tile_size[1],
            pos=[0, scene.app.window.screen_size[1]/2.8],
        )

        self.color = scene.theme["base-color"]
        self.border_color = scene.theme["border-color"]

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
