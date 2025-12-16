import pygame
import asyncio
import random
from config import *
from engine import GameEngine
import graphics as gfx

async def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Hand Cricket")
    clock = pygame.time.Clock()
    
    font_main = pygame.font.SysFont("Arial", 30, bold=True)
    font_big = pygame.font.SysFont("Arial", 40, bold=True)
    
    game = GameEngine()
    hitboxes = [] 
    menu_btn_rect = None 
    toss_choice = None 
    toss_frame = 0 
    anim_timer = 0
    back_btn_rect = None
    
    # UI State for Profile
    profile_tab = "AI" 
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.active_rule_mode:
                    game.active_rule_mode = None
                    continue

                if back_btn_rect and back_btn_rect.collidepoint(mouse_pos):
                    if game.state == STATE_PROFILE:
                        game.state = STATE_MENU
                    elif game.state == STATE_MODE_SELECT:
                        game.state = STATE_MENU
                    elif game.state == STATE_OVERS_SELECT:
                        game.state = STATE_MODE_SELECT
                    elif game.state in [STATE_TOSS, STATE_PLAYING, STATE_INNINGS_BREAK]:
                        game.paused_state = game.state
                        game.state = STATE_WARNING
                    continue

                if game.state == STATE_WARNING:
                    btn_yes = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 + 50, 140, 50)
                    btn_no = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 50, 140, 50)
                    if btn_yes.collidepoint(mouse_pos):
                        game.reset_game()
                        game.state = STATE_MENU
                    elif btn_no.collidepoint(mouse_pos):
                        game.state = game.paused_state
                    continue

                if game.state == STATE_MENU:
                    prof_rect = gfx.draw_menu(screen, mouse_pos) 
                    if prof_rect.collidepoint(mouse_pos):
                        game.state = STATE_PROFILE
                    elif pygame.Rect(WIDTH//2 - 125, 400, 250, 60).collidepoint(mouse_pos):
                        game.opponent_type = "AI"
                        game.state = STATE_MODE_SELECT
                    elif pygame.Rect(WIDTH//2 - 125, 300, 250, 60).collidepoint(mouse_pos):
                        game.opponent_type = "FRIEND"
                        game.state = STATE_MODE_SELECT

                elif game.state == STATE_PROFILE:
                    # Handle Tab Switching
                    tab_rects = gfx.draw_profile_screen(screen, game.user_stats, mouse_pos, profile_tab)
                    if tab_rects["AI"].collidepoint(mouse_pos):
                        profile_tab = "AI"
                    elif tab_rects["FRIEND"].collidepoint(mouse_pos):
                        profile_tab = "FRIEND"

                elif game.state == STATE_MODE_SELECT:
                    btns = gfx.draw_mode_select(screen, mouse_pos)
                    if btns["STD"].collidepoint(mouse_pos):
                        game.mode = MODE_STANDARD
                        game.state = STATE_OVERS_SELECT
                    elif btns["HRD"].collidepoint(mouse_pos):
                        game.mode = MODE_HARDCORE
                        game.state = STATE_OVERS_SELECT
                    elif btns["Q_STD"].collidepoint(mouse_pos):
                        game.active_rule_mode = "STANDARD"
                    elif btns["Q_HRD"].collidepoint(mouse_pos):
                        game.active_rule_mode = "HARDCORE"
                
                elif game.state == STATE_OVERS_SELECT:
                    btns = gfx.draw_overs_select(screen, mouse_pos)
                    for overs, rect in btns.items():
                        if rect.collidepoint(mouse_pos):
                            game.start_match(overs)
                            game.state = STATE_TOSS

                elif game.state == STATE_TOSS:
                    if pygame.Rect(200, 450, 150, 60).collidepoint(mouse_pos):
                        toss_choice = "Heads"
                    elif pygame.Rect(450, 450, 150, 60).collidepoint(mouse_pos):
                        toss_choice = "Tails"
                    if toss_choice:
                        game.state = STATE_TOSS_ANIM
                        anim_timer = 90 

                elif game.state == STATE_PLAYING:
                    if menu_btn_rect and menu_btn_rect.collidepoint(mouse_pos):
                        game.show_rules = not game.show_rules
                        continue
                    if game.show_rules:
                        game.show_rules = False
                        continue
                    for rect, run_val, fingers in hitboxes:
                        if rect.collidepoint(mouse_pos):
                            game.process_turn(run_val, fingers)
                
                elif game.state == STATE_INNINGS_BREAK:
                    game.state = STATE_PLAYING 
                
                elif game.state == STATE_GAME_OVER:
                    if pygame.Rect(WIDTH//2 - 125, 500, 250, 60).collidepoint(mouse_pos):
                        game.reset_game()
                        game.state = STATE_MENU

        screen.fill(BG_COLOR)
        
        if game.state not in [STATE_MENU, STATE_WARNING, STATE_GAME_OVER]:
            back_btn_rect = gfx.draw_back_button(screen, mouse_pos)
        else:
            back_btn_rect = None

        if game.state == STATE_MENU:
            gfx.draw_menu(screen, mouse_pos)

        elif game.state == STATE_PROFILE:
            # We already called draw inside event loop to get rects, call again for display
            gfx.draw_profile_screen(screen, game.user_stats, mouse_pos, profile_tab)

        elif game.state == STATE_MODE_SELECT:
            gfx.draw_mode_select(screen, mouse_pos)
            
        elif game.state == STATE_OVERS_SELECT:
            gfx.draw_overs_select(screen, mouse_pos)

        elif game.state == STATE_TOSS:
            gfx.draw_text_centered(screen, "TOSS TIME!", 150, font_big, ACCENT_COLOR)
            gfx.draw_coin_animated(screen, WIDTH//2, 330, 0, final_result=None)
            gfx.draw_button(screen, pygame.Rect(200, 450, 150, 60), "HEADS", mouse_pos)
            gfx.draw_button(screen, pygame.Rect(450, 450, 150, 60), "TAILS", mouse_pos)

        elif game.state == STATE_TOSS_ANIM:
            gfx.draw_text_centered(screen, "Flipping...", 150, font_big, ACCENT_COLOR)
            toss_frame += 1
            anim_timer -= 1
            if anim_timer > 0:
                gfx.draw_coin_animated(screen, WIDTH//2, 330, toss_frame)
            else:
                result = random.choice(["Heads", "Tails"])
                gfx.draw_coin_animated(screen, WIDTH//2, 330, 0, final_result=result)
                pygame.display.flip()
                await asyncio.sleep(2)
                if toss_choice == result:
                    game.batting = "PLAYER"
                    game.msg = "You Bat First."
                else:
                    game.batting = "AI"
                    game.msg = "AI Bats First."
                game.state = STATE_PLAYING

        elif game.state == STATE_PLAYING:
            menu_btn_rect = gfx.draw_hud(screen, game)
            curr_score = game.p_score if game.batting == "PLAYER" else game.ai_score
            curr_wickets = game.p_wickets if game.batting == "PLAYER" else game.ai_wickets
            score_txt = f"{game.batting}: {curr_score}/{curr_wickets}"
            gfx.draw_text_centered(screen, score_txt, 30, font_main, TEXT_COLOR)
            curr_overs = game.p_overs if game.batting == "PLAYER" else game.ai_overs
            overs_txt = f"Overs: {int(curr_overs)}.{game.balls_in_over} ({game.total_overs})"
            gfx.draw_text_centered(screen, overs_txt, 60, font_main, ACCENT_COLOR)
            if game.target:
                gfx.draw_text_centered(screen, f"TARGET: {game.target + 1}", 90, font_main, (200, 200, 200))
            msg_color = ALERT_COLOR if "WICKET" in game.msg or "NO BALL" in game.msg else ACCENT_COLOR
            gfx.draw_text_centered(screen, game.msg, 180, font_big, msg_color)
            if game.free_hit:
                pygame.draw.rect(screen, ALERT_COLOR, (WIDTH//2 - 100, 225, 200, 40), border_radius=10)
                gfx.draw_text_centered(screen, "FREE HIT!", 230, font_main, TEXT_COLOR)
            gfx.draw_game_hands(screen, game.p_vis, game.ai_vis)
            if game.p_last >= 0:
                gfx.draw_text_centered(screen, f"You Played: {game.p_last}", 460, font_main, TEXT_COLOR)
            hitboxes = gfx.draw_selection_panel(screen, mouse_pos, game)

        elif game.state == STATE_INNINGS_BREAK:
            menu_btn_rect = gfx.draw_hud(screen, game)
            gfx.draw_scorecard_overlay(screen, game)

        elif game.state == STATE_GAME_OVER:
             gfx.draw_game_over_screen(screen, game, mouse_pos)

        if game.state == STATE_WARNING:
            gfx.draw_exit_warning(screen, mouse_pos)

        if game.show_rules:
            gfx.draw_rules_overlay(screen)
            
        if game.active_rule_mode:
            gfx.draw_mode_rules_overlay(screen, game.active_rule_mode)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())