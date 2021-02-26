from sif_splitting_service import *


class RealTimeSifExtractor:

    def __init__(self, sample_rate):
        self.sss = SifSplittingService(sample_rate)

    def extractSifs(self, signal):

        sifs, _ = self.sss.split(signal)

        return sifs
