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

from core import *

""" 1.0.2024-beta Release """
# DONE :)

""" 1.1.2024-beta TODO """
# CONFIGURE FORGE TO GENERATE PROJECT DIR (new dir on new map)
# Sublayering
# Layer shifting: if you have 3 sublayers on background, and delete layer 1(2) then layer 2(3) should be come 1(2) so that sublayers persist and remain interactive
# Copy/Paste Selection: state.clipboard will house all the tile objects that are selected and paste will simply write them to data at their new positions.
# Move selection: state.move will house all the tile _map.GetTile objects being moved, and apply the delta to all of their positions.
# MAP VIEW : Show a tree of the map layers and the tiles in them allowing for easy access of map data/ tile props.
# Allow fill to replace selection of tiles if ids are different


class State:
    menu=NULL
    colliderColor="ColliderG"
    _map:str=None
    grid:bool=OFF
    component=None
    selection=None
    tool:str="Draw"
    selectDone=False
    selectOrigin=None
    UIRendered=False
    layerMenu = True
    saving:bool=False
    gridRendered=False
    activeTab:Tab=None
    tileIndex:int=None
    button:Button=None
    running:bool=False
    loading:bool=False
    interface:bool=ON
    header:Header=None
    clicking:bool=False
    dragging:bool=False
    clickingR:bool=False
    tile:pg.Surface=None
    view:str|TileView=None
    layer:list="background"
    layerState = {
        "background": 0,
        "midground": 0,
        "foreground": 0
    }
    viewComponent:str|TileView=None
    eraserSize:Hue.Vector2=Hue.Vector2(16,16)

