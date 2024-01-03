# PythonTermColor | Color






#Global Variables
Colors = {
    'red' : (200, 0, 0),
    'green' : (0, 200, 0),
    'blue': (0, 0, 200),
    'purple': (200, 0, 200),
    'yellow' : (200, 200, 0),
    'orange' : (200, 100, 0),

    'brightred' : (255, 0, 0),
    'brightgreen' : (0, 255, 0),
    'brightblue': (0, 0, 255),
    'brightpurple': (255, 0, 255),
    'brightyellow' : (255, 255, 0),
    'brightorange' : (255, 175, 0),

    'lightred' : (200, 100, 100),
    'lightgreen' : (100, 200, 100),
    'lightblue': (100, 100, 200),
    'lightpurple': (200, 100, 200),
    'lightyellow' : (200, 200, 100),
    'lightorange' : (200, 150, 100),

    'darkred' : (100, 0, 0),
    'darkgreen' : (0, 100, 0),
    'darkblue': (0, 0, 100),
    'darkpurple': (100, 0, 100),
    'darkyellow' : (100, 100, 0),
    'darkorange' : (100, 50, 0),
}

Decorations = {
    'bold' : '1',
    'italic' : '3',
    'underline' : '4',
    'inverted' : '7',
    'doubleunderline' : '21'
}






#Private Functions
def __isValidRGB(rgb: tuple) -> bool:
    if type(rgb) != tuple: raise ValueError('Argument rgb must be a tuple.')
    if len(rgb) < 3: raise ValueError('Argument rgb must contain all rgb values.')
    if len(rgb) > 3: raise ValueError('Argument rgb contains too many values to be a valid rgb value.')
    if any([True for i in rgb if not type(i) is int]): return False
    if any([True for i in rgb if i < 0 or i > 255]): return False
    return True



def __createColor(rgb: tuple) -> str:
    red = str(rgb[0])
    green = str(rgb[1])
    blue = str(rgb[2])

    return red + ';' + green + ';' + blue



def __constructEscapeString(textColor: str, backgroundColor: str, decorations: list) -> str:
    escapeString = '\033[38;2;' + textColor
    if backgroundColor: escapeString += ';48;2;' + backgroundColor
    for decoration in decorations: escapeString += ';' + decoration
    return escapeString + 'm'
    







#Public Functions
def showColorList() -> None:
    '''
    Prints off list of valid arguments for color.
    '''
    global Colors
    for color in Colors: print(color)



def showDecorationList() -> None:
    '''
    Prints off list of valid arguments for decoration.
    '''
    global Decorations
    for decoration in Decorations: print(decoration)



def printRGBColor(text: str, textRGB: tuple, backgroundRGB: tuple = (), decorations: list | str = [], end: str = '\n') -> None:
    '''
    Prints text in color from a given rgb format.\n
    text: str
     Text to print off.
    textRGB: tuple
     Tuple of rgb values to make text.
    backroundRGB: tuple
     Tuple of rgb values to make background.
    decorations: list | str
     List or string of decoration values to add to the text.
    end: str
     How the printed text should end.
    '''
    
    global Decorations

    if type(decorations) == str: decorations = [decorations]
    if not __isValidRGB(textRGB): raise ValueError('Argument textRGB contains an illegal value, all values must be between 0-255.')
    if len(backgroundRGB) > 0 and not __isValidRGB(backgroundRGB): raise ValueError('Argument backgroundRGB contains an illegal value, all values must be between 0-255.')
    if any([True for i in decorations if i not in Decorations]): raise ValueError('Argument decorations must contain valid decoration types from given list of Decorations.')
    
    textColor = __createColor(textRGB)
    if len(backgroundRGB) == 3: backgroundColor = __createColor(backgroundRGB)
    else: backgroundColor = ''
    decorations = [Decorations[decoration] for decoration in decorations]

    print(__constructEscapeString(textColor, backgroundColor, decorations), end = '')
    print(text, end = '')
    print('\033[0m', end = end)



def printColor(text: str, textColor: str, backgroundColor: str = None, decorations: list | str = [], end: str = '\n') -> None:
    '''
    Prints text in color from a given color.\n
    text: str
     Text to print off.
    textColor: str
     String of the color to make text.
    backgroundColor: str
     String of the color to make background.
    decorations: list | str
     List or string of decoration values to add to the text.
    end: str
     How the printed text should end.
    '''
    global Colors
    global Decorations

    if type(decorations) == str: decorations = [decorations]
    if textColor not in Colors: raise ValueError('Argument textColor must be a valid color from given list of Colors.')
    if not backgroundColor is None and backgroundColor not in Colors: raise ValueError('Argument backgroundColor must be a valid color from given list of Colors.')
    if any([True for i in decorations if i not in Decorations]): raise ValueError('Argument decorations must contain valid decoration types from given list of Decorations.')

    textColor = Colors[textColor]
    if backgroundColor is None: backgroundColor = ()
    else: backgroundColor = Colors[backgroundColor]

    printRGBColor(text, textColor, backgroundColor, decorations, end)