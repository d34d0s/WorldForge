#  WorldForge ©️
#  Level/Map Editor
#  2023-2024 Setoichi Yumaden <setoichi.dev@gmail.com>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.

from PyForge import pg
from tkinter import filedialog
import json, os, tkinter as tk, sys, datetime, pytz, PyForge as Hue, uuid

ON = True
OFF = False
NULL = None
TAB_MIN = 305
TAB_GAP = 160
ZOOM_MIN = .34
ZOOM_MAX = 1.0
TAB_MAX = 1525
FONT = "..\\assets\\fonts\\slkscr.ttf"

COMMANDS = {
    "PLACE TILE": "001",
    "ERASE TILE": "002",
    "FILL": "003",
    "REMSELECT": "004",
}

defaultTrigger =  { "OnFirstPass": False, "OnFullPass": False }

defaultProps = {
    "collisions": False
}

class Command:
    def __init__(self, forge, mapObj):
        self.forge = forge
        self.type = None
        self._map = mapObj

    def Execute(self):
        pass

    def Undo(self):
        pass

EST_ZONE = pytz.timezone("US/Eastern")
TIME_FORMAT = (
    "%I:%M %p"  # %I for 12-hour format, %M for minutes, %p for AM/PM
)

def Hue_IsSurfaceBlank(surface:pg.Surface):
    for x in range(surface.get_width()):
        for y in range(surface.get_height()):
            if surface.get_at((x, y))[3] != 0:
                return False
    return True

class Bindings:
    Swap = Hue.Keyboard.S
    Draw = Hue.Keyboard.D
    Fill = Hue.Keyboard.F
    Save = Hue.Keyboard.F1
    Props = Hue.Keyboard.P
    Select = Hue.Keyboard.M
    Eraser = Hue.Keyboard.E
    Close = Hue.Keyboard.F12
    Import = Hue.Keyboard.F3
    NewMap = Hue.Keyboard.F4
    Export = Hue.Keyboard.F2
    HideView = Hue.Keyboard.T
    LastView = Hue.Keyboard.C
    NextView = Hue.Keyboard.V
    ZoomIn = Hue.Mouse.WheelUp
    ToggleGrid = Hue.Keyboard.G
    Drag = Hue.Mouse.WheelClick
    Escape = Hue.Keyboard.Escape
    ExportPNG = Hue.Keyboard.F12
    ZoomOut = Hue.Mouse.WheelDown
    NewLayer = Hue.Keyboard.F7
    RemLayer = Hue.Keyboard.F8
    DumpLayer = Hue.Keyboard.F6
    LastLayer = Hue.Keyboard.Left
    NextLayer = Hue.Keyboard.Right
    LastBaseLayer = Hue.Keyboard.Up
    NextBaseLayer = Hue.Keyboard.Down
    ToggleToolBar = Hue.Keyboard.B
    ToggleLayerMenu = Hue.Keyboard.L
    ToggleInterface = Hue.Keyboard.F11
KeyBinds = Bindings()

class Storage:
    images: dict = {}
    sounds: dict = {}

    @classmethod
    def StoreImage(cls, key:str, image: pg.Surface = None, path: str = None) -> bool:
        stored: bool = False
        if isinstance(image, pg.Surface):
            cls.images[key] = image
            stored = True
        elif isinstance(path, str):
            try:
                image = Hue.loadSurface(path)
                cls.images[key] = image
                stored = True
            except FileNotFoundError:
                pass
        return stored

    @classmethod
    def StoreSound(cls, key:str, path: str) -> bool:
        stored: bool = False
        if isinstance(path, str):
            try:
                sound = pg.mixer.Sound(path)
                cls.sounds[key] = sound
                stored = True
            except FileNotFoundError:
                pass
            except pg.error as e:
                print(f"Error loading sound: {e}")
        return stored

    @classmethod
    def GetImage(self, key:str) -> pg.Surface|None:
        try:
            image = self.images[key]
        except (KeyError):
            image = None
        return image
    
    @classmethod
    def GetSound(self, key:str) -> pg.mixer.Sound|None:
        try:
            sound = self.sounds[key]
        except (KeyError):
            sound = None
        return sound

