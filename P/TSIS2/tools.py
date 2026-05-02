import pygame

def flood_fill(surface, start_x, start_y, target_color, fill_color):
    target_color = tuple(target_color)[:3]
    fill_color = tuple(fill_color)[:3]
    if target_color == fill_color:
        return

    width, height = surface.get_size()
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack.pop()
        if tuple(surface.get_at((x, y)))[:3] == target_color:
            surface.set_at((x, y), fill_color)
            if x > 0: stack.append((x - 1, y))
            if x < width - 1: stack.append((x + 1, y))
            if y > 0: stack.append((x, y - 1))
            if y < height - 1: stack.append((x, y + 1))

def draw_shape(surface, tool, color, start_p, end_p, thickness):
    x1, y1 = start_p
    x2, y2 = end_p
    
    rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
    rect.normalize()

    if tool == 'line':
        pygame.draw.line(surface, color, start_p, end_p, thickness)
    elif tool == 'rect':
        pygame.draw.rect(surface, color, rect, thickness)
    elif tool == 'square':
        size = max(abs(x2 - x1), abs(y2 - y1))
        sign_x = 1 if (x2 - x1) > 0 else -1
        sign_y = 1 if (y2 - y1) > 0 else -1
        sq_rect = pygame.Rect(x1, y1, size * sign_x, size * sign_y)
        sq_rect.normalize()
        pygame.draw.rect(surface, color, sq_rect, thickness)
    elif tool == 'circle':
        radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
        thick = min(thickness, radius) if radius > 0 else 0
        if radius > 0:
            pygame.draw.circle(surface, color, start_p, radius, thick)
    elif tool == 'right_tri':
        if rect.width > 0 and rect.height > 0:
            points = [(rect.left, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom)]
            pygame.draw.polygon(surface, color, points, thickness)
    elif tool == 'eq_tri':
        if rect.width > 0 and rect.height > 0:
            points = [(rect.centerx, rect.top), (rect.left, rect.bottom), (rect.right, rect.bottom)]
            pygame.draw.polygon(surface, color, points, thickness)
    elif tool == 'rhombus':
        if rect.width > 0 and rect.height > 0:
            points = [(rect.centerx, rect.top), (rect.right, rect.centery),
                      (rect.centerx, rect.bottom), (rect.left, rect.centery)]
            pygame.draw.polygon(surface, color, points, thickness)