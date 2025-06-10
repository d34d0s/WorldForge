from globals import box

class ToolButton(box.resource.BOXelement):
    def __init__(self, scene, _type: str, pos: list[int]) -> None:
        self.scene = scene
        super().__init__(
            pos=pos[:],
            size=[18*3.5, 16],
            color=scene.theme["base-color"],
            border_color=scene.theme["border-color"]
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
            self.border_color = self.scene.theme["select-color"]
        else:
            self.border_color= self.scene.theme["deselect-color"]

    def on_unhover(self) -> None:
        self.border_color = self.scene.theme["border-color"]

    def on_click(self) -> None:
        self.scene.tile_id = self.tile_id
        self.border_color = self.scene.theme["select-color"]

    def on_render(self, surface):
        surface.blit(self.scene.cache.get_surface(self._type), self.icon_pos)
        
class ToolBar(box.resource.BOXlabel):
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
        self.color= self.scene.theme["base-color"]

        self.border_size = [2, 2]
        self.border_color = self.scene.theme["border-color"]

        self.set_element("red-btn", ToolButton(scene, "draw", [16, 32]))
        self.set_element("green-btn", ToolButton(scene, "eraser", [16, 64]))
        self.set_element("blue-btn", ToolButton(scene, "fill", [16, 96]))
