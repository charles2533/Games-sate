import pygame
import sys
import time
import random
import os
import asyncio # 1. Import asyncio

pygame.init()

# --- SETUP RESOLUSI BROWSER (PYGBAG) ---
# Gunakan resolusi dasar statis. Pygbag akan otomatis men-scale canvas di browser.
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Go Sate! - Juragan Level Up") 
CLOCK = pygame.time.Clock()

# Ratio di-set 1.0 karena resolusi sudah statis 900x600
W_RATIO = 1.0
H_RATIO = 1.0

LEVELS = {
    1: {
        "title": "Level 1: Kampung Sebelah",
        "target_money": 20000,
        "target_portions": 10,
        "time_limit": 60,       
        "patience": 15.0,      
        "cust_spawn_rate": 4.0  
    },
    2: {
        "title": "Level 2: Alun-Alun Kota",
        "target_money": 35000,
        "target_portions": 15,
        "time_limit": 90,
        "patience": 12.0,       
        "cust_spawn_rate": 3.0
    },
    3: {
        "title": "Level 3: Festival Kuliner",
        "target_money": 50000,
        "target_portions": 20,
        "time_limit": 120,
        "patience": 10.0,        
        "cust_spawn_rate": 2.5
    }
}

# --- WARNA ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED_MEAT = (220, 20, 60)
BROWN_COOKED = (139, 69, 19)
BROWN_SAUCE = (160, 82, 45)
GREEN = (34, 139, 34)
ORANGE_BRAND = (255, 69, 0)
RED_BAR = (255, 0, 0)
YELLOW_BAR = (255, 255, 0)

# Deteksi lokasi folder (Diubah untuk WebAssembly)
BASE_DIR = "."

