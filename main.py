import math
import time
import random
import threading
import arcade
from arcade.key import RIGHT

SCREENWIDTH=700
SCREENHEIGHT=600


class EnamySpaceShip(arcade.Sprite) :
    def __init__(self):
            super().__init__(':resources:images/space_shooter/playerLife1_orange.png')
            self.width = 40
            self.height = 40
            self.center_x = random.randint(self.width , SCREENWIDTH - self.width)
            self.center_y = SCREENHEIGHT + self.height//2
            self.speed = 3

    def move(self):
        self.center_y -= self.speed


class OurSpaceShip(arcade.Sprite) :
    def __init__(self) :
            super().__init__(':resources:images/space_shooter/playerShip1_green.png')
            self.width = 50
            self.height = 50
            self.score = 0
            self.live = 3
            self.center_x = SCREENWIDTH//2
            self.center_y = 32
            self.angle = 0
            self.change_angle = 0
            self.speed = 4
            self.bullet_list = []
            self.lives_image = arcade.load_texture("lives.jpg")
            self.sound = arcade.load_sound(":resources:sounds/hurt5.wav")

    def Fire(self) :
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(self.sound)

             

    def rotate(self):
        self.angle += self.speed * self.change_angle

class Bullet(arcade.Sprite) :
    def __init__(self,airplane) :
            super().__init__(':resources:images/space_shooter/laserRed01.png')
            self.center_x = airplane.center_x
            self.center_y = airplane.center_y
            self.speed = 6
            self.angle = airplane.angle
            self.change_angle = 0

    def move(self) :
        self.center_x -= self.speed * math.sin(math.radians(self.angle))
        self.center_y += self.speed * math.cos(math.radians(self.angle))  

      

          

class Game(arcade.Window) :
    def __init__(self) :
        super().__init__(SCREENWIDTH,SCREENHEIGHT,"Airplane Game 🚀", antialiasing=False)
        arcade.set_background_color(arcade.color.DARK_BLUE)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.gameover_image = arcade.load_texture("GameOver.png")
        self.boom = arcade.load_sound(":resources:sounds/fall1.wav")
        self.MySpaceShip = OurSpaceShip()
        self.Enemy_list = []
        self.start_time = time.time()
        self.my_thread =threading.Thread(target = self.AddEnemy)
        self.my_thread.start()

    def AddEnemy(self):
        while True:
            self.Enemy_list.append(EnamySpaceShip())
            time.sleep(5)
            for enemy in self.Enemy_list:
                enemy.speed += 0.1

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREENWIDTH,SCREENHEIGHT,self.background_image)
        self.MySpaceShip.draw()

        for enemy in self.Enemy_list :
            enemy.draw()

        for bul in self.MySpaceShip.bullet_list :
            bul.draw()    

        arcade.draw_text(f"SCORES: {self.MySpaceShip.score}",SCREENWIDTH-170,SCREENHEIGHT-580,arcade.color.WILD_ORCHID,20,width = 10,align="left")

        for i in range(self.MySpaceShip.live):
            arcade.draw_lrwh_rectangle_textured(30 * i, 10, 30, 30, self.MySpaceShip.lives_image)
            
        if self.MySpaceShip.live < 1:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREENWIDTH, SCREENHEIGHT, self.gameover_image)    

    def on_update(self, delta_time: float):
       
        self.MySpaceShip.rotate()

        for enemy in self.Enemy_list :
            enemy.move()

        for bul in self.MySpaceShip.bullet_list :
            bul.move()       

        for enemy in self.Enemy_list:
            for bul in self.MySpaceShip.bullet_list:

                if arcade.check_for_collision(bul, enemy):
                    arcade.play_sound(self.boom)
                    self.MySpaceShip.bullet_list.remove(bul)
                    self.Enemy_list.remove(enemy)
                    self.MySpaceShip.score += 1

        for bul in self.MySpaceShip.bullet_list:
            if (bul.center_y > self.height or bul.center_x < 0 or bul.center_x > self.width):
                self.MySpaceShip.bullet_list.remove(bul)   

        for enemy in self.Enemy_list:
            if enemy.center_y < 0:
                self.MySpaceShip.live -= 1
                self.Enemy_list.remove(enemy)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.MySpaceShip.Fire()
        elif symbol == arcade.key.LEFT:
            self.MySpaceShip.change_angle = 1
        elif symbol == arcade.key.RIGHT:      
            self.MySpaceShip.change_angle = -1  
 
    def on_key_release(self, symbol: int, modifiers: int):
        self.MySpaceShip.change_angle = 0
        self.MySpaceShip.change_x = 0
        self.MySpaceShip.change_y = 0

MyGame=Game()       
arcade.run()     