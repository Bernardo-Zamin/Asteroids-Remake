

from OpenGL.GL import glColor3f

# Lista de valores RBB para cores
# Valores obtidos em https://community.khronos.org/t/color-tables/22518/5
# 
#
#

# Define colors as a list
colors = [
(0,0,0),	#	Black
(1,1,1),	#	White
(0.5,0.5,0.5),	#	Gray
(1,1,0),	#	Yellow
(1,0,0),	#	Red
(0,1,0),	#	Green
(0,0,1),	#	Blue
(0.439216,0.858824,0.576471),	#	Aquamarine
(0.62352,0.372549,0.623529),	#	BlueViolet
(0.647059,0.164706,0.164706),	#	Brown
(0.372549,0.623529,0.623529),	#	CadetBlue
(1.0,0.498039,0.0),	#	Coral
(0.258824,0.258824,0.435294),	#	CornflowerBlue
(0.184314,0.309804,0.184314),	#	DarkGreen
(0.309804,0.309804,0.184314),	#	DarkOliveGreen
(0.6,0.196078,0.8),	#	DarkOrchid
(0.419608,0.137255,0.556863),	#	DarkSlateBlue
(0.184314,0.309804,0.309804),	#	DarkSlateGray
(0.184314,0.309804,0.309804),	#	DarkSlateGrey
(0.439216,0.576471,0.858824),	#	DarkTurquoise
(0.556863,0.137255,0.137255),	#	Firebrick
(0.137255,0.556863,0.137255),	#	ForestGreen
(0.8,0.498039,0.196078),	#	Gold
(0.858824,0.858824,0.439216),	#	Goldenrod
(0.576471,0.858824,0.439216),	#	GreenYellow
(0.309804,0.184314,0.184314),	#	IndianRed
(0.623529,0.623529,0.372549),	#	Khaki
(0.74902,0.847059,0.847059),	#	LightBlue
(0.560784,0.560784,0.737255),	#	LightSteelBlue
(0.196078,0.8,0.196078),	#	LimeGreen
(0.556863,0.137255,0.419608),	#	Maroon
(0.196078,0.8,0.6),	#	MediumAquamarine
(0.196078,0.196078,0.8),	#	MediumBlue
(0.419608,0.556863,0.137255),	#	MediumForestGreen
(0.917647,0.917647,0.678431),	#	MediumGoldenrod
(0.576471,0.439216,0.858824),	#	MediumOrchid
(0.258824,0.435294,0.258824),	#	MediumSeaGreen
(0.498039,1.0,),	#	MediumSlateBlue
(0.498039,1.0,),	#	MediumSpringGreen
(0.439216,0.858824,0.858824),	#	MediumTurquoise
(0.858824,0.439216,0.576471),	#	MediumVioletRed
(0.184314,0.184314,0.309804),	#	MidnightBlue
(0.137255,0.137255,0.556863),	#	Navy
(0.137255,0.137255,0.556863),	#	NavyBlue
(1,0.5,0.0),	#	Orange
(1.0,0.25,),	#	OrangeRed
(0.858824,0.439216,0.858824),	#	Orchid
(0.560784,0.737255,0.560784),	#	PaleGreen
(0.737255,0.560784,0.560784),	#	Pink
(0.917647,0.678431,0.917647),	#	Plum
(0.435294,0.258824,0.258824),	#	Salmon
(0.137255,0.556863,0.419608),	#	SeaGreen
(0.556863,0.419608,0.137255),	#	Sienna
(0.196078,0.6,0.8),	#	SkyBlue
(0.498039,1.0,),	#	SlateBlue
(1.0,0.498039,),	#	SpringGreen
(0.137255,0.419608,0.556863),	#	SteelBlue
(0.858824,0.576471,0.439216),	#	Tan
(0.847059,0.74902,0.847059),	#	Thistle
(0.678431,0.917647,0.917647),	#	Turquoise
(0.309804,0.184314,0.309804),	#	Violet
(0.8,0.196078,0.6),	#	VioletRed
(0.847059,0.847059,0.74902),	#	Wheat
(0.6,0.8,0.196078),	#	YellowGreen
(0.22,0.69,0.87),	#	SummerSky
(0.35,0.35,0.67),	#	RichBlue
(0.71,0.65,0.26),	#	Brass
(0.72,0.45,0.20),	#	Copper
(0.55,0.47,0.14),	#	Bronze
(0.65,0.49,0.24),	#	Bronze2
(0.90,0.91,0.98),	#	Silver
(0.85,0.85,0.10),	#	BrightGold
(0.81,0.71,0.23),	#	OldGold
(0.82,0.57,0.46),	#	Feldspar
(0.85,0.85,0.95),	#	Quartz
(1.00,0.43,0.78),	#	NeonPink
(0.53,0.12,0.47),	#	DarkPurple
(0.30,0.30,1.00),	#	NeonBlue
(0.85,0.53,0.10),	#	CoolCopper
(0.89,0.47,0.20),	#	MandarinOrange
(0.91,0.76,0.65),	#	LightWood
(0.65,0.50,0.39),	#	MediumWood
(0.52,0.37,0.26),	#	DarkWood
(1.00,0.11,0.68),	#	SpicyPink
(0.42,0.26,0.15),	#	SemiSweetChoc
(0.36,0.20,0.09),	#	BakersChoc
(0.96,0.80,0.69),	#	Flesh
(0.92,0.78,0.62),	#	NewTan
(0.00,0.00,0.61),	#	NewMidnightBlue
(0.35,0.16,0.14),	#	VeryDarkBrown
(0.36,0.25,0.20),	#	DarkBrown
(0.59,0.41,0.31),	#	DarkTan
(0.32,0.49,0.46),	#	GreenCopper
(0.29,0.46,0.43),	#	DkGreenCopper
(0.52,0.39,0.39),	#	DustyRose
(0.13,0.37,0.31),	#	HuntersGreen
(0.55,0.09,0.09),	#	Scarlet
(0.73,0.16,0.96),	#	Med_Purple
(0.87,0.58,0.98),	#	Light_Purple
(0.94,0.81,0.99)	#	Very_Light_Purple

]

