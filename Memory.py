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

    def sorted_values(self):
        return sorted(self.results.items())


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

    def add_leftclick(self, delay_before, delay_between):
        # print "Randoms: ", delayBefore, " - ", delayBetween
        # Average
        self.avgDelayBefore *= self.totalClick
        self.avgDelayBetween *= self.totalClick

        self.avgDelayBefore += delay_before
        self.avgDelayBetween += delay_between

        self.totalClick += 1

        self.avgDelayBefore /= self.totalClick
        self.avgDelayBetween /= self.totalClick

        # Min
        if delay_before < self.minDelayBefore:
            self.minDelayBefore = delay_before
        if delay_between < self.minDelayBetween:
            self.minDelayBetween = delay_between

        # Max
        if delay_before > self.maxDelayBefore:
            self.maxDelayBefore = delay_before
        if delay_between > self.maxDelayBetween:
            self.maxDelayBetween = delay_between

    def overview_text(self):
        text = ""
        text += "Total Clicks: " + str(self.totalClick) + "\n" + "\n"
        text += "Before" + "\n"
        text += "Min: " + str(self.minDelayBefore)[:-7] + "\tAvg: " + str(self.avgDelayBefore)[:-7] + \
            "\tMax: " + str(self.maxDelayBefore)[:-7] + "\n" + "\n"
        text += "Between" + "\n"
        text += "Min: " + str(self.minDelayBetween)[:-7] + "\tAvg: " + str(self.avgDelayBetween)[:-7] + \
            "\tMax: " + str(self.maxDelayBetween)[:-7] + "\n"
        return text
