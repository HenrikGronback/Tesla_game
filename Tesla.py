import pygame
from level1 import Level1
from level2 import Level2

pygame.font.init()

pygame.display.set_caption("Tesla!")

def main():
    current_level = "level1"
    quit = False
    
    while not quit:
        if current_level == "level1":
            level_1=Level1()
            quit = level_1.level1(quit)
            pygame.event.clear()
            current_level="level2"
        elif current_level == "level2":
            level_2=Level2()
            quit = level_2.level2(quit)
            pygame.event.clear()
            quit=True

    pygame.quit()

        


if __name__ == "__main__":
    main()
