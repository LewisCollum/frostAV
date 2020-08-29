def fromLines(laneLines):
    state = 'NoLane'
    if laneLines.left and laneLines.right:
        state = 'Lane'
    elif laneLines.left:
        state = 'LeftOnly'
    elif laneLines.right:
        state = 'RightOnly'
    return state        
        
        
