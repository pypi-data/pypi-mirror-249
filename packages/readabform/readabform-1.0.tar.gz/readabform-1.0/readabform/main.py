from bestErrors import OutOfRangeError, InvalidTypeError
from typing import overload, Union, Any


class abbrevs:
    def __init__(self) -> None:
        self.abbrs = [
            "",
            "K",
            "M",
            "B",
            "T",
            "Qa",
            "Qt",
            "Sx",
            "Sp",
            "Oc",
            "No",
            "Dc",
            "UDc",
            "DDc",
            "TDc",
            "QaDc",
            "QiDc",
            "SxDc",
            "SpDc",
            "OcDc",
            "NmDc",
            "Vg",
            "UVg",
            "DVg",
            "TVg",
            "QaVg",
            "QiVg",
            "SxVg",
            "SpVg",
            "OcVg",
            "NmVg",
            "Tg",
            "UTg",
            "DTg",
            "TTg",
            "QaTg",
            "QiTg",
            "SxTg",
            "SpTg",
            "OcTg",
            "NmTg",
            "Qa",
            "UQa",
            "DQa",
            "TQa",
            "QaQa",
            "QiQa",
            "SxQa",
            "SpQa",
            "OcQa",
            "NoQa",
            "Qi",
            "UQi",
            "DQi",
            "TQi",
            "QaQi",
            "QiQi",
            "SxQi",
            "SpQi",
            "OcQi",
            "NoQi",
            "Se",
            "USe",
            "DSe",
            "TSe",
            "QaSe",
            "QiSe",
            "SxSe",
            "SpSe",
            "OcSe",
            "NoSe",
            "St",
            "USt",
        ]


class readabform:
    def __init__(self, text: int | float | str) -> None:
        self.text = text
        self.abbrs = [
            "",
            "K",
            "M",
            "B",
            "T",
            "Qa",
            "Qt",
            "Sx",
            "Sp",
            "Oc",
            "No",
            "Dc",
            "UDc",
            "DDc",
            "TDc",
            "QaDc",
            "QiDc",
            "SxDc",
            "SpDc",
            "OcDc",
            "NmDc",
            "Vg",
            "UVg",
            "DVg",
            "TVg",
            "QaVg",
            "QiVg",
            "SxVg",
            "SpVg",
            "OcVg",
            "NmVg",
            "Tg",
            "UTg",
            "DTg",
            "TTg",
            "QaTg",
            "QiTg",
            "SxTg",
            "SpTg",
            "OcTg",
            "NmTg",
            "Qa",
            "UQa",
            "DQa",
            "TQa",
            "QaQa",
            "QiQa",
            "SxQa",
            "SpQa",
            "OcQa",
            "NoQa",
            "Qi",
            "UQi",
            "DQi",
            "TQi",
            "QaQi",
            "QiQi",
            "SxQi",
            "SpQi",
            "OcQi",
            "NoQi",
            "Se",
            "USe",
            "DSe",
            "TSe",
            "QaSe",
            "QiSe",
            "SxSe",
            "SpSe",
            "OcSe",
            "NoSe",
            "St",
            "USt",
        ]

    def form(self) -> int | float | str:
        if isinstance(self.text, (int, float)):
            test_num = self.text
            try:
                self.text = float("{:.3g}".format(self.text))
            except Exception as e:
                print(e)

            magnitude = 0

            while abs(self.text) >= 1000:
                magnitude += 1
                self.text /= 1000.0

            try:
                abbr = self.abbrs[magnitude]
            except Exception:
                raise OutOfRangeError(message="{} is too big! 🤯".format(test_num))

            return "{}{}".format("{:f}".format(self.text).rstrip("0").rstrip("."), abbr)
        elif isinstance(self.text, str):
            try:
                numeric_part = float(self.text[:-1])
            except Exception as e:
                raise InvalidTypeError(e)
            abbr = self.text[-1]

            if abbr in self.abbrs:
                factor = 10 ** ((self.abbrs.index(abbr) + 1) * 3)
                return int(numeric_part * factor)
            else:
                raise OutOfRangeError(
                    message="The suffix " + str(abbr) + " is not supported or found."
                )
        else:
            raise InvalidTypeError("Invalid type: {}".format(type(self.text)))

    def __str__(self) -> str:
        return self.text


def form(text: int | float | str) -> readabform:
    return readabform(text=text)


Abbrevs: abbrevs = abbrevs()

abbreviations = Abbrevs.abbrs
abbrs = Abbrevs.abbrs


@overload
def formm(num: float) -> str:
    ...


@overload
def formm(readabform: str) -> int | float:
    ...


def formm(arg: Union[int, float, str]) -> Union[str, int, float]:
    if isinstance(arg, (int, float)):
        if type(arg) not in [int, float]:
            raise InvalidTypeError("Invalid type: {}".format(type(arg)))
        else:
            test_num = arg
            arg = float("{:.3g}".format(arg))
            magnitude = 0

            while abs(arg) >= 1000:
                magnitude += 1
                arg /= 1000.0

            try:
                abbr = abbrs[magnitude]
            except Exception:
                raise OutOfRangeError(message="{} is too big! 🤯".format(test_num))

            return "{}{}".format("{:f}".format(arg).rstrip("0").rstrip("."), abbr)
    elif isinstance(arg, str):
        if type(arg) == str:
            numeric_part = float(arg[:-1])
            abbr = arg[-1]

            if abbr in abbrs:
                factor = 10 ** (abbrs.index(abbr) * 3)
                return int(numeric_part * factor)
            else:
                raise OutOfRangeError(
                    message="The suffix " + str(abbr) + " is not supported or found."
                )
        else:
            raise InvalidTypeError("Invalid type: {}".format(type(arg)))
    else:
        raise InvalidTypeError("Invalid type: {}".format(type(arg)))
