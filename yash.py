import pygame, sys, random, time
pygame.init()
# Settings 
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Memory Puzzle Game")
clock = pygame.time.Clock()
FPS = 60
def get_font(size):
    return pygame.font.SysFont("segoeuiemoji", size) or pygame.font.SysFont(None, size)
TITLE_FONT = get_font(84)
SUBTITLE_FONT = get_font(44)
BTN_FONT = get_font(36)
HUD_FONT = get_font(28)
SMALL_FONT = get_font(24)
COLORS = {
    "menu": ((255, 120, 40), (200, 40, 90)),     # orange → pink
    "theme": ((120, 30, 150), (50, 200, 180)),   # purple → teal
    "grid": ((50, 160, 90), (40, 190, 210)),     # green → light blue
    "game": ((40, 40, 120), (100, 50, 180)),     # blue → violet
    "win": ((255, 215, 0), (200, 90, 20)),       # gold → dark orange
}
BTN_BASE = (70, 90, 160)
BTN_HOVER = (120, 160, 220)
CARD_BACK = (50, 70, 140)
CARD_FACE = (255, 255, 255)
OUTLINE = (220, 220, 230)
HUD_TEXT = (245, 245, 245)
THEMES = {
    "🏎 Cars": ["🚗","🚙","🚕","🚓","🚑","🚒","🚐","🚌","🚎","🚚","🚛","🏎️","🚔","🚖"],
    "🍉 Fruits": ["🍎","🍌","🍇","🍉","🍊","🍍","🥭","🍓","🍒","🥝","🍐","🍋","🍈","🥥"],
    "🍴 Foods":  ["🍔","🍕","🍟","🌭","🍿","🥪","🍣","🍱","🍩","🍪","🍰","🍫","🍝","🍜"],
    "📘 Books":  ["📕","📗","📘","📙","📓","📔","📒","📚","📖","📑","🔖","📎","🧾","📌"]
}
def draw_vertical_gradient(surface, top_color, bottom_color):
    h, w = surface.get_height(), surface.get_width()
    for y in range(h):
        ratio = y / max(h-1, 1)
        r = int(top_color[0]*(1-ratio) + bottom_color[0]*ratio)
        g = int(top_color[1]*(1-ratio) + bottom_color[1]*ratio)
        b = int(top_color[2]*(1-ratio) + bottom_color[2]*ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (w,y))
