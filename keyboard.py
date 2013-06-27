keyList = [
    [ 1, 1,"A"],
    [ 1, 1,"D"],
    [ 1, 3,"Down"],
    [ 1, 4,"Not"],
    [ 1, 5,"Delete"],
    [ 1, 6,"Up"],
    [ 1,10,"Left"],
    [ 1,11,"Insert"],
    [ 2, 7,"Right"],
    [ 2,12,"0"],
    [ 2,14,"8",],
    [ 3, 7,"Text"],
    [ 3,12,"6"],
    [ 4, 7,"Row",],
    [ 4, 9,"Cont"],
    [ 4, 9,"List"],
    [ 4,12,"1"],
    [ 4,14,"9"],
    [ 5, 7,"Format"],
    [ 5,12,"4"],
    [ 5,14,"C"],
    [ 5,14,"E",],
    [ 6, 7,"Mode"],
    [ 6,12,"5"],
    [ 7,11,"Blank"],
    [ 7,13,"Stop"],
    [10,12,"7"],
    [10,14,"F"],
    [11,14,"B"],
    [12,11,"3"],
    [12,13,"2"]
    ]

# for 3-tupple in the list[n]=[a,b,key]
# set b-input
# set a-output
# set a-high
# read b (high = 1)
# set a-low, set a-input
# if old[n] = 0 and b = 1, then send "key" (pressed)
# if old[n] = 1 and b = 0, then send "key" (released)
# old[n] = b