# Define color constants
Black	=	0
White	=	1
Gray	=	2
Yellow	=	3
Red	=	4
Green	=	5
Blue	=	6
Aquamarine	=	7
BlueViolet	=	8
Brown	=	9
CadetBlue	=	10
Coral	=	11
CornflowerBlue	=	12
DarkGreen	=	13
DarkOliveGreen	=	14
DarkOrchid	=	15
DarkSlateBlue	=	16
DarkSlateGray	=	17
DarkSlateGrey	=	18
DarkTurquoise	=	19
Firebrick	=	20
ForestGreen	=	21
Gold	=	22
Goldenrod	=	23
GreenYellow	=	24
IndianRed	=	25
Khaki	=	26
LightBlue	=	27
LightSteelBlue	=	28
LimeGreen	=	29
Maroon	=	30
MediumAquamarine	=	31
MediumBlue	=	32
MediumForestGreen	=	33
MediumGoldenrod	=	34
MediumOrchid	=	35
MediumSeaGreen	=	36
MediumSlateBlue	=	37
MediumSpringGreen	=	38
MediumTurquoise	=	39
MediumVioletRed	=	40
MidnightBlue	=	41
Navy	=	42
NavyBlue	=	43
Orange	=	44
OrangeRed	=	45
Orchid	=	46
PaleGreen	=	47
Pink	=	48
Plum	=	49
Salmon	=	50
SeaGreen	=	51
Sienna	=	52
SkyBlue	=	53
SlateBlue	=	54
SpringGreen	=	55
SteelBlue	=	56
Tan	=	57
Thistle	=	58
Turquoise	=	59
Violet	=	60
VioletRed	=	61
Wheat	=	62
YellowGreen	=	63
SummerSky	=	64
RichBlue	=	65
Brass	=	66
Copper	=	67
Bronze	=	68
Bronze2	=	69
Silver	=	70
BrightGold	=	71
OldGold	=	72
Feldspar	=	73
Quartz	=	74
NeonPink	=	75
DarkPurple	=	76
NeonBlue	=	77
CoolCopper	=	78
MandarinOrange	=	79
LightWood	=	80
MediumWood	=	81
DarkWood	=	82
SpicyPink	=	83
SemiSweetChoc	=	84
BakersChoc	=	85
Flesh	=	86
NewTan	=	87
NewMidnightBlue	=	88
VeryDarkBrown	=	89
DarkBrown	=	90
DarkTan	=	91
GreenCopper	=	92

def SetColor (cor):
    pass
    # print("SetColor")
    # print (*colors[cor])
    r, g, b = colors[cor]
    #glColor3f(r, g, b)
    glColor3f(*colors[cor])
    

