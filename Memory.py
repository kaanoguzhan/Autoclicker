class Diffmemory:
    results = {}
    step = 0

    def __init__(self, start, end, step):
        self.results = {}
        self.step = step
        current = start
        while current < end:
            self.results[current] = 0
            current = current + step

    def add(self, diff):
        place = 0
        if diff < self.step:
            self.results[place * self.step] = self.results.get(place * self.step, 0) + 1
        while diff > 0:
            place += 1
            diff -= self.step
            if diff < 0:
                self.results[place * self.step] = self.results.get(place * self.step, 0) + 1

    def getValues(self):
        return sorted(self.results.iteritems())


class ClickMemory:
    totalClick = 0
    minDelayBefore = float("inf")
    minDelayBetween = float("inf")
    maxDelayBefore = -float("inf")
    maxDelayBetween = -float("inf")
    avgDelayBefore = 0
    avgDelayBetween = 0

    def __init__(self):
        self.totalClick = 0
        self.minDelayBefore = float("inf")
        self.minDelayBetween = float("inf")
        self.maxDelayBefore = -float("inf")
        self.maxDelayBetween = -float("inf")

    def addLeftClick(self, delayBefore, delayBetween):
        # print "Randoms: ", delayBefore, " - ", delayBetween
        # Average
        self.avgDelayBefore *= self.totalClick
        self.avgDelayBetween *= self.totalClick

        self.avgDelayBefore += delayBefore
        self.avgDelayBetween += delayBetween

        self.totalClick += 1

        self.avgDelayBefore /= self.totalClick
        self.avgDelayBetween /= self.totalClick

        # Min
        if delayBefore < self.minDelayBefore:
            self.minDelayBefore = delayBefore
        if delayBetween < self.minDelayBetween:
            self.minDelayBetween = delayBetween

        # Max
        if delayBefore > self.maxDelayBefore:
            self.maxDelayBefore = delayBefore
        if delayBetween > self.maxDelayBetween:
            self.maxDelayBetween = delayBetween

    def clickOverview(self):
        text = ""
        text += "Total Clicks: " + str(self.totalClick) + "\n" + "\n"
        text += "Before" + "\n"
        text += "Min: " + str(self.minDelayBefore)[:-7] + "\tAvg: " + str(self.avgDelayBefore)[:-7] + \
            "\tMax: " + str(self.maxDelayBefore)[:-7] + "\n" + "\n"
        text += "Between" + "\n"
        text += "Min: " + str(self.minDelayBetween)[:-7] + "\tAvg: " + str(self.avgDelayBetween)[:-7] + \
            "\tMax: " + str(self.maxDelayBetween)[:-7] + "\n"
        return text
