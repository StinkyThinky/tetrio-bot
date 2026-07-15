# (tHeld ,tCurrent, b2bTA ,b2bTM,
# nb2bTA, nb2bTM, b2bt, nb2bt,
# clearedLines,
# b2bAS, nb2bAS,
# b2bTetris, nb2bTetris,
# comboLow ,comboMed, comboHigh,
# tripleTA, tripleTM,
# TSMove, TSBestMove,
# TS,
# PC,
# lost_b2b,
# iSlot,
# iSlotCount,
# tower,
# hole,
# blockade,
# messy1, messy2, messy3,
# largestDifference,
# highestPeak,
# heightMax,
# heightMediumM,
# heightMediumS,
# heightMin,
# discountTST) = [60, 60, 300, 100, 200, 50, 130, 70, 0, 80, 30,
#                 600, 400, 20, 20, 30, 300, 100, 80, 50, 200, 9999, 100,
#                20, 50, 50, 60, 25, 2, 5, 5, 10, 10, 5, 2, 5, 1, 500]

class Parameters:
    def __init__(self):
        self.params = [60, 60, 300, 100, 200, 50, 130, 70, 0, 80, 30, 600, 400, 20, 20, 30, 300, 100, 80, 50, 200, 9999, 100, 20, 50, 50, 60, 25, 2, 5, 5, 10, 10, 5, 2, 5, 1, 500]

    def __str__(self):
        return self.params

    def change(self, parameters):
        assert isinstance(parameters, str)
        self.params = parameters


parameter = Parameters()