def center_text(surface, text, font, color, y):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(WIDTH//2, y))
    surface.blit(surf, rect)
    return rect
def first_choice_screen():
    options = [("👤  Single Player", 0), ("👥  Multiplayer", 1)]
    while True:
        draw_vertical_gradient(screen, *COLORS["menu"])
        center_text(screen, "Memory Puzzle", TITLE_FONT, (255,255,255), HEIGHT*0.2)
        mouse = pygame.mouse.get_pos()
        click = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1: click = True
        tile_w, tile_h = 400, 140
        gap = 60
        start_x = (WIDTH - (tile_w*2+gap))//2
        y = int(HEIGHT*0.45)
        for i,(label,val) in enumerate(options):
            rect = pygame.Rect(start_x+i*(tile_w+gap), y, tile_w, tile_h)
            hover = rect.collidepoint(mouse)
            pygame.draw.rect(screen, BTN_HOVER if hover else BTN_BASE, rect, border_radius=18)
            pygame.draw.rect(screen, OUTLINE, rect, 2, border_radius=18)
            t = BTN_FONT.render(label, True, (255,255,255))
            screen.blit(t, t.get_rect(center=rect.center))
            if hover and click: return val
        pygame.display.flip(); clock.tick(FPS)
def theme_choice_screen():
    keys = list(THEMES.keys())
    while True:
        draw_vertical_gradient(screen, *COLORS["theme"])
        center_text(screen, "Choose Theme", TITLE_FONT, (255,255,255), HEIGHT*0.2)
        mouse = pygame.mouse.get_pos()
        click=False
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: return None
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1: click=True
        tile_w,tile_h=250,100; gap=40
        total=len(keys)*tile_w+(len(keys)-1)*gap
        start_x=(WIDTH-total)//2; y=int(HEIGHT*0.45)
        for i,k in enumerate(keys):
            rect=pygame.Rect(start_x+i*(tile_w+gap), y, tile_w, tile_h)
            hover=rect.collidepoint(mouse)
            pygame.draw.rect(screen, BTN_HOVER if hover else BTN_BASE, rect, border_radius=14)
            pygame.draw.rect(screen, OUTLINE, rect, 2, border_radius=14)
            screen.blit(BTN_FONT.render(k,True,(255,255,255)), rect.move(70,25))
            if hover and click: return k
        pygame.display.flip(); clock.tick(FPS)
def grid_choice_screen(theme):
    options=[("4×4",4),("6×6",6),("8×8",8)]
    while True:
        draw_vertical_gradient(screen,*COLORS["grid"])
        center_text(screen, f"Theme: {theme}", SUBTITLE_FONT, (255,255,255), HEIGHT*0.2)
        center_text(screen, "Choose Grid Size", TITLE_FONT, (255,255,255), HEIGHT*0.3)
        mouse=pygame.mouse.get_pos(); click=False
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: return None
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1: click=True
        btn_w,btn_h=250,90; gap=60
        total=len(options)*btn_w+(len(options)-1)*gap
        start_x=(WIDTH-total)//2; y=int(HEIGHT*0.5)
        for i,(label,size) in enumerate(options):
            rect=pygame.Rect(start_x+i*(btn_w+gap), y, btn_w, btn_h)
            hover=rect.collidepoint(mouse)
            pygame.draw.rect(screen, BTN_HOVER if hover else BTN_BASE, rect, border_radius=16)
            pygame.draw.rect(screen, OUTLINE, rect, 2, border_radius=16)
            screen.blit(BTN_FONT.render(label,True,(255,255,255)), rect.move(80,25))
            if hover and click: return (size,size)
        pygame.display.flip(); clock.tick(FPS)
def create_board(rows, cols, theme):
    num_pairs=(rows*cols)//2
    deck=(THEMES[theme]*((num_pairs//len(THEMES[theme]))+1))[:num_pairs]
    deck=deck*2; random.shuffle(deck)
    pad=10
    max_w=(WIDTH-200)//cols
    max_h=(HEIGHT-300)//rows
    size=min(max_w,max_h)
    start_x=(WIDTH-(cols*size+(cols-1)*pad))//2
    start_y=(HEIGHT-(rows*size+(rows-1)*pad))//2
    cards=[]
    for r in range(rows):
        row=[]
        for c in range(cols):
            x=start_x+c*(size+pad)
            y=start_y+r*(size+pad)
row.append({"rect":pygame.Rect(x,y,size,size),"emoji":deck.pop(),"revealed":False,"matched":False})
        cards.append(row)
    font=get_font(int(size*0.6))
    return cards,font
def winning_screen(mode, players, moves, elapsed):
    while True:
        draw_vertical_gradient(screen,*COLORS["win"])
        mins,secs=divmod(elapsed,60)
        timer=f"{mins:02}:{secs:02}"
        center_text(screen,"🏆 Game Over! 🏆",TITLE_FONT,(50,30,0),HEIGHT*0.2)
        if mode==0:
            msg=f"Pairs Found: {moves//2}   Moves: {moves}   Time: {timer}"
        else:
            if players[0]>players[1]:
                msg=f"🎉 Player 1 Wins! ({players[0]} vs {players[1]})"
            elif players[1]>players[0]:
                msg=f"🎉 Player 2 Wins! ({players[1]} vs {players[0]})"
            else:
                msg=f"🤝 It's a Tie! ({players[0]} - {players[1]})"
        center_text(screen,msg,SUBTITLE_FONT,(80,0,0),HEIGHT*0.4)
        btn_w,btn_h=220,80; gap=50
        total=btn_w*3+gap*2; start_x=(WIDTH-total)//2
        y=int(HEIGHT*0.7)
        mouse=pygame.mouse.get_pos(); click=False
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1: click=True
        actions=[("🏠 Menu","menu"),("🔄 Restart","restart"),("❌ Quit","quit")]
        for i,(label,val) in enumerate(actions):
            rect=pygame.Rect(start_x+i*(btn_w+gap),y,btn_w,btn_h)
            hover=rect.collidepoint(mouse)
            pygame.draw.rect(screen,BTN_HOVER if hover else BTN_BASE,rect,border_radius=16)
            pygame.draw.rect(screen,OUTLINE,rect,2,border_radius=16)
            t=BTN_FONT.render(label,True,(255,255,255))
            screen.blit(t,t.get_rect(center=rect.center))
            if hover and click: return val
        pygame.display.flip(); clock.tick(FPS)
# ---------------- Game ----------------
def play_game(mode, rows, cols, theme):
    cards,font=create_board(rows,cols,theme)
    first=second=None; matches=0; moves=0; players=[0,0]; turn=0
    start_time=time.time()
    flip_timer=None
    # bottom control buttons
    btn_w,btn_h=200,60; gap=40
    total=btn_w*3+gap*2; start_x=(WIDTH-total)//2
    y=HEIGHT-80
    prev_rect=pygame.Rect(start_x,y,btn_w,btn_h)
    menu_rect=pygame.Rect(start_x+btn_w+gap,y,btn_w,btn_h)
    restart_rect=pygame.Rect(start_x+(btn_w+gap)*2,y,btn_w,btn_h)
    while True:
        draw_vertical_gradient(screen,*COLORS["game"])
        elapsed=int(time.time()-start_time)
        mins,secs=divmod(elapsed,60)
        timer=f"{mins:02}:{secs:02}"
        # HUD
        if mode==0:
            hud=f"Pairs: {matches}/{(rows*cols)//2}   Moves: {moves}   Time: {timer}"
            hud_color=(255,255,255)
        else:
            hud=f"P1:{players[0]}  |  P2:{players[1]}  |  Turn: P{turn+1}  |  Time:{timer}"
            hud_color=(255,180,180) if turn==0 else (180,200,255)
        screen.blit(HUD_FONT.render(hud,True,hud_color),(40,40))
        # Draw cards
        for row in cards:
            for card in row:
                rect=card["rect"]
                pygame.draw.rect(screen,CARD_FACE if card["revealed"] or card["matched"] else CARD_BACK,rect,border_radius=12)
                pygame.draw.rect(screen,OUTLINE,rect,2,border_radius=12)
                if card["revealed"] or card["matched"]:
                    t=font.render(card["emoji"],True,(0,0,0))
                    screen.blit(t,t.get_rect(center=rect.center))
        # Controls
        mouse=pygame.mouse.get_pos()
        for (rect,label) in [(prev_rect,"⬅ Prev"),(menu_rect,"🏠 Menu"),(restart_rect,"🔄 Restart")]:
            hover=rect.collidepoint(mouse)
            pygame.draw.rect(screen,BTN_HOVER if hover else BTN_BASE,rect,border_radius=12)
            pygame.draw.rect(screen,OUTLINE,rect,2,border_radius=12)
            txt=SMALL_FONT.render(label,True,(255,255,255))
            screen.blit(txt,txt.get_rect(center=rect.center))
        click=False
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_ESCAPE: return "menu"
            if e.type==pygame.MOUSEBUTTONDOWN and e.button==1: click=True; mpos=e.pos
        if click and not flip_timer:  # disable clicks during flip check
            if prev_rect.collidepoint(mpos): return "prev"
            if menu_rect.collidepoint(mpos): return "menu"
            if restart_rect.collidepoint(mpos): return "restart"
            for r,row in enumerate(cards):
                for c,card in enumerate(row):
                    if card["rect"].collidepoint(mpos) and not card["revealed"] and not card["matched"]:
                        card["revealed"]=True
                        if first is None: first=(r,c)
                        elif second is None and first!=(r,c):
                            second=(r,c); moves+=1; flip_timer=time.time()+0.8
                        break
        # Check match
        if flip_timer and time.time()>flip_timer:
            a=cards[first[0]][first[1]]; b=cards[second[0]][second[1]]
            if a["emoji"]==b["emoji"]:
                a["matched"]=b["matched"]=True; matches+=1
                if mode==1: players[turn]+=1
            else:
                a["revealed"]=b["revealed"]=False
                if mode==1: turn=1-turn
            first=second=None; flip_timer=None
        if matches==(rows*cols)//2:
            elapsed=int(time.time()-start_time)
            return winning_screen(mode,players,moves,elapsed)
        pygame.display.flip(); clock.tick(FPS)
# ---------------- Main Flow ----------------
def main():
    while True:
        mode=first_choice_screen()
        theme=theme_choice_screen()
        if theme is None: continue
        while True:
            grid=grid_choice_screen(theme)
            if grid is None: break
            rows,cols=grid
            action=play_game(mode,rows,cols,theme)
            if action=="prev": continue   # back to grid selection
            elif action=="menu": break
            elif action=="restart": play_game(mode,rows,cols,theme)
if __name__=="__main__":
    main()

