import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))  
    is_drawing = False  
    brush_size = 5  
    draw_color = 'white'  
    draw_mode = 'pen'  
    last_mouse_pos = (0, 0)  
    start_pos = None  


    #draw line
    def draw_line(screen, start_pos, end_pos, width, color): 
        pygame.draw.line(screen, pygame.Color(color), start_pos, end_pos, width)

    #draw rectangle
    def draw_rectangle(screen, start_pos, end_pos, width, color): 
        if start_pos is None or end_pos is None:
            return
        x1, y1 = start_pos
        x2, y2 = end_pos
        pygame.draw.rect(screen, pygame.Color(color), (min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)), width)

    #draw_circle
    def draw_circle(screen, start_pos, end_pos, width, color): 
        if start_pos is None or end_pos is None:
            return
        x1, y1 = start_pos
        x2, y2 = end_pos
        center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
        radius = max(abs(x1 - x2), abs(y1 - y2)) // 2
        pygame.draw.circle(screen, pygame.Color(color), (center_x, center_y), radius, width)

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                color_keys = {
                    pygame.K_r: 'red',
                    pygame.K_g: 'green',
                    pygame.K_b: 'blue',
                    pygame.K_y: 'yellow',
                    pygame.K_p: 'purple',
                    pygame.K_w: 'white'
                }
                if event.key in color_keys:
                    draw_color = color_keys[event.key]

                mode_keys = {
                    pygame.K_t: 'rectangle',
                    pygame.K_c: 'circle',
                    pygame.K_e: 'eraser',
                    pygame.K_n: 'pen'
                }
                if event.key in mode_keys:
                    draw_mode = mode_keys[event.key]

            if event.type == pygame.MOUSEBUTTONDOWN:
                is_drawing = True
                start_pos = event.pos  
                last_mouse_pos = event.pos  

            if event.type == pygame.MOUSEBUTTONUP:
                is_drawing = False
                if draw_mode == 'rectangle':
                    draw_rectangle(screen, start_pos, event.pos, brush_size, draw_color)
                elif draw_mode == 'circle':
                    draw_circle(screen, start_pos, event.pos, brush_size, draw_color)

            if event.type == pygame.MOUSEMOTION and is_drawing:
                if draw_mode == 'pen':
                    draw_line(screen, last_mouse_pos, event.pos, brush_size, draw_color)
                elif draw_mode == 'eraser': #eraser
                    draw_line(screen, last_mouse_pos, event.pos, brush_size * 3, 'black')  
                last_mouse_pos = event.pos  

        pygame.display.flip()
        clock.tick(60)

main()