# --- LOAD ASSETS ---
def load_image(file_name, size=None):
    path = os.path.join(BASE_DIR, "assets", file_name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except FileNotFoundError:
        print(f"Gambar {path} tidak ditemukan!")
        surface = pygame.Surface(size if size else (50, 50))
        surface.fill((255, 0, 255))
        return surface
    
# Dictionary untuk menyimpan semua gambar yang sudah diskala
ASSETS = {
    "bg_home": load_image("latar home.png", (WIDTH, HEIGHT)),
    "bg_game": load_image("latar game.png", (WIDTH, HEIGHT)),
    "table": load_image("meja game.png", (WIDTH, int(HEIGHT * 0.4))),
    
    "char1": load_image("character1.png", (int(100 * W_RATIO), int(200 * H_RATIO))),
    "char2": load_image("character2.png", (int(100 * W_RATIO), int(200 * H_RATIO))),
    "char3": load_image("character3.png", (int(100 * W_RATIO), int(200 * H_RATIO))),
    "speech": load_image("speechBubble.png", (int(120 * W_RATIO), int(80 * H_RATIO))),
    
    "logo": load_image("logo.png", (int(250 * W_RATIO), int(250 * H_RATIO))), 
    "btn_start": load_image("tombolStart.png", (int(180 * W_RATIO), int(150 * H_RATIO))), 
    "btn_shop": load_image("logoBelanja.png", (int(115 * W_RATIO), int(55 * H_RATIO))),
    "btn_back": load_image("tombolBack.png", (int(150 * W_RATIO), int(90 * H_RATIO))),

    "grill": load_image("grill.png", (int(130 * W_RATIO), int(100 * H_RATIO))),
    "plate": load_image("piring.png", (int(120 * W_RATIO), int(120 * H_RATIO))),
    "plate_complete": load_image("piringLengkap.png", (int(120 * W_RATIO), int(120 * H_RATIO))),
    "trash": load_image("sampah.png", (int(40 * W_RATIO), int(60 * H_RATIO))),
    
    "btn_lontong": load_image("tombolLontong.png", (int(70 * W_RATIO), int(70 * H_RATIO))),
    "btn_sauce": load_image("tombolBumbuKacang.png", (int(70 * W_RATIO), int(70 * H_RATIO))),
    
    "lontong": load_image("lontong.png", (int(40 * W_RATIO), int(40 * H_RATIO))),
    "sauce": load_image("bumbuKacang.png", (int(50 * W_RATIO), int(50 * H_RATIO))),
    
    "sate_burnt": load_image("SateGosong.png", (int(90 * W_RATIO), int(45 * H_RATIO))),
    "sate_matang": load_image("sateMatang.png", (int(90 * W_RATIO), int(45 * H_RATIO))),
    "sate_mentah": load_image("SateMentah.png", (int(90 * W_RATIO), int(45 * H_RATIO))),
    "sateUntukShop": load_image("sateMentah.png", (int(120 * W_RATIO), int(90 * H_RATIO)))
}

# --- LOAD SOUNDS ---
def load_sound(file_name):
    path = os.path.join(BASE_DIR, "assets", file_name)
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(0.7)
        return sound
    except FileNotFoundError:
        return None

SOUNDS = {"click": load_sound("click.ogg")}

def play_bgm(file_name):
    path = os.path.join(BASE_DIR, "assets", file_name)
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        pass

# --- FONT ---
def get_font(size):
    try:
        return pygame.font.SysFont("comicsans", int(size * H_RATIO))
    except:
        return pygame.font.SysFont("Arial", int(size * H_RATIO))

FONT_UI = get_font(18)
FONT_BIG = get_font(60)
FONT_MED = get_font(30)
FONT_SMALL = get_font(16)

# --- CLASS PIRING (PLATE) ---
class Plate:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ASSETS["plate"].get_width(), ASSETS["plate"].get_height())
        self.reset()

    def reset(self):
        self.has_sate = False
        self.has_lontong = False
        self.has_sauce = False

    def is_complete(self):
        return self.has_sate and self.has_lontong and self.has_sauce

    def draw(self, screen):
        if self.is_complete():
            screen.blit(ASSETS["plate_complete"], self.rect.topleft)
        else:
            screen.blit(ASSETS["plate"], self.rect.topleft)
            
            if self.has_lontong:
                screen.blit(ASSETS["lontong"], (self.rect.x + int(20 * W_RATIO), self.rect.y + int(20 * H_RATIO)))
            if self.has_sate:
                screen.blit(ASSETS["sate_matang"], (self.rect.x + int(30 * W_RATIO), self.rect.y + int(50 * H_RATIO)))
            if self.has_sauce:
                screen.blit(ASSETS["sauce"], (self.rect.x + int(45 * W_RATIO), self.rect.y + int(70 * H_RATIO)))