class WorldForge:
    _version:str=""
    theme:dict
    system:dict
    config:dict
    dt:float=0.0
    tabs:dict={}
    maps:dict={}
    menus:dict={}
    cursor:Cursor
    sheets:dict={}
    zoom:float=1.0
    dimensions:dict
    window:pg.Surface
    screen:pg.Surface
    cursor:pg.Surface
    components:dict={}
    state:State=State()
    interfaceData:dict={}
    storage:Storage=Storage()
    interface:Hue.DebugInterface
    pan:Hue.Vector2=Hue.Vector2()
    clock:pg.time.Clock=pg.time.Clock()
    dragData:dict={
        "start": Hue.Vector2()
    }
    editorLayers:dict[pg.sprite.Group]={
        "main": {
            0:pg.sprite.Group()
        },
        "UI": {
            0:pg.sprite.Group()
        }
    }
    
    def __init__(self):
        ...

    def NULL_FUNC(self):
        return NULL

    def WriteToRegistry_Tilesets(self, asset:str, dirname:str):
        self.registry["tilesets"][asset] = dirname
        with open(".wf2C", "w") as config:
            json.dump(self.config, config, indent=4)
            config.close()
        print(f"Wrote {asset} to Registry[tilesets] as {dirname}!")

    def LoadForge(self):
        currentStep = 0
        totalSteps = 250 # 8000 # 100
        with open(".wf2C", "r") as config:
            self.config = json.load(config)
            self.registry = self.config["registry"]
            self.forgeInfo = self.config["forge info"]
            self._version = f"{self.forgeInfo["version"]}"
            print(f"WorldForge2 {self._version}")
            self.theme = self.config["Themes"][list(self.config["Themes"].keys())[0]]
            load1 = [ 255, 255, 255 ] #self.theme["Load1"].copy()
            load2 = [ 25, 25, 25 ] #self.theme["Load2"].copy()
            progressBar = ProgressBar((0, 780), (500, 20), load1, load2)
        
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.system = self.config["System"]
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.dimensions = self.system["Dimensions"]
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.InitForge(progressBar, currentStep, totalSteps)
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)


        for i in range(totalSteps):
            currentStep += 1
            progressBar.Update((currentStep / totalSteps) * 100)

            self.LoadingScreen(progressBar)
            self.Events()
            Hue.sendFrame()
            if (currentStep == totalSteps): 
                self.state.loading = False
                break
        pg.mouse.set_visible(False)

    def InitForge(self, progressBar:ProgressBar, currentStep:int, totalSteps:int):
        """ LOAD WORLDFORGE ASSETS """
        Hue.INIT_FONTS()
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        
        self.window = pg.display.set_mode(self.dimensions["Window"], pg.RLEACCEL)
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.screen = pg.Surface((self.dimensions["Window"][0]//self.zoom, self.dimensions["Window"][1]//self.zoom))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.interface = Hue.DebugInterface(self.window, Hue.Vector2( 1082, 710 ), self.clock, textColor=self.theme["Stats"])
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        Hue.setIcon("..\\assets\\wf2\\Logo.ico")
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        Hue.setTitle(f"WorldForge2 {self._version}")
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Title", Hue.scaleSurface(Hue.loadSurface("..\\assets\\wf2\\Name.png"), [ 168, 15 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        
        self.storage.StoreImage("Cursor", Hue.loadSurface("..\\assets\\wf2\\Cursor.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        btnLogo = pg.Surface((8,8))
        pg.draw.circle(
            btnLogo,
            [255,255,255],
            [4,4],
            4,
        )
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        
        self.storage.StoreImage("Tab-Logo", btnLogo)
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Load-Screen", Hue.scaleSurface(Hue.loadSurface("..\\assets\\wf2\\BannerALT.png"), [ 1400, 800 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Header-Logo", Hue.scaleSurface(Hue.loadSurface("..\\assets\\wf2\\LogoSolo.png"), [ 64, 64 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Header-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\wf2\\LogoSolo.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Header-Logo16", Hue.scaleSurface(Hue.loadSurface("..\\assets\\wf2\\LogoSolo.png"), [ 16, 16 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)


        """ LOAD ICON ASSETS """
        self.storage.StoreImage("SaveAs-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\SaveAs.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("SaveAs-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\SaveAs.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Import-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Import.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Import-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Import.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Export-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Export.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Export-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Export.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        
        self.storage.StoreImage("Dump-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Dump.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Dump-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Dump.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Rem-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Rem.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Rem-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Rem.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("New-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\New.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("New-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\New.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Draw-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Draw.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Draw-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Draw.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Swap-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Swap.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Swap-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Swap.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Next-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Next.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Next-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Next.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Back-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Back.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Back-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Back.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Fill-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Fill.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Fill-Logo64", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Fill.png"), [ 64, 64 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Fill-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Fill.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Collider-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Collider.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Collider-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Collider.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Eraser-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Eraser.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Eraser-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Eraser.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Select-Logo32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Select.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("Select-Logo48", Hue.scaleSurface(Hue.loadSurface("..\\assets\\icon\\Select.png"), [ 48, 48 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        

        """ LOAD TILE-BASED ASSETS """
        self.storage.StoreImage("ColliderR", Hue.loadSurface("..\\assets\\tile\\ColliderR.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("ColliderG", Hue.loadSurface("..\\assets\\tile\\ColliderG.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("ColliderB", Hue.loadSurface("..\\assets\\tile\\ColliderB.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("ColliderY", Hue.loadSurface("..\\assets\\tile\\ColliderY.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("ColliderP", Hue.loadSurface("..\\assets\\tile\\ColliderP.png"))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("CorrupTile32", Hue.scaleSurface(Hue.loadSurface("..\\assets\\tile\\CorrupTile.png"), [ 32, 32 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        self.storage.StoreImage("CorrupTile64", Hue.scaleSurface(Hue.loadSurface("..\\assets\\tile\\CorrupTile.png"), [ 64, 64 ]))
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)
        

        self.ConfigureForge()
        currentStep += 1
        progressBar.Update((currentStep / totalSteps) * 100)

        """ FORGE RUNNING """
        self.state.running = True

    def LoadingScreen(self, progressBar:ProgressBar):
        self.window.fill([255,255,255])
        self.window.blit(self.storage.GetImage("Load-Screen"), (0,0))
        progressBar.Draw(self.window)

    def ConfigureForge(self):
        """ HEADER """
        self.components["Header"] = Header(self, "Title", logoPosition=[115,45], position=Hue.Vector2(), size=[self.system["Dimensions"]["Window"][0], 100], group=self.editorLayers["UI"][0])
        self.components["Header"].buttons["WF2"] = Button(
            self,
            text="",
            logo="Header-Logo",
            logoPosition=[0,0],
            position=[25, 14],
            size=[64, 64],
            group=self.editorLayers["UI"][0]
        )
        self.components["Header"].buttons["New"] = Button(
            self,
            text="",
            logo="New-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-286, 16],
            size=[64, 64],
            group=self.editorLayers["UI"][0]
        )
        self.components["Header"].buttons["Import"] = Button(
            self,
            text="",
            logo="Import-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-186, 16],
            size=[64, 64],
            group=self.editorLayers["UI"][0]
        )
        self.components["Header"].buttons["Export"] = Button(
            self,
            text="",
            logo="Export-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-86, 16],
            size=[64, 64],
            group=self.editorLayers["UI"][0]
        )
        self.components["Header"].buttons["New"].CallBack = self.NewMapCallBack
        self.components["Header"].buttons["Export"].CallBack = self.ExportCallBack
        self.components["Header"].buttons["Import"].CallBack = self.ImportCallBack

        self.menus["Save-As"] = Menu(
            self,
            [1025,100],
            [250, 250],
        )
        self.menus["Save-As"].title = "Save-As"
        self.menus["Save-As"].fields["Map-Name"] = TextField(
            self,
            [1050, 150],
            [25,48],
            [200, 60]
        )
        self.menus["Save-As"].buttons["Confirm"] = Button(
            self,
            text="Yes",
            logo="Draw-Logo32",
            position=[1062, 255],
            size= [64, 60],
            group=self.editorLayers["UI"][0]
        )
        self.menus["Save-As"].buttons["Deny"] = Button(
            self,
            text="No",
            logo="Draw-Logo32",
            position=[1178, 255],
            size= [64, 60],
            group=self.editorLayers["UI"][0]
        )
        self.menus["Save-As"].buttons["Confirm"].CallBack = self.SaveMap
        self.menus["Save-As"].buttons["Deny"].CallBack = self.EscapeCallBack

        self.menus["New-Map"] = Menu(
            self,
            [1025,100],
            [250, 350],
        )
        self.menus["New-Map"].title = "New-Map"
        self.menus["New-Map"].fields["Map-Name"] = TextField (
            self,
            [1050, 150],
            [25,48],
            [200, 60],
        )
        self.menus["New-Map"].fields["Width"] = TextField (
            self,
            [1050, 255],
            [25,148],
            [50, 60],
        )
        self.menus["New-Map"].fields["Height"] = TextField (
            self,
            [1150, 255],
            [125,148],
            [50, 60],
        )
        self.menus["New-Map"].fields["Tile-Size"] = TextField (
            self,
            [1050, 355],
            [25,248],
            [200, 60],
        )
        
        """ TOOLBAR """
        self.components["ToolBar"] = ToolBar(self, size=[100,510], position=[self.system["Dimensions"]["Window"][0]-100, self.system["Dimensions"]["Window"][1]/5], group=self.editorLayers["UI"][0])
        self.components["ToolBar"].buttons["Fill"] = Button(
            self,
            text="",
            logo="Fill-Logo64",
            logoPosition=[0,0],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/4.51],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Eraser"] = Button(
            self,
            text="",
            logo="Eraser-Logo48",
            logoPosition=[8,12],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/3.06],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Draw"] = Button(
            self,
            text="",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/2.33],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Select"] = Button(
            self,
            text="",
            logo="Select-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/1.88],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Swap"] = Button(
            self,
            text="",
            logo="Swap-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/1.58],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Collider"] = Button(
            self,
            text="",
            logo="Collider-Logo48",
            logoPosition=[8,8],
            position=[self.system["Dimensions"]["Window"][0]-82,self.system["Dimensions"]["Window"][1]/1.36],
            size=[64, 64], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ToolBar"].buttons["Fill"].CallBack = self.FillCallBack
        self.components["ToolBar"].buttons["Draw"].CallBack = self.DrawCallBack
        self.components["ToolBar"].buttons["Swap"].CallBack = self.SwapCallBack
        self.components["ToolBar"].buttons["Eraser"].CallBack = self.EraseCallBack
        self.components["ToolBar"].buttons["Select"].CallBack = self.SelectCallBack
        self.components["ToolBar"].buttons["Collider"].CallBack = self.TilePropsCallBack
    
        """ FOOTER """
        self.components["Footer"] = ToolBar(self, size=[self.system["Dimensions"]["Window"][0], 48], position=[0, self.system["Dimensions"]["Window"][1]-48], group=self.editorLayers["UI"][0])
        self.components["Footer"].buttons["Cursor-Position"] = Button(
            self,
            text="0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[16,self.system["Dimensions"]["Window"][1]-34],
            size=[148, 21], 
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["Dimensions"] = Button(
            self,
            text="1000x1000",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[164,self.system["Dimensions"]["Window"][1]-34],
            size=[148, 21], 
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["Tile-Size"] = Button(
            self,
            text="8x8",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            size=[80, 21], 
            position=[312,self.system["Dimensions"]["Window"][1]-34],
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["Tool"] = Button(
            self,
            text="0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[390,self.system["Dimensions"]["Window"][1]-34],
            size=[148, 21], 
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["Time"] = Button(
            self,
            text="11:26",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[self.system["Dimensions"]["Window"][0]/2-100,self.system["Dimensions"]["Window"][1]-34],
            size=[164, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["TileID"] = Button(
            self,
            text="Tile ID: 0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[self.system["Dimensions"]["Window"][0]-582,self.system["Dimensions"]["Window"][1]-34],
            size=[148, 21], 
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["PATH"] = Button(
            self,
            text="C:/SAVE/PATH",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[self.system["Dimensions"]["Window"][0]-422,self.system["Dimensions"]["Window"][1]-34],
            size=[400, 21], 
            group=self.editorLayers["UI"][0]
        )
        self.components["Footer"].buttons["Time"].CallBack = self.NULL_FUNC
        self.components["Footer"].buttons["TileID"].CallBack = self.NULL_FUNC
        self.components["Footer"].buttons["Tool"].CallBack = self.ToolCallBack
        self.components["Footer"].buttons["PATH"].CallBack = self.PathCallBack
        self.components["Footer"].buttons["Tile-Size"].CallBack = self.NULL_FUNC
        self.components["Footer"].buttons["Dimensions"].CallBack = self.NULL_FUNC
        self.components["Footer"].buttons["Cursor-Position"].CallBack = self.NULL_FUNC

        """ LAYER MENU """
        #self.components["Layer-Menu"] = ToolBar(self, size=[400, 64], position=[0, self.system["Dimensions"]["Window"][1]-96], group=self.editorLayers["UI"][0])
        self.components["Layer-Menu"] = ToolBar(self, size=[330, 98], position=[0, self.system["Dimensions"]["Window"][1]-194], group=self.editorLayers["UI"][0])
        #self.components["Layer-Menu"].buttons[""]
        self.components["Layer-Menu"].buttons["BGCOUNT"] = Button(
            self,
            text="BGC",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[16,self.system["Dimensions"]["Window"][1]-185],
            size=[48, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["BGLAYER"] = Button(
            self,
            text="Background",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[76,self.system["Dimensions"]["Window"][1]-185],
            size=[164, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["BGLAYERNUM"] = Button(
            self,
            text="CL:0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[250,self.system["Dimensions"]["Window"][1]-185],
            size=[64, 21],
            group=self.editorLayers["UI"][0]
        )
        

        self.components["Layer-Menu"].buttons["MGCOUNT"] = Button(
            self,
            text="MGC",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[16,self.system["Dimensions"]["Window"][1]-155],
            size=[48, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["MGLAYER"] = Button(
            self,
            text="Midground",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[76,self.system["Dimensions"]["Window"][1]-155],
            size=[164, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["MGLAYERNUM"] = Button(
            self,
            text="CL:0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[250,self.system["Dimensions"]["Window"][1]-155],
            size=[64, 21],
            group=self.editorLayers["UI"][0]
        )

        self.components["Layer-Menu"].buttons["FGCOUNT"] = Button(
            self,
            text="FGC",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[16,self.system["Dimensions"]["Window"][1]-125],
            size=[48, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["FGLAYER"] = Button(
            self,
            text="Foreground",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[76,self.system["Dimensions"]["Window"][1]-125],
            size=[164, 21],
            group=self.editorLayers["UI"][0]
        )
        self.components["Layer-Menu"].buttons["FGLAYERNUM"] = Button(
            self,
            text="CL:0",
            logo="Draw-Logo48",
            logoPosition=[12,12],
            position=[250,self.system["Dimensions"]["Window"][1]-125],
            size=[64, 21],
            group=self.editorLayers["UI"][0]
        )


        self.components["Layer-Menu"].buttons["BGCOUNT"].CallBack = self.NULL_FUNC
        self.components["Layer-Menu"].buttons["BGLAYER"].CallBack = self.BackGroundLayerCallBack
        self.components["Layer-Menu"].buttons["BGLAYERNUM"].CallBack = self.NULL_FUNC
        
        self.components["Layer-Menu"].buttons["MGCOUNT"].CallBack = self.NULL_FUNC
        self.components["Layer-Menu"].buttons["MGLAYER"].CallBack = self.MidGroundLayerCallBack
        self.components["Layer-Menu"].buttons["MGLAYERNUM"].CallBack = self.NULL_FUNC

        self.components["Layer-Menu"].buttons["FGCOUNT"].CallBack = self.NULL_FUNC
        self.components["Layer-Menu"].buttons["FGLAYER"].CallBack = self.ForeGroundLayerCallBack
        self.components["Layer-Menu"].buttons["FGLAYERNUM"].CallBack = self.NULL_FUNC

        """ LAYER BAR """
        self.components["LayerBar"] = ToolBar(self, size=[330, 48], position=[0,self.system["Dimensions"]["Window"][1]-96], group=self.editorLayers["UI"][0])
        self.components["LayerBar"].buttons["Hide-LayerMenu"] = Button(
            self,
            text="",
            logo="Header-Logo32",
            logoPosition=[0,0],
            position=[16,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["LayerBar"].buttons["Last-Layer"] = Button(
            self,
            text="",
            logo="Back-Logo32",
            logoPosition=[0,0],
            position=[(16*2)+37,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["LayerBar"].buttons["Next-Layer"] = Button(
            self,
            text="",
            logo="Next-Logo32",
            logoPosition=[0,0],
            position=[(16*3)+37*2,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["LayerBar"].buttons["New-Layer"] = Button(
            self,
            text="",
            logo="New-Logo32",
            logoPosition=[0,0],
            position=[(16*4)+37*3,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["LayerBar"].buttons["Rem-Layer"] = Button(
            self,
            text="",
            logo="Rem-Logo32",
            logoPosition=[1,0],
            position=[(16*5)+37*4,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["LayerBar"].buttons["Dump-Layer"] = Button(
            self,
            text="",
            logo="Dump-Logo32",
            logoPosition=[0,-4],
            position=[(16*6)+37*5,self.system["Dimensions"]["Window"][1]-82],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        
        self.components["LayerBar"].buttons["Hide-LayerMenu"].CallBack = self.ToggleLayerMenuCallBack
        self.components["LayerBar"].buttons["Last-Layer"].CallBack = self.NULL_FUNC
        # FIX THIS FUNCTION # self.LastLayerCallBack

        self.components["LayerBar"].buttons["Next-Layer"].CallBack = self.NULL_FUNC
        # FIX THIS FUNCTION # self.NextLayerCallBack

        self.components["LayerBar"].buttons["New-Layer"].CallBack = self.NULL_FUNC
        # FIX THIS FUNCTION # self.NewLayerCallBack

        self.components["LayerBar"].buttons["Dump-Layer"].CallBack = self.DumpLayerCallBack
        self.components["LayerBar"].buttons["Rem-Layer"].CallBack = self.NULL_FUNC
        # FIX THIS FUNCTION # self.RemLayerCallBack

        """ VIEWBAR """
        self.components["ViewBar"] = ToolBar(self, size=[200, 48], position=[0,self.system["Dimensions"]["Window"][1]-700], group=self.editorLayers["UI"][0])
        self.components["ViewBar"].buttons["Last-View"] = Button(
            self,
            text="",
            logo="Back-Logo32",
            logoPosition=[0,0],
            position=[57,self.system["Dimensions"]["Window"][1]-698],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ViewBar"].buttons["Next-View"] = Button(
            self,
            text="",
            logo="Next-Logo32",
            logoPosition=[0,0],
            position=[107,self.system["Dimensions"]["Window"][1]-698],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ViewBar"].buttons["New-View"] = Button(
            self,
            text="",
            logo="New-Logo32",
            logoPosition=[0,0],
            position=[156,self.system["Dimensions"]["Window"][1]-698],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ViewBar"].buttons["Hide-View"] = Button(
            self,
            text="",
            logo="Header-Logo32",
            logoPosition=[0,0],
            position=[8,self.system["Dimensions"]["Window"][1]-698],
            size=[32, 32], 
            group=self.editorLayers["UI"][0]
        )
        self.components["ViewBar"].buttons["New-View"].CallBack = self.NewViewCallBack
        self.components["ViewBar"].buttons["Last-View"].CallBack = self.LastViewCallBack
        self.components["ViewBar"].buttons["Next-View"].CallBack = self.NextViewCallBack
        self.components["ViewBar"].buttons["Hide-View"].CallBack = self.HideViewCallBack

        """ PROPS VIEW """
        self.menus["PropView"] = Menu(
            self,
            position=[0,148],
            size=[300, 400],
            group=self.editorLayers["UI"][0]
        )
        self.menus["PropView"].title = "Tile Props"
        self.menus["PropView"].buttons
        self.menus["PropView"].buttons["Layer"] = Button(
            self,
            "Draw-Logo32",
            "background",
            [0,0],
            [16, 164],
            [132,52],
            fontSize=16,
            group=self.editorLayers["UI"][0]
        )
        self.menus["PropView"].buttons["Pos"] = Button(
            self,
            "Draw-Logo32",
            "0.0,0.0",
            [0,0],
            [155 , 164],
            [132,52],
            fontSize=13,
            group=self.editorLayers["UI"][0]
        )
        self.menus["PropView"].buttons["Collisions"] = Button(
            self,
            "Draw-Logo32",
            "Collisions",
            [0,0],
            [155 , 164],
            [132,52],
            fontSize=13,
            group=self.editorLayers["UI"][0]
        )
        self.menus["PropView"].fields["Alpha"] = TextField(
            self,
            offset=[16, 98],
            position=[16 , 264],
            size=[98,52],
            group=self.editorLayers["UI"][0]
        )
        

        self.cursor = Cursor(self, self.storage.GetImage("Cursor"), self.editorLayers["UI"][0])

        self.EscapeCallBack()

    def Events(self):
        for e in pg.event.get():
            match (e.type):
                case Hue.QUIT:
                    self.Exit()
                case Hue.VIDEOEXPOSE:
                    pg.display.update()
                case Hue.DROPFILE:
                    print(os.path.basename(e.file))
                    self.DropFileCallBack(e.file)
                case Hue.KEYDOWN:
                    if (self.state.menu and self.state.menu.active):
                        for field in self.state.menu.fields:
                            if (self.state.menu.fields[field].active): self.state.menu.HandleText(e.key)
                    match (e.key):
                        case Hue.Keyboard.Comma:
                            self.state.layer = "background"
                        case Hue.Keyboard.Period:
                            self.state.layer = "midground"
                        case Hue.Keyboard.Slash:
                            self.state.layer = "foreground"
                        case Hue.Keyboard.X:
                            if (pg.key.get_mods() & Hue.KMOD_CTRL and self.state.selectDone):
                                self.RemSelect()
                        case Hue.Keyboard.A:
                            if (pg.key.get_mods() & Hue.KMOD_CTRL):
                                self.AllSelect()
                        case Hue.Keyboard.Z:
                            if (pg.key.get_mods() & Hue.KMOD_CTRL):
                                if (len(self.maps) and self.state._map and self.maps.__contains__(self.state._map)):
                                    _map = self.maps[self.state._map]
                                    _map.Undo()
                        case Hue.Keyboard.Y:
                            if (pg.key.get_mods() & Hue.KMOD_CTRL):
                                if (len(self.maps) and self.state._map and self.maps.__contains__(self.state._map)):
                                    _map = self.maps[self.state._map]
                                    _map.Redo()
                        case KeyBinds.Fill:
                            self.FillCallBack()
                        case KeyBinds.Select:
                            self.SelectCallBack()
                        case KeyBinds.Escape:
                            self.EscapeCallBack()
                        case KeyBinds.Close:
                            self.Exit()
                        case KeyBinds.Props:
                            self.TilePropsCallBack()
                        case KeyBinds.Draw:
                            if (not self.state.menu): self.DrawCallBack()
                        case KeyBinds.Swap:
                            if (not self.state.menu): self.SwapCallBack()
                        case KeyBinds.Eraser:
                            if (not self.state.menu): self.EraseCallBack()
                        case KeyBinds.Export:
                            if (not self.state.menu): self.ExportCallBack()
                        case KeyBinds.ToggleGrid:
                            self.state.grid = not self.state.grid
                        case KeyBinds.NewMap:
                            self.NewMapCallBack()
                        case KeyBinds.Import:
                            self.ImportCallBack()
                        case KeyBinds.RemLayer:
                            self.RemLayerCallBack()
                        case KeyBinds.NextLayer:
                            # FIX LAYERING FEATURE FIRST #self.NextLayerCallBack()
                            pass
                        case KeyBinds.LastLayer:
                            # FIX LAYERING FEATURE FIRST #self.LastLayerCallBack()
                            pass
                        case KeyBinds.LastBaseLayer:
                            self.LastBaseLayerCallBack()
                        case KeyBinds.NextBaseLayer:
                            self.NextBaseLayerCallBack()
                        case KeyBinds.DumpLayer:
                            self.DumpLayerCallBack()
                        case KeyBinds.NextView:
                            self.NextViewCallBack()
                        case KeyBinds.LastView:
                            self.LastViewCallBack()
                        case KeyBinds.ToggleLayerMenu:
                            self.ToggleLayerMenuCallBack()
                        case KeyBinds.ToggleToolBar:
                            self.ToolCallBack()
                        case KeyBinds.HideView:
                            if (not self.state.menu): self.HideViewCallBack(clicked=False)
                        case KeyBinds.ToggleInterface:
                            self.state.interface = not self.state.interface
                case Hue.MOUSEBUTTONDOWN:
                    match (e.button):
                        case Hue.Mouse.LeftClick:
                            self.state.clicking = True
                        case Hue.Mouse.RightClick:
                            self.state.clickingR = True
                        case KeyBinds.Drag:
                            if (self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and not self.state.header and not self.state.viewComponent and not self.state.component):
                                self.state.dragging = True
                                self.dragData["start"] = self.cursor.position
                        case KeyBinds.ZoomIn:
                            if (self.state._map and self.state.view and self.CursorIsOn(self.maps[self.state._map].tileViews[self.state.view])):
                                self.maps[self.state._map].tileViews[self.state.view].Scroll(-1)
                            else:
                                if (self.state._map):
                                    if (self.state._map and self.zoom - .2 > ZOOM_MIN):
                                        self.zoom -= .2
                                    else: self.zoom = ZOOM_MIN
                        case KeyBinds.ZoomOut:
                            if (self.state._map and self.state.view and self.CursorIsOn(self.maps[self.state._map].tileViews[self.state.view])):
                                self.maps[self.state._map].tileViews[self.state.view].Scroll(1)
                            else:
                                if (self.state._map):
                                    if (self.state._map and self.zoom + .2 < ZOOM_MAX):
                                        self.zoom += .2
                                    else: self.zoom = ZOOM_MAX
                case Hue.MOUSEBUTTONUP:
                    match (e.button):
                        case Hue.Mouse.LeftClick:
                            self.state.clicking = False
                        case Hue.Mouse.RightClick:
                            self.state.clickingR = False
                        case KeyBinds.Drag:
                            self.state.dragging = False
                            self.pan = Hue.Vector2()
                            self.dragData["start"] = Hue.Vector2()

    def AddToInterface(self, data, key:str=None):
        if (key): self.interfaceData[key] = data
        else: self.interfaceData[data] = data
    
    def AddTileView(self, path:str):
        if (self.state._map):
            if (self.state.view):
                for view in self.maps[self.state._map].tileViews:
                    self.maps[self.state._map].tileViews[view].kill()
                    self.maps[self.state._map].tileViews[view].visible = False

            if (type(path) == str and os.path.exists(path)):
                
                tv = TileView(
                    self,
                    self.maps[self.state._map].tileSizeRAW,
                    [0,self.system["Dimensions"]["Window"][1]-652],
                    group=self.editorLayers["UI"][0]
                )
                tv.LoadTileSet(path=path)
                tv.LoadTiles()
                self.state.view = str(len(self.maps[self.state._map].tileViews))
                self.maps[self.state._map].tileViews[self.state.view] = tv
            else: return None
    
    def SwapTileView(self):
        print("Swapping TV")
        if (self.state._map):
            if (self.state.view):
                for view in self.maps[self.state._map].tileViews:
                    self.maps[self.state._map].tileViews[view].kill()
                    self.maps[self.state._map].tileViews[view].visible = False
            path = self.ManageSelection_File(msg="Select Tileset")

            if (type(path) == str):
                _map = self.maps[self.state._map]
                _map.tileViews.pop(self.state.view)
                
                view = TileView(
                    self,
                    _map.tileSizeRAW,
                    [0,self.system["Dimensions"]["Window"][1]-652],
                    group=self.editorLayers["UI"][0]
                )
                view.LoadTileSet(path=path)
                view.LoadTiles()
                _map.tileViews[self.state.view] = view 

                # layers = [ "background", "midground", "foreground" ]
                # for layer in layers:
                #     for tile in _map.data[layer]:
                #         pos = tile.split(";")
                #         pos = [int(pos[0]), int(pos[1])]
                #         tileData = _map.data[layer][tile]
                #         self.state.tileIndex = tileData["id"]
                #         self.state.tile = self.maps[self.state._map].tileViews[self.state.view].tile["images"][self.state.tileIndex]
                #         _map = self.maps[self.state._map]
                #         print(f"PLACING TILE FOR SWAP TILEVIEW {pos}")
                #         placeTileCommand = PlaceTileCommand(self, _map, tileData["layer"], tileData["subLayer"], Hue.Vector2(pos), self.state.tileIndex)
                #         _map.ExecuteCommand(placeTileCommand)
                # self.maps[self.state._map].rendered = False
        
    def ManageMenus(self):
        if (self.state.menu):
            menu = self.state.menu
            Hue.drawRect(self.window, Hue.createRect(menu.position, [menu.size.x+1, menu.size.y+1]), self.theme["Trim"], 3)
            for label, field in self.state.menu.fields.items():
                if (len(menu.fields)):
                        Hue.renderText(
                            menu.image,
                            FONT,
                            menu.title,
                            menu.titlePosition,
                            size=12,
                            center=False
                        )
                        Hue.renderText(
                            menu.image,
                            FONT,
                            label,
                            [field.offset[0], field.offset[1]-16],
                            size=18,
                            center=False
                        )
                        Hue.renderText(
                            field.image,
                            FONT,
                            field.text,
                            [8, 16],
                            size=12,
                            center=False
                        )
                        menu.image.blit(field.image, [field.offset[0], field.offset[1]+16])

                        if (self.state.menu == self.menus["Save-As"] and self.state.menu.returned): self.SaveMap()

                        if (self.state.menu and menu == self.menus["New-Map"] and menu.returned):
                            if (self.state._map): path = self.maps[self.state._map].path
                            else: path = self.ManageSelection_SaveDir()
                            name = menu.fields["Map-Name"].text
                            try:
                                mapSize = Hue.Vector2(int(menu.fields["Width"].text), int(menu.fields["Height"].text))
                            except (ValueError):
                                print("Width/Height Values Must Be Numerical!\n")
                                menu.returned = False
                                return
                            try:
                                tileSize = int(menu.fields["Tile-Size"].text)
                            except (ValueError):
                                print("TileSize Value Must Be Numerical!\n")
                                menu.returned = False
                                return
                            try:
                                self.AddMap(
                                    path,
                                    tileSize,
                                    mapSize,
                                    name
                                )
                                menu.returned = False
                            except (pg.error):
                                print("Error Creating Map")
                                menu.returned = False

            if (self.state.menu and self.state.menu.buttons):
                for button in self.state.menu.buttons:
                    bttn = self.state.menu.buttons[button]
                    if (self.CursorIsOn(bttn)): self.state.button = button
                    bttn.Update()            

    def AddMap(self, savePath:str, tileSize:int, mapSize:list|Hue.Vector2=[1026, 610], name:str="Map"):
        self.EscapeCallBack()
        if (len(self.maps) and self.state._map):
            self.maps[self.state._map].kill()
            self.maps[self.state._map].active = False
            self.tabs[self.state._map].active = False
            self.state.layer = "background"
            self.state.layerState[self.state.layer] = 0
            for view in self.maps[self.state._map].tileViews:
                self.maps[self.state._map].tileViews[view].kill()
            
            self.state.view = None
            self.state.viewComponent = None
            self.state.tile = None
            self.state.tileIndex = None
        self.state._map = name
        self.maps[self.state._map] = Map(
            self,
            name,
            savePath,
            tileSize,
            mapSize,
            self.editorLayers["main"][0]
        )

    def ManageButtons(self):
        try:
            if (self.components[self.state.component].visible and self.CursorIsOn(self.components[self.state.component].buttons[self.state.button])):
                button = self.components[self.state.component].buttons[self.state.button]
                try:
                    button.CallBack()
                    self.state.clicking = False
                except(TypeError):
                    pass
        except(KeyError):
            pass    # Button Doesnt Exist Here
        
        try:
            if (self.CursorIsOn(self.tabs[self.state.activeTab].buttons[self.state.button])):
                button = self.tabs[self.state.activeTab].buttons[self.state.button]
                try:
                    button.CallBack()
                    self.state.clicking = False
                except(TypeError):
                    pass
        except(KeyError):
            pass    # Button Doesnt Exist Here
        
        try:
            if (self.state.menu and self.state.menu.buttons.__contains__(self.state.button) and self.CursorIsOn(self.state.menu.buttons[self.state.button])):
                button = self.state.menu.buttons[self.state.button]
                try:
                    button.CallBack()
                    self.state.clicking = False
                except(TypeError):
                    pass
        except(KeyError):
            pass    # Button Doesnt Exist Here

    def ManageComponents(self):
        for component in self.components:
            if (type(self.components[component]) != dict):
                self.components[component].Update()
                if (self.CursorIsOn(self.components[component])): 
                    self.state.component = component
                if (hasattr(self.components[component], "buttons")):
                    for button in self.components[component].buttons:
                        bttn = self.components[component].buttons[button]
                        if (bttn and self.CursorIsOn(bttn)):
                            self.state.button = button

        for tab in self.tabs:
            for button in self.tabs[tab].buttons:
                if (self.CursorIsOn(self.tabs[tab]) and self.CursorIsOn(self.tabs[tab].buttons[button])):
                    #button = self.tabs[tab].buttons[button]
                    self.state.button = button

    def ManageTileViews(self):
        if (self.state._map and len(self.maps[self.state._map].tileViews)):
            for view in self.maps[self.state._map].tileViews:
                if (self.state.view):
                    if(self.maps[self.state._map].tileViews[self.state.view].visible):
                        self.maps[self.state._map].tileViews[self.state.view].Render()
                        self.maps[self.state._map].tileViews[self.state.view].Update()
                        if (self.CursorIsOn(self.maps[self.state._map].tileViews[self.state.view])): 
                            self.state.viewComponent = view
                        else: self.state.viewComponent = None
                    else:    
                        self.maps[self.state._map].tileViews[self.state.view].kill()

    def ManageFooter(self):
        self.components["Footer"].buttons["Tool"].text = f"{self.state.tool}"
        if (self.state._map): self.components["Footer"].buttons["Cursor-Position"].text = f"{self.CursorPosition_Map(self.maps[self.state._map])}"
        else: self.components["Footer"].buttons["Cursor-Position"].text = f"[x, x]"

        EST = datetime.datetime.now(EST_ZONE)
        timeText = f"{EST.strftime(TIME_FORMAT)}"
        self.components["Footer"].buttons["Time"].text = timeText
        if (self.state._map):
            self.components["Footer"].buttons["PATH"].text = self.maps[self.state._map].path
            tileSize = self.maps[self.state._map].data["mapInfo"]["tilesize"]
            tileSize = f"{tileSize}x{tileSize}"
            self.components["Footer"].buttons["Tile-Size"].text = tileSize
            mapSize = self.maps[self.state._map].data["mapInfo"]["width/height"]
            mapSize = f"{int(mapSize[0])}x{int(mapSize[1])}"
            self.components["Footer"].buttons["Dimensions"].text = mapSize
            if (len(self.maps[self.state._map].tileViews)):
                if (self.state.tileIndex): self.components["Footer"].buttons["TileID"].text = f"Tile ID: {self.state.tileIndex}"
                else: self.components["Footer"].buttons["TileID"].text = f"Tile ID: X"
        else:
            self.components["Footer"].buttons["TileID"].text = "Tile ID: X"
            self.components["Footer"].buttons["Tile-Size"].text = "8x8"
            self.components["Footer"].buttons["PATH"].text = "C:/SAVE/PATH"
            self.components["Footer"].buttons["Dimensions"].text = "1000x1000"

    def ManageInterface(self):
        for data in self.interfaceData:
            self.interface.addToInterface(self.interfaceData[data])
    
    def ManageState(self):  # STATE MANAGEMENT

        self.ManageInterface()
        self.SelectFunction()
        self.LayerMenuFunction()
        if (self.state._map and self.state.interface):
            if (self.state._map): self.AddToInterface(f"{self.CursorPosition_Map(self.maps[self.state._map])}","Mouse-Pos")
            self.interface.visualOutput()
        if (self.state._map and self.state.dragging):
            dX = self.cursor.position.x - self.dragData["start"].x
            dY = self.cursor.position.y - self.dragData["start"].y
            self.pan.x = dX
            self.pan.y = dY
            self.dragData["start"] = self.cursor.position
            #print(f"Drag Start: {self.dragData["start"]}\nPan: {self.pan}")
        if (self.state.clickingR and self.state.tileIndex != None and self.state._map and self.state.tile and not self.state.component and not self.state.header and not self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Draw"):
            self.state.tile = None
            self.state.tileIndex = None
        if (self.state.clicking and not self.state.header and not self.state.component and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Eraser"):
            self.ManageRemoving_Tile()
        if (self.state.clickingR and not self.state.header and not self.state.component and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Eraser" and self.state.selectDone):
            self.RemSelect()
        if (self.state.clicking and not self.state.header and not self.state.component and not self.state.viewComponent and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Swap"):
            self.SwapFunction()
        if (self.state.clicking and not self.state.header and not self.state.component and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Props"):
            self.EditTileProps_Collider(self.state.clickingR)
        elif (self.state.clickingR and not self.state.header and not self.state.component and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool == "Props"):
            self.EditTileProps_Collider(self.state.clickingR)
        if (self.state.clicking and not self.state.header and not self.state.component and self.state.tileIndex != None and self.state.tile and self.state._map and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.tool in ["Draw", "Fill"]):
            self.ManagePlacement_Tile()
        if (self.state.button and self.state.clicking):
            self.ManageButtons()
        if (self.state.component and not self.CursorIsOn(self.components[self.state.component])):
            self.state.button = None
            self.state.component = None
        if (self.state.view and self.state.viewComponent and self.state.tool == "Draw"):
            if (self.state._map and self.CursorIsOn(self.maps[self.state._map].tileViews[self.state.view]) and self.state.clicking):
                self.ManageSelection_Tile()
        if (self.state.clicking and self.state.menu):
            self.ManageSelection_MenuField()
        if (self.state.clicking and self.state.menu and not self.CursorIsOn(self.state.menu)): self.EscapeCallBack()

    def ManageMaps(self):
        if (len(self.maps) and self.state._map and self.maps[self.state._map].active):
            self.maps[self.state._map].position += self.pan * self.zoom
            self.maps[self.state._map].Update()
            self.maps[self.state._map].Render()
        elif (len(self.maps) and self.state._map and not self.maps[self.state._map].active):
            self.maps[self.state._map].kill()
        
    def ManageTabs(self):
        for label, m in self.maps.items():
            if (not self.tabs.__contains__(label)):
                self.tabs[label] = Tab(self, position=[TAB_MIN +(TAB_GAP * len(self.tabs)), 60],group=self.editorLayers["UI"][0])
                self.tabs[label].map = m
                self.tabs[label].buttons["Close"].CallBack = self.CloseTabCallBack
            
            if (label != self.state._map): self.tabs[label].active = False
            else: self.state.activeTab = label

            self.tabs[label].Render()
            self.tabs[label].Update()

            if (self.state.clicking):
                if (self.CursorIsOn(self.tabs[label]) and not self.CursorIsOn(self.tabs[label].buttons["Close"])):
                    self.maps[self.state._map].kill()
                    self.maps[self.state._map].active = False
                    self.tabs[self.state.activeTab].active = False
                    for view in self.maps[self.state._map].tileViews:
                        self.maps[self.state._map].tileViews[view].kill()

                    self.state._map = label
                    self.state.activeTab = label
                    self.maps[self.state._map].active = True
                    self.editorLayers["main"][0].add(self.maps[self.state._map])
                    self.tabs[self.state.activeTab].active = True

                    if (len(self.maps[self.state._map].tileViews)):
                        self.state.view = "0"
                        self.state.viewComponent = self.maps[self.state._map].tileViews[self.state.view]
                    else:
                        self.state.view = None
                        self.state.viewComponent = None
                    self.state.tile = None
                    self.state.tileIndex = None

    def ManageSelection_MenuField(self):
        if (self.state.menu):
            for label, field in self.state.menu.fields.items():
                field.active = False
                if (self.CursorIsOn(field)):
                    field.active = True
                    self.state.clicking = False

    def ManageSelection_Tile(self):
        self.state.clicking = False
        if(self.state.view):
            view = self.maps[self.state._map].tileViews[self.state.view]

            # Adjust mousePos based on TileView's scroll and position
            relX, relY = (self.cursor.position[0]+8) - view.position[0], (self.cursor.position[1]+8) - view.position[1] + view.data["scroll"]
            

            # Calculate the column and row based on the mouse position
            col = (relX - view.data["padding"][0]) // (view.tile["size"] + view.data["padding"][0] * 2)
            row = (relY - view.data["padding"][1]) // (view.tile["size"] + view.data["padding"][1] * 2)

            # Calculate the top-left corner of the hovered tile's rectangle
            tileX = view.data["padding"][0] + col * (view.tile["size"] + view.data["padding"][0] * 2)
            tileY = view.data["padding"][1] + row * (view.tile["size"] + view.data["padding"][1] * 2) - view.data["scroll"]

            # Calculate the index of the hovered tile
            index = row * view.data["rowMax"] + col
            if 0 <= index < len(view.tile["images"]):
                tile = int(index)
                self.state.tileIndex = tile
                self.state.tile = self.maps[self.state._map].tileViews[self.state.view].tile["images"][self.state.tileIndex].copy()
            else:
                self.state.tile = None
                self.state.tileIndex = None

    def ManageSelection_SaveDir(self):
        ### MUST KEEP APP RESPONSIVE HERE
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        folder_path = filedialog.askdirectory(title="Select Save Destination Folder")
        return folder_path

    def ManageSelection_File(self, msg:str="Select File"):
        ### MUST KEEP APP RESPONSIVE HERE
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        file = filedialog.askopenfile(title=msg)
        if file != None:
            path = file.name
            return path
        else:
            pass

    def ManageSelection_SaveFile(self, msg="Save Map As"):
        # Keep the application responsive
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        file_types = [("WorldForge Files", "*.wf2")]

        # Open a dialog to select a save path and specify a file name
        filePath = filedialog.asksaveasfilename(title=msg, filetypes=file_types, defaultextension=".wf2")

        # Check if a file path was selected
        if (filePath):
            fileName = os.path.basename(filePath)
            if (len(self.maps) and self.maps.__contains__(self.state._map) and self.maps[self.state._map]):
                fileName = os.path.basename(filePath)
                fp = os.path.dirname(filePath)
                self.maps[self.state._map].name = fileName.removesuffix(".wf2")
            return fp
        else:
            # Handle the case where the dialog was cancelled or no file was selected
            return None

    def ManageRemoving_Tile(self):
        if (self.state._map and not self.state.viewComponent and not self.state.component and not self.state.header):
            pos = self.CursorPosition_Map(self.maps[self.state._map])
            tileKey = f"{int(pos[0])};{int(pos[1])}"

            # Check if there's a tile to erase
            if self.maps[self.state._map].data[self.maps[self.state._map].forge.state.layer].get(tileKey):
                if (self.state.selectDone and self.state.selection):
                    if (self.state.selection.left <= pos.x <= self.state.selection.right and
                        self.state.selection.top <= pos.y <= self.state.selection.bottom):
                            eraseCommand = EraseCommand(self, self.maps[self.state._map], self.state.layer, self.state.layerState[self.state.layer], pos)
                            self.maps[self.state._map].ExecuteCommand(eraseCommand)
                else:
                    eraseCommand = EraseCommand(self, self.maps[self.state._map], self.state.layer, self.state.layerState[self.state.layer], pos)
                    self.maps[self.state._map].ExecuteCommand(eraseCommand)

    def ManagePlacement_Tile(self):
        if (self.state._map and not self.state.viewComponent and not self.state.component and not self.state.header):
            pos = self.CursorPosition_Map(self.maps[self.state._map])

            if (self.state.tool == "Fill"):
                if (self.state.selectDone and self.state.selection):
                    if (self.state.selection.left <= pos.x <= self.state.selection.right and
                            self.state.selection.top <= pos.y <= self.state.selection.bottom):
                        self.FillFunction(pos, self.state.tileIndex, self.state.selection)
                else:
                    self.FillFunction(pos, self.state.tileIndex)
            else:
                # Handle other tools like tile placement
                if (self.state.selectDone and self.state.selection):
                    if (self.state.selection.left <= pos.x <= self.state.selection.right and
                            self.state.selection.top <= pos.y <= self.state.selection.bottom):
                        
                        _map = self.maps[self.state._map]
                        placeTileCommand = PlaceTileCommand(self, _map, self.state.layer, self.state.layerState[self.state.layer], pos, self.state.tileIndex)
                        _map.ExecuteCommand(placeTileCommand)
                else:
                    _map = self.maps[self.state._map]
                    placeTileCommand = PlaceTileCommand(self, _map, self.state.layer, self.state.layerState[self.state.layer], pos, self.state.tileIndex)
                    _map.ExecuteCommand(placeTileCommand)

    def CursorIsOn(self, target) -> bool:
        mPos = self.cursor.position
        mPos = Hue.Vector2(mPos.x+8, mPos.y+8)
        mPos = Hue.Vector2(mPos.x, mPos.y)
        return mPos.x > target.position.x and mPos.x < target.position.x + target.size.x and mPos.y > target.position.y and mPos.y < target.position.y + target.size.y
    
    def CursorIsOn_Z(self, target) -> bool:
        mPos = self.cursor.position
        mPos = Hue.Vector2(mPos.x+8, mPos.y+8)
        mPos = Hue.Vector2(mPos.x * self.zoom, mPos.y * self.zoom)
        return mPos.x > target.position.x and mPos.x < target.position.x + target.size.x and mPos.y > target.position.y and mPos.y < target.position.y + target.size.y

    def CursorPosition_Map(self, _map:Map) -> Hue.Vector2:
        mPos = self.cursor.position
        mPos = Hue.Vector2(mPos.x+8, mPos.y+8)
        mPos = Hue.Vector2(mPos.x * self.zoom, mPos.y * self.zoom)
        mPos = Hue.Vector2(int(mPos.x-_map.position.x), int(mPos.y-_map.position.y)) # Account for map position
        mPos = Hue.Vector2(int(mPos.x/_map.tileSize), int(mPos.y/_map.tileSize))         # Convert mouse position to grid cells
        mPos = Hue.Vector2(int(mPos.x)*_map.tileSize, int(mPos.y)*_map.tileSize)         # Convert back into pixel values
        return mPos

    def RenderCursorSelection_Tile(self):
        if (self.state._map and self.state.tileIndex != None and self.state.tile and self.state.tool == "Draw" and len(self.maps[self.state._map].tileViews)):
            tile = self.state.tile.copy()
            tile.set_alpha(195)
            pos = [self.cursor.position.x-8, self.cursor.position.y-8]
            self.window.blit(self.state.tile, pos)

    def RenderGrid(self):
        if (len(self.maps) and self.state._map):
            _map = self.maps[self.state._map]
            if (not self.state.grid and _map.rendered): _map.rendered = False

    def RenderComponents(self):
        for component in self.components:
            if (component != "tileViews" and self.components[component].visible):
                self.components[component].Render()
                if (hasattr(self.components[component], "buttons")):
                    for button in self.components[component].buttons:
                        bttn = self.components[component].buttons[button]
                        Hue.drawRect(self.window, Hue.createRect(bttn.position, [bttn.size.x+1, bttn.size.y+1]), self.theme["Trim"], 2)
                        bttn.Render()
        for tab in self.tabs:
            for button in self.tabs[tab].buttons:
                bttn = self.tabs[tab].buttons[button]
                Hue.drawRect(self.window, Hue.createRect(bttn.position, bttn.size), self.theme["Trim"], 1)
                bttn.Render()
        for menu in self.menus:
            if (self.menus[menu].active):
                for button in self.menus[menu].buttons:
                    bttn = self.menus[menu].buttons[button]
                    Hue.drawRect(self.window, Hue.createRect(bttn.position, bttn.size), self.theme["Trim"], 1)
                    bttn.Render()

    def RenderUI(self):
        for layer in self.editorLayers:
            for group in self.editorLayers[layer]:
                if (layer == "UI" and not self.state.UIRendered): self.editorLayers[layer][group].draw(self.window)
        self.RenderMenus()
        self.ManageTileViews()
        self.RenderComponents()
        self.ManageFooter()
        self.ManageTabs()

    def RenderMenus(self):
        for menu in self.menus:
            if (self.menus[menu].active):
                self.menus[menu].Render()
                self.ManageMenus()
                [self.menus[menu].fields[field].Render() for field in self.menus[menu].fields]
            else: ...

    def Render(self):
        for layer in self.editorLayers:
            for group in self.editorLayers[layer]:
                if (layer != "UI"): self.editorLayers[layer][group].draw(self.screen)
        self.ManageMaps()
        self.RenderGrid()
        if (type(self.state.selection) == Hue.Rect and self.state._map):
            # Draw the selection rectangle
            Hue.drawRect(self.maps[self.state._map].image, self.state.selection, [255, 0, 0])

            # Calculate the start and end grid positions based on the selection rectangle
            startX = self.state.selection.left // self.maps[self.state._map].tileSize
            endX = (self.state.selection.right + self.maps[self.state._map].tileSize) // self.maps[self.state._map].tileSize
            startY = self.state.selection.top // self.maps[self.state._map].tileSize
            endY = (self.state.selection.bottom + self.maps[self.state._map].tileSize) // self.maps[self.state._map].tileSize

            # Iterate over tiles within the selection rectangle
            for x in range(startX, endX):
                for y in range(startY, endY):
                    # Calculate the screen position for the tile
                    tileScreenX = x * self.maps[self.state._map].tileSize
                    tileScreenY = y * self.maps[self.state._map].tileSize
                    # Create a rectangle for the tile
                    tileRect = Hue.Rect(tileScreenX, tileScreenY, self.maps[self.state._map].tileSize, self.maps[self.state._map].tileSize)
                    # Draw a red rectangle over the tile
                    Hue.drawRect(self.maps[self.state._map].image, tileRect, [255, 0, 0])

    def Exit(self):
        print("-- Exiting WorldForge2! --")
        pg.quit()
        sys.exit()

    def SendFrame(self):
        self.window.blit(Hue.scaleSurface(self.screen, (self.dimensions["Window"][0]/self.zoom, self.dimensions["Window"][1]/self.zoom)), (0,0))
        if (not self.state.UIRendered): self.RenderUI()
        self.ManageState()
        self.editorLayers["UI"][0].remove(self.cursor)
        self.editorLayers["UI"][0].add(self.cursor)
        self.RenderCursorSelection_Tile()
        Hue.sendFrame()

    def ToggleLayerMenuCallBack(self):
        self.state.layerMenu = not self.state.layerMenu
        self.components["Layer-Menu"].visible = not self.components["Layer-Menu"].visible
        if (self.state.layerMenu):
            self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
            [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
        else:
            [self.editorLayers["UI"][0].remove(self.components["Layer-Menu"].buttons[button]) for button in self.components["Layer-Menu"].buttons]
            self.editorLayers["UI"][0].remove(self.components["Layer-Menu"])
    
    def LastLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            if (not self.state.layerMenu):
                self.state.layerMenu = True
                self.components["Layer-Menu"].visible = True
                self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
                [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
            layer = self.state.layer
            subLayer = self.state.layerState[layer]
            if (subLayer-1 >= 0):
                self.state.layerState[layer] -= 1
    
    def NextLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            if (not self.state.layerMenu):
                self.state.layerMenu = True
                self.components["Layer-Menu"].visible = True
                self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
                [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
            layer = self.state.layer
            _map = self.maps[self.state._map]
            subLayer = self.state.layerState[layer]
            if (subLayer+1 <= 99 and subLayer+1 in _map.layers[layer]):
                self.state.layerState[layer] += 1
    
    def NewLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            if (not self.state.layerMenu):
                self.state.layerMenu = True
                self.components["Layer-Menu"].visible = True
                self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
                [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
            layer = self.state.layer
            _map = self.maps[self.state._map]
            subLayer = self.state.layerState[layer]
            if (subLayer+1 <= 99):
                _map.NewLayer(layer)
                self.state.layerState[self.state.layer] += 1

    def DumpLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            if (not self.state.layerMenu):
                self.state.layerMenu = True
                self.components["Layer-Menu"].visible = True
                self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
                [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
            layer = self.state.layer
            _map = self.maps[self.state._map]
            subLayer = self.state.layerState[self.state.layer]
            print(subLayer)
            _map.DumpLayer(layer, subLayer)
    
    def RemLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            if (not self.state.layerMenu):
                self.state.layerMenu = True
                self.components["Layer-Menu"].visible = True
                self.editorLayers["UI"][0].add( self.components["Layer-Menu"] )
                [self.editorLayers["UI"][0].add( self.components["Layer-Menu"].buttons[button] ) for button in self.components["Layer-Menu"].buttons]
            layer = self.state.layer
            _map = self.maps[self.state._map]
            subLayer = self.state.layerState[self.state.layer]
            print(subLayer)
            if (subLayer-1 >= 0):
                _map.RemLayer(layer, subLayer)
                self.state.layerState[self.state.layer] -= 1
            else: print("Cannot Remove Base Layer! Try Dumping the layer to unload it, or clear it!")

    def LayerMenuFunction(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps and self.components["Layer-Menu"].visible):
            _map = self.maps[self.state._map]
            layer = self.state.layer
            subLayer = str(self.state.layerState[self.state.layer])
            #self.components["Layer-Menu"].buttons["BGCOUNT"]
            self.components["Layer-Menu"].buttons["BGCOUNT"].text = str(len(_map.layers["background"]))
            #self.components["Layer-Menu"].buttons["BGLAYERNUM"]
            self.components["Layer-Menu"].buttons["BGLAYERNUM"].text = str(self.state.layerState["background"])

            #self.components["Layer-Menu"].buttons["MGCOUNT"]
            self.components["Layer-Menu"].buttons["MGCOUNT"].text = str(len(_map.layers["midground"]))
            #self.components["Layer-Menu"].buttons["MGLAYERNUM"]
            self.components["Layer-Menu"].buttons["MGLAYERNUM"].text = str(self.state.layerState["midground"])

            #self.components["Layer-Menu"].buttons["FGCOUNT"]
            self.components["Layer-Menu"].buttons["FGCOUNT"].text = str(len(_map.layers["foreground"]))
            #self.components["Layer-Menu"].buttons["FGLAYERNUM"]
            self.components["Layer-Menu"].buttons["FGLAYERNUM"].text = str(self.state.layerState["foreground"])

            match layer:
                case "background":
                    rect = self.components["Layer-Menu"].buttons["BGLAYER"].rect
                    rect = Hue.createRect( [rect.x, rect.y], [rect.w+1, rect.h+1])
                    Hue.drawRect(self.window, rect, self.theme["Hover"], 2)
                case "midground":
                    rect = self.components["Layer-Menu"].buttons["MGLAYER"].rect
                    rect = Hue.createRect( [rect.x, rect.y], [rect.w+1, rect.h+1])
                    Hue.drawRect(self.window, rect, self.theme["Hover"], 2)
                case "foreground":
                    rect = self.components["Layer-Menu"].buttons["FGLAYER"].rect
                    rect = Hue.createRect( [rect.x, rect.y], [rect.w+1, rect.h+1])
                    Hue.drawRect(self.window, rect, self.theme["Hover"], 2)
                case _:
                    pass

    def LastBaseLayerCallBack(self):
        match self.state.layer:
            case "background":
                return "AT LAST BASE LAYER!!!!"
            case "midground":
                self.state.layer = "background"
                return "MOVING FROM MIDGROUND TO BACKGROUND!!!!"
            case "foreground":
                self.state.layer = "midground"
                return "MOVING FROM FOREGROUND TO MIDGROUND!!!!"
            case _: pass

    def NextBaseLayerCallBack(self):
        match self.state.layer:
            case "background":
                self.state.layer = "midground"
                return "MOVING FROM BACKGROUND TO MIDGROUND !!!!"
            case "midground":
                self.state.layer = "foreground"
                return "MOVING FROM MIDGROUND TO FOREGROUND!!!!"
            case "foreground":
                return "AT MAX BASE LAYER!!!!"
            case _: pass

    def BackGroundLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            self.state.layer = "background"

    def MidGroundLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            self.state.layer = "midground"

    def ForeGroundLayerCallBack(self):
        if (self.state._map and len(self.maps) and self.state._map in self.maps):
            self.state.layer = "foreground"

    def FillFunction(self, pos, tileID, selection=None):
        _map = self.maps[self.state._map]
        fillCommand = FillCommand(self, _map, self.state.layer, self.state.layerState[self.state.layer], pos, tileID, selection)
        _map.ExecuteCommand(fillCommand)

    def SelectFunction(self):
        if(self.state.tool == "Select"):
            if (self.state._map and self.state.clicking and not self.state.component and not self.state.header and not self.state.viewComponent and not self.state.button and self.CursorIsOn_Z(self.maps[self.state._map])):
                cPos = self.CursorPosition_Map(self.maps[self.state._map])
                if (self.state.selectDone):
                    if (
                        self.state.selection and
                        cPos.y >= self.state.selection.top and
                        cPos.x >= self.state.selection.left and
                        cPos.x <= self.state.selection.right and
                        cPos.y <= self.state.selection.bottom
                    ): pass #print("Inside Select Region")
                    else:
                        self.state.selection = None
                        self.state.selectDone = False
                        self.state.selectOrigin = None
                else:
                    if (self.state.selectOrigin == None):
                        if (self.state._map and not 
                            self.state.component and not 
                            self.state.header and 
                            self.CursorIsOn_Z(self.maps[self.state._map]) and 
                            self.state.tool == "Select"):
                            self.state.selectDone = False
                            self.state.selectOrigin = self.CursorPosition_Map(self.maps[self.state._map])
                            self.state.selection = Hue.createRect(self.state.selectOrigin, [self.maps[self.state._map].tileSize - 1, self.maps[self.state._map].tileSize - 1])
                    
                    elif (type(self.state.selection) == Hue.Rect):
                        self.state.selectDone = False
                        dX = cPos.x - self.state.selectOrigin.x
                        dY = cPos.y - self.state.selectOrigin.y
                        # Adjust width and height to be at least tileSize
                        width = max(abs(dX), self.maps[self.state._map].tileSize - 1)
                        height = max(abs(dY), self.maps[self.state._map].tileSize - 1)
                        # Update the rectangle's position and size
                        self.state.selection.topleft = min(self.state.selectOrigin.x, cPos.x), min(self.state.selectOrigin.y, cPos.y)
                        self.state.selection.size = width, height
                        # Capture Tiles Within Select Region
                        key = f"{int(cPos.x)},{int(cPos.y)}"
                self.maps[self.state._map].rendered = False
            elif (self.state._map and not self.state.component and not self.state.header and not self.state.viewComponent and not self.state.button and self.CursorIsOn_Z(self.maps[self.state._map]) and self.state.clickingR):
                self.state.selection = None
                self.state.selectDone = False
                self.state.selectOrigin = None
            else:
                self.state.selectDone = True
        else:
            self.state.selectDone = True

    def PropViewCallBack(self, pos, layer, props):
        self.state.menu = self.menus["PropView"]
        self.state.menu.active = True
        self.editorLayers["UI"][0].add(self.state.menu)
        [self.editorLayers["UI"][0].add(self.state.menu.fields[field]) for field in self.state.menu.fields]
        [self.editorLayers["UI"][0].add(self.state.menu.buttons[button]) for button in self.state.menu.buttons]
        
        self.menus["PropView"].buttons["Pos"].text = pos
        self.menus["PropView"].buttons["Layer"].text = layer

    def EditTileProps_Collider(self, remove:bool=False):
        #self.state.clicking = False
        #self.state.clickingR = False
        if (self.state._map and len(self.maps) and self.state._map in self.maps and not self.state.component):
            _map = self.maps[self.state._map]
            pos = self.CursorPosition_Map(_map)
            
            if(not remove): _map.AddColliderAt(pos)
            else: _map.RemColliderAt(pos)

    def RemSelect(self):
        if (self.state._map and self.state.selectDone):
            _map = self.maps[self.state._map]
            selection = self.state.selection

            removeSelectionCommand = RemoveSelectionCommand(self, _map, self.state.layer, self.state.layerState[self.state.layer], selection)
            _map.ExecuteCommand(removeSelectionCommand)

            # Reset the selection state after removing the tiles
            self.state.selection = None
            self.state.selectDone = False
            
            self.state.clickingR = False

    def AllSelect(self):
        if (self.state._map):
            _map = self.maps[self.state._map]
            mapSize = _map.size

            self.state.selection = Hue.Rect(0, 0, mapSize[0], mapSize[1])
            self.state.selectDone = True

            print("Entire map selected")

    def ImportCallBack(self, mapPath:str=None):
        layers = [ "background", "midground", "foreground" ]
        if (mapPath == None): mapPath = self.ManageSelection_File("Select Map File")
        if (mapPath):
            if (mapPath.endswith(".wf2")):
                try:
                    with open(mapPath, "r") as file:
                        # Load the JSON data and initialize a Map() instance with it
                        mapData = json.load(file)
                        data = mapData["mapInfo"]
                        self.AddMap(
                            savePath=os.path.dirname(mapPath),
                            tileSize=data["tilesize"],
                            mapSize=Hue.Vector2(data["width/height"]),
                            name=data["name"]
                        )
                        self.maps[self.state._map].ImportData(mapData)

                        views = []
                        corruptTiles = []
                        for layer in layers:
                            for tile in mapData[layer]:
                                tileData = mapData[layer][tile]
                                if (tileData["asset"] in self.registry["tilesets"]):
                                    assetPath = f"{tileData["asset"]}"
                                elif (os.path.exists(tileData["asset"])):
                                    assetPath = f"{tileData["asset"]}"
                                    self.WriteToRegistry_Tilesets(tileData["asset"], os.path.dirname(tileData["asset"]))
                                else: 
                                    corruptTiles.append(tileData)
                                    assetPath = "..\\assets\\tile\\CorrupTile.png"
                        
                                if (assetPath not in views): 
                                    self.AddTileView(assetPath)
                                    views.append(assetPath)

                        for layer in layers:
                            for tile in mapData[layer]:
                                pos = tile.split(";")
                                pos = [int(pos[0]), int(pos[1])]
                                tileData = mapData[layer][tile]
                                tileIndex = tileData["id"]

                                _map = self.maps[self.state._map]
                                for tv in self.maps[self.state._map].tileViews: # Make sure tiles are placed bassed on their asset
                                    tileView = self.maps[self.state._map].tileViews[tv]
                                    # if (tileData["asset"] == os.path.basename(tileView.path)): # no.. not yet.. 
                                    if (tileData["asset"] == tileView.path):
                                        self.state.view = tv
                                        self.state.layer = tileData["layer"]
                                        self.state.tile = tileView.tile["images"][tileIndex]

                                        placeTileCommand = PlaceTileCommand(self, _map, tileData["layer"], tileData["subLayer"], Hue.Vector2(pos), tileIndex)
                                        _map.ExecuteCommand(placeTileCommand)

                                if (tileData["properties"]["collisions"]): _map.AddColliderAt(pos)
                        
                        self.maps[self.state._map].rendered = False

                except FileNotFoundError:
                    # Handle the case where the file is not found
                    print(f"File not found: {mapPath}")
            else:
                # Handle the case where the selected file is not a JSON file
                print(f"Invalid file format: {mapPath}")
    
    def SaveMap(self):
        self.maps[self.state._map].SaveData(self.state.menu.fields["Map-Name"].text)
        self.maps[self.state._map].ExportPNG()
        self.CloseTabCallBack()
        self.EscapeCallBack()

    def SaveAsCallBack(self):
        self.state.menu = self.menus["Save-As"]
        self.state.menu.active = True
        self.state.menu.fields["Map-Name"].text = self.state._map
        
        self.editorLayers["UI"][0].add(self.state.menu)
        [self.editorLayers["UI"][0].add(self.state.menu.buttons[button]) for button in self.state.menu.buttons]

    def NewMapCallBack(self):
        if (len(self.maps)+1 <= 5):
            self.state.menu = self.menus["New-Map"]
            self.state.menu.active = True
            [self.editorLayers["UI"][0].add(self.state.menu.fields[field]) for field in self.state.menu.fields]
            self.editorLayers["UI"][0].add(self.state.menu)
        else: print("5 Maps Reached! Save and close one of your maps to add a new one!")

    def EscapeCallBack(self):
        if (self.state.selectDone and self.state.selection):
            self.state.selection = None
            self.state.selectDone = False
            self.state.selectOrigin = None
        else:
            self.DrawCallBack()
            self.state.menu = None
            self.state.tile = None
            self.state.tileIndex = None
            [v.kill() for k,v in self.menus.items()]
            for k,v in self.menus.items(): v.active = False 
            [v.fields[field].kill() for k,v in self.menus.items() for field in v.fields]
            [v.buttons[button].kill() for k,v in self.menus.items() for button in v.buttons]

    def CloseTabCallBack(self):
        print(f"Close Tab {self.state.activeTab}: {self.tabs[self.state.activeTab]}!")
        if (len(self.maps) and self.maps.__contains__(self.state._map) and self.maps[self.state._map].saved):
            print(f"Killing Map {self.state._map}")
            [self.maps[self.state._map].tileViews[view].kill() for view in self.maps[self.state._map].tileViews]
            self.maps[self.state._map].kill()
            self.tabs[self.state.activeTab].kill()
            self.tabs[self.state.activeTab].buttons["Close"].kill()
            
            closedMap = self.state._map
            closedTab = self.tabs[self.state.activeTab]

            self.maps.pop(self.state._map)
            self.tabs.pop(self.state.activeTab)

            if (len(self.maps) and len(self.tabs)):
                self.state._map = list(self.maps.keys())[len(self.maps)-1]
                self.state.activeTab = list(self.tabs.keys())[len(self.tabs)-1]

                self.maps[self.state._map].active = True
                self.editorLayers["main"][0].add(self.maps[self.state._map])
                if (len(self.maps[self.state._map].tileViews)):
                    [self.editorLayers["UI"][0].add(self.maps[self.state._map].tileViews[view]) for view in self.maps[self.state._map].tileViews]

                for i,tab in enumerate(self.tabs):
                    if (self.tabs[tab].position.x > closedTab.position.x):
                        shift = TAB_GAP
                        if (self.tabs[tab].position.x - shift >= TAB_MIN):
                            self.tabs[tab].position.x -= shift
                            self.tabs[tab].buttons["Close"].position.x -= shift
                            self.tabs[tab].buttons["Close"].Update()
                            self.tabs[tab].buttons["Close"].Render()
                        else: print("Closed Index", i)
            else:
                self.state._map = None
                self.state.activeTab = None
        else: 
            print("Map Yet To Be Saved")
            self.SaveAsCallBack()

    def NextViewCallBack(self):
        self.state.tileIndex = None
        if (self.state.view and int(self.state.view)+1 < len(self.maps[self.state._map].tileViews) and self.maps[self.state._map].tileViews.__contains__(str(int(self.state.view)+1))):
            self.maps[self.state._map].tileViews[self.state.view].visible = False
            self.editorLayers["UI"][0].remove(self.maps[self.state._map].tileViews[self.state.view])
            
            self.state.view = str(int(self.state.view)+1)
            self.maps[self.state._map].tileViews[self.state.view].visible = True
            self.editorLayers["UI"][0].add(self.maps[self.state._map].tileViews[self.state.view])
            
            self.editorLayers["UI"][0].remove(self.cursor)
            self.editorLayers["UI"][0].add(self.cursor)
        return "At Newest TileView!"
    
    def LastViewCallBack(self):
        self.state.tileIndex = None
        if (self.state.view and int(self.state.view)-1 >= 0  and self.maps[self.state._map].tileViews.__contains__(str(int(self.state.view)-1))): 
            self.maps[self.state._map].tileViews[self.state.view].visible = False
            self.editorLayers["UI"][0].remove(self.maps[self.state._map].tileViews[self.state.view])
            
            self.state.view = str(int(self.state.view)-1)
            self.maps[self.state._map].tileViews[self.state.view].visible = True
            self.editorLayers["UI"][0].add(self.maps[self.state._map].tileViews[self.state.view])
            
            self.editorLayers["UI"][0].remove(self.cursor)
            self.editorLayers["UI"][0].add(self.cursor)
        else: return "At Last TileView!"
    
    def NewViewCallBack(self):
        self.state.tileIndex = None
        try:
            path = self.ManageSelection_File("Select Tileset Image")
            self.AddTileView(path)
        except (FileNotFoundError, pg.error):
            print(f"Error Creating New Tileset From Path {path}")

    def HideViewCallBack(self, clicked:bool=True):
        if (clicked and self.state._map and self.state.view and len(self.maps[self.state._map].tileViews) and self.state.tool == "Swap"):
            self.SwapTileView()
        elif (clicked and self.state._map and self.state.view and len(self.maps[self.state._map].tileViews) and self.state.tool != "Swap"):
            self.maps[self.state._map].tileViews[self.state.view].visible = not self.maps[self.state._map].tileViews[self.state.view].visible
            if (not self.maps[self.state._map].tileViews[self.state.view].visible): self.editorLayers["UI"][0].remove(self.maps[self.state._map].tileViews[self.state.view])
            else: 
                self.editorLayers["UI"][0].add(self.maps[self.state._map].tileViews[self.state.view])
                self.editorLayers["UI"][0].remove(self.cursor)
                self.editorLayers["UI"][0].add(self.cursor)
        elif (not clicked and self.state._map and self.state.view and len(self.maps[self.state._map].tileViews)):
            self.maps[self.state._map].tileViews[self.state.view].visible = not self.maps[self.state._map].tileViews[self.state.view].visible
            if (not self.maps[self.state._map].tileViews[self.state.view].visible): self.editorLayers["UI"][0].remove(self.maps[self.state._map].tileViews[self.state.view])
            else: 
                self.editorLayers["UI"][0].add(self.maps[self.state._map].tileViews[self.state.view])
                self.editorLayers["UI"][0].remove(self.cursor)
                self.editorLayers["UI"][0].add(self.cursor)

    def ToolCallBack(self):
        self.components["ToolBar"].visible = not self.components["ToolBar"].visible
        if (not self.components["ToolBar"].visible): 
            for button in self.components["ToolBar"].buttons:
                self.editorLayers["UI"][0].remove(self.components["ToolBar"].buttons[button])
            self.editorLayers["UI"][0].remove(self.components["ToolBar"])
        else: 
            self.editorLayers["UI"][0].add(self.components["ToolBar"])
            for button in self.components["ToolBar"].buttons:
                self.editorLayers["UI"][0].add(self.components["ToolBar"].buttons[button])
            self.editorLayers["UI"][0].remove(self.cursor)
            self.editorLayers["UI"][0].add(self.cursor)

    def PathCallBack(self):
        newPath = self.ManageSelection_SaveFile()
        if (newPath and self.state._map): self.maps[self.state._map].path = newPath
    
    def ExportCallBack(self):
        if (self.state._map):
            self.maps[self.state._map].saved = True
            self.maps[self.state._map].SaveData()
            self.maps[self.state._map].ExportPNG()

    def SelectCallBack(self):
        image = self.storage.GetImage("Select-Logo32")
        if (self.cursor.image != image and self.state.tool != "Select"):
            self.cursor.image = image
            self.state.tool = "Select"
        else:
            self.DrawCallBack()

    def SwapCallBack(self):
        image = self.storage.GetImage("Swap-Logo32")
        if (self.cursor.image != image and self.state.tool != "Swap"): 
            self.cursor.image = image
            self.state.tool = "Swap"
        else: 
            self.cursor.image = self.storage.GetImage("Cursor")
            self.state.tool = "Draw"
    
    def TilePropsCallBack(self):
        image = self.storage.GetImage("Collider-Logo32")
        if (self.cursor.image != image and self.state.tool != "Props"): 
            self.cursor.image = image
            self.state.tool = "Props"
        else: 
            self.DrawCallBack()

    def SwapFunction(self):
        self.state.clicking = False
        if (self.state._map):
            pos = self.CursorPosition_Map(self.maps[self.state._map])
            pos = f"{int(pos[0])};{int(pos[1])}"
            tileIndex = self.maps[self.state._map].GetTileID(pos)
            if (tileIndex != None):
                self.state.tileIndex = tileIndex
                self.state.tile = self.maps[self.state._map].tileViews[self.state.view].tile["images"][self.state.tileIndex]
                self.DrawCallBack()

    def DrawCallBack(self):
        image = self.storage.GetImage("Cursor")
        if (self.cursor.image != image and self.state.tool != "Draw"): 
            self.cursor.image = image
            self.state.tool = "Draw"

    def FillCallBack(self):
        image = self.storage.GetImage("Fill-Logo32")
        if (self.cursor.image != image and self.state.tool != "Fill"): 
            self.cursor.image = image
            self.state.tool = "Fill"
        else: 
            self.cursor.image = self.storage.GetImage("Cursor")
            self.state.tool = "Draw"

    def EraseCallBack(self):
        image = self.storage.GetImage("Eraser-Logo32")
        if (self.cursor.image != image and self.state.tool != "Eraser"): 
            self.cursor.image = image
            self.state.tool = "Eraser"
        else: 
            self.cursor.image = self.storage.GetImage("Cursor")
            self.state.tool = "Draw"

    def DropFileCallBack(self, file):
        base = os.path.basename(file)
        if (str(base).endswith(".wf2")):
            try:
                self.ImportCallBack(file)
            except:
                print("Error Importing Map!")
        if (str(base).endswith(( ".png",".jpg",".svg" ))):
            try:
                self.AddTileView(file)
            except:
                print("Error Making New TileView!")

    def Run(self):
        self.state.loading = True
        while self.state.loading:
            self.LoadForge()
        while self.state.running and not self.state.loading:
            self.dt = Hue.tickGetDeltaTime(self.clock, self.system["FPS"])
            self.window.fill(self.theme["Background"])
            self.screen.fill(self.theme["Background"])
            self.ManageComponents()
            self.Events()
            self.cursor.Update()
            self.Render()
            self.SendFrame()

            

WorldForge().Run()