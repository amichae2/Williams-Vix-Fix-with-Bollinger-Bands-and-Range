import math

import pandas


class Custom_Indicators:

    def get_wvf(self, source, length, lows):

        WVFs = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None]

        working_closes = []
        count = 0
        highest_closes = []
        lowest_closes = []
        for close in source:
            count += 1
            working_closes.append(close)
            if count > (length - 1):
                highest_closes.append(max(working_closes))
                lowest_closes.append(min(working_closes))
                working_closes.remove(working_closes[0])
                count -= 1

        for i in range(len(highest_closes)):
            WVFs.append(((highest_closes[i] - lows[i+21]) / highest_closes[i]) * 100)

        return WVFs

    def get_sma(self, source, length):

        SMAs = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None]

        SUM = 0
        the_closes = []
        count = 0
        for close in source:
            if close is not None:
                count += 1
                the_closes.append(close)
                if count > (length - 1):
                    for i in the_closes:
                        SUM += (i / length)
                    count -= 1
                    SMAs.append(SUM)
                    the_closes.remove(the_closes[0])
                    SUM = 0

        return SMAs

    def get_sum(self, fst, snd):

        EPS = 1e-10
        res = fst + snd
        if abs(res) <= EPS:
            res = 0
        else:
            if not abs(res) <= 1e-4:
                res = res
            else:
                res = 15

        return res

    def sma_std(self, source, length):

        STDs = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None]

        SMAs = self.get_sma(source=source, length=length)
        sum_of_square_deviations = 0
        count = 0
        the_sums = []
        for i in range(len(SMAs)):
            if SMAs[i] is not None:
                count += 1
                the_sum = self.get_sum(fst=source[i], snd=-SMAs[i])
                the_sums.append(the_sum)
                if count > (length - 1):
                    for sum in the_sums:
                        sum_of_square_deviations += (sum * sum)
                    count -= 1
                    stdev = math.sqrt(sum_of_square_deviations / length)
                    STDs.append(stdev)
                    the_sums.remove(the_sums[0])
                    sum_of_square_deviations = 0

        return {'STDs': STDs, 'SMAs': SMAs}

    def mult_sdev(self, source, mult):

        new_STDs = []
        for i in source.get('STDs'):
            if i is None:
                new_STDs.append(None)
            else:
                new_STDs.append(i * mult)

        return new_STDs

    def BB_bands(self, SMAs, STDs):

        lower = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None]
        upper = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                 None, None]
        for idx, i in enumerate(STDs):
            if STDs[idx] is not None:
                lower.append(SMAs.get('SMAs')[idx] - STDs[idx])
                upper.append(SMAs.get('SMAs')[idx] + STDs[idx])

        return {'low BB': lower, 'up BB': upper}

    def get_high_and_low(self, source, length, high_pe, low_pe):

        range_high = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                      None, None,
                      None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                      None,
                      None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                      None, None, None]
        range_low = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                     None, None,
                     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                     None,
                     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                     None, None, None]

        working_closes = []
        count = 0
        for wvf in source:
            if wvf is not None:
                count += 1
                working_closes.append(wvf)
                if count > (length - 1):
                    range_high.append(max(working_closes) * high_pe)
                    range_low.append(min(working_closes) * low_pe)
                    working_closes.remove(working_closes[0])
                    count -= 1

        return {'high ranges': range_high, 'low ranges': range_low}


    def Williams_VIX_Fix_BB_STD(self, closes):

        stock_pd = closes
        add_pd = {'WVF': None, 'STD': None, 'BB Up': None, 'BB Low': None, 'WVF SMA': None, 'High Range': None, 'Low Range': None}

        WVF_lookback_p_STD = 22
        BB_length = 20
        BB_STD_up = 2
        lookback_p_high_pe = 50
        highest_pe = .85
        lowest_pe = 1.01

        WVFs = self.get_wvf(source=stock_pd['Close'].to_list(), length=WVF_lookback_p_STD, lows=stock_pd['Low'].to_list())
        add_pd['WVF'] = WVFs

        STDs_and_SMAs = self.sma_std(source=WVFs, length=BB_length)
        add_pd['WVF SMA'] = STDs_and_SMAs.get('SMAs')

        mult_stdev = self.mult_sdev(source=STDs_and_SMAs, mult=BB_STD_up)
        add_pd['STD'] = mult_stdev

        low_and_up_bands = self.BB_bands(SMAs=STDs_and_SMAs, STDs=mult_stdev)
        add_pd['BB Up'] = low_and_up_bands.get('up BB')
        add_pd['BB Low'] = low_and_up_bands.get('low BB')

        high_and_low_range = self.get_high_and_low(source=WVFs, length=lookback_p_high_pe, high_pe=highest_pe,
                                                   low_pe=lowest_pe)
        add_pd['High Range'] = high_and_low_range.get('high ranges')
        add_pd['Low Range'] = high_and_low_range.get('low ranges')

        new_df = pandas.DataFrame(add_pd, index=stock_pd.index)
        stock_pd = stock_pd.join(new_df)

        return stock_pd