class ProgressBar:
    def __init__(self, position, dimensions, color, background_color):
        self.position = position
        self.dimensions = dimensions
        self.color = color
        self.background_color = background_color
        self.progress = 0  # Represents progress as a percentage (0-100)
        self.load1 = pg.Surface((0,0))

    def Update(self, progress):
        self.progress = progress

    def Draw(self, surface):
        # Draw the background
        bg_rect = pg.Rect(self.position, self.dimensions)
        pg.draw.rect(surface, self.background_color, bg_rect)

        # Draw the progress bar
        if (self.progress >= 20.0):
            nc = self.color
            if (nc[0] + 1 > 0 and nc[0] + 1 < 255): nc[0] += .1
            if (nc[1] - .5 > 0 and nc[1] - .5 < 255): nc[1] += .1
            self.color = nc
        if (self.progress >= 50.0):
            nc = self.color
            if (nc[0] - .5 > 0 and nc[0] - .5 < 255): nc[0] -= .5
            if (nc[1] - .5 > 0 and nc[1] - .5 < 255): nc[1] -= .2
            if (nc[2] + 1 > 0 and nc[2] + 1 < 255): nc[2] += .2
            self.color = nc
        if (self.progress >= 70.0):
            nc = self.color
            if (nc[0] + 1 > 0 and nc[0] + 1 < 255): nc[0] += .5
            if (nc[1] + .5 > 0 and nc[1] + .5 < 255): nc[1] += .5
            if (nc[2] + 1 > 0 and nc[2] + 1 < 255): nc[2] -= .5
            self.color = nc
        progress_width = (self.progress / 100) * self.dimensions[0]
        progress_rect = pg.Rect(self.position, (progress_width, self.dimensions[1]))
        self.load1 = pg.Surface((progress_rect.w, progress_rect.h))
        self.load1.fill(self.color)
        surface.blit(self.load1, progress_rect, )

class Cursor(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, image:pg.Surface, group:pg.sprite.Group):
        super().__init__(group)
        self.forge = forge
        self.image = image
        self.position= Hue.Vector2()
        self.rect = pg.Rect(self.position, (0,0))

    def Update(self):
        self.position = Hue.getMousePosition()
        self.position = Hue.Vector2(self.position.x - 8, self.position.y - 8)
        self.rect = pg.Rect(self.position, (16,16))

