class CrossTrackError:
    def __init__(self, frameWidth):
        self.frameWidth = frameWidth

    def __call__(self, lanes):
        ctes = []
            
        if lanes is not None:
            for lane in lanes:
                x = lane[0][0]
                ctes.append(self.frameWidth/2 - x)
                
        return ctes
