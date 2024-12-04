### sokoban_loader overflow code

 # check for colors

        # check for small amoutns of brown thatshould be empty cells

    # elif 'brown' in tally.keys() and tally['brown'] >= width*height*0.15: return 'w'
    # elif 'tan' in tally.keys(): return 'p' # is this order correct
    # elif len(tally) == 1: # either box or target
    # else:
        # check if box color count is greater than brown
        # for col,colFreq in tally.items():
        #     # print(f'in else, color is {col}')
        #     if col != 'brown': return col[0] if colFreq > 4000 else col[0].upper()
        #         # return col[0] if colFreq > ((width-m)*(height-m))*0.5 else col[0].upper()
        #     elif col == 'brown' and colFreq < width*height*0.5: return '-'

    #     # capitalize if more color than white
    #     otherColor = list(tally.keys()) # difference with mostColor
    #     pass
