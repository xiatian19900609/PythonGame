class Setting():
    def __init__(self):
        """存储外星人所有设置的类"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (163, 148, 128)
        # 飞船的速度设置
        self.ship_limit = 3
        # 子弹设置
        self.bullet_width = 4
        self.bullet_height = 6
        self.bullet_color = (255, 182, 193)
        self.bullet_allowed = 50
        # 外星人设置
        self.row_number = 3
        self.alien_point = 50
        self.fleet_drop_sheed = 10

        # 以什么样的速度加快游戏节奏
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed_factor = 1.5
        self.bullet_sheed_factor = 3
        self.alien_sheed_factor = 1
        # fleet_direction为1外星人向右移动 , -1向左移动
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_sheed_factor *= self.speedup_scale
        self.alien_sheed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point * self.speedup_scale)
