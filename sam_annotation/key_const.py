"""キー定数"""

# 数字
KEY_0 = ord('0')
KEY_1 = ord('1')
KEY_2 = ord('2')
KEY_3 = ord('3')
KEY_4 = ord('4')
KEY_5 = ord('5')
KEY_6 = ord('6')
KEY_7 = ord('7')
KEY_8 = ord('8')
KEY_9 = ord('9')

# 大文字アルファベット
KEY_A = ord('A')
KEY_B = ord('B')
KEY_C = ord('C')
KEY_D = ord('D')
KEY_E = ord('E')
KEY_F = ord('F')
KEY_G = ord('G')
KEY_H = ord('H')
KEY_I = ord('I')
KEY_J = ord('J')
KEY_K = ord('K')
KEY_L = ord('L')
KEY_M = ord('M')
KEY_N = ord('N')
KEY_O = ord('O')
KEY_P = ord('P')
KEY_Q = ord('Q')
KEY_R = ord('R')
KEY_S = ord('S')
KEY_T = ord('T')
KEY_U = ord('U')
KEY_V = ord('V')
KEY_W = ord('W')
KEY_X = ord('X')
KEY_Y = ord('Y')
KEY_Z = ord('Z')

# 小文字アルファベット
KEY_a = ord('a')
KEY_b = ord('b')
KEY_c = ord('c')
KEY_d = ord('d')
KEY_e = ord('e')
KEY_f = ord('f')
KEY_g = ord('g')
KEY_h = ord('h')
KEY_i = ord('i')
KEY_j = ord('j')
KEY_k = ord('k')
KEY_l = ord('l')
KEY_m = ord('m')
KEY_n = ord('n')
KEY_o = ord('o')
KEY_p = ord('p')
KEY_q = ord('q')
KEY_r = ord('r')
KEY_s = ord('s')
KEY_t = ord('t')
KEY_u = ord('u')
KEY_v = ord('v')
KEY_w = ord('w')
KEY_x = ord('x')
KEY_y = ord('y')
KEY_z = ord('z')

# 記号文字
KEY_EXCLAMATION = ord('!')
KEY_DOUBLE_QUOTE = ord('"')
KEY_HASH = ord('#')
KEY_DOLLAR = ord('$')
KEY_PERCENT = ord('%')
KEY_AMPERSAND = ord('&')
KEY_SINGLE_QUOTE = ord("'")
KEY_OPEN_PAREN = ord('(')
KEY_CLOSE_PAREN = ord(')')
KEY_ASTERISK = ord('*')
KEY_PLUS = ord('+')
KEY_COMMA = ord(',')
KEY_MINUS = ord('-')
KEY_PERIOD = ord('.')
KEY_SLASH = ord('/')
KEY_COLON = ord(':')
KEY_SEMICOLON = ord(';')
KEY_LESS_THAN = ord('<')
KEY_EQUAL = ord('=')
KEY_GREATER_THAN = ord('>')
KEY_QUESTION = ord('?')
KEY_AT = ord('@')
KEY_OPEN_BRACKET = ord('[')
KEY_BACKSLASH = ord('\\')
KEY_CLOSE_BRACKET = ord(']')
KEY_CARET = ord('^')
KEY_UNDERSCORE = ord('_')
KEY_BACKTICK = ord('`')
KEY_OPEN_BRACE = ord('{')
KEY_VERTICAL_BAR = ord('|')
KEY_CLOSE_BRACE = ord('}')
KEY_TILDE = ord('~')

# 矢印キー
KEY_LEFT_ARROW = 0x250000
KEY_UP_ARROW = 0x260000
KEY_RIGHT_ARROW = 0x270000
KEY_DOWN_ARROW = 0x280000

# 特殊キー
KEY_BACKSPACE = 0x08 # 8
KEY_TAB = 0x09 # 9
KEY_ENTER = 0x0D # 13
KEY_ESCAPE = 0x1B # 27
KEY_SPACE = 0x20 # 32

KEY_PAGE_UP = 0x210000
KEY_PAGE_DOWN = 0x220000
KEY_END = 0x230000
KEY_HOME = 0x240000
KEY_INSERT = 0x2D0000
KEY_DELETE = 0x2E0000

# ファンクションキー
KEY_F1 = 0x700000
KEY_F2 = 0x710000
KEY_F3 = 0x720000
KEY_F4 = 0x730000
KEY_F5 = 0x740000
KEY_F6 = 0x750000
KEY_F7 = 0x760000
KEY_F8 = 0x770000
KEY_F9 = 0x780000
KEY_F10 = 0x790000
KEY_F11 = 0x7A0000
KEY_F12 = 0x7B0000

