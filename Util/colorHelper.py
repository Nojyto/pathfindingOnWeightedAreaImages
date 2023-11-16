class msPaintColors:
    black         = (  0,   0,   0)
    white         = (255, 255, 255)
    gray          = (127, 127, 127)
    silver        = (195, 195, 195)
    darkred       = (136,   0,  21)
    peru          = (185, 122,  87)
    crimson       = (237,  28,  36)
    lightpink     = (255, 174, 201)
    coral         = (255, 127,  39)
    gold          = (255, 201,  14)
    yellow        = (255, 242,   0)
    palegoldenrod = (239, 228, 176)
    seagreen      = ( 34, 177,  76)
    greenyellow   = (181, 230,  29)
    deepskyblue   = (  0, 162, 232)
    lightblue     = (153, 217, 234)
    royalblue     = ( 63,  72, 204)
    cadetblue     = (112, 146, 190)
    darkorchid    = (163,  73, 164)
    thistle       = (200, 191, 231)
    
    
START_COLOR = msPaintColors.seagreen
PATH_COLOR = msPaintColors.black
VISITED_COLOR = msPaintColors.silver
END_COLOR = msPaintColors.crimson
COLOR_TO_WEIGHT_LOOKUP = {
    msPaintColors.peru : 1,
    msPaintColors.royalblue: 2,
    msPaintColors.gray: 200
}


def scaleColorValue(rgb, k):
    r, g, b = rgb
    return (r * k, g * k, b * k)