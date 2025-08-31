import pygame
import random
import sys
from pygame import mixer
import math

# 初始化Pygame
pygame.init()
mixer.init()

# 顏色定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)

# 遊戲設置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 100  # 從20改為100，放大5倍
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# 創建遊戲窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('貪吃蛇遊戲 - 雙倍點數版 + 速度提升 + 移動食物 + 五倍長度 + 隨機事件 + 五倍大小 + 自動重置')
clock = pygame.time.Clock()

# 字體
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0
        self.speed_level = 0  # 速度等級
        self.invincible = False  # 無敵狀態
        self.invincible_timer = 0  # 無敵計時器
        self.rainbow_mode = False  # 彩虹模式
        self.rainbow_timer = 0  # 彩虹模式計時器

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        
        if not self.invincible and new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        
        # 更新倍數計時器
        if self.multiplier_timer > 0:
            self.multiplier_timer -= 1
            if self.multiplier_timer == 0:
                self.multiplier = 1
        
        # 更新無敵計時器
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            if self.invincible_timer == 0:
                self.invincible = False
        
        # 更新彩虹模式計時器
        if self.rainbow_timer > 0:
            self.rainbow_timer -= 1
            if self.rainbow_timer == 0:
                self.rainbow_mode = False
        
        return True

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.multiplier = 1
        self.multiplier_timer = 0
        self.speed_level = 0
        self.invincible = False
        self.invincible_timer = 0
        self.rainbow_mode = False
        self.rainbow_timer = 0

    def render(self, surface):
        for i, p in enumerate(self.positions):
            if self.rainbow_mode:
                # 彩虹模式：每個部分都有不同顏色
                hue = (i * 30 + pygame.time.get_ticks() // 50) % 360
                color = pygame.Color(0, 0, 0)
                color.hsva = (hue, 100, 100, 100)
            elif self.invincible:
                # 無敵模式：閃爍效果
                if (pygame.time.get_ticks() // 100) % 2:
                    color = GOLD
                else:
                    color = GREEN if i == 0 else (0, 200, 0)
            else:
                color = GREEN if i == 0 else (0, 200, 0)
            
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE),
                             (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.points = 10
        self.type = "normal"
        self.move_direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.move_timer = 0
        self.move_interval = 60  # 每60幀移動一次（從30改為60，讓移動更慢）
        self.randomize_position()
        self.randomize_type()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

    def randomize_type(self):
        # 擴展食物類型，增加更多隨機性
        rand = random.random()
        if rand < 0.5:
            self.type = "normal"
            self.color = RED
            self.points = 10
        elif rand < 0.7:
            self.type = "golden"
            self.color = GOLD
            self.points = 20
        elif rand < 0.8:
            self.type = "blue"
            self.color = BLUE
            self.points = 30
        elif rand < 0.9:
            self.type = "orange"
            self.color = ORANGE
            self.points = 50
        else:
            self.type = "pink"
            self.color = PINK
            self.points = 100

    def update(self):
        """更新食物的移動"""
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move()

    def move(self):
        """移動食物"""
        x, y = self.position
        dx, dy = self.move_direction
        
        # 計算新位置
        new_x = (x + dx) % GRID_WIDTH
        new_y = (y + dy) % GRID_HEIGHT
        
        # 檢查是否會撞到邊界，如果會則改變方向
        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            # 隨機選擇新方向
            self.move_direction = random.choice([UP, DOWN, LEFT, RIGHT])
            dx, dy = self.move_direction
            new_x = (x + dx) % GRID_WIDTH
            new_y = (y + dy) % GRID_HEIGHT
        
        self.position = (new_x, new_y)

    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        
        # 為特殊食物添加標記
        if self.type == "golden":
            pygame.draw.circle(surface, WHITE, 
                             (self.position[0] * GRID_SIZE + GRID_SIZE//2,
                              self.position[1] * GRID_SIZE + GRID_SIZE//2), 3)
        elif self.type == "blue":
            pygame.draw.circle(surface, WHITE, 
                             (self.position[0] * GRID_SIZE + GRID_SIZE//2,
                              self.position[1] * GRID_SIZE + GRID_SIZE//2), 2)
        elif self.type == "orange":
            pygame.draw.circle(surface, WHITE, 
                             (self.position[0] * GRID_SIZE + GRID_SIZE//2,
                              self.position[1] * GRID_SIZE + GRID_SIZE//2), 4)
        elif self.type == "pink":
            pygame.draw.circle(surface, WHITE, 
                             (self.position[0] * GRID_SIZE + GRID_SIZE//2,
                              self.position[1] * GRID_SIZE + GRID_SIZE//2), 5)

class Obstacle:
    def __init__(self):
        self.position = (0, 0)
        self.color = GRAY
        self.randomize_position()
        self.life_timer = random.randint(100, 300)  # 隨機生命時間

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))

    def update(self):
        self.life_timer -= 1
        return self.life_timer > 0

    def render(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE,
                           self.position[1] * GRID_SIZE),
                          (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

class ParticleEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.life = 30
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0

    def render(self, surface):
        alpha = int(255 * (self.life / 30))
        color = (*self.color, alpha)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRAY, rect, 1)

def show_score(surface, score, multiplier, speed_level):
    score_text = font.render(f'分數: {score}', True, WHITE)
    surface.blit(score_text, (10, 10))
    
    if multiplier > 1:
        multiplier_text = font.render(f'倍數: x{multiplier}', True, GOLD)
        surface.blit(multiplier_text, (10, 50))
    
    # 顯示速度等級
    speed_text = font.render(f'速度: {speed_level + 1}', True, PURPLE)
    surface.blit(speed_text, (10, 90))

def show_food_legend(surface):
    legend_y = WINDOW_HEIGHT - 120
    # 普通食物說明
    pygame.draw.rect(surface, RED, (WINDOW_WIDTH - 200, legend_y, 20, 20))
    legend_text = font.render('普通: 10分', True, WHITE)
    surface.blit(legend_text, (WINDOW_WIDTH - 170, legend_y))
    
    # 金色食物說明
    pygame.draw.rect(surface, GOLD, (WINDOW_WIDTH - 200, legend_y + 25, 20, 20))
    legend_text2 = font.render('金色: 20分', True, WHITE)
    surface.blit(legend_text2, (WINDOW_WIDTH - 170, legend_y + 25))
    
    # 藍色食物說明
    pygame.draw.rect(surface, BLUE, (WINDOW_WIDTH - 200, legend_y + 50, 20, 20))
    legend_text3 = font.render('藍色: 30分', True, WHITE)
    surface.blit(legend_text3, (WINDOW_WIDTH - 170, legend_y + 50))
    
    # 橙色食物說明
    pygame.draw.rect(surface, ORANGE, (WINDOW_WIDTH - 200, legend_y + 75, 20, 20))
    legend_text4 = font.render('橙色: 50分', True, WHITE)
    surface.blit(legend_text4, (WINDOW_WIDTH - 170, legend_y + 75))
    
    # 粉色食物說明
    pygame.draw.rect(surface, PINK, (WINDOW_WIDTH - 200, legend_y + 100, 20, 20))
    legend_text5 = font.render('粉色: 100分', True, WHITE)
    surface.blit(legend_text5, (WINDOW_WIDTH - 170, legend_y + 100))

def show_game_over(surface):
    game_over_text = big_font.render('遊戲結束!', True, RED)
    restart_text = font.render('按R重新開始，按Q退出', True, WHITE)
    
    surface.blit(game_over_text, 
                (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 
                 WINDOW_HEIGHT//2 - 50))
    surface.blit(restart_text, 
                (WINDOW_WIDTH//2 - restart_text.get_width()//2, 
                 WINDOW_HEIGHT//2 + 50))

def get_game_speed(speed_level):
    """根據速度等級返回遊戲速度"""
    base_speed = 10
    # 每5個食物增加1級速度，每級增加2幀/秒
    speed_increase = min(speed_level * 2, 20)  # 最大增加20幀/秒
    return base_speed + speed_increase

def trigger_random_event(snake):
    """觸發隨機事件"""
    event = random.random()
    if event < 0.1:  # 10% 機率觸發無敵模式
        snake.invincible = True
        snake.invincible_timer = 100
        return "無敵模式啟動！"
    elif event < 0.2:  # 10% 機率觸發彩虹模式
        snake.rainbow_mode = True
        snake.rainbow_timer = 150
        return "彩虹模式啟動！"
    elif event < 0.3:  # 10% 機率觸發分數翻倍
        snake.score *= 2
        return "分數翻倍！"
    elif event < 0.4:  # 10% 機率觸發速度重置
        snake.speed_level = max(0, snake.speed_level - 2)
        return "速度重置！"
    return None

def main():
    snake = Snake()
    food = Food()
    obstacles = []  # 障礙物列表
    particles = []  # 粒子效果列表
    running = True
    game_over = False
    event_message = ""
    event_timer = 0
    auto_reset_timer = 0  # 自動重置計時器

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # 手動重置
                        snake.reset()
                        food.randomize_position()
                        food.randomize_type()
                        obstacles.clear()
                        particles.clear()
                        game_over = False
                        auto_reset_timer = 0
                    elif event.key == pygame.K_q:
                        running = False
                else:
                    if event.key == pygame.K_UP and snake.direction != DOWN:
                        snake.direction = UP
                    elif event.key == pygame.K_DOWN and snake.direction != UP:
                        snake.direction = DOWN
                    elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                        snake.direction = LEFT
                    elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                        snake.direction = RIGHT

        if not game_over:
            # 更新蛇的位置
            if not snake.update():
                game_over = True
                auto_reset_timer = 180  # 3秒後自動重置（60FPS * 3）
                continue

            # 更新食物的移動
            food.update()

            # 隨機生成障礙物
            if random.random() < 0.005:  # 0.5% 機率生成障礙物
                obstacle = Obstacle()
                obstacles.append(obstacle)

            # 更新障礙物
            obstacles = [obs for obs in obstacles if obs.update()]

            # 更新粒子效果
            particles = [p for p in particles if p.update()]

            # 檢查是否吃到食物
            if snake.get_head_position() == food.position:
                # 計算分數（考慮倍數）
                base_points = food.points
                final_points = base_points * snake.multiplier
                snake.score += final_points
                
                # 增加速度等級
                snake.speed_level += 1
                
                # 根據食物類型設置特殊效果
                if food.type == "golden":
                    snake.multiplier = 2
                    snake.multiplier_timer = 50  # 50幀的雙倍時間
                elif food.type == "blue":
                    snake.multiplier = 3
                    snake.multiplier_timer = 80  # 80幀的三倍時間
                elif food.type == "orange":
                    snake.multiplier = 4
                    snake.multiplier_timer = 120  # 120幀的四倍時間
                elif food.type == "pink":
                    snake.multiplier = 5
                    snake.multiplier_timer = 200  # 200幀的五倍時間
                
                # 蛇的長度增加5倍（從1000改為5）
                snake.length += 5
                
                # 添加粒子效果
                for _ in range(20):
                    particles.append(ParticleEffect(
                        food.position[0] * GRID_SIZE + GRID_SIZE//2,
                        food.position[1] * GRID_SIZE + GRID_SIZE//2,
                        food.color
                    ))
                
                # 觸發隨機事件
                event_msg = trigger_random_event(snake)
                if event_msg:
                    event_message = event_msg
                    event_timer = 120
                
                food.randomize_position()
                food.randomize_type()
                # 確保食物不會出現在蛇身上
                while food.position in snake.positions:
                    food.randomize_position()
                    food.randomize_type()

            # 檢查是否撞到障礙物
            if not snake.invincible:
                for obstacle in obstacles:
                    if snake.get_head_position() == obstacle.position:
                        game_over = True
                        auto_reset_timer = 180  # 3秒後自動重置
                        break

        # 自動重置功能
        if game_over and auto_reset_timer > 0:
            auto_reset_timer -= 1
            if auto_reset_timer == 0:
                # 自動重置遊戲
                snake.reset()
                food.randomize_position()
                food.randomize_type()
                obstacles.clear()
                particles.clear()
                game_over = False
                event_message = ""
                event_timer = 0

        # 更新事件消息計時器
        if event_timer > 0:
            event_timer -= 1

        # 繪製
        screen.fill(BLACK)
        draw_grid(screen)
        
        # 繪製障礙物
        for obstacle in obstacles:
            obstacle.render(screen)
        
        # 繪製粒子效果
        for particle in particles:
            particle.render(screen)
        
        snake.render(screen)
        food.render(screen)
        show_score(screen, snake.score, snake.multiplier, snake.speed_level)
        show_food_legend(screen)
        
        # 顯示事件消息
        if event_timer > 0 and event_message:
            event_text = font.render(event_message, True, CYAN)
            screen.blit(event_text, 
                        (WINDOW_WIDTH//2 - event_text.get_width()//2, 150))
        
        if game_over:
            show_game_over(screen)
            # 顯示自動重置倒計時
            if auto_reset_timer > 0:
                countdown = (auto_reset_timer // 60) + 1
                countdown_text = font.render(f'自動重置: {countdown}秒', True, CYAN)
                screen.blit(countdown_text, 
                           (WINDOW_WIDTH//2 - countdown_text.get_width()//2, 
                            WINDOW_HEIGHT//2 + 100))

        pygame.display.update()
        
        # 根據速度等級調整遊戲速度
        current_speed = get_game_speed(snake.speed_level)
        clock.tick(current_speed)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 