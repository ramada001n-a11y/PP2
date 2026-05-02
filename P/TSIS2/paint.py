import pygame
import sys
import datetime
from tools import flood_fill, draw_shape  

pygame.init()

WIDTH, HEIGHT = 1000, 700
UI_HEIGHT = 80
FPS = 60

# Цвета
COLORS = [
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)
]
BG_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2: Paint Application")

canvas = pygame.Surface((WIDTH, HEIGHT - UI_HEIGHT))
canvas.fill(BG_COLOR)

ui_font = pygame.font.SysFont('Arial', 16)
canvas_font = pygame.font.SysFont('Arial', 24)

current_tool = 'pencil'
current_color = COLORS[0]
brush_size = 2

drawing = False
start_pos = (0, 0)
last_pos = (0, 0)

typing = False
text_input = ""
text_pos = (0, 0)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text_input:
                        txt_surf = canvas_font.render(text_input, True, current_color)
                        canvas.blit(txt_surf, text_pos)
                    typing = False
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    text_input += event.unicode
            continue

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"canvas_{now}.png"
                pygame.image.save(canvas, filename)
                print(f"Canvas saved as: {filename}")
            
            elif event.key == pygame.K_1: brush_size = 2
            elif event.key == pygame.K_2: brush_size = 5
            elif event.key == pygame.K_3: brush_size = 10
            
            elif event.key == pygame.K_p: current_tool = 'pencil'
            elif event.key == pygame.K_l: current_tool = 'line'
            elif event.key == pygame.K_r: current_tool = 'rect'
            elif event.key == pygame.K_c: current_tool = 'circle'
            elif event.key == pygame.K_s: current_tool = 'square'
            elif event.key == pygame.K_t: current_tool = 'right_tri'
            elif event.key == pygame.K_e: current_tool = 'eq_tri'
            elif event.key == pygame.K_h: current_tool = 'rhombus'
            elif event.key == pygame.K_f: current_tool = 'fill'
            elif event.key == pygame.K_a: current_tool = 'text'
            elif event.key == pygame.K_x: current_tool = 'eraser'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                
                if y < UI_HEIGHT:
                    for i, color in enumerate(COLORS):
                        color_rect = pygame.Rect(10 + i * 40, 40, 30, 30)
                        if color_rect.collidepoint(x, y):
                            current_color = color
                else:
                    canvas_pos = (x, y - UI_HEIGHT)

                    if current_tool == 'text':
                        if typing and text_input:
                            txt_surf = canvas_font.render(text_input, True, current_color)
                            canvas.blit(txt_surf, text_pos)
                        typing = True
                        text_pos = canvas_pos
                        text_input = ""
                    elif current_tool == 'fill':
                        target_color = canvas.get_at(canvas_pos)
                        flood_fill(canvas, canvas_pos[0], canvas_pos[1], target_color, current_color)
                    else:
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                if current_tool in ['pencil', 'eraser']:
                    draw_color = BG_COLOR if current_tool == 'eraser' else current_color
                    pygame.draw.line(canvas, draw_color, last_pos, canvas_pos, brush_size)
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                canvas_pos = (event.pos[0], event.pos[1] - UI_HEIGHT)
                if current_tool not in ['pencil', 'eraser', 'fill', 'text']:
                    draw_shape(canvas, current_tool, current_color, start_pos, canvas_pos, brush_size)

    screen.fill((200, 200, 200))
    
    temp_canvas = canvas.copy()
    if drawing and current_tool not in ['pencil', 'eraser', 'fill', 'text']:
        current_canvas_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - UI_HEIGHT)
        draw_shape(temp_canvas, current_tool, current_color, start_pos, current_canvas_pos, brush_size)
    
    if typing:
        txt_surf = canvas_font.render(text_input + "|", True, current_color)
        temp_canvas.blit(txt_surf, text_pos)

    screen.blit(temp_canvas, (0, UI_HEIGHT))

    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, UI_HEIGHT))
    pygame.draw.line(screen, (100, 100, 100), (0, UI_HEIGHT - 1), (WIDTH, UI_HEIGHT - 1), 2)

    info_text = (f"Tool: {current_tool.upper()} | Size: {brush_size}px | "
                 f"Save: Ctrl+S | Sizes: 1-3 | "
                 f"P=Pencil L=Line R=Rect C=Circle S=Square T=RightTri E=EqTri H=Rhombus F=Fill A=Text X=Eraser")
    text_surf = ui_font.render(info_text, True, (0, 0, 0))
    screen.blit(text_surf, (10, 10))

    for i, color in enumerate(COLORS):
        rect_x, rect_y = 10 + i * 40, 40
        pygame.draw.rect(screen, color, (rect_x, rect_y, 30, 30))
        if color == current_color:
            pygame.draw.rect(screen, (255, 0, 0), (rect_x - 2, rect_y - 2, 34, 34), 2)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()