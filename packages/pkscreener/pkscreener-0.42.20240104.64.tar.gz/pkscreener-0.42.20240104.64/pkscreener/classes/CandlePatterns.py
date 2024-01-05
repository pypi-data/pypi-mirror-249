"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

from PKDevTools.classes.ColorText import colorText

from pkscreener.classes.Pktalib import pktalib


class CandlePatterns:
    reversalPatternsBullish = [
        "Morning Star",
        "Morning Doji Star",
        "3 Inside Up",
        "Hammer",
        "3 White Soldiers",
        "Bullish Engulfing",
        "Dragonfly Doji",
        "Supply Drought",
        "Demand Rise",
    ]
    reversalPatternsBearish = [
        "Evening Star",
        "Evening Doji Star",
        "3 Inside Down",
        "Inverted Hammer",
        "Hanging Man",
        "3 Black Crows",
        "Bearish Engulfing",
        "Shooting Star",
        "Gravestone Doji",
    ]

    def __init__(self):
        pass

    # Find candle-stick patterns
    # Arrange if statements with max priority from top to bottom
    def findPattern(self, data, dict, saveDict):
        data = data.head(4)
        data = data[::-1]
        # Only 'doji' and 'inside' is internally implemented by pandas_ta.
        # Otherwise, for the rest of the candle patterns, they also need
        # TA-Lib.
        check = pktalib.CDLDOJI(data["Open"], data["High"], data["Low"], data["Close"])
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = colorText.BOLD + "Doji" + colorText.END
            saveDict["Pattern"] = "Doji"
            return True

        check = pktalib.CDLMORNINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "Morning Star" + colorText.END
            )
            saveDict["Pattern"] = "Morning Star"
            return True

        check = pktalib.CDLMORNINGDOJISTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "Morning Doji Star" + colorText.END
            )
            saveDict["Pattern"] = "Morning Doji Star"
            return True

        check = pktalib.CDLEVENINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "Evening Star" + colorText.END
            )
            saveDict["Pattern"] = "Evening Star"
            return True

        check = pktalib.CDLEVENINGDOJISTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "Evening Doji Star" + colorText.END
            )
            saveDict["Pattern"] = "Evening Doji Star"
            return True

        check = pktalib.CDLLADDERBOTTOM(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.GREEN + "Ladder Bottom" + colorText.END
                )
                saveDict["Pattern"] = "Bullish Ladder Bottom"
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "Ladder Bottom" + colorText.END
                )
                saveDict["Pattern"] = "Bearish Ladder Bottom"
            return True

        check = pktalib.CDL3LINESTRIKE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.GREEN + "3 Line Strike" + colorText.END
                )
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "3 Line Strike" + colorText.END
                )
            saveDict["Pattern"] = "3 Line Strike"
            return True

        check = pktalib.CDL3BLACKCROWS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "3 Black Crows" + colorText.END
            )
            saveDict["Pattern"] = "3 Black Crows"
            return True

        check = pktalib.CDL3INSIDE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.GREEN + "3 Outside Up" + colorText.END
                )
                saveDict["Pattern"] = "3 Inside Up"
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "3 Outside Down" + colorText.END
                )
                saveDict["Pattern"] = "3 Inside Down"
            return True

        check = pktalib.CDL3OUTSIDE(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.GREEN + "3 Outside Up" + colorText.END
                )
                saveDict["Pattern"] = "3 Outside Up"
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "3 Outside Down" + colorText.END
                )
                saveDict["Pattern"] = "3 Outside Down"
            return True

        check = pktalib.CDL3WHITESOLDIERS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "3 White Soldiers" + colorText.END
            )
            saveDict["Pattern"] = "3 White Soldiers"
            return True

        check = pktalib.CDLHARAMI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.GREEN + "Bullish Harami" + colorText.END
                )
                saveDict["Pattern"] = "Bullish Harami"
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "Bearish Harami" + colorText.END
                )
                saveDict["Pattern"] = "Bearish Harami"
            return True

        check = pktalib.CDLHARAMICROSS(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD
                    + colorText.GREEN
                    + "Bullish Harami Cross"
                    + colorText.END
                )
                saveDict["Pattern"] = "Bullish Harami Cross"
            else:
                dict["Pattern"] = (
                    colorText.BOLD
                    + colorText.FAIL
                    + "Bearish Harami Cross"
                    + colorText.END
                )
                saveDict["Pattern"] = "Bearish Harami Cross"
            return True

        check = pktalib.CDLMARUBOZU(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD
                    + colorText.GREEN
                    + "Bullish Marubozu"
                    + colorText.END
                )
                saveDict["Pattern"] = "Bullish Marubozu"
            else:
                dict["Pattern"] = (
                    colorText.BOLD + colorText.FAIL + "Bearish Marubozu" + colorText.END
                )
                saveDict["Pattern"] = "Bearish Marubozu"
            return True

        check = pktalib.CDLHANGINGMAN(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "Hanging Man" + colorText.END
            )
            saveDict["Pattern"] = "Hanging Man"
            return True

        check = pktalib.CDLHAMMER(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "Hammer" + colorText.END
            )
            saveDict["Pattern"] = "Hammer"
            return True

        check = pktalib.CDLINVERTEDHAMMER(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "Inverted Hammer" + colorText.END
            )
            saveDict["Pattern"] = "Inverted Hammer"
            return True

        check = pktalib.CDLSHOOTINGSTAR(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "Shooting Star" + colorText.END
            )
            saveDict["Pattern"] = "Shooting Star"
            return True

        check = pktalib.CDLDRAGONFLYDOJI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.GREEN + "Dragonfly Doji" + colorText.END
            )
            saveDict["Pattern"] = "Dragonfly Doji"
            return True

        check = pktalib.CDLGRAVESTONEDOJI(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            dict["Pattern"] = (
                colorText.BOLD + colorText.FAIL + "Gravestone Doji" + colorText.END
            )
            saveDict["Pattern"] = "Gravestone Doji"
            return True

        check = pktalib.CDLENGULFING(
            data["Open"], data["High"], data["Low"], data["Close"]
        )
        if check is not None and check.tail(1).item() != 0:
            if check.tail(1).item() > 0:
                dict["Pattern"] = (
                    colorText.BOLD
                    + colorText.GREEN
                    + "Bullish Engulfing"
                    + colorText.END
                )
                saveDict["Pattern"] = "Bullish Engulfing"
            else:
                dict["Pattern"] = (
                    colorText.BOLD
                    + colorText.FAIL
                    + "Bearish Engulfing"
                    + colorText.END
                )
                saveDict["Pattern"] = "Bearish Engulfing"
            return True

        dict["Pattern"] = ""
        saveDict["Pattern"] = ""
        return False
