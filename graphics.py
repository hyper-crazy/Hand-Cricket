import pygame
import math
from config import *

# --- 1. HAND DRAWING ---
def draw_hand_icon(surface, x, y, fingers, scale=1.0, is_left=False):
    base_w, base_h = 220, 260 
    temp_surf = pygame.Surface((base_w, base_h), pygame.SRCALPHA)
    draw_hand_logic(temp_surf, 60, 60, fingers, SKIN_BASE, is_left)
    target_w = int(base_w * scale)
    target_h = int(base_h * scale)
    scaled_surf = pygame.transform.smoothscale(temp_surf, (target_w, target_h))
    rect = scaled_surf.get_rect(center=(x, y))
    surface.blit(scaled_surf, rect)

def draw_hand_logic(surface, x, y, fingers_up, color, is_left):
    palm_w, palm_h = 100, 95
    palm_rect = pygame.Rect(x, y + 30, palm_w, palm_h)
    pygame.draw.rect(surface, color, palm_rect, border_radius=20)
    pygame.draw.aaline(surface, (220,190,160), (x+20, y+50), (x+50, y+90))
    finger_specs = [(2, 10, 22, 85), (3, 36, 24, 95), (4, 64, 22, 90), (5, 90, 20, 70)]
    for fid, off_x, w, h in finger_specs:
        draw_x = x + off_x
        if is_left: draw_x = x + (palm_w - off_x - w)
        is_open = fingers_up and fid in fingers_up
        draw_smooth_finger(surface, draw_x, y + 30, w, h, is_open)
    thumb_open = fingers_up and 1 in fingers_up
    draw_thumb_smooth(surface, x, y + 30, is_left, thumb_open)
    pygame.draw.rect(surface, OUTLINE, palm_rect, 2, border_radius=20)

