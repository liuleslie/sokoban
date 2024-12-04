'''


file path splitting
set level
pickling: if os.path exists at file path, then read pickle
else write pickle




'''




#######

L=[['w', 'w', 'w', 'w', 'w', 'w'],
 ['w', 'B', 'G', 'p', 'R', 'w'],
 ['w', '-', '-', 'r', '-', 'w'],
 ['w', 'w', 'g', 'w', 'w', 'w'],
 ['w', '-', '-', 'b', '-', 'w'],
 ['w', '-', '-', '-', '-', 'w'],
 ['w', '-', '-', '-', '-', 'w'],
 ['w', 'w', 'w', 'w', 'w', 'w']]

M=[['w', 'w', 'w', 'w', 'w', 'w'],
 ['w', 'B', 'G', 'p', 'R', 'w'],
 ['w', '-', '-', 'r', '-', 'w'],
 ['w', 'w', 'p', 'w', 'w', 'w'],
 ['w', '-', '-', 'b', '-', 'w'],
 ['w', '-', '-', '-', '-', 'w'],
 ['w', '-', '-', '-', '-', 'w'],
 ['w', 'w', 'w', 'w', 'w', 'w']]

print(L==M)

for i in range(len(L)):
    for j in range(len(L[0])):
        if L[i][j] != M[i][j]:
            print(f'not matching at {i},{j}')


'''

    # if True:
    #     mostFreqColor,colorFreq = getMostFrequentColor(tally)
    #     if mostFreqColor == 'brown' and colorFreq > 365: return 'w' # wall
    #     elif 'tan' in tally.keys(): return 'p' # player
    #     else:
    #         # check frequencies, capitalize accordingly
    #         if len(tally) == 1:
    #             if 'brown' in tally.keys(): return '-'
    #             elif colorFreq < 365: return '-'
    #         return mostFreqColor[0] if colorFreq > 4000 else mostFreqColor[0].upper()
    

'''