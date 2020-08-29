class WhiteBalancer:
    def __call__(self, frame):
        balanced_img = numpy.zeros_like(frame) #Initialize final image

        for i in range(3): #i stands for the channel index 
            hist, bins = numpy.histogram(frame[..., i].ravel(), 256, (0, 256))
            bmin = numpy.min(numpy.where(hist>(hist.sum()*0.0005)))
            bmax = numpy.max(numpy.where(hist>(hist.sum()*0.0005)))
            balanced_img[...,i] = numpy.clip(frame[...,i], bmin, bmax)
            balanced_img[...,i] = (balanced_img[...,i]-bmin) / (bmax - bmin) * 255
            
        return balanced_img