class Sheet(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, size:list|Hue.Vector2=[ 200, 400 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.size = size
        self.image = pg.Surface(self.size)
        self.image.fill( [255, 255, 255] )
        self.position = Hue.Vector2( 100, 100 )
        self.rect = pg.Rect(self.position, self.size)

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class RemoveSelectionCommand(Command):
    def __init__(self, forge, mapObj, layer, subLayer, selection):
        super().__init__(forge, mapObj)
        self.layer = layer
        self.subLayer = subLayer
        self.type = COMMANDS["REMSELECT"]
        self.selection = selection
        self._pos = None
        self.tileID = None
        self.removedTiles = {}  # Dictionary to store removed tiles' positions and data

    def Execute(self):
        if (self.selection):
            startX = self.selection.left // self._map.tileSize
            endX = (self.selection.right + self._map.tileSize) // self._map.tileSize
            startY = self.selection.top // self._map.tileSize
            endY = (self.selection.bottom + self._map.tileSize) // self._map.tileSize

            for x in range(startX, endX):
                for y in range(startY, endY):
                    tilePos = Hue.Vector2(x * self._map.tileSize, y * self._map.tileSize)
                    tileKey = f"{int(tilePos.x)};{int(tilePos.y)}"
                    self._pos = Hue.Vector2(*map(int, tileKey.split(';')))

                    
                    if (tileKey in self._map.data[self._map.forge.state.layer] and tileKey not in self.removedTiles):
                        # Store the original tile data before removal
                        self.removedTiles[tileKey] = self._map.data[self._map.forge.state.layer][tileKey]
                        # Remove the tile
                        self._map.RemTile(self._pos, self.layer, self.subLayer)

    def Undo(self):
        # Restore all removed tiles
        for tileKey, tileData in self.removedTiles.items():
            if (tileData):
                self.tileID = tileData["id"]
                self._pos = Hue.Vector2(*map(int, tileKey.split(';')))
                self._map.data[self._map.forge.state.layer][tileKey] = tileData
                self._map.PlaceTile(self._pos, tileKey, tileData["id"], self.layer, self.subLayer)
                self._map.WriteData_Tile(self._pos, self.tileID, self.layer, self.subLayer)

class FillCommand(Command):
    def __init__(self, forge, mapObj, layer, subLayer, start_pos, tileID, selection=None):
        super().__init__(forge, mapObj)
        self.layer = layer
        self.subLayer = subLayer
        self.type = COMMANDS["FILL"]
        self._pos = start_pos
        self.tileID = tileID
        self.selection = selection
        self.filledTiles = []  # List to store positions of filled tiles

    def Execute(self):
        queue = [self._pos]
        visited = set()

        while queue:
            current_pos = queue.pop(0)
            tileKey = f"{int(current_pos.x)};{int(current_pos.y)}"

            if self.selection:
                if not (self.selection.left <= current_pos.x <= self.selection.right and self.selection.top <= current_pos.y <= self.selection.bottom):
                    continue
            elif not (0 <= current_pos.x < self._map.size[0] and 0 <= current_pos.y < self._map.size[1]):
                continue

            if tileKey in self._map.data[self._map.forge.state.layer] or tileKey in visited:
                continue

            # Fill the tile and mark as visited
            self._map.PlaceTile(current_pos, tileKey, self.tileID, self.layer, self.subLayer)
            self._map.WriteData_Tile(current_pos, self.tileID, self.layer, self.subLayer)
            self.filledTiles.append(current_pos)
            visited.add(tileKey)

            # Add neighboring tiles to the queue
            neighbors = [Hue.Vector2(current_pos.x + self._map.tileSize, current_pos.y), Hue.Vector2(current_pos.x - self._map.tileSize, current_pos.y),
                        Hue.Vector2(current_pos.x, current_pos.y + self._map.tileSize), Hue.Vector2(current_pos.x, current_pos.y - self._map.tileSize)]
            queue.extend(neighbors)

    def Undo(self):
        batch = []
        for pos in self.filledTiles:
            batch.append(pos)
            if len(batch) == 50:  # Process the batch when it reaches 50 tiles
                self._map.RemTileBatch(batch, self.layer, self.subLayer)
                batch.clear()

        if batch:  # Process any remaining tiles in the batch
            self._map.RemTileBatch(batch, self.layer, self.subLayer)

class EraseCommand(Command):
    def __init__(self, forge, mapObj, layer, subLayer, pos):
        super().__init__(forge, mapObj)
        self.layer = layer
        self.subLayer = subLayer
        self._pos = pos
        self.type = COMMANDS["ERASE TILE"]
        self.tileID = f"{int(pos.x)};{int(pos.y)}"
        self._prevTileData = None

    def Execute(self):
        # Capture the tile data before erasing for undo
        prevData = self._map.data.get(self.layer, {}).get(self.tileID, None)
        if (prevData and self.tileID in self._map.data[self.layer] and prevData["subLayer"] == self.subLayer):
            self._prevTileData = prevData
            # Erase the tile by removing its data
            tile = self._map.GetTile(self._pos, self.layer)
            if (tile and tile["subLayer"] == self.subLayer):
                self._map.RemTile(self._pos, self.layer, self.subLayer)

    def Undo(self):
        if self._prevTileData:
            # Restore the erased tile using the captured data
            self._map.data[self._prevTileData["layer"]][self.tileID] = self._prevTileData
            tileID = self._prevTileData["id"]
            tile = self._map.GetTile(self._pos, self.layer)
            if (tile and tile["subLayer"] == self.subLayer):
                self._map.PlaceTile(self._pos, self.tileID, tileID, self._prevTileData["layer"], self._prevTileData["subLayer"])
                self._map.WriteData_Tile(self._pos, tileID, self._prevTileData["layer"], self._prevTileData["subLayer"])

class PlaceTileCommand(Command):
    def __init__(self, forge, mapObj, layer, subLayer, pos, tileID, corrupt=False):
        super().__init__(forge, mapObj)
        self.layer = layer
        self.subLayer = subLayer
        self._pos = pos
        self.tileID = tileID
        self.corrupt = corrupt
        self.type = COMMANDS["PLACE TILE"]
        self._tileKey = f"{int(pos.x)};{int(pos.y)}"
        self._prevTileData = None

    def Execute(self):
        # Capture previous tile data for undo
        prevData = self._map.data.get(self.layer, {}).get(self._tileKey, None)
        if (prevData and prevData["id"] != self.tileID):
            self._prevTileData = prevData
        elif (prevData and prevData["id"] == self.tileID):
            asset = self._map.data.get(self.layer, {}).get(self._tileKey, None)["asset"]
            if(prevData["asset"] != asset):
                self._prevTileData = prevData
        
        # Place the tile visually
        self._map.PlaceTile(self._pos, self._tileKey, self.tileID, self.layer, self.subLayer, corrupt=self.corrupt)
        
        # Write the tile data
        self._map.WriteData_Tile(self._pos, self.tileID, self.layer, self.subLayer)

        tileProperties = self._map.data[self.layer][self._tileKey]["properties"]
        if(tileProperties["collisions"]): 
            self._map.AddColliderAt(self._pos)

    def Undo(self):
        if (self._prevTileData and self._prevTileData["subLayer"] == self.subLayer):
            # Restore previous tile data if it exists
            self._map.data[self.layer][self._tileKey] = self._prevTileData
            # Place the tile visually
            self._map.PlaceTile(self._pos, self._tileKey, self._prevTileData["id"], self._prevTileData["layer"], self._prevTileData["subLayer"], corrupt=self.corrupt)
            
            # Write the tile data
            self._map.WriteData_Tile(self._pos, self._prevTileData["id"], self._prevTileData["layer"], self._prevTileData["subLayer"])

            if(self._prevTileData["properties"]["collisions"]):
                self._map.AddColliderAt(self._pos)
        else:
            # Remove the tile if there was no previous data
            self._map.RemTile(self._pos, self.layer, self.subLayer)
                
class Map(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, name:str, path:str, tileSize:int, size:list|Hue.Vector2=[ 200, 400 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.saved = False
        self.name = name
        self.size = size
        self.path = path
        self.grid = None
        self.future = []
        self.history = []
        self.active = True
        self.rendered = False
        self.tileViews = {}
        self.showColliders = True
        self.tileSize = tileSize if tileSize >= 16 else 16
        self.tileSizeRAW = tileSize
        self.image = pg.Surface(self.size)
        self.image.fill( [255, 255, 255] )
        self.position = Hue.Vector2( 100, 100 )
        self.map = {"__data__": {"col,row": [0,0]}}
        self.rect = pg.Rect(self.position, self.size)
        
        self.colliders = {
            "background": {},
            "midground": {},
            "foreground": {}
        }
        self.colliderGroup = {
            "background": {},
            "midground": {},
            "foreground": {}
        }
        self.tiles:dict={
            "background": {},
            "midground": {},
            "foreground": {}
        }
        self.layers:dict[pg.sprite.Group]={
            "background": {
                0:pg.sprite.Group()
            },
            "midground": {
                0:pg.sprite.Group()
            },
            "foreground": {
                0:pg.sprite.Group()
            }
        }
        self.data:dict={
            "mapInfo": {
                "version": self.forge.config["forge info"]["version"],
                "name": self.name,
                "width/height": list(self.size),
                "tilesize": self.tileSizeRAW
            },
            "background": {},
            "midground": {},
            "foreground": {}
        }
        self.Configure()
        self.CreateGrid()

    def Configure(self):
        for col in range(int(self.size.x/self.tileSize)+1):
            self.map["__data__"]["col,row"][0] = col
            for row in range(int(self.size.y/self.tileSize)+1):
                self.map["__data__"]["col,row"][1] = row

    def GetTileID(self, pos):
        try:
            return self.tiles[self.forge.state.layer][pos][0]
        except (KeyError):
            #return"Error Getting Tile!\n"
            return None
    
    def GetTile(self, pos, layer):
        tile = None
        tileKey = f"{int(pos[0])};{int(pos[1])}"
        try:
            tile = self.data[layer][tileKey]
            return tile
        except:
            return tile
        
    def GetTileProps(self, pos, layer):
        props = None
        tileKey = f"{int(pos[0])};{int(pos[1])}"
        try:
            tile = self.data[layer][tileKey]
            props = tile["props"]
            return props
        except:
            return props

    def ExecuteCommand(self, command):
        command.Execute()
        if not any((c.tileID == command.tileID and c._pos == command._pos) for c in self.history):
            self.history.append(command)
        self.future.clear()

    def Undo(self):
        if (self.history):
            command = self.history.pop()
            if (command.subLayer == self.forge.state.layerState[self.forge.state.layer]): command.Undo()

            self.future.append(command)
            self.saved = False
            self.rendered = False
            
            #print(f"Current: {self.data}\nUndo: {self.history}\nRedo: {self.future}")

    def Redo(self):
        if (self.future):
            command = self.future.pop()
            if (command.subLayer == self.forge.state.layerState[self.forge.state.layer]): command.Execute()
            
            self.history.append(command)
            self.saved = False
            self.rendered = False
            
            #print(f"Current: {self.data}\nUndo: {self.history}\nRedo: {self.future}")

    def RemColliderAt(self, pos):
        tileKey = f"{int(pos[0])};{int(pos[1])}"
        layer = self.forge.state.layer
        tile = self.GetTile(pos, layer)
        subLayer = self.forge.state.layerState[self.forge.state.layer]
        if (
            tile and
            tileKey in self.data[layer] and 
            tileKey in self.tiles[layer] and 
            tile["subLayer"] == subLayer and
            tile["layer"] == layer and 
            tile["layer"] in self.colliders and 
            tileKey in self.colliders[tile["layer"]]
            ):
            self.colliderGroup[tile["layer"]][tileKey] = pg.sprite.Group()
            self.colliders[tile["layer"]].pop(tileKey)
            self.data[self.forge.state.layer][tileKey]["properties"] = {"collisions": False}
        else: return(f"\nERROR REMOVING COLLIDER AT {pos} LAYER {layer}")

    def AddColliderAt(self, pos):
        tileKey = f"{int(pos[0])};{int(pos[1])}"
        layer = self.forge.state.layer
        tile = self.GetTile(pos, layer)
        subLayer = self.forge.state.layerState[self.forge.state.layer]
        if (tile and tile["subLayer"] == subLayer):
            try:
                self.data[self.forge.state.layer][tileKey]["properties"] = {"collisions": True}
                
                collider = self.forge.storage.GetImage(self.forge.state.colliderColor)
                colliderSprite = Hue.Sprite()
                colliderSprite.image = Hue.scaleSurface(collider, [self.tileSize, self.tileSize])
                colliderSprite.rect = Hue.createRect(pos, [self.tileSize, self.tileSize])
                self.colliders[layer][tileKey] = colliderSprite
        
                if (tileKey not in self.colliderGroup[layer]):
                    self.colliderGroup[layer][tileKey] = pg.sprite.Group()

                self.colliderGroup[layer][tileKey].add(self.colliders[layer][tileKey])
        
                self.saved = False
                self.rendered = False
            except: return(f"\nERROR ADDING COLLIDER AT {pos}")

    def WriteData_Tile(self, pos:Hue.Vector2, tileID, layer, subLayer):
        if (len(self.tileViews)):
            tileKey = f"{int(pos[0])};{int(pos[1])}"
            tile = {}
            tile["id"] = tileID
            tile["subLayer"] = subLayer
            tile["layer"] = layer
            tile["properties"] = defaultProps
            tileAsset = self.tileViews[self.forge.state.view].path
            # tileAsset = os.path.basename(self.tileViews[self.forge.state.view].path) # no.. not yet...
            tile["asset"] = tileAsset

            self.data[layer][tileKey] = tile

    def PlaceTile(self, pos, key, tileID, layer, subLayer, corrupt=False):
        
        # Allow first time placement
        if (key not in self.tiles[layer]):
            rawTile = pg.sprite.Sprite()
            
            image = self.tileViews[self.forge.state.view].tile["images"][tileID] if not corrupt else self.forge.storage.GetImage("CorruptTile32")
            rawTile.image = Hue.scaleSurface(image, [self.tileSize, self.tileSize])
            rawTile.image.set_alpha(255)
            rawTile.rect = Hue.createRect(pos, [self.tileSize, self.tileSize])
        
            self.tiles[layer][key] = [tileID, rawTile]

        # Allow same layer overwrites
        elif (key in self.tiles[layer] and self.tiles[layer][key][0] != tileID):
            rawTile = pg.sprite.Sprite()
            
            image = self.tileViews[self.forge.state.view].tile["images"][tileID] if not corrupt else self.forge.storage.GetImage("CorruptTile32")
            rawTile.image = Hue.scaleSurface(image, [self.tileSize, self.tileSize])
            rawTile.image.set_alpha(255)
            rawTile.rect = Hue.createRect(pos, [self.tileSize, self.tileSize])

            self.layers[layer][subLayer].remove(self.tiles[layer][key][1])
            self.tiles[layer][key] = [tileID, rawTile]

        # Add tile to corresponding sprite group
        if (key in self.tiles[layer] and subLayer in self.layers[layer] and len(self.tiles[layer][key])):
            self.layers[layer][subLayer].add(self.tiles[layer][key][1])

        self.saved = False
        self.rendered = False

    def RemTileBatch(self, positions, layer, subLayer):
        for pos in positions:
            tileKey = f"{int(pos.x)};{int(pos.y)}"  # Assuming pos is a Hue.Vector2 object
            if (
                tileKey in self.data[layer] and 
                tileKey in self.tiles[layer] and 
                self.data[layer][tileKey]["subLayer"] == subLayer and
                self.data[layer][tileKey]["layer"] == layer
                ):
                if (self.data[layer][tileKey]["properties"]["collisions"]): self.RemColliderAt(pos)
                self.data[layer][tileKey] = "REM"
                # Consider if self.data = self.FilterData() can be optimized or moved outside the loop
                self.layers[layer][subLayer].remove(self.tiles[layer][tileKey][1])
                self.tiles[layer].pop(tileKey)
        self.rendered = False  # Set rendered to False after all tiles are processed
        self.data = self.FilterData()

    def RemTile(self, pos, layer, subLayer):
        try:
            tileKey = f"{int(pos[0])};{int(pos[1])}"
            if (
                tileKey in self.data[layer] and 
                tileKey in self.tiles[layer] and 
                self.data[layer][tileKey]["subLayer"] == subLayer and
                self.data[layer][tileKey]["layer"] == layer
                ):
                if (self.data[layer][tileKey]["properties"]["collisions"]): self.RemColliderAt(pos)
                self.data[layer][tileKey] = "REM"
                self.data = self.FilterData()
                self.layers[layer][subLayer].remove(self.tiles[layer][tileKey][1])
                self.tiles[layer].pop(tileKey)
                self.rendered = False
        except:
            return None

    def NewLayer(self, spec:str="background"):
        try:
            self.layers[spec][len(self.layers[spec])] = pg.sprite.Group()
            print(f"Added Layer {spec}: {len(self.layers[spec])}")
        except:
            print("Error Adding New Layer!\n")

    def RemLayer(self, spec:str="background", num:int=0):
        try:
            for tile in self.layers[spec][num].sprites():
                self.RemTile(tile.rect.topleft, spec, num)
            self.layers[spec][num].empty()
            self.layers[spec].pop(num)
            print(f"Removed Layer {spec}: {num}")
        except:
            print("Error Removing Layer!\n")
    
    def DumpLayer(self, spec:str="background", num:int=0):
        try:
            self.layers[spec][num].empty()
            print(f"Dumped Layer {spec}: {num}")
        except:
            print("Error Dumping Layer!\n")
    
    def DumpLayerALL(self, spec:str="background"):
        try:
            for layer in self.layers[spec]:
                self.layers[spec][layer].empty()
            print(f"Dumped-All Layer {spec}")
        except:
            print("Error Dump-All Layer!\n")

    def ImportData(self, mapData:dict):
        self.data = mapData

    def FilterData(self):
        data = self.data.copy()
        # List of layers to clean
        layers_to_clean = ["background", "midground", "foreground"]

        for layer in layers_to_clean:
            if layer in data:  # Check if the layer exists in the data
                # Filter out the 'REM' entries in the current layer
                data[layer] = {k: v for k, v in data[layer].items() if v != "REM"}

        return data

    def SaveData(self, name:str=None):
        if (name): self.name = name
        try:
            if (os.path.exists(self.path)):
                with open(f"{self.path}\\{self.name}.wf2", "w") as mapData:
                    data = self.FilterData()
                    json.dump(data, mapData, indent=3)
                    mapData.close()
            else:
                os.mkdir(self.path)
                with open(f"{self.path}\\{self.name}.wf2", "w") as mapData:
                    data = self.FilterData()
                    json.dump(data, mapData, indent=3)
                    mapData.close()
            print(f"Map Saved To {self.path}/{self.name}.wf2")
            self.saved = True
        except (FileNotFoundError):
            print("Path/File Doesnt Exist!\n")

    def ExportPNG(self, grid:bool=False):
        if (not grid):
            exportSurface = pg.Surface(self.size)
            exportSurface.fill((255, 255, 255))

            for layer in self.layers:
                for inLayer in self.layers[layer]:
                    self.layers[layer][inLayer].draw(exportSurface)

            exportFilename = f'{self.name}.png'
            fullExportPath = os.path.join(self.path, exportFilename)
            pg.image.save(exportSurface, fullExportPath)
        else:
            exportFilename = f'{self.name}.png'
            fullExportPath = os.path.join(self.path, exportFilename)
            pg.image.save(self.image, fullExportPath)
        print(f"Map exported as {fullExportPath}")

    def CreateGrid(self):
        cellSize = self.tileSize
        colRow = self.map["__data__"]["col,row"]

        self.grid = pg.sprite.Sprite()
        self.grid.image = pg.Surface(self.size)
        self.grid.image.set_colorkey([0,0,0])
        self.grid.image.fill([0,0,0])

        for col in range(int(colRow[0])+1):
            for row in range( int(colRow[1])+1):
                pg.draw.rect(self.grid.image, self.forge.theme["Grid"], pg.Rect((col*cellSize, row*cellSize), (cellSize, cellSize)), width=1)

    def RenderCursor_GridCell(self):
        cellSize = self.tileSize
        if (self.forge.CursorIsOn_Z(self)): pg.draw.rect(self.image, self.forge.theme["Hover"], pg.Rect(self.forge.CursorPosition_Map(self), (cellSize, cellSize)), width=1)

    def Render(self):
        if (not self.rendered):
            self.image.fill( [ 255, 255, 255 ] )
            for layer in self.layers:
                for inLayer in self.layers[layer]:
                    self.layers[layer][inLayer].draw(self.image)
                if (self.showColliders):
                    for tileKey in self.colliderGroup[layer]:
                        self.colliderGroup[layer][tileKey].draw(self.image)
            
            self.rendered = True
        if (self.grid and self.forge.state.grid): self.image.blit(self.grid.image, [0,0])
        self.RenderCursor_GridCell()

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class Header(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, logo:str, logoPosition:list|Hue.Vector2=[ 25, 15 ], position:list|Hue.Vector2=[ 0, 0 ], size:list|Hue.Vector2=[ 1400, 100 ], group:pg.sprite.Group=[], draggable:bool=False):
        super().__init__(group)
        self.forge = forge
        self.buttons = {}
        self.logoStr = logo
        self.visible:bool=True
        self.draggable = draggable
        self.size = Hue.Vector2(size)
        self.position = Hue.Vector2(position)
        self.image = pg.Surface(self.size)
        self.logoPosition = Hue.Vector2(logoPosition)
        self.rect = pg.Rect(self.position, self.size)
        self.logo:pg.Surface = self.forge.storage.GetImage(logo)

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Base"])
        self.logo:pg.Surface = self.forge.storage.GetImage(self.logoStr)
        self.image.blit(self.logo, self.logoPosition)

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class TileView(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, tileSize:int, position:list|Hue.Vector2=[ 0, 0 ], size:list|Hue.Vector2=[ 200, 400 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.path:str=None
        self.visible:bool=True
        self.size = Hue.Vector2(size)
        self.position = Hue.Vector2(position)
        self.image = pg.Surface(self.size)
        Hue.fillSurface(self.image, self.forge.theme["Base"])
        self.rect = pg.Rect(self.position, self.size)
        self.tile:dict={
            "size": 32,
            "sizeRAW": tileSize,
            "set": None,
            "images": [],
            "group": pg.sprite.Group()
        }
        self.data:dict={
            "scroll": 0,
            "hidden": False,
            "padding": Hue.Vector2(self.tile["sizeRAW"],self.tile["sizeRAW"]) if self.tile["sizeRAW"] < 16 else Hue.Vector2(self.tile["sizeRAW"]/2,self.tile["sizeRAW"]/2),
            "rowMax": None
        }
        self.data["rowMax"] = self.size[0] // (self.tile["size"] + self.data["padding"].x * 2)

    def LoadTileSet(self, path:str=None, tileSet:pg.Surface=None):
        ts = None
        self.path = path

        asset = os.path.basename(path)
        if (asset not in self.forge.registry["tilesets"]):
            self.forge.WriteToRegistry_Tilesets(asset, os.path.dirname(path))

        if (path and type(path) == str and not tileSet):
            try:
                ts = Hue.loadSurface(path)
            except (FileNotFoundError):
                pass
        if (tileSet and isinstance(tileSet, pg.Surface) and not path):
            ts = tileSet
        self.tile["set"] = ts

    def LoadTiles(self):
        if (self.tile["set"]):
            for tile in Hue.surfaceCutout(self.tile["set"], self.tile["sizeRAW"]):
                if (not Hue_IsSurfaceBlank(tile)): self.tile["images"].append(Hue.scaleSurface(tile, (self.tile["size"], self.tile["size"])))

    def HoverTile(self):
        # Adjust mousePos based on TileView's scroll and position
        relX, relY = (self.forge.cursor.position[0]+8) - self.position[0], (self.forge.cursor.position[1]+8) - self.position[1] + self.data["scroll"]
        
        # Calculate the column and row based on the mouse position
        col = (relX - self.data["padding"][0]) // (self.tile["size"] + self.data["padding"][0] * 2)
        row = (relY - self.data["padding"][1]) // (self.tile["size"] + self.data["padding"][1] * 2)

        # Calculate the top-left corner of the hovered tile's rectangle
        tileX = self.data["padding"][0] + col * (self.tile["size"] + self.data["padding"][0] * 2)
        tileY = self.data["padding"][1] + row * (self.tile["size"] + self.data["padding"][1] * 2) - self.data["scroll"]

        # Calculate the index of the hovered tile
        index = row * self.data["rowMax"] + col
        if (0 <= index < len(self.tile["images"])):
            hoveredTile = pg.Rect(tileX, tileY, self.tile["size"]+2, self.tile["size"]+2)
            pg.draw.rect(self.image, self.forge.theme["Hover"], hoveredTile, width=2)
    
    def SetUpTiles(self):
        self.tile["group"].empty()
        tile_x = self.data["padding"][0]
        tile_y = self.data["padding"][1] - self.data["scroll"]
        for index, tile in enumerate(self.tile["images"]):
            if tile_y + self.tile["size"] <= self.size[1]:  # Only draw visible tiles
                tile_rect = Hue.createRect([tile_x, tile_y], [self.tile["size"], self.tile["size"]])
                tileSprite = pg.sprite.Sprite(self.tile["group"])
                tileSprite.rect = tile_rect
                tileSprite.image = pg.Surface((self.tile["size"] + 2, self.tile["size"] + 2))
                tileSprite.image.set_colorkey([1,1,1])
                tileSprite.image.fill([1,1,1])
                Hue.drawRect(tileSprite.image, tileSprite.image.get_rect(),self.forge.theme["Trim"],width=1)
                tileSprite.image.blit(tile,[1,1])
            tile_x += self.tile["size"] + self.data["padding"][0] * 2  # Move to the next tile position
            if (index + 1) % self.data["rowMax"] == 0:  # Wrap to the next row after filling the current row
                tile_y += self.tile["size"] + self.data["padding"][1] * 2
                tile_x = self.data["padding"][0]

    def Scroll(self, scroll_amount):
        max_scroll = (len(self.tile["images"]) // self.data["rowMax"] + 1) * (self.tile["size"] + self.data["padding"][1] * 2) - self.size[1]
        self.data["scroll"] += self.tile["size"] if scroll_amount > 0 else -self.tile["size"]
        self.data["scroll"] = max(0, min(self.data["scroll"], max_scroll))
        self.SetUpTiles()

    def Render(self):
        if (self.data["hidden"]): return
        Hue.fillSurface(self.image, self.forge.theme["Base"])
        self.SetUpTiles()
        self.tile["group"].draw(self.image)
        self.HoverTile()

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class Button(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, logo:str, text:str="Button", logoPosition:list|Hue.Vector2=[ 25, 15 ], position:list|Hue.Vector2=[ 0, 0 ], size:list|Hue.Vector2=[ 100, 50 ], fontSize:int=21, group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.fontSize = fontSize
        self.text = text
        self.logoStr = logo
        self.size = Hue.Vector2(size)
        self.image = pg.Surface(self.size)
        self.image.set_colorkey([1,1,1])
        self.image.fill([1,1,1])
        self.position = Hue.Vector2(position)
        self.rect = pg.Rect(self.position, self.size)
        self.logoPosition = Hue.Vector2(logoPosition)
        self.logo:pg.Surface = self.forge.storage.GetImage(logo)

    def CallBack(self):
        print("\nButton Callback!")

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Base"])
        if (self.text == ""):
            self.logo:pg.Surface = self.forge.storage.GetImage(self.logoStr)
            self.image.blit(self.logo, self.logoPosition)
        else: Hue.renderText(self.image, FONT, self.text, Hue.Vector2(self.size.x/2, self.size.y/2),size=self.fontSize)

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class ToolBar(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, position:list|Hue.Vector2=[ 1300, 300 ], size:list|Hue.Vector2=[ 100, 400 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.buttons = {}
        self.visible:bool=True
        self.size = Hue.Vector2(size)
        self.image = pg.Surface(self.size)
        self.position = Hue.Vector2(position)
        self.rect = pg.Rect(self.position, self.size)

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Base"])
    
    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class TextField(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, position:list|Hue.Vector2=[ 300, 300 ], offset:list|Hue.Vector2=[0,0],  size:list|Hue.Vector2=[ 200, 400 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.text = ""
        self.forge = forge
        self.active = False
        self.offset = offset
        self.size = Hue.Vector2(size)
        self.image = pg.Surface(self.size)
        self.position = Hue.Vector2(position)
        self.rect = pg.Rect(self.position, self.size)

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Background"])
    
    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class Menu(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, position:list|Hue.Vector2=[ 300, 300 ],size:list|Hue.Vector2=[ 400, 250 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.forge = forge
        self.fields = {}
        self.buttons = {}
        self.active:bool=True
        self.returned = False
        self.title = "WorldForge2"
        self.titlePosition = [4,4]
        self.size = Hue.Vector2(size)
        self.image = pg.Surface(self.size)
        self.position = Hue.Vector2(position)
        self.rect = pg.Rect(self.position, self.size)

    def HandleFileDrop(self, file_path) -> pg.Surface|None:
        try:
            image = pg.image.load(file_path)
            return image
        except pg.error:
            print(f"Failed to load image from: {file_path}")
            return None

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Base"])
    
    def HandleText(self, key):
        self.returned = False
        for label, field in self.fields.items():
            if field.active:
                if pg.key.name(key) == "return":
                    field.active = False
                    self.returned = True
                elif pg.key.name(key) == "space":
                    field.text += " "
                elif pg.key.name(key) == "backspace":
                    # Check if there's text to delete
                    if field.text:
                        field.text = field.text[:-1]
                elif pg.key.name(key).isalnum():
                    # Handle alphanumeric key presses
                    field.text += pg.key.name(key)
                elif (len(pg.key.name(key)) == 1): field.text += pg.key.name(key)

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)

class Tab(pg.sprite.Sprite):
    forge=None
    def __init__(self, forge, position:list|Hue.Vector2=[ 305, 60 ], size:list|Hue.Vector2=[ 132, 40 ], group:pg.sprite.Group=[]):
        super().__init__(group)
        self.map:Map=NULL
        self.forge = forge
        self.active = True
        self.size = Hue.Vector2(size)
        self.image = pg.Surface(self.size)
        self.position = Hue.Vector2(position)
        self.rect = pg.Rect(self.position, self.size)
        self.buttons = {
            "Close" : Button(
            forge,
            "Tab-Logo",
            "",
            logoPosition=[7, 6],
            position=[self.position.x, self.position.y+10],
            size=[22,20],
            group=group
            )
        }

    def Render(self):
        Hue.fillSurface(self.image, self.forge.theme["Base"])
        Hue.drawRect(self.forge.window, Hue.createRect(self.position, [self.size.x+1, self.size.y+1]), [255, 255, 255], 1)
        Hue.renderText(
            self.image,
            FONT,
            self.map.name,
            [62, self.size.y/2],
            size=12
        ) if (self.map) else Hue.renderText(
            self.image,
            FONT,
            "No Map!",
            [62, self.size.y/2],
            size=12,
            color=[255,0,0]
        )

    def Update(self):
        self.rect = pg.Rect(self.position, self.size)



