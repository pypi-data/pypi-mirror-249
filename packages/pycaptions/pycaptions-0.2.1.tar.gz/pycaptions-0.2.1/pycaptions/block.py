import budoux
import textwrap
from collections import defaultdict
from .microTime import MicroTime as MT


class BlockType:
    CAPTION = 1
    COMMENT = 2
    STYLE = 3
    LAYOUT = 4
    METADATA = 5


class Block:
    """
    Represents a block of content in a multimedia file or document.

    Methods:
        getLines: Format text of specific language into multiple lines
        get: Get the text content of the block for a specific language.
        append: Append text to the block for a specific language.
        shift_time: Shift start and end times of the block by a specified duration.
        shift_start: Shift start time of the block by a specified duration.
        shif_end: Shift end time of the block by a specified duration.
        copy: Returns a copy of the current block.
        shift_time_us: Shift time of the block by microseconds.
        shift_start_us: Shift start time of the block by microseconds.
        shift_end_us: Shift end time of the block by microseconds.
        __getitem__: Retrieve the text of specific language.
        __setitem__: Set the text of specific language.
        __str__: Return a string representation of the block.
        __iadd__: In-place addition for the Block.
        __add__: Addition for the Blocks.
        __isub__: In-place subtraction for a specific language.
        __sub__: Subtraction for a specific language.
        __iter__: Iterator for iterating through the block languages.
        __next__: Iterator method returning a tuple of language and text.
    """
    def __init__(self, block_type: int, lang: str = "und", start_time: MT = None,
                 end_time: MT = None, text: str = "", **options):
        """
        Initialize a new instance of the Block class.

        Parameters:
        - block_type (int): The type of the block, represented as an integer, options in BlockType class
        - lang (str, optional): The language of the text in the block (default is "und" for undefined).
        - start_time (int, optional): The starting time of the block in microseconds (default is 0).
        - end_time (int, optional): The ending time of the block in microseconds (default is 0).
        - text (str, optional): The content of the block (default is an empty string).
        - **options: Additional keyword arguments for customization (e.g style, layout, ...).
        """
        self.block_type = block_type
        self.languages = defaultdict(str)
        if options.get("languages"):
            for i, j in options.get("languages").items():
                self.languages[i] = j
            del options["languages"]
        self.default_language = lang
        if text:
            self.languages[lang] = text.strip()
        self.start_time = start_time
        self.end_time = end_time
        self.options = options or {}

    def __getitem__(self, index: str):
        return self.languages[index]

    def __setitem__(self, index: str, value: str):
        self.languages[index] = value

    def __str__(self):
        temp = '\n'.join(f" {lang}: {text}" for lang, text in self.languages.items())
        return f"start: {self.start_time} end: {self.end_time}\n{temp}"

    def __iadd__(self, value):
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        for key, language in value:
            self.languages[key] = language
        return self

    def __add__(self, value):
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        out = Block(block_type=self.block_type, start_time=self.start_time,
                    end_time=self.end_time, lang=self.default_language, options=self.options)
        out.languages = self.languages.copy()
        for key, language, comment in value:
            out.languages[key] = language
        return out

    def __isub__(self, language: str):
        if language in self.languages:
            del self.languages[language]
        return self

    def __sub__(self, language: str):
        out = Block(block_type=self.block_type, start_time=self.start_time,
                    end_time=self.end_time, lang=self.default_language, options=self.options)
        out.languages = self.languages.copy()
        if language in out.languages:
            del out.languages[language]
        return out

    def __iter__(self):
        self._keys_iterator = iter(self.languages)
        return self

    def __next__(self):
        try:
            key = next(self._keys_iterator)
            return key, self.languages.get(key)
        except StopIteration:
            raise StopIteration

    def copy(self):
        return Block(self.block_type, self.default_language, self.start_time,
                     self.end_time, languages=self.languages, **self.options)

    def getLines(self, lang: str = "und", lines: int = 0) -> list[str]:
        """
        Format text of specific language into multiple lines.

        Args:
            lang (str, optional): Language code (default is "und" for undefined).
            lines (int, optional): The number of lines to format to. (default is 0 - autoformat).

        Returns:
            list[str]: A list of text lines.
        """
        text = self.get(lang)
        if lang == "ja":
            parser = budoux.load_default_japanese_parser()
            return parser.parse(text)
        elif lang in ["zh", "zh-CN", "zh-SG", "zh-Hans"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        elif lang in ["zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        else:
            return textwrap.wrap(text)

    def get(self, lang: str) -> str:
        return self.languages.get(lang)

    def append(self, text: str, lang: str = "und"):
        if not self.default_language:
            self.default_language = lang
        if lang not in ["ja", "zh", "zh-CN", "zh-SG", "zh-Hans",
                        "zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            if self.languages[lang]:
                self.languages[lang] += " " + text.strip()
            else:
                self.languages[lang] = text.strip()
        else:
            self.languages[lang] += text

    def shift_time_us(self, microseconds: int):
        self.start_time += microseconds
        self.end_time += microseconds

    def shift_time(self, time: MT):
        self.start_time += time
        self.end_time += time

    def shift_start_us(self, microseconds: int):
        self.start_time += microseconds

    def shift_start(self, time: MT):
        self.start_time += time

    def shift_end_us(self, microseconds: int):
        self.end_time += microseconds

    def shift_end(self, time: MT):
        self.end_time += time