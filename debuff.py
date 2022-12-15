from game_bonuses import GameBonuses
import random


class Debuff(GameBonuses):
    def __init__(self, x_range, y_range, image):
        super(Debuff, self).__init__(x_range, y_range, image)

    def assess_draw_powerup(self) -> None:
        rand_number = random.randrange(0, 1000)
        if rand_number == 1:
            if not self.power_up_active:
                self.draw_powerup = True
