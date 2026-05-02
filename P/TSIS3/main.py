import pygame
import sys
from persistence import load_settings, save_settings, load_leaderboard, save_leaderboard
from ui import Button, InputBox, draw_text, TITLE_FONT, FONT
from racer import GameEngine

pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("TSIS 3: Racer Game")

def main():
    settings = load_settings()
    leaderboard = load_leaderboard()
    current_state = "MENU"
    player_name = "Player1"
    last_results = None

    # Кнопки для меню
    btn_play = Button(100, 200, 200, 50, "Play")
    btn_leader = Button(100, 280, 200, 50, "Leaderboard")
    btn_set = Button(100, 360, 200, 50, "Settings")
    btn_quit = Button(100, 440, 200, 50, "Quit")

    # Кнопки для других экранов
    btn_back = Button(100, 500, 200, 50, "Back")
    btn_retry = Button(100, 400, 200, 50, "Retry")
    
    # Кнопки настроек
    btn_color = Button(50, 200, 300, 50, f"Car Color: {settings['car_color']}")
    btn_diff = Button(50, 280, 300, 50, f"Difficulty: {settings['difficulty']}")
    
    input_box = InputBox(100, 300, 200, 40, player_name)

    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_state == "MENU":
            draw_text(screen, "RACER", TITLE_FONT, (255, 200, 0), SCREEN_WIDTH//2, 100, center=True)
            for btn in [btn_play, btn_leader, btn_set, btn_quit]:
                btn.draw(screen)
                for event in events:
                    if btn.handle_event(event):
                        if btn == btn_play: current_state = "NAME_INPUT"
                        elif btn == btn_leader: current_state = "LEADERBOARD"
                        elif btn == btn_set: current_state = "SETTINGS"
                        elif btn == btn_quit: pygame.quit(); sys.exit()

        elif current_state == "NAME_INPUT":
            draw_text(screen, "Enter Username:", FONT, (255, 255, 255), SCREEN_WIDTH//2, 250, center=True)
            input_box.draw(screen)
            for event in events:
                if input_box.handle_event(event):
                    player_name = input_box.text if input_box.text else "Player"
                    current_state = "PLAY"

        elif current_state == "PLAY":
            game = GameEngine(screen, settings)
            results = game.run()
            if results is None: 
                pygame.quit(); sys.exit()
            
            last_results = results
            leaderboard.append({
                "name": player_name,
                "score": results["score"],
                "distance": results["distance"]
            })
            save_leaderboard(leaderboard)
            current_state = "GAMEOVER"

        elif current_state == "GAMEOVER":
            draw_text(screen, "GAME OVER", TITLE_FONT, (255, 50, 50), SCREEN_WIDTH//2, 100, center=True)
            draw_text(screen, f"Score: {last_results['score']}", FONT, (255, 255, 255), SCREEN_WIDTH//2, 200, center=True)
            draw_text(screen, f"Distance: {last_results['distance']}m", FONT, (255, 255, 255), SCREEN_WIDTH//2, 250, center=True)
            
            btn_retry.draw(screen)
            btn_back.text = "Main Menu"
            btn_back.draw(screen)
            
            for event in events:
                if btn_retry.handle_event(event): current_state = "PLAY"
                if btn_back.handle_event(event): current_state = "MENU"

        elif current_state == "LEADERBOARD":
            draw_text(screen, "TOP 10", TITLE_FONT, (255, 200, 0), SCREEN_WIDTH//2, 50, center=True)
            y = 120
            for i, entry in enumerate(leaderboard):
                txt = f"{i+1}. {entry['name']} - {entry['score']} ({entry['distance']}m)"
                draw_text(screen, txt, FONT, (200, 200, 200), 50, y)
                y += 35
            
            btn_back.text = "Back"
            btn_back.draw(screen)
            for event in events:
                if btn_back.handle_event(event): current_state = "MENU"

        elif current_state == "SETTINGS":
            draw_text(screen, "SETTINGS", TITLE_FONT, (255, 255, 255), SCREEN_WIDTH//2, 100, center=True)
            
            btn_color.text = f"Car Color: {settings['car_color']}"
            btn_diff.text = f"Difficulty: {settings['difficulty']}"
            
            for btn in [btn_color, btn_diff, btn_back]:
                btn.draw(screen)
                for event in events:
                    if btn.handle_event(event):
                        if btn == btn_color:
                            colors = ["red", "blue", "green"]
                            idx = colors.index(settings["car_color"])
                            settings["car_color"] = colors[(idx + 1) % len(colors)]
                            save_settings(settings)
                        elif btn == btn_diff:
                            diffs = ["easy", "normal", "hard"]
                            idx = diffs.index(settings["difficulty"])
                            settings["difficulty"] = diffs[(idx + 1) % len(diffs)]
                            save_settings(settings)
                        elif btn == btn_back:
                            current_state = "MENU"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()