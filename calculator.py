import pygame
from pygame.locals import RESIZABLE

__version__ = '1.0'


class Button:
    #            focused, touched: color(r, g, b)
    color_dict = {(False, False): (160, 160, 160),
                  (False, True): (191, 191, 191),
                  (True, False): (224, 224, 224),
                  (True, True): (127, 127, 127)}

    def __init__(self, parent, label: str, font, pos: [int, int], size: [int, int], func):
        self.label_text = self.label = self.label_rect = self.font = None
        self.pos = pos
        self.size = size
        self.render_text(label, font)
        self.parent = parent
        self.maxpos = [pos[0] + size[0], pos[1] + size[1]]
        self.func = func
        self.focused = self.ffocused = self.touched = False

    def __contains__(self, item: [int, int]):
        return all(self.pos[i] <= item[i] <= self.maxpos[i] for i in range(2))

    def render_text(self, text: str, font):
        if isinstance(font, str):
            font = pygame.font.SysFont(font, int(min(self.size[1], self.size[0] / len(text))))
        self.label_text = text
        self.label = font.render(text, True, BLACK)
        self.label_rect = self.label.get_rect()
        self.label_rect.center = [self.pos[0] + self.size[0] // 2, self.pos[1] + self.size[1] // 2]

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.parent, self.color_dict[(self.focused, self.touched)],
                         (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        self.parent.blit(self.label, self.label_rect)

    def touch_began(self):
        if self.focused:
            self.touched = True

    def touch_moved(self, pos: [int, int]):
        self.focused = pos in self

    def touch_ended(self):
        if self.touched and self.focused:
            self.func(self)
        self.touched = False


class ButtonTouched:
    functions = {'sqrt': lambda x, y=2: x ** (1 / y)}
    first_text = 'Write!'
    error_text = 'Error'
    stdin = first_text
    stdout = 'Pygame Calculator. Made by ProkhPav'
    draw_text = shadow_text = None

    def __init__(self, b):
        if isinstance(b, ButtonTouched):
            self.draw_text = self.shadow_text = None
            self.stdin = b.stdin
            self.stdout = b.stdout

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key in ('stdin', 'stdout'):
            self.update_texts(key)

    def update_texts(self, name):
        if name == 'stdin':
            self.draw_text = button_font.render(self.stdin, True, BLACK)
        else:
            self.shadow_text = shadow_font.render(self.stdout, True, GRAY)

    def draw(self):
        pygame.draw.rect(screen, LGRAY, (lines, lines, desk_size[0], desk_size[1]))
        w1, w2 = self.draw_text.get_width(), self.shadow_text.get_width()
        screen.blit(self.draw_text, (b_font_pos[0] - w1, b_font_pos[1]))
        screen.blit(self.shadow_text, (s_font_pos[0] - w2, s_font_pos[1]))

    def __call__(self, button: Button):
        label: str = button.label_text.replace(' ', '')
        if self.stdin in (self.first_text, self.error_text):
            self.stdin = ' '
        if label.isdigit():
            if self.stdin[-1] != '0':
                self.stdin += label
        elif label == '(':
            if self.stdin[-1].isdigit():
                self.stdin += ' x '
            self.stdin += label
        elif label == ')':
            if self.stdin[-1] == '(':
                self.stdin = self.stdin[:-1]
            elif self.stdin.count('(') > self.stdin.count(')'):
                self.stdin += label
        elif label == '√':
            if self.stdin[-1].isdigit():
                self.stdin += ' x '
            self.stdin += label + '('
        elif label in '+-x÷^':
            if self.stdin[-1] not in ' (.':
                self.stdin += ' %s ' % label
            elif len(self.stdin) >= 3:
                self.stdin = self.stdin[:-3] + ' %s ' % label
        elif label == '◄':
            if self.stdin[-1] == ' ':
                if len(self.stdin) >= 3:
                    self.stdin = self.stdin[:-3]
                else:
                    self.stdin = ' '
            elif len(self.stdin) >= 1:
                self.stdin = self.stdin[:-1]
                if self.stdin[-1] == '√':
                    self.stdin = self.stdin[:-1]
        elif label == 'C':
            if self.stdin == ' ':
                self.stdout = ' '
            self.stdin = self.first_text
        elif label == '.':
            if '.' not in self.stdin[self.stdin.rfind(' '):]:
                self.stdin += label
        elif label == '=':
            try:
                stdout = str(self.stdin)
                stdin = self.stdin.replace('÷', '/').replace('x', '*').replace('^', '**').replace('√', 'sqrt')
                stdin = eval(stdin, self.functions)
                self.stdin = (str(int(stdin)) if stdin == int(stdin) else str(stdin))
                self.stdout = stdout + ' = ' + self.stdin
            except (SyntaxError, ZeroDivisionError):
                self.stdin = self.error_text
        if self.stdin == ' ':
            self.stdin = self.first_text

    def __str__(self):
        return 'in: %s, out: %s' % (self.stdin, self.stdout)

    def __repr__(self):
        return str(self)


def screen_resize(size):
    global sc_size, screen, block_size, button_size, desk_size, indent_size, button_font, shadow_font, buttons, \
        button_touched, b_font_pos, s_font_pos
    sc_size = size
    block_size = [(size[0] - lines) // buttons_num[0], (size[1] - lines) // (buttons_num[1] + 2)]
    screen = pygame.display.set_mode([block_size[0] * buttons_num[0] + lines,
                                      block_size[1] * (buttons_num[1] + 2) + lines], RESIZABLE)
    button_size = [block_size[i] - lines for i in range(2)]
    desk_size = [size[0] - lines * 2, block_size[1] * 2 - lines]
    indent_size = [lines, desk_size[1] + lines * 2]

    buttons = []
    button_font = pygame.font.SysFont('Arial', int(min(block_size[i] / 2 for i in range(2))))
    shadow_font = pygame.font.SysFont('Arial', int(min(block_size[i] / 3 for i in range(2))))
    b_font_pos = [size[0] - 4 * lines, desk_size[1] // 2 + lines]
    s_font_pos = [b_font_pos[0], desk_size[1] // 4 + lines // 2]
    button_touched = ButtonTouched(button_touched)
    y = indent_size[1]
    for i in range(buttons_num[1]):
        x = indent_size[0]
        for j in range(buttons_num[0]):
            buttons.append(Button(screen, texts[i][j], button_font, [x, y], button_size, button_touched))
            x += block_size[0]
        y += block_size[1]


lines = 1

texts = [i.split('|') for i in '''
C|MC|M+|M-|◄
7|8|9|(|)
4|5|6|^|√
1|2|3|x|÷
=|0|.|+|-
'''.split('\n')[1:-1]]

buttons_num = [len(texts[0]), len(texts)]

BLACK, BLUE, GRAY, LGRAY = (0, 0, 0), (96, 96, 192), (96, 96, 96), (192, 192, 192)

pygame.init()
timer = pygame.time.Clock()

button_touched = ButtonTouched(False)
screen_resize([350, 450])
pygame.display.set_caption('Calculator')

last_focus = False
keep_going = True
while keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        elif event.type == pygame.VIDEORESIZE:
            size = event.size
            screen_resize(size)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.touch_began()
        elif event.type == pygame.MOUSEMOTION:
            for button in buttons:
                button.touch_moved(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.touch_ended()
    if pygame.mouse.get_focused():
        last_focus = True
    else:
        if last_focus:
            for button in buttons:
                button.touch_moved([-1000, -1000])
        last_focus = False

    screen.fill(BLUE)
    for button in buttons:
        button.draw()
    button_touched.draw()

    timer.tick(60)
    pygame.display.update()

pygame.quit()
