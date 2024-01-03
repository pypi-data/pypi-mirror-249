import os, math
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

GAME_CLASS = None

class Game:
    def __init__(self,size=(500,500),icon=None):
        global GAME_CLASS
        GAME_CLASS = self
        self._size = size
        if icon != None:
            icon = pygame.image.load(icon)
        self._config = {
            "fps": 30,
            "title": "Unithon Game",
            "icon": icon
        }
        self._scenes = {}
        self._current_scene = None
        self.keys = {}
        pygame.init()

    def set(self,config,val):
        self._config[config] = val

    def add_scene(self, scene):
        self._scenes[scene.__name__] = scene

    def change_scene(self,name):
        self._current_scene = self._scenes[name](self)
        self._current_scene.init()

    def run(self):
        self.change_scene("Main")
        pygame.display.set_caption(self._config["title"])
        screen = pygame.display.set_mode(self._size)
        if self._config["icon"] != None:
            pygame.display.set_icon(self._config["icon"])
        clock = pygame.time.Clock()
        run = True
        while run:
            self._update(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        event.unicode = "ArrowLeft"
                    if event.key == pygame.K_RIGHT:
                        event.unicode = "ArrowRight"
                    if event.key == pygame.K_UP:
                        event.unicode = "ArrowUp"
                    if event.key == pygame.K_DOWN:
                        event.unicode = "ArrowDown"
                    if event.unicode != "":
                        self.keys[event.unicode] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        event.unicode = "ArrowLeft"
                    if event.key == pygame.K_RIGHT:
                        event.unicode = "ArrowRight"
                    if event.key == pygame.K_UP:
                        event.unicode = "ArrowUp"
                    if event.key == pygame.K_DOWN:
                        event.unicode = "ArrowDown"
                    if event.unicode != "":
                        self.keys[event.unicode] = False

            clock.tick(self._config["fps"])
        pygame.quit()

    def _update(self,screen):
        self._current_scene._update_obj()
        self._current_scene.update()

        screen.fill(self._current_scene._config["bg-color"])

        z_indexes = {}

        for obj in self._current_scene._objects:
            if not str(obj.z_layer) in z_indexes: z_indexes[str(obj.z_layer)] = []
            z_indexes[str(obj.z_layer)].append(obj)

        for i in range(1998):
            if not str(i-999) in z_indexes: continue
            for obj in z_indexes[str(i-999)]: obj.draw(screen)

    def drawObject(self,screen,obj,offsetX=0,offsetY=0):
        for child in obj._childs:
            self.drawObject(screen,child,offsetX=offsetX+obj.x,offsetY=offsetY+obj.y)

        obj.x += offsetX
        obj.y += offsetY
        obj.draw(screen)
        obj.x -= offsetX
        obj.y -= offsetY

def key_pressed(key):
    if not key in GAME_CLASS.keys:
        return False
    return GAME_CLASS.keys[key]

class Scene:
    def __init__(self,gameFather):
        self._config = {
            "bg-color": (0,0,0)
        }
        self._objects = []
        self._game = gameFather

    def set(self,config,val):
        self._config[config] = val

    def addObject(self,*obj):
        if len(obj) > 1:
            for objet in obj:
                self.addObject(objet)
            return
        obj = obj[0]
        self._objects.append(obj)
        obj._scene = self

    def _update_obj(self):
        for obj in self._objects:
            if hasattr(obj, "update") and callable(obj.update):
                obj.update()

class Object:
    def __init__(self, childs=[]):
        self.father = None
        self._childs = childs
        self.z_layer = 0

        self.x = 0
        self.y = 0

        self._scene = None

        if hasattr(self, "init") and callable(self.init):
            self.init()

    def draw(self,screen):
        pass

    def appendChild(self,child):
        self._childs.append(child)
        child.father = self

    def getScreenPos(self):
        if self.father == None:
            return (self.x,self.y)
        fatherPos = self.father.getScreenPos()
        return (self.x+fatherPos[0],self.y+fatherPos[1])

class HitBox(Object):
    def __init__(self,width,height):
        super().__init__()
        self.width = width
        self.height = height
        self.visible = False

    def draw(self,screen):
        if not self.visible: return
        pygame.draw.rect(screen, (255,0,0), (self.x,self.y,self.width,self.height))

    def touching_border(self):
        screenSize = GAME_CLASS._size
        if self.getScreenPos()[0] + self.width > screenSize[0]: return True
        if self.getScreenPos()[0] < 0: return True
        if self.getScreenPos()[1] + self.height > screenSize[1]: return True
        if self.getScreenPos()[1] < 0: return True
        return False
    
    def touching_hitbox(self,otherHitbox):
        if otherHitbox == self: return False

        posSelf = self.getScreenPos()
        posOther = otherHitbox.getScreenPos()

        if posSelf[0] < posOther[0] + otherHitbox.width and posSelf[0] + self.width > posOther[0]  and posSelf[1] < posOther[1] + otherHitbox.height and posSelf[1] + self.height > posOther[1]: return True

        return False

class Rect(Object):
    def __init__(self,width,height,color,childs=[]):
        super().__init__(childs=childs)
        self.width = width
        self.height = height
        self.color = color

    def draw(self,screen):
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height))

class Circle(Object):
    def __init__(self,radius,color,childs=[]):
        super().__init__(childs=childs)
        self.radius = radius
        self.color = color

    def draw(self,screen):
        pygame.draw.circle(screen,self.color,(self.x+self.radius,self.y+self.radius),self.radius)

class Text(Object):
    def __init__(self,text,size,color,font=None):
        super().__init__(childs=[])
        self.text = text
        self.size = size
        self.color = color
        self.font = font

    def draw(self, screen):
        font = pygame.font.SysFont(self.font,self.size)
        surface = font.render(self.text, True, self.color)
        screen.blit(surface,(self.x,self.y))

class Image(Object):
    def __init__(self,path,scale=1):
        super().__init__(childs=[])
        self._path = path
        self._scale = scale
        self._reloadImage()
        self.flipX = False
        self.flipY = False
    
    def get_path(self):
        return self._path
    
    def change_path(self,new_path):
        self._path = new_path
        self._reloadImage()

    def get_scale(self):
        return self._scale
    
    def change_scale(self,new_scale):
        self._scale = new_scale
        self._reloadImage()

    def _reloadImage(self):
        path = self._path
        self._surface = pygame.image.load(path)
        self._surface = pygame.transform.scale_by(self._surface, self._scale)

    def draw(self,screen):
        if self.flipX or self.flipY:
            surface = pygame.transform.flip(self._surface,self.flipX,self.flipY)
        else:
            surface = self._surface
        screen.blit(surface,(self.x,self.y))

class Sprite(Object):
    def __init__(self,childs=[]):
        super().__init__(childs=childs)
        self._animations = {}
        self.animation = None
        self._frame = 0

    def newAnimation(self,name,data):
        if not "images" in data or len(data["images"]) == 0:
            raise ValueError("The animation data must have a 'images' key with one or more images.")
        if not "fps" in data and len(data["images"]) > 1:
            raise ValueError("The animation data must have a 'fps' key with the fps of the animation.")
        self._animations[name] = data

    def draw(self,screen):
        anim = self._animations[self.animation]
        frame = math.floor(self._frame/(GAME_CLASS._config["fps"]/anim["fps"])) % len(anim["images"])
        image = anim["images"][frame]
        image.x += self.x
        image.y += self.y
        image.draw(screen)
        image.x -= self.x
        image.y -= self.y
        self._frame += 1