def draw_smooth_finger(surface, x, y, w, h, is_open):
    if not is_open:
        rect = pygame.Rect(x, y + 30, w, 35)
        pygame.draw.rect(surface, SKIN_BASE, rect, border_radius=8)
        pygame.draw.rect(surface, OUTLINE, rect, 2, border_radius=8)
        return
    tip_w = w * 0.85
    margin = (w - tip_w) / 2
    points = [(x, y+20), (x+margin, y-h), (x+w-margin, y-h), (x+w, y+20)]
    pygame.draw.polygon(surface, SKIN_BASE, points)
    pygame.draw.polygon(surface, SKIN_SHADOW, [(x+w-5, y-h+10), (x+w, y+20), (x+w-margin, y-h+5)])
    center_x, center_y = x + w // 2, y - h
    pygame.draw.circle(surface, SKIN_BASE, (int(center_x), int(center_y)), int(tip_w // 2))
    pygame.draw.aaline(surface, OUTLINE, points[0], points[1])
    pygame.draw.aaline(surface, OUTLINE, points[3], points[2])
    rect_arc = pygame.Rect(center_x - tip_w//2, center_y - tip_w//2, tip_w, tip_w)
    pygame.draw.arc(surface, OUTLINE, rect_arc, 0, math.pi, 2)
    pygame.draw.aaline(surface, (200,150,100), (x+5, y-h*0.4), (x+w-5, y-h*0.4))

def draw_thumb_smooth(surface, x, y, is_left, is_open):
    if not is_left:
        base_x, base_y = x - 10, y + 55  
    else:
        base_x, base_y = x + 90, y + 55
    if is_open:
        angle_deg = 120 if not is_left else 60 
        length, width = 65, 28
        rad = math.radians(angle_deg)
        tip_x = base_x + math.cos(rad) * length
        tip_y = base_y - math.sin(rad) * length 
        pygame.draw.line(surface, SKIN_BASE, (base_x+10, base_y), (tip_x, tip_y), width)
        pygame.draw.circle(surface, SKIN_BASE, (int(tip_x), int(tip_y)), width//2)
        offset = width // 2
        pygame.draw.line(surface, OUTLINE, (base_x+10, base_y-offset+2), (tip_x, tip_y-offset+2), 2)
        pygame.draw.line(surface, OUTLINE, (base_x+10, base_y+offset-2), (tip_x, tip_y+offset-2), 2)
        pygame.draw.circle(surface, OUTLINE, (int(tip_x), int(tip_y)), width//2, 2)
    else:
        rect_x = base_x if not is_left else base_x - 10
        rect = pygame.Rect(rect_x, base_y - 10, 35, 30)
        pygame.draw.rect(surface, SKIN_BASE, rect, border_radius=10)
        pygame.draw.rect(surface, OUTLINE, rect, 2, border_radius=10)

def draw_game_hands(surface, p_fingers, ai_fingers):
    draw_hand_icon(surface, 200, 330, p_fingers, scale=0.75, is_left=False)
    draw_hand_icon(surface, 600, 330, ai_fingers, scale=0.75, is_left=True)

# --- 2. UI HELPERS ---
def draw_text_centered(surface, text, y, font, color):
    shadow = font.render(text, True, (0, 0, 0))
    rect_s = shadow.get_rect(center=(WIDTH//2 + 2, y + 2))
    surface.blit(shadow, rect_s)
    img = font.render(text, True, color)
    rect = img.get_rect(center=(WIDTH//2, y))
    surface.blit(img, rect)

def draw_button(surface, rect, text, mouse_pos, color=PANEL_COLOR):
    is_hover = rect.collidepoint(mouse_pos)
    btn_col = HOVER_COLOR if is_hover else color
    pygame.draw.rect(surface, btn_col, rect, border_radius=15)
    pygame.draw.rect(surface, ACCENT_COLOR, rect, 3, border_radius=15)
    font = pygame.font.SysFont("Arial", 25, bold=True)
    txt_surf = font.render(text, True, TEXT_COLOR)
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)
    return is_hover

def draw_back_button(surface, mouse_pos):
    rect = pygame.Rect(10, 10, 50, 50)
    is_hover = rect.collidepoint(mouse_pos)
    col = HOVER_COLOR if is_hover else PANEL_COLOR
    pygame.draw.circle(surface, col, rect.center, 25)
    pygame.draw.circle(surface, ACCENT_COLOR, rect.center, 25, 2)
    c = rect.center
    pygame.draw.line(surface, TEXT_COLOR, (c[0]+5, c[1]-10), (c[0]-5, c[1]), 3)
    pygame.draw.line(surface, TEXT_COLOR, (c[0]-5, c[1]), (c[0]+5, c[1]+10), 3)
    return rect

def draw_exit_warning(surface, mouse_pos):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 220))
    surface.blit(overlay, (0, 0))
    box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
    pygame.draw.rect(surface, PANEL_COLOR, box, border_radius=20)
    pygame.draw.rect(surface, ALERT_COLOR, box, 3, border_radius=20)
    draw_text_centered(surface, "WARNING!", HEIGHT//2 - 100, pygame.font.SysFont("Arial", 40, bold=True), ALERT_COLOR)
    draw_text_centered(surface, "All match progress will be lost.", HEIGHT//2 - 40, pygame.font.SysFont("Arial", 25), TEXT_COLOR)
    btn_yes = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 50, 140, 50)
    btn_no = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 50, 140, 50)
    draw_button(surface, btn_yes, "EXIT", mouse_pos, color=ALERT_COLOR)
    draw_button(surface, btn_no, "CANCEL", mouse_pos)
    return {"YES": btn_yes, "NO": btn_no}

# --- 3. SCREENS ---
def draw_menu(surface, mouse_pos):
    draw_text_centered(surface, "HAND CRICKET", 150, pygame.font.SysFont("Arial", 50, bold=True), ACCENT_COLOR)
    draw_button(surface, pygame.Rect(WIDTH//2 - 125, 300, 250, 60), "PLAY WITH FRIEND", mouse_pos)
    draw_button(surface, pygame.Rect(WIDTH//2 - 125, 400, 250, 60), "PLAY WITH AI", mouse_pos)
    prof_rect = pygame.Rect(WIDTH-70, 20, 50, 50)
    is_hover = prof_rect.collidepoint(mouse_pos)
    col = HOVER_COLOR if is_hover else PANEL_COLOR
    pygame.draw.circle(surface, col, prof_rect.center, 25)
    pygame.draw.circle(surface, ACCENT_COLOR, prof_rect.center, 25, 2)
    pygame.draw.circle(surface, TEXT_COLOR, (prof_rect.centerx, prof_rect.centery-8), 8)
    pygame.draw.arc(surface, TEXT_COLOR, (prof_rect.centerx-12, prof_rect.centery-5, 24, 25), 0, 3.14, 2)
    return prof_rect

def draw_profile_screen(surface, stats, mouse_pos, current_tab):
    """Rebuilt to show Tabs (AI/Friends) and Columns (Std/Hard)"""
    draw_text_centered(surface, "CAREER PROFILE", 60, pygame.font.SysFont("Arial", 40, bold=True), ACCENT_COLOR)
    
    # 1. TABS
    tab_w, tab_h = 150, 50
    tab_y = 120
    rect_ai = pygame.Rect(WIDTH//2 - tab_w, tab_y, tab_w, tab_h)
    rect_fr = pygame.Rect(WIDTH//2, tab_y, tab_w, tab_h)
    
    # Draw Tabs (Active one is bright)
    col_ai = ACCENT_COLOR if current_tab == "AI" else PANEL_COLOR
    col_fr = ACCENT_COLOR if current_tab == "FRIEND" else PANEL_COLOR
    
    pygame.draw.rect(surface, col_ai, rect_ai, border_top_left_radius=15, border_bottom_left_radius=15)
    pygame.draw.rect(surface, col_fr, rect_fr, border_top_right_radius=15, border_bottom_right_radius=15)
    
    # Tab Text
    f = pygame.font.SysFont("Arial", 20, bold=True)
    t_ai = f.render("VS AI", True, (0,0,0) if current_tab == "AI" else TEXT_COLOR)
    t_fr = f.render("VS FRIEND", True, (0,0,0) if current_tab == "FRIEND" else TEXT_COLOR)
    surface.blit(t_ai, t_ai.get_rect(center=rect_ai.center))
    surface.blit(t_fr, t_fr.get_rect(center=rect_fr.center))
    
    # 2. STATS BOX (Container)
    box_rect = pygame.Rect(50, 180, 700, 350)
    pygame.draw.rect(surface, PANEL_COLOR, box_rect, border_radius=20)
    pygame.draw.rect(surface, ACCENT_COLOR, box_rect, 2, border_radius=20)
    
    # 3. COLUMNS (Standard vs Hardcore)
    # Helper to draw a stats column
    def draw_col(title, x_off, data):
        head = pygame.font.SysFont("Arial", 22, bold=True)
        body = pygame.font.SysFont("Arial", 18)
        
        # Title
        t = head.render(title, True, ACCENT_COLOR)
        surface.blit(t, (x_off, 200))
        pygame.draw.line(surface, (100,100,100), (x_off, 230), (x_off+200, 230), 2)
        
        # Stats
        lines = [
            f"Matches: {data['matches']}",
            f"Wins: {data['wins']}",
            f"Losses: {data['losses']}",
            f"Runs: {data['runs']}",
            f"Wickets: {data['wickets']}"
        ]
        
        dy = 250
        for l in lines:
            surface.blit(body.render(l, True, TEXT_COLOR), (x_off, dy))
            dy += 35

    # Get data for current tab
    current_data = stats[current_tab]
    
    # Draw Left Column (Standard)
    draw_col("STANDARD MODE", 100, current_data["STANDARD"])
    
    # Draw Divider
    pygame.draw.line(surface, (80,80,80), (WIDTH//2, 200), (WIDTH//2, 500), 2)
    
    # Draw Right Column (Hardcore)
    draw_col("HARDCORE MODE", 450, current_data["HARDCORE"])

    return {"AI": rect_ai, "FRIEND": rect_fr}

def draw_mode_select(surface, mouse_pos):
    draw_text_centered(surface, "SELECT AI MODE", 150, pygame.font.SysFont("Arial", 40, bold=True), ACCENT_COLOR)
    btn_std = pygame.Rect(WIDTH//2 - 125, 300, 250, 60)
    draw_button(surface, btn_std, "STANDARD MODE", mouse_pos)
    btn_help_std = pygame.Rect(WIDTH//2 + 140, 305, 50, 50)
    draw_button(surface, btn_help_std, "?", mouse_pos, color=INFO_COLOR)
    btn_hrd = pygame.Rect(WIDTH//2 - 125, 400, 250, 60)
    draw_button(surface, btn_hrd, "HARDCORE MODE", mouse_pos)
    btn_help_hrd = pygame.Rect(WIDTH//2 + 140, 405, 50, 50)
    draw_button(surface, btn_help_hrd, "?", mouse_pos, color=INFO_COLOR)
    return {"STD": btn_std, "HRD": btn_hrd, "Q_STD": btn_help_std, "Q_HRD": btn_help_hrd}

def draw_mode_rules_overlay(surface, mode):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 240))
    surface.blit(overlay, (0, 0))
    title = f"{mode} RULES"
    draw_text_centered(surface, title, 100, pygame.font.SysFont("Arial", 35, bold=True), ACCENT_COLOR)
    font = pygame.font.SysFont("Arial", 22)
    y = 180
    if mode == "STANDARD":
        lines = ["1. Classic Hand Cricket mechanics.", "2. You choose a number (1-6).", "3. If AI chooses same NUMBER, you are OUT.", "4. Gesture shape does NOT matter, only value."]
    else: 
        lines = ["1. Pro Level mechanics.", "2. To get OUT, numbers AND gestures must match.", "3. You must match the exact finger pattern.", "4. NO BALL RULE: Playing same gesture 6x in a row", "   results in a No Ball + Free Hit."]
    for line in lines:
        surface.blit(font.render(line, True, TEXT_COLOR), (80, y))
        y += 40
    draw_text_centered(surface, "CLICK TO CLOSE", HEIGHT - 100, pygame.font.SysFont("Arial", 20), (150,150,150))

def draw_overs_select(surface, mouse_pos):
    draw_text_centered(surface, "MATCH SETTINGS", 120, pygame.font.SysFont("Arial", 40, bold=True), ACCENT_COLOR)
    y_start = 250
    btns = {}
    for overs, data in MATCH_PRESETS.items():
        rect = pygame.Rect(WIDTH//2 - 150, y_start, 300, 60)
        label = f"{overs} OVERS ({data['wickets']} Wkts)"
        draw_button(surface, rect, label, mouse_pos)
        btns[overs] = rect
        y_start += 100
    return btns

def draw_game_over_screen(surface, game, mouse_pos):
    draw_text_centered(surface, "GAME OVER", 200, pygame.font.SysFont("Arial", 50, bold=True), ACCENT_COLOR)
    draw_text_centered(surface, game.result_desc, 300, pygame.font.SysFont("Arial", 40, bold=True), TEXT_COLOR)
    btn_rect = pygame.Rect(WIDTH//2 - 125, 500, 250, 60)
    draw_button(surface, btn_rect, "MAIN MENU", mouse_pos)
    return btn_rect

def draw_scorecard_overlay(surface, game):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 230))
    surface.blit(overlay, (0, 0))
    draw_text_centered(surface, "INNINGS SUMMARY", 30, pygame.font.SysFont("Arial", 30, bold=True), ACCENT_COLOR)
    font_sm = pygame.font.SysFont("Arial", 16)
    y = 80
    surface.blit(font_sm.render("BATSMAN", True, ACCENT_COLOR), (50, y))
    surface.blit(font_sm.render("R (B)", True, ACCENT_COLOR), (250, y))
    y += 20
    pygame.draw.line(surface, (100,100,100), (40, y), (350, y), 1)
    y += 10
    if game.batting == "AI": 
        batsmen = game.p_batsmen
        bowlers = game.ai_bowlers
    else:
        batsmen = game.ai_batsmen
        bowlers = game.p_bowlers
    for b in batsmen:
        if b.balls > 0 or b.is_out:
            c = TEXT_COLOR
            if b.is_out: c = (255, 100, 100)
            surface.blit(font_sm.render(b.name, True, c), (50, y))
            surface.blit(font_sm.render(f"{b.runs} ({b.balls})", True, c), (250, y))
            y += 20
            if y > 350: break
    y = 380
    surface.blit(font_sm.render("BOWLER", True, ACCENT_COLOR), (50, y))
    surface.blit(font_sm.render("O-M-R-W", True, ACCENT_COLOR), (250, y))
    y += 20
    pygame.draw.line(surface, (100,100,100), (40, y), (350, y), 1)
    y += 10
    for b in bowlers:
        if b.overs_bowled > 0 or b.wickets_taken > 0:
            txt = f"{b.overs_bowled}-{0}-{b.runs_conceded}-{b.wickets_taken}"
            surface.blit(font_sm.render(b.name, True, TEXT_COLOR), (50, y))
            surface.blit(font_sm.render(txt, True, TEXT_COLOR), (250, y))
            y += 20
    draw_text_centered(surface, "CLICK TO CONTINUE", HEIGHT - 50, pygame.font.SysFont("Arial", 20), (150,150,150))

def draw_hud(surface, game):
    font = pygame.font.SysFont("Arial", 16)
    curr_batsmen = game.p_batsmen if game.batting == "PLAYER" else game.ai_batsmen
    striker = curr_batsmen[game.striker_idx]
    non_striker = curr_batsmen[game.non_striker_idx]
    s_txt = f"{striker.name}* : {striker.runs}({striker.balls})"
    surface.blit(font.render(s_txt, True, ACCENT_COLOR), (20, 70))
    ns_txt = f"{non_striker.name} : {non_striker.runs}({non_striker.balls})"
    surface.blit(font.render(ns_txt, True, TEXT_COLOR), (20, 95))
    curr_bowlers = game.ai_bowlers if game.batting == "PLAYER" else game.p_bowlers
    bowl = curr_bowlers[game.current_bowler_idx]
    b_txt = f"Bowler: {bowl.name}"
    b_stats = f"{bowl.wickets_taken}/{bowl.runs_conceded}"
    surface.blit(font.render(b_txt, True, TEXT_COLOR), (WIDTH - 200, 70))
    surface.blit(font.render(b_stats, True, TEXT_COLOR), (WIDTH - 200, 95))
    draw_timeline(surface, game.timeline)
    rect = pygame.Rect(WIDTH-50, 10, 40, 40)
    pygame.draw.rect(surface, PANEL_COLOR, rect, border_radius=5)
    pygame.draw.line(surface, TEXT_COLOR, (WIDTH-40, 20), (WIDTH-20, 20), 2)
    pygame.draw.line(surface, TEXT_COLOR, (WIDTH-40, 30), (WIDTH-20, 30), 2)
    pygame.draw.line(surface, TEXT_COLOR, (WIDTH-40, 40), (WIDTH-20, 40), 2)
    return rect

def draw_timeline(surface, timeline):
    start_x = WIDTH // 2 - (len(timeline) * 25)
    y = 125 
    font = pygame.font.SysFont("Arial", 14, bold=True)
    for event in timeline:
        color = (50, 200, 50) 
        if event == "W": color = (200, 50, 50) 
        elif event == "NB": color = (200, 200, 50) 
        elif event == "0": color = (150, 150, 150)
        elif event in ["4", "6"]: color = (100, 100, 255) 
        pygame.draw.circle(surface, color, (start_x, y), 18)
        pygame.draw.circle(surface, (255,255,255), (start_x, y), 18, 2)
        txt = font.render(event, True, (255,255,255))
        rect = txt.get_rect(center=(start_x, y))
        surface.blit(txt, rect)
        start_x += 50

def draw_coin_animated(surface, center_x, center_y, frame, final_result=None):
    COIN_SIZE = 130 
    width_scale = math.cos(frame * 0.2) 
    width = int(COIN_SIZE * abs(width_scale)) 
    height = COIN_SIZE
    is_heads = width_scale > 0
    if width < 4: width = 4
    coin_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    rect = pygame.Rect(0, 0, width, height)
    pygame.draw.ellipse(coin_surf, COIN_EDGE, rect)
    pygame.draw.ellipse(coin_surf, COIN_COLOR, rect.inflate(-10, -10))
    if width > 30:
        txt = "H" if (final_result == "Heads" if final_result else is_heads) else "T"
        font = pygame.font.SysFont("Times New Roman", 60, bold=True)
        t_surf = font.render(txt, True, (255,255,255))
        t_w = int(t_surf.get_width() * abs(width_scale))
        if t_w > 1:
            t_surf = pygame.transform.scale(t_surf, (t_w, t_surf.get_height()))
            t_rect = t_surf.get_rect(center=(width//2, height//2))
            coin_surf.blit(t_surf, t_rect)
    screen_rect = coin_surf.get_rect(center=(center_x, center_y))
    surface.blit(coin_surf, screen_rect)

def draw_selection_panel(surface, mouse_pos, game):
    hitboxes = []
    panel_start_y = 550
    pygame.draw.rect(surface, PANEL_COLOR, (0, panel_start_y, WIDTH, HEIGHT))
    pygame.draw.line(surface, ACCENT_COLOR, (0, panel_start_y), (WIDTH, panel_start_y), 3)
    font = pygame.font.SysFont("Arial", 16, bold=True)
    surface.blit(font.render("SELECT YOUR MOVE:", True, (200, 200, 200)), (10, panel_start_y + 10))
    start_x, start_y = 60, panel_start_y + 60
    options = []
    valid_keys = sorted(VALID_HANDS.keys())
    for r in valid_keys:
        for v in VALID_HANDS[r]: options.append((r, v))
    for i, (run_val, fingers) in enumerate(options):
        row, col = i // 7, i % 7
        x = start_x + (col * 110)
        y = start_y + (row * 85)
        btn_rect = pygame.Rect(x - 40, y - 40, 80, 80)
        is_disabled = (run_val == 5 and not game.free_hit)
        if not is_disabled:
            if btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, HOVER_COLOR, btn_rect, border_radius=10)
                pygame.draw.rect(surface, ACCENT_COLOR, btn_rect, 2, border_radius=10)
        else:
            pygame.draw.rect(surface, DISABLED_COLOR, btn_rect, border_radius=10)
        draw_hand_icon(surface, x, y, fingers, scale=0.3, is_left=False)
        if is_disabled:
            s = pygame.Surface((80,80), pygame.SRCALPHA)
            s.fill((0,0,0,150))
            surface.blit(s, (x-40, y-40))
            pygame.draw.line(surface, (100,100,100), (x-20, y-20), (x+20, y+20), 3)
            pygame.draw.line(surface, (100,100,100), (x+20, y-20), (x-20, y+20), 3)
        surface.blit(font.render(str(run_val), True, ACCENT_COLOR if not is_disabled else (100,100,100)), (x + 15, y + 15))
        if not is_disabled:
            hitboxes.append((btn_rect, run_val, fingers))
    return hitboxes