# キー定数と文字列のマップ
KEYMAP = {
    KEY_BACKSPACE: 'BACKSPACE',
    KEY_TAB: 'TAB',
    KEY_ENTER: 'ENTER',
    KEY_ESCAPE: 'ESC',
    KEY_SPACE: 'SPACE',
    KEY_PAGE_UP: 'PAGE_UP',
    KEY_PAGE_DOWN: 'PAGE_DOWN',
    KEY_END: 'END',
    KEY_HOME: 'HOME',
    KEY_INSERT: 'INSERT',
    KEY_DELETE: 'DELETE',
    KEY_LEFT_ARROW: 'LEFT_ARROW',
    KEY_UP_ARROW: 'UP_ARROW',
    KEY_RIGHT_ARROW: 'RIGHT_ARROW',
    KEY_DOWN_ARROW: 'DOWN_ARROW',
    
    KEY_0: '0',
    KEY_1: '1',
    KEY_2: '2',
    KEY_3: '3',
    KEY_4: '4',
    KEY_5: '5',
    KEY_6: '6',
    KEY_7: '7',
    KEY_8: '8',
    KEY_9: '9',
    
    KEY_A: 'A',
    KEY_B: 'B',
    KEY_C: 'C',
    KEY_D: 'D',
    KEY_E: 'E',
    KEY_F: 'F',
    KEY_G: 'G',
    KEY_H: 'H',
    KEY_I: 'I',
    KEY_J: 'J',
    KEY_K: 'K',
    KEY_L: 'L',
    KEY_M: 'M',
    KEY_N: 'N',
    KEY_O: 'O',
    KEY_P: 'P',
    KEY_Q: 'Q',
    KEY_R: 'R',
    KEY_S: 'S',
    KEY_T: 'T',
    KEY_U: 'U',
    KEY_V: 'V',
    KEY_W: 'W',
    KEY_X: 'X',
    KEY_Y: 'Y',
    KEY_Z: 'Z',
    
    KEY_a: 'a',
    KEY_b: 'b',
    KEY_c: 'c',
    KEY_d: 'd',
    KEY_e: 'e',
    KEY_f: 'f',
    KEY_g: 'g',
    KEY_h: 'h',
    KEY_i: 'i',
    KEY_j: 'j',
    KEY_k: 'k',
    KEY_l: 'l',
    KEY_m: 'm',
    KEY_n: 'n',
    KEY_o: 'o',
    KEY_p: 'p',
    KEY_q: 'q',
    KEY_r: 'r',
    KEY_s: 's',
    KEY_t: 't',
    KEY_u: 'u',
    KEY_v: 'v',
    KEY_w: 'w',
    KEY_x: 'x',
    KEY_y: 'y',
    KEY_z: 'z',
    
    KEY_EXCLAMATION: '!',
    KEY_DOUBLE_QUOTE: '"',
    KEY_HASH: '#',
    KEY_DOLLAR: '$',
    KEY_PERCENT: '%',
    KEY_AMPERSAND: '&',
    KEY_SINGLE_QUOTE: "'",
    KEY_OPEN_PAREN: '(',
    KEY_CLOSE_PAREN: ')',
    KEY_ASTERISK: '*',
    KEY_PLUS: '+',
    KEY_COMMA: ',',
    KEY_MINUS: '-',
    KEY_PERIOD: '.',
    KEY_SLASH: '/',
    KEY_COLON: ':',
    KEY_SEMICOLON: ';',
    KEY_LESS_THAN: '<',
    KEY_EQUAL: '=',
    KEY_GREATER_THAN: '>',
    KEY_QUESTION: '?',
    KEY_AT: '@',
    KEY_OPEN_BRACKET: '[',
    KEY_BACKSLASH: '\\',
    KEY_CLOSE_BRACKET: ']',
    KEY_CARET: '^',
    KEY_UNDERSCORE: '_',
    KEY_BACKTICK: '`',
    KEY_OPEN_BRACE: '{',
    KEY_VERTICAL_BAR: '|',
    KEY_CLOSE_BRACE: '}',
    KEY_TILDE: '~',
    
    # KEY_LEFT_WINDOWS: 'LEFT_WINDOWS',
    # KEY_RIGHT_WINDOWS: 'RIGHT_WINDOWS',
    # KEY_SELECT: 'SELECT',
    # KEY_NUMPAD_0: 'NUMPAD_0',
    # KEY_NUMPAD_1: 'NUMPAD_1',
    # KEY_NUMPAD_2: 'NUMPAD_2',
    # KEY_NUMPAD_3: 'NUMPAD_3',
    # KEY_NUMPAD_4: 'NUMPAD_4',
    # KEY_NUMPAD_5: 'NUMPAD_5',
    # KEY_NUMPAD_6: 'NUMPAD_6',
    # KEY_NUMPAD_7: 'NUMPAD_7',
    # KEY_NUMPAD_8: 'NUMPAD_8',
    # KEY_NUMPAD_9: 'NUMPAD_9',
    # KEY_NUMPAD_MULTIPLY: 'NUMPAD_MULTIPLY',
    # KEY_NUMPAD_ADD: 'NUMPAD_ADD',
    # KEY_NUMPAD_SUBTRACT: 'NUMPAD_SUBTRACT',
    # KEY_NUMPAD_DECIMAL: 'NUMPAD_DECIMAL',
    # KEY_NUMPAD_DIVIDE: 'NUMPAD_DIVIDE',
    KEY_F1: 'F1',
    KEY_F2: 'F2',
    KEY_F3: 'F3',
    KEY_F4: 'F4',
    KEY_F5: 'F5',
    KEY_F6: 'F6',
    KEY_F7: 'F7',
    KEY_F8: 'F8',
    KEY_F9: 'F9',
    KEY_F10: 'F10',
    KEY_F11: 'F11',
    KEY_F12: 'F12',
    # KEY_NUM_LOCK: 'NUM_LOCK',
    # KEY_SCROLL_LOCK: 'SCROLL_LOCK',
    KEY_SEMICOLON: ';',
    KEY_EQUAL: '=',
    KEY_COMMA: ',',
    KEY_MINUS: '-',
    KEY_PERIOD: '.',
    KEY_SLASH: '/',
    # KEY_BACK_QUOTE: 'BACK_QUOTE',
    KEY_OPEN_BRACKET: 'OPEN_BRACKET',
    # KEY_BACK_SLASH: 'BACK_SLASH',
    KEY_CLOSE_BRACKET: 'CLOSE_BRACKET',
    # KEY_QUOTE: 'QUOTE'
    
}
