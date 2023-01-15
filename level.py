import pygame
import os
import math

pygame.font.init()

class Level:
    def __init__(self):
        self.TESLA_HIT_BAT = pygame.USEREVENT + 1
        self.TESLA_HIT_GAS = pygame.USEREVENT + 2
        self.TESLA_NO_JUICE = pygame.USEREVENT + 3
        self.TESLA_HIT_HONDA = pygame.USEREVENT + 4
        self.BATTERY_FONT = pygame.font.SysFont('comicsans', 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        self.LOSER_FONT = pygame.font.SysFont('comicsans', 60)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 128, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255,255,0)
        self.WIDTH, self.HEIGHT = 900, 500
        self.ROAD_IMAGE = pygame.image.load((os.path.join('Assets', 'roads.jpg')))
        self.background = pygame.transform.scale(self.ROAD_IMAGE, (self.WIDTH, self.HEIGHT))
        self.X_OFFSET = 20
        self.FPS = 100
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_window(self,car, text=""):
        self.WIN.blit(self.background, (0, 20))
        pygame.draw.rect(self.WIN, (0,0,0), pygame.Rect(0,0,(self.WIDTH),20))

        if car.flip:
            self.WIN.blit(car.image_flip, (car.x, car.y))
        else:
            self.WIN.blit(car.image, (car.x, car.y))
            
        for bat in car.battery_list_right:
            self.WIN.blit(bat.image, (bat.x,bat.y))

        for bat in car.battery_list_left:
            self.WIN.blit(bat.image, (bat.x,bat.y))

        for gas in car.gas_list_right:
            self.WIN.blit(gas.image, (gas.x, gas.y))

        for gas in car.gas_list_left:
            self.WIN.blit(gas.image, (gas.x, gas.y))

        for honda in car.honda_list:
            self.WIN.blit(honda.image_flip, (honda.x, honda.y))
        
        pygame.draw.rect(self.WIN, (128,128,128), pygame.Rect(0,0,self.WIDTH,20), 1)
        if car.stateOfCharge < 1:
            pygame.draw.rect(self.WIN, (255,0,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(self.WIDTH),20))

        elif car.stateOfCharge >=1 and car.stateOfCharge <= 6:
            pygame.draw.rect(self.WIN, (255,165,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(self.WIDTH),20))
        else:
            pygame.draw.rect(self.WIN, (124,252,0), pygame.Rect(0,0,car.stateOfCharge*0.1*(self.WIDTH),20))

        draw_text = self.LOSER_FONT.render(text, True, self.YELLOW)
        self.WIN.blit(draw_text, (self.WIDTH/2 - draw_text.get_width()/2, self.HEIGHT/2 - draw_text.get_height()/2))
        
    
        pygame.display.update()

    def handle_blue_movement(self, keys_pressed, car):
        if keys_pressed[pygame.K_LEFT] and car.x - car.car_vel > 0:  # LEFT
            car.x -= car.car_vel
            car.flip = False
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_RIGHT] and car.x + car.car_vel < self.WIDTH - int(car.image.get_width()) :  # RIGHT
            car.x += car.car_vel
            car.flip = True
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_UP] and car.y - car.car_vel-self.X_OFFSET > 0:  # UP
            car.y -= car.car_vel
            car.stateOfCharge -=car.consumption
        if keys_pressed[pygame.K_DOWN] and car.y + car.car_vel < self.HEIGHT - int(car.image.get_height()):  # DOWN
            car.y += car.car_vel
            car.stateOfCharge -=car.consumption
        if car.stateOfCharge <=0:
            pygame.event.post(pygame.event.Event(self.TESLA_NO_JUICE))

    


    def handle_object_movement(self, car, amplitude = 0):
        
            for bat in car.battery_list_right:
                bat.x += bat.item_vel

            for bat in car.battery_list_left:
                bat.x -= bat.item_vel

            for gas in car.gas_list_right:
                gas.x += gas.item_vel

            for gas in car.gas_list_left:
                gas.x -= gas.item_vel

            for honda in car.honda_list:
                honda.x += honda.car_vel
                angle = 2*math.pi*honda.x/(self.WIDTH/3)
                sin_value = math.sin(angle) * amplitude
                honda.y += sin_value
                if honda.y > self.HEIGHT:
                    honda.y = self.HEIGHT-honda.image.get_height()

    def check_collision(self, car):
        for bat in car.battery_list_right:
            offset_x = car.x - bat.x
            offset_y = car.y - bat.y

            if car.flip:
                collision = bat.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = bat.mask.overlap(car.mask, (int(offset_x), int(offset_y)))
            if collision:
                pygame.event.post(pygame.event.Event(self.TESLA_HIT_BAT))
                car.battery_list_right.remove(bat)

        for bat in car.battery_list_left:
            offset_x = car.x - bat.x
            offset_y = car.y - bat.y

            if car.flip:
                collision = bat.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = bat.mask.overlap(car.mask, (int(offset_x), int(offset_y)))
            if collision:
                pygame.event.post(pygame.event.Event(self.TESLA_HIT_BAT))
                car.battery_list_left.remove(bat)

        for gas in car.gas_list_right:
            offset_x = car.x - gas.x
            offset_y = car.y - gas.y

            if car.flip:
                collision = gas.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = gas.mask.overlap(car.mask, ((int(offset_x), int(offset_y))))

            if collision:
                pygame.event.post(pygame.event.Event(self.TESLA_HIT_GAS))

        for gas in car.gas_list_left:
            offset_x = car.x - gas.x
            offset_y = car.y - gas.y

            if car.flip:
                collision = gas.mask.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = gas.mask.overlap(car.mask, (int(offset_x), int(offset_y)))

            if collision:
                pygame.event.post(pygame.event.Event(self.TESLA_HIT_GAS))

        for honda in car.honda_list:
            offset_x = car.x - honda.x
            offset_y = car.y - honda.y

            if car.flip:
                collision = honda.mask_flip.overlap(car.mask_flip, (int(offset_x), int(offset_y)))
            else:
                collision = honda.mask_flip.overlap(car.mask, (int(offset_x), int(offset_y)))

            if collision:
                pygame.event.post(pygame.event.Event(self.TESLA_HIT_HONDA))


    def draw_winner(self, text):
        draw_text = self.WINNER_FONT.render(text, True, self.GREEN)
        self.WIN.blit(draw_text, (self.WIDTH/2 - draw_text.get_width()/2, self.HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)


    def draw_loser(self, text):
        draw_text = self.LOSER_FONT.render(text, True, self.RED)
        self.WIN.blit(draw_text, (self.WIDTH/2 - draw_text.get_width()/2, self.HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(2000)


    def restart(self, quit, level):
        self.WIN.blit(self.background, (0, 20))
        pygame.draw.rect(self.WIN, (0,0,0), pygame.Rect(0,0,(self.WIDTH),20))
        quit = level(quit)
        return quit
        
        