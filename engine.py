import json
import os
from ai_bot import SmartBot
from config import *
import random

class Stats:
    def __init__(self, name):
        self.name = name
        self.runs = 0
        self.balls = 0
        self.is_out = False
        self.overs_bowled = 0
        self.wickets_taken = 0
        self.runs_conceded = 0

class GameEngine:
    def __init__(self):
        self.bot = SmartBot()
        
        # Default stats structure template
        self.empty_stats = {
            "matches": 0, "wins": 0, "losses": 0, 
            "runs": 0, "wickets": 0
        }
        
        self.user_stats = self.load_user_stats()
        self.reset_game()
        self.mode = MODE_STANDARD 
        self.state = STATE_MENU 
        self.opponent_type = "AI" # "AI" or "FRIEND"
        
        self.show_rules = False
        self.active_rule_mode = None 
        self.paused_state = None

    def load_user_stats(self):
        """Loads complex stats structure or creates default"""
        default = {
            "AI": {
                "STANDARD": self.empty_stats.copy(),
                "HARDCORE": self.empty_stats.copy()
            },
            "FRIEND": {
                "STANDARD": self.empty_stats.copy(),
                "HARDCORE": self.empty_stats.copy()
            }
        }
        
        if os.path.exists("user_stats.json"):
            try:
                with open("user_stats.json", "r") as f:
                    data = json.load(f)
                    # Simple validation to ensure structure exists
                    if "AI" in data and "STANDARD" in data["AI"]:
                        return data
            except:
                pass
        return default

    def save_user_stats(self):
        with open("user_stats.json", "w") as f:
            json.dump(self.user_stats, f)

    def update_career_stats(self, result):
        """
        result: "WIN", "LOSE", "TIE"
        Updates the specific nested stat block.
        """
        # Get the correct dictionary based on current settings
        target_stats = self.user_stats[self.opponent_type][self.mode]
        
        target_stats["matches"] += 1
        target_stats["runs"] += self.p_score
        target_stats["wickets"] += self.ai_wickets # Wickets taken by user
        
        if result == "WIN":
            target_stats["wins"] += 1
        elif result == "LOSE":
            target_stats["losses"] += 1
            
        self.save_user_stats()

    def reset_game(self):
        self.total_overs = 5
        self.max_wickets = 2
        self.max_overs_per_bowler = 3
        
        self.innings = 1
        self.target = None
        self.batting = None 
        
        self.p_score = 0
        self.p_wickets = 0
        self.p_overs = 0.0
        self.ai_score = 0
        self.ai_wickets = 0
        self.ai_overs = 0.0

        self.p_batsmen = [Stats(f"Player {i+1}") for i in range(11)]
        self.p_bowlers = [Stats(f"P-Bowler {i+1}") for i in range(5)]
        
        # Name opponents based on type
        opp_name = "AI" if getattr(self, 'opponent_type', 'AI') == 'AI' else "Friend"
        self.ai_batsmen = [Stats(f"{opp_name} {i+1}") for i in range(11)]
        self.ai_bowlers = [Stats(f"{opp_name}-Bow {i+1}") for i in range(5)]

        self.striker_idx = 0
        self.non_striker_idx = 1
        self.current_bowler_idx = 0
        self.balls_in_over = 0
        
        self.streak_visuals = []
        self.streak_count = 0
        self.free_hit = False
        self.msg = ""
        self.result_desc = ""
        self.timeline = [] 
        
        self.p_vis = []
        self.ai_vis = []
        self.p_last = -1 
        self.ai_last = 0

    def start_match(self, overs):
        preset = MATCH_PRESETS[overs]
        self.total_overs = overs
        self.max_wickets = preset["wickets"]
        self.max_overs_per_bowler = preset["limit"]
        self.msg = "TOSS TIME!"

    def get_current_stats(self):
        if self.batting == "PLAYER":
            bat = self.p_batsmen[self.striker_idx]
            bowl = self.ai_bowlers[self.current_bowler_idx]
        else:
            bat = self.ai_batsmen[self.striker_idx]
            bowl = self.p_bowlers[self.current_bowler_idx]
        return bat, bowl

    def switch_strike(self):
        self.striker_idx, self.non_striker_idx = self.non_striker_idx, self.striker_idx

    def rotate_bowler(self):
        start = self.current_bowler_idx
        while True:
            self.current_bowler_idx = (self.current_bowler_idx + 1) % len(self.p_bowlers)
            bowler_list = self.p_bowlers if self.batting == "AI" else self.ai_bowlers
            if bowler_list[self.current_bowler_idx].overs_bowled < self.max_overs_per_bowler:
                break
            if self.current_bowler_idx == start: break 

    def check_hardcore_streak(self, hand_visual):
        self.streak_visuals.append(hand_visual)
        if len(self.streak_visuals) > 6:
            self.streak_visuals.pop(0)
        
        if len(self.streak_visuals) == 6:
            first = sorted(self.streak_visuals[0])
            if all(sorted(h) == first for h in self.streak_visuals):
                return True
        return False

    def process_turn(self, p_run, p_hand_visual):
        is_ai_batting = (self.batting == "AI")
        ai_move = self.bot.get_move(is_ai_batting, self.free_hit)
        self.bot.record_move(p_run)
        
        self.p_last = p_run
        self.ai_last = ai_move
        self.p_vis = p_hand_visual
        self.ai_vis = self.bot.get_hand_visual(ai_move)

        curr_bat, curr_bowl = self.get_current_stats()
        
        batter_run = p_run if self.batting == "PLAYER" else ai_move
        bowler_run = ai_move if self.batting == "PLAYER" else p_run
        
        status_text = ""
        timeline_event = ""
        is_out = False
        is_no_ball = False

        if self.mode == MODE_HARDCORE and not self.free_hit:
             if self.check_hardcore_streak(p_hand_visual):
                 is_no_ball = True
                 status_text = "NO BALL! Free Hit!"
                 self.streak_visuals = []

        if not is_no_ball:
            if batter_run == bowler_run:
                if self.mode == MODE_STANDARD:
                    is_out = True
                elif self.mode == MODE_HARDCORE:
                    if set(self.p_vis) == set(self.ai_vis):
                        is_out = True
                    else:
                        status_text = "SAVED! Mismatch!"

        curr_bowl.runs_conceded += 0 if is_out else batter_run
        
        if is_no_ball:
            self.free_hit = True
            curr_bowl.runs_conceded += 1
            if self.batting == "PLAYER": self.p_score += 1
            else: self.ai_score += 1
            timeline_event = "NB"
        
        elif is_out:
            if self.free_hit:
                status_text = "FREE HIT SAVE!"
                self.free_hit = False
                curr_bat.runs += batter_run
                curr_bat.balls += 1
                if self.batting == "PLAYER": self.p_score += batter_run
                else: self.ai_score += batter_run
                timeline_event = str(batter_run)
            else:
                curr_bat.is_out = True
                curr_bat.balls += 1
                curr_bowl.wickets_taken += 1
                timeline_event = "W"
                self.timeline.append(timeline_event) 
                self.handle_wicket()
                return "OUT"
        
        else: 
            if self.free_hit:
                status_text = "Free Hit Used"
                self.free_hit = False
            
            curr_bat.runs += batter_run
            curr_bat.balls += 1
            
            if self.batting == "PLAYER": self.p_score += batter_run
            else: self.ai_score += batter_run
            
            timeline_event = str(batter_run)

            if batter_run % 2 != 0:
                self.switch_strike()
                
            self.balls_in_over += 1

        self.timeline.append(timeline_event)
        if len(self.timeline) > 8: self.timeline.pop(0)

        if not is_out and not is_no_ball and self.balls_in_over == 6:
             self.end_over(curr_bowl)

        if self.target:
            score = self.p_score if self.batting == "PLAYER" else self.ai_score
            if score > self.target:
                self.state = STATE_GAME_OVER
                wickets_left = self.max_wickets - (self.p_wickets if self.batting == "PLAYER" else self.ai_wickets)
                self.result_desc = f"{self.batting} Won by {wickets_left} Wickets"
                self.msg = "MATCH ENDED"
                self.update_career_stats("WIN")
                return "WIN"

        self.msg = status_text if status_text else f"{batter_run} Runs"
        return "PLAY"

    def end_over(self, bowler_obj):
        self.balls_in_over = 0
        bowler_obj.overs_bowled += 1
        if self.batting == "PLAYER": self.p_overs += 1
        else: self.ai_overs += 1
        self.switch_strike()
        self.rotate_bowler()
        current_overs = self.p_overs if self.batting == "PLAYER" else self.ai_overs
        if current_overs >= self.total_overs:
            self.end_innings()

    def handle_wicket(self):
        if self.batting == "PLAYER":
            self.p_wickets += 1
            wicks = self.p_wickets
        else:
            self.ai_wickets += 1
            wicks = self.ai_wickets
        if wicks >= self.max_wickets:
            self.end_innings()
        else:
            next_idx = max(self.striker_idx, self.non_striker_idx) + 1
            self.striker_idx = next_idx
            self.msg = "WICKET!!!"

    def end_innings(self):
        self.timeline = [] 
        if self.innings == 1:
            self.innings = 2
            self.state = STATE_INNINGS_BREAK
            if self.batting == "PLAYER":
                self.target = self.p_score
                self.msg = f"Innings Over! AI needs {self.target + 1}"
                self.batting = "AI"
            else:
                self.target = self.ai_score
                self.msg = f"Innings Over! You need {self.target + 1}"
                self.batting = "PLAYER"
            self.balls_in_over = 0
            self.current_bowler_idx = 0
            self.striker_idx = 0
            self.non_striker_idx = 1
        else:
            self.state = STATE_GAME_OVER
            if self.p_score > self.ai_score:
                margin = self.p_score - self.ai_score
                self.result_desc = f"PLAYER Won by {margin} Runs"
                self.update_career_stats("WIN")
            elif self.ai_score > self.p_score:
                margin = self.ai_score - self.p_score
                self.result_desc = f"AI Won by {margin} Runs"
                self.update_career_stats("LOSE")
            else:
                self.result_desc = "MATCH TIED!"
                self.update_career_stats("TIE")
            self.msg = "MATCH ENDED"