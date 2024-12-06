# sokoban_sfx.py
#   loading sound effects for Sokoban.
# Leslie Liu / leslieli / Section Q

# thanks to SubspaceAudio on OpenGameArt.org for the public domain 8-bit game sounds!
# https://opengameart.org/content/512-sound-effects-8-bit-style

from cmu_graphics import *

SFX_URL = {
    'cantMove' : {'sfx/cantMove1.wav','sfx/cantMove2.wav'},
    'moveIntoEmptyCell' : {'sfx/move1.wav', 'sfx/move2.wav'},
    'moveBox' : {'sfx/moveBox1.wav', 'sfx/moveBox2.wav'},
    'overTarget' : {'sfx/overTarget1.wav', 'sfx/overTarget2.wav'},
    'playerWins' : 'sfx/pWins.wav'
}

SFX = dict()
for sfxCategory in SFX_URL:
    for oneSfx in SFX_URL[sfxCategory]:
        SFX[sfxCategory] = Sound(oneSfx)

