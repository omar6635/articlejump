from game_bonuses import GameBonuses


class PowerUp(GameBonuses):
    def __init__(self, x_range, y_range, image):
        super(PowerUp, self).__init__(x_range, y_range, image)