# --- CLASS PANGGANGAN ---
class Grill:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ASSETS["grill"].get_width(), ASSETS["grill"].get_height())
        self.status = "EMPTY"  
        self.start_time = 0
        self.cook_time = 3.0   
        self.burn_time = 8.0   

    def draw(self, screen):
        screen.blit(ASSETS["grill"], self.rect.topleft)

        if self.status != "EMPTY":
            elapsed = time.time() - self.start_time
            if self.status == "RAW":
                img_sate = ASSETS["sate_mentah"]
                if elapsed >= self.cook_time: self.status = "COOKED"
            elif self.status == "COOKED":
                img_sate = ASSETS["sate_matang"]
                if elapsed >= self.burn_time: self.status = "BURNT"
            elif self.status == "BURNT":
                img_sate = ASSETS["sate_burnt"]

            # Render sate di tengah panggangan
            screen.blit(img_sate, (self.rect.centerx - img_sate.get_width()//2, self.rect.centery - img_sate.get_height()//2 - int(10 * H_RATIO)))
            
            # Progress bar
            if self.status != "BURNT":
                progress = min(elapsed / self.burn_time, 1.0)
                bar_width = int(self.rect.width * progress)
                bar_color = GREEN if self.status == "RAW" else YELLOW_BAR
                pygame.draw.rect(screen, bar_color, (self.rect.x, self.rect.y - int(15 * H_RATIO), bar_width, int(8 * H_RATIO)))
                pygame.draw.rect(screen, BLACK, (self.rect.x, self.rect.y - int(15 * H_RATIO), self.rect.width, int(8 * H_RATIO)), 1)

    def reset(self):
        self.status = "EMPTY"

    def start_cooking(self):
        self.status = "RAW"
        self.start_time = time.time()

# --- CLASS PELANGGAN ---
class Customer:
    def __init__(self, patience_duration):
        self.image = random.choice([ASSETS["char1"], ASSETS["char2"], ASSETS["char3"]])
        self.x = random.randint(int(WIDTH * 0.1), int(WIDTH * 0.7))
        self.y = int(HEIGHT * 0.25)
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        
        self.spawn_time = time.time()
        self.patience_duration = patience_duration

    def get_remaining_patience(self):
        elapsed = time.time() - self.spawn_time
        return max(0, self.patience_duration - elapsed)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
        bubble = ASSETS["speech"]
        bx = self.rect.left - int(60 * W_RATIO)
        by = self.rect.top - int(30 * H_RATIO)
        screen.blit(bubble, (bx, by))
        
        txt = FONT_UI.render("Sate bang!", True, BLACK)
        screen.blit(txt, (bx + int(20 * W_RATIO), by + int(20 * H_RATIO)))

        ratio = self.get_remaining_patience() / self.patience_duration
        bar_w = int(100 * W_RATIO)
        bar_h = int(10 * H_RATIO)
        bar_x = self.rect.centerx - bar_w // 2
        bar_y = self.rect.top - int(15 * H_RATIO)
        
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h))
        current_w = int(bar_w * ratio)
        col = GREEN if ratio > 0.6 else (YELLOW_BAR if ratio > 0.3 else RED_BAR)
        pygame.draw.rect(screen, col, (bar_x, bar_y, current_w, bar_h))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 1)

