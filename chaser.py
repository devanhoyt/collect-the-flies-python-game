import random
import arcade
import math
import os


#SETTINGS
enemy_list = [10, 15, 20, 20, 30, 40, 40, 50, 60, 100]

#How big the player is
SPRITE_SCALING_PLAYER = 0.5
#How big the Enemy is
SPRITE_SCALING_ENEMY = .2#random.choice(enemy_list)
#How fast the enemy is
enemy_SPEED = 5 
#How many enemies there are
enemy_COUNT = 15 #random.choice(enemy_list)
#Number of flies
FLY_COUNT = 10
#Screen size and info
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Chaser game"

SPRITE_SPEED = 5

#Enemy class, different attributes for the enemy are here
class Enemy(arcade.Sprite):
   
    def following_enemy(self, player_sprite):
      

        self.center_x += self.change_x
        self.center_y += self.change_y

        #Changing the number in the randrange below changes how often the enemies course correct to hit the player
        if random.randrange(80) == 0:
            start_x = self.center_x
            start_y = self.center_y

            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * enemy_SPEED
            self.change_y = math.sin(angle) * enemy_SPEED

class Fly(arcade.Sprite):

   pass

class MyGame(arcade.Window):
   

    def __init__(self):
      
        
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.set_mouse_visible(False)

        self.player_list = None
        self.enemy_list = None
        self.fly_list = None
        self.player_sprite = None
        self.score = 0
        
        #Background color
        arcade.set_background_color(arcade.color.BONE)
        #Sound file for when enemy hits player
        self.hit_enemy_sound = arcade.load_sound(":resources:sounds/hurt2.wav")
        self.hit_fly_sound = arcade.load_sound(":resources:sounds/coin4.wav")
        

    def setup(self):
       

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.fly_list = arcade.SpriteList()

        # Score
        self.score = 0

        
        self.player_sprite = arcade.Sprite(":resources:images/enemies/frog.png",
                                           SPRITE_SCALING_PLAYER)#, max_health=10)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        # Create the enemys
        for i in range(enemy_COUNT):
            # Create the enemy instance
            
            enemy = Enemy(":resources:images/enemies/saw.png", SPRITE_SCALING_ENEMY)

            enemy.center_y = random.randrange(SCREEN_HEIGHT)
            enemy.center_x = random.randrange(SCREEN_WIDTH)
            self.enemy_list.append(enemy)
            
        for i in range(FLY_COUNT):
            #create the fly instances
            fly = Fly(":resources:images/enemies/fly.png", SPRITE_SCALING_ENEMY)

            fly.center_x = random.randrange(SCREEN_WIDTH)
            fly.center_y = random.randrange(SCREEN_HEIGHT)
            self.fly_list.append(fly)

#Anyhting that goes on the screen goes through draw
    def on_draw(self):
        #Sprites
        arcade.start_render()
        self.enemy_list.draw()
        self.player_list.draw()
        self.fly_list.draw()

        #Text
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)
        arcade.draw_text("Collect the flies to win!",
                         SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.GRAY, font_size=20, anchor_x="center",
                        )

    #Sets the game controls to the mouse. Could also be keyboard
    def on_mouse_motion(self, x, y, dx, dy):
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y


    #Game logic
    def on_update(self, delta_time):
        
        #Sets the enemies to chase the frog
        for enemy in self.enemy_list:
            enemy.following_enemy(self.player_sprite)


        #Checks for hits
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        collect_list = arcade.check_for_collision_with_list(self.player_sprite, self.fly_list)

        #If enemy hits
        for enemy in hit_list:
            enemy.kill()
            arcade.play_sound(self.hit_enemy_sound)
            self.score -= 1
        
        #If player touches fly
        for fly in collect_list:
            fly.remove_from_sprite_lists()
            arcade.play_sound(self.hit_fly_sound)
            self.score += 3
            
        #Game ending condition 
        if len(self.fly_list) == 0:
            
            arcade.exit()
             




def main():
    
    window = MyGame()
    window.setup()
    

    arcade.run()


if __name__ == "__main__":
    main()