# --- CLASS GAME UTAMA ---
class Game:
    def __init__(self):
        self.state = "MENU"
        self.money = 5000     
        self.score = 0
        
        self.stock_meat = 5
        self.stock_lontong = 5
        self.stock_sauce = 5
        
        gy = int(HEIGHT * 0.69)
        self.grills = [
            Grill(int(WIDTH * 0.05), gy), 
            Grill(int(WIDTH * 0.20), gy), 
            Grill(int(WIDTH * 0.35), gy)
        ]
        
        py = int(HEIGHT * 0.735)
        self.plates = [
            Plate(int(WIDTH * 0.51), py), 
            Plate(int(WIDTH * 0.66), py), 
            Plate(int(WIDTH * 0.81), py)
        ]
        
        ty = int(HEIGHT * 0.87)
        bw = ASSETS["btn_lontong"].get_width()
        bh = ASSETS["btn_lontong"].get_height()
        self.lontong_box = pygame.Rect(int(WIDTH * 0.15), ty, bw, bh)
        self.sauce_bowl = pygame.Rect(int(WIDTH * 0.05), ty, bw, bh)
        
        tw = ASSETS["trash"].get_width()
        th = ASSETS["trash"].get_height()
        self.trash_can = pygame.Rect(int(WIDTH * 0.93), int(HEIGHT * 0.49), tw, th) 

        self.btn_shop_rect = pygame.Rect(WIDTH - int(150*W_RATIO), int(20*H_RATIO), ASSETS["btn_shop"].get_width(), ASSETS["btn_shop"].get_height())
        self.btn_start_rect = ASSETS["btn_start"].get_rect(center=(WIDTH//2, int(HEIGHT * 0.65)))

        self.customers = []
        self.last_customer_time = 0
        self.notification = ""
        self.notif_timer = 0
        self.current_level = 1
        self.level_start_time = 0
        self.portions_sold = 0
        self.game_over_status = "" 

    def start_level(self, level_id):
        self.current_level = level_id
        config = LEVELS[level_id]
        
        self.money = 5000 
        self.portions_sold = 0
        self.stock_meat = 8
        self.stock_lontong = 8
        self.stock_sauce = 8
        self.customers = []
        
        for g in self.grills: g.reset()
        for p in self.plates: p.reset()
        
        self.level_start_time = time.time()
        self.last_customer_time = time.time()
        self.state = "GAME"
        self.show_notif(f"Mulai {config['title']}!")

    # 2. Fungsi run diubah menjadi asinkron
    async def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            CLOCK.tick(60)
            await asyncio.sleep(0) # 3. WAJIB DITAMBAHKAN AGAR BROWSER TIDAK FREEZE

    def handle_events(self):
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SOUNDS["click"]: SOUNDS["click"].play()
                    
                if self.state == "MENU":
                    if self.btn_start_rect.collidepoint(mx, my):
                        self.state = "LEVEL_SELECT"

                elif self.state == "LEVEL_SELECT":
                    box_w, box_h = int(250*W_RATIO), int(250*H_RATIO)
                    spacing = (WIDTH - (3 * box_w)) // 4
                    y = int(HEIGHT * 0.4)
                    
                    if spacing < mx < spacing + box_w and y < my < y + box_h:
                        self.start_level(1)
                    elif spacing*2 + box_w < mx < spacing*2 + box_w*2 and y < my < y + box_h:
                        self.start_level(2)
                    elif spacing*3 + box_w*2 < mx < spacing*3 + box_w*3 and y < my < y + box_h:
                        self.start_level(3)
                    
                    if 20 < mx < int(150*W_RATIO) and 20 < my < int(70*H_RATIO):
                        self.state = "MENU"

                elif self.state == "RESULT":
                    if WIDTH//2 - int(120*W_RATIO) < mx < WIDTH//2 + int(120*W_RATIO) and int(HEIGHT*0.7) < my < int(HEIGHT*0.7) + int(80*H_RATIO):
                        self.state = "LEVEL_SELECT"

                elif self.state == "SHOP":
                    if 20 < mx < int(150*W_RATIO) and 20 < my < int(70*H_RATIO):
                        self.state = "GAME"
                    
                    box_w, box_h = int(250*W_RATIO), int(250*H_RATIO)
                    spacing = (WIDTH - (3 * box_w)) // 4
                    sy = int(HEIGHT * 0.4)
                    
                    if spacing < mx < spacing + box_w and sy < my < sy + box_h:
                        if self.money >= 500: self.money -= 500; self.stock_meat += 1
                    elif spacing*2 + box_w < mx < spacing*2 + box_w*2 and sy < my < sy + box_h:
                        if self.money >= 200: self.money -= 200; self.stock_lontong += 1
                    elif spacing*3 + box_w*2 < mx < spacing*3 + box_w*3 and sy < my < sy + box_h:
                        if self.money >= 300: self.money -= 300; self.stock_sauce += 1

                elif self.state == "GAME":
                    if self.btn_shop_rect.collidepoint(mx, my):
                        self.state = "SHOP"

                    for grill in self.grills:
                        if grill.rect.collidepoint(mx, my):
                            if grill.status == "EMPTY":
                                if self.stock_meat > 0:
                                    self.stock_meat -= 1; grill.start_cooking()
                                else: self.show_notif("Daging Habis! Beli Dulu!")
                            elif grill.status == "COOKED":
                                placed = False
                                for p in self.plates:
                                    if not p.has_sate:
                                        p.has_sate = True; grill.reset(); placed = True; break
                                if not placed: self.show_notif("Piring Penuh Sate!")
                            elif grill.status == "BURNT":
                                grill.reset()

                    if self.lontong_box.collidepoint(mx, my):
                        if self.stock_lontong > 0:
                            for p in self.plates:
                                if p.has_sate and not p.has_lontong:
                                    p.has_lontong = True; self.stock_lontong -= 1; break
                        else: self.show_notif("Lontong Habis!")

                    if self.sauce_bowl.collidepoint(mx, my):
                        if self.stock_sauce > 0:
                            for p in self.plates:
                                if p.has_sate and not p.has_sauce:
                                    p.has_sauce = True; self.stock_sauce -= 1; break
                        else: self.show_notif("Bumbu Habis!")
                    
                    if self.trash_can.collidepoint(mx, my):
                        for p in self.plates: p.reset()

                    for cust in self.customers[:]:
                        if cust.rect.collidepoint(mx, my):
                            served = False
                            for p in self.plates:
                                if p.is_complete():
                                    p.reset(); self.money += 4000; self.portions_sold += 1
                                    self.customers.remove(cust); self.show_notif("Makasih BANG! (+4k)")
                                    served = True; break
                            if not served: self.show_notif("Pesanan Belum Lengkap!")

    def show_notif(self, text):
        self.notification = text
        self.notif_timer = time.time()

    def update(self):
        if self.state == "GAME":
            lvl_config = LEVELS[self.current_level]
            elapsed_time = time.time() - self.level_start_time
            remaining_time = lvl_config['time_limit'] - elapsed_time
            
            if remaining_time <= 0:
                self.game_over_status = "LOSE"
                self.state = "RESULT"
                return

            if self.money >= lvl_config['target_money'] and self.portions_sold >= lvl_config['target_portions']:
                self.game_over_status = "WIN"
                self.state = "RESULT"
                return

            if time.time() - self.last_customer_time > lvl_config['cust_spawn_rate']:
                if len(self.customers) < 4:
                    self.customers.append(Customer(lvl_config['patience']))
                self.last_customer_time = time.time()

            for cust in self.customers[:]:
                if cust.get_remaining_patience() <= 0:
                    self.customers.remove(cust)
                    self.money -= 500
                    self.show_notif("PELANGGAN MARAH! (-500)")
            
            if time.time() - self.notif_timer > 1.5:
                self.notification = ""

    def draw(self):
        SCREEN.fill((255, 239, 213))

        if self.state == "MENU": self.draw_menu()
        elif self.state == "LEVEL_SELECT": self.draw_level_select()
        elif self.state == "GAME": self.draw_game()
        elif self.state == "SHOP": self.draw_shop()
        elif self.state == "RESULT": self.draw_result()

        pygame.display.flip()

    def draw_menu(self):
        SCREEN.blit(ASSETS["bg_home"], (0, 0))
        
        logo = ASSETS["logo"]
        SCREEN.blit(logo, (WIDTH//2 - logo.get_width()//2, int(HEIGHT * 0.10)))
        
        subtitle = FONT_MED.render("Tekan ESC untuk keluar game", True, (56,29,25))
        SCREEN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, int(HEIGHT * 0.7)))
        
        SCREEN.blit(ASSETS["btn_start"], self.btn_start_rect.topleft)

    def draw_level_select(self):
        SCREEN.blit(ASSETS["bg_home"], (0, 0))
        
        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.set_alpha(150); dark.fill(BLACK)
        SCREEN.blit(dark, (0, 0))
        
        title = FONT_BIG.render("PILIH LEVEL", True, WHITE)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, int(HEIGHT * 0.1)))

        SCREEN.blit(ASSETS["btn_back"], (20, 20))

        box_w, box_h = int(250*W_RATIO), int(250*H_RATIO)
        spacing = (WIDTH - (3 * box_w)) // 4
        y = int(HEIGHT * 0.4)
        
        for i, (lvl_id, data) in enumerate(LEVELS.items()):
            x = spacing + (i * (box_w + spacing))
            pygame.draw.rect(SCREEN, WHITE, (x, y, box_w, box_h), border_radius=15)
            pygame.draw.rect(SCREEN, ORANGE_BRAND, (x, y, box_w, box_h), 5, border_radius=15)
            
            lbl_lvl = FONT_MED.render(f"Level {lvl_id}", True, BLACK)
            SCREEN.blit(lbl_lvl, (x + box_w//2 - lbl_lvl.get_width()//2, y + 20))
            
            lbl_money = FONT_SMALL.render(f"Target: Rp {data['target_money']:,}", True, (50, 50, 50))
            lbl_port = FONT_SMALL.render(f"Jual: {data['target_portions']} Porsi", True, (50, 50, 50))
            lbl_time = FONT_SMALL.render(f"Waktu: {data['time_limit']} Dtk", True, RED_MEAT)
            
            SCREEN.blit(lbl_money, (x + 20, y + int(box_h * 0.4)))
            SCREEN.blit(lbl_port, (x + 20, y + int(box_h * 0.55)))
            SCREEN.blit(lbl_time, (x + 20, y + int(box_h * 0.7)))

    def draw_game(self):
        SCREEN.blit(ASSETS["bg_game"], (0, 0))
        lvl_config = LEVELS[self.current_level]
        
        pygame.draw.rect(SCREEN, WHITE, (0, 0, WIDTH, int(100 * H_RATIO)))
        pygame.draw.line(SCREEN, BLACK, (0, int(100 * H_RATIO)), (WIDTH, int(100 * H_RATIO)), 3)
        
        SCREEN.blit(FONT_MED.render(f"{lvl_config['title']}", True, ORANGE_BRAND), (20, 10))
        SCREEN.blit(FONT_UI.render(f"Uang: Rp {self.money:,} / {lvl_config['target_money']:,}", True, BLACK), (20, int(45*H_RATIO)))
        SCREEN.blit(FONT_UI.render(f"Terjual: {self.portions_sold} / {lvl_config['target_portions']}", True, BLACK), (20, int(70*H_RATIO)))

        elapsed = time.time() - self.level_start_time
        remain = max(0, int(lvl_config['time_limit'] - elapsed))
        txt_time = FONT_MED.render(f"WAKTU: {remain}", True, RED_MEAT if remain < 10 else BLACK)
        SCREEN.blit(txt_time, (WIDTH//2 - txt_time.get_width()//2, int(32*H_RATIO)))

        SCREEN.blit(FONT_UI.render(f"Daging: {self.stock_meat}", True, RED_MEAT), (WIDTH - int(300*W_RATIO), int(20*H_RATIO)))
        SCREEN.blit(FONT_UI.render(f"Lontong: {self.stock_lontong}", True, GREEN), (WIDTH - int(300*W_RATIO), int(40*H_RATIO)))
        SCREEN.blit(FONT_UI.render(f"Bumbu: {self.stock_sauce}", True, BROWN_SAUCE), (WIDTH - int(300*W_RATIO), int(60*H_RATIO)))

        SCREEN.blit(ASSETS["btn_shop"], self.btn_shop_rect.topleft)

        for cust in self.customers: cust.draw(SCREEN)

        table_y = HEIGHT - ASSETS["table"].get_height()
        SCREEN.blit(ASSETS["table"], (0, table_y))

        for grill in self.grills: grill.draw(SCREEN)
        for plate in self.plates: plate.draw(SCREEN)

        SCREEN.blit(ASSETS["btn_lontong"], self.lontong_box.topleft)
        SCREEN.blit(ASSETS["btn_sauce"], self.sauce_bowl.topleft)
        SCREEN.blit(ASSETS["trash"], self.trash_can.topleft)

        if self.notification:
            bg_rect = pygame.Rect(WIDTH//2 - int(250*W_RATIO), int(120*H_RATIO), int(500*W_RATIO), int(50*H_RATIO))
            pygame.draw.rect(SCREEN, BLACK, bg_rect, border_radius=10)
            txt = FONT_UI.render(self.notification, True, WHITE)
            SCREEN.blit(txt, (WIDTH//2 - txt.get_width()//2, int(135*H_RATIO)))

    def draw_shop(self):
        SCREEN.fill((240, 230, 140))
        title = FONT_BIG.render("TOKO GO SATE", True, ORANGE_BRAND)
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, int(HEIGHT * 0.1)))
        
        info = FONT_MED.render(f"Uang Kamu: Rp {self.money:,}", True, GREEN)
        SCREEN.blit(info, (WIDTH//2 - info.get_width()//2, int(HEIGHT * 0.25)))
        
        box_w, box_h = int(250*W_RATIO), int(250*H_RATIO)
        spacing = (WIDTH - (3 * box_w)) // 4
        sy = int(HEIGHT * 0.4)
        
        items = [
            (ASSETS["sateUntukShop"], RED_MEAT, spacing, self.stock_meat, 500),
            (ASSETS["btn_lontong"], GREEN, spacing*2 + box_w, self.stock_lontong, 200),
            (ASSETS["btn_sauce"], BROWN_SAUCE, spacing*3 + box_w*2, self.stock_sauce, 300)
        ]
        
        for img_asset, col, x, stk, price in items:
            pygame.draw.rect(SCREEN, col, (x, sy, box_w, box_h), border_radius=10)
            
            img_x = x + (box_w - img_asset.get_width()) // 2
            img_y = sy + int(20 * H_RATIO)
            SCREEN.blit(img_asset, (img_x, img_y))

            text_x = x + int(30*W_RATIO) 
            SCREEN.blit(FONT_UI.render(f"Stok: {stk}", True, WHITE), (text_x, sy + int(110*H_RATIO)))
            SCREEN.blit(FONT_UI.render(f"Rp {price}", True, WHITE), (text_x, sy + int(140*H_RATIO)))
            
            btn_y = sy + int(180*H_RATIO)
            pygame.draw.rect(SCREEN, BLACK, (x + int(25*W_RATIO), btn_y, box_w - int(50*W_RATIO), int(50*H_RATIO)), 2)
            lbl = FONT_UI.render("KLIK BELI", True, WHITE)
            SCREEN.blit(lbl, (x + box_w//2 - lbl.get_width()//2, btn_y + int(15*H_RATIO)))

        SCREEN.blit(ASSETS["btn_back"], (20, 20))

    def draw_result(self):
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(200); s.fill((0,0,0))
        SCREEN.blit(s, (0,0))

        if self.game_over_status == "WIN":
            msg, col, desc = "LEVEL SELESAI!", GREEN, "Kamu berhasil mencapai target!"
        else:
            msg, col, desc = "GAME OVER", RED_MEAT, "Waktu Habis atau Target Gagal!"

        txt_msg = FONT_BIG.render(msg, True, col)
        SCREEN.blit(txt_msg, (WIDTH//2 - txt_msg.get_width()//2, int(HEIGHT * 0.3)))
        
        txt_desc = FONT_MED.render(desc, True, WHITE)
        SCREEN.blit(txt_desc, (WIDTH//2 - txt_desc.get_width()//2, int(HEIGHT * 0.5)))

        ry = int(HEIGHT * 0.7)
        pygame.draw.rect(SCREEN, WHITE, (WIDTH//2 - int(120*W_RATIO), ry, int(240*W_RATIO), int(80*H_RATIO)), border_radius=15)
        lbl = FONT_UI.render("MENU LEVEL", True, BLACK)
        SCREEN.blit(lbl, (WIDTH//2 - lbl.get_width()//2, ry + int(25*H_RATIO)))

# 4. Bungkus pemanggilan program utama dalam asyncio.run()
async def main():
    play_bgm("bgm.ogg")
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())