import json
import io
import os
from langcodes import standardize_tag, tag_is_valid
from .block import Block
from .microTime import MicroTime as MT


class FileExtensions:
    SAMI = ".sami"
    SRT = ".srt"
    SUB = ".sub"
    TTML = ".ttml"
    VTT = ".vtt"


class CaptionsFormat:
    """
    Represents a format for handling captions in a multimedia context.

    Attributes:
        extensions (FileExtensions): An instance of the FileExtensions class for managing file extensions.

     Methods:
        setDefaultLanguage: Set the default language for captions.
        insert: Insert a block at the specified index.
        detect: Detect the format of the captions file.
        read: Read captions from content.
        checkContent: Check if the content is valid type.
        save: Save captions to a file.
        makeFilename: Adds languages and extension to filename.
        append: Append a Block to the list of blocks.
        shift_time: Shift the timing of all blocks by the specified duration.
        shift_start: Shift the start time of all blocks by the specified duration.
        shift_end: Shift the end time of all blocks by the specified duration.
        fromJson: Load captions format from a JSON file.
        toJson: Save captions format to a JSON file.
        join: Joins another CaptionsFormat class data.
        joinFile: Joins CaptionsFormat data from file.
        __getitem__: Retrieve the block at the specified index.
        __setitem__: Set the block at the specified index.
        __str__: Return a string representation of the captions format.
        __iadd__: In-place addition for concatenating blocks.
        __isub__: In-place subtraction for removing blocks in a specific language.
        __iter__: Iterator for iterating through blocks.
        __len__: Return the number of blocks in the captions format.
        __enter__: Enter the context for managing resources.
        __exit__: Exit the context, handling exceptions.
    """

    def __init__(self, filename: str = None, default_language: str = "und",
                 time_length: MT = None, file_extensions = None, **options):
        """
        Initialize a new instance of CaptionsFormat class.

        Parameters:
        - filename (str, optional): The name of the file associated with the captions, used for "with" keyword (default is None).
        - default_language (str, optional): The default language for captions (default is "und" for undefined).
        - **options: Additional keyword arguments for customization (e.g. metadata, style, ...).
        """
        self.time_length = MT() or time_length
        self.filename = filename
        self.options = options or {}
        self._block_list: list[Block] = []
        self.setDefaultLanguage(default_language)
        self.extensions = file_extensions or FileExtensions()

    def __getitem__(self, index: int):
        return self._block_list[index]

    def __setitem__(self, index: int, value: Block):
        self._block_list[index] = value

    def __iadd__(self, value):
        if not isinstance(value, CaptionsFormat):
            raise ValueError("Unsupported type. Must be an instance of `CaptionsFormat`")
        for i, value in enumerate(value):
            if i < len(self._block_list):
                self._block_list[i] += value
            else:
                self.append(value)
        return self

    def __isub__(self, language: str):
        for value in self._block_list:
            value -= language
        return self

    def __iter__(self):
        return iter(self._block_list)

    def __str__(self):
        return "\n".join(f"{i}. {caption}" for i, caption in enumerate(self._block_list))

    def __enter__(self):
        encoding = self.options.get("encoding") or "UTF-8"
        filename, ext = os.path.splitext(self.filename)
        if ext == ".json":
            self.fromJson(self.filename)
        else:
            with open(self.filename, "r", encoding=encoding) as stream:
                if self.detect(stream):
                    languages = self.getLanguagesFromFilename(self.filename)
                    if languages:
                        self.setDefaultLanguage(languages[0])
                    self.read(stream, languages)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __len__(self):
        return len(self._block_list)

    def setDefaultLanguage(self, language: str):
        standardized = standardize_tag(language, macro=True)
        self.default_language = standardized if tag_is_valid(standardized) else "und"

    def insert(self, index: int, value: Block):
        self._block_list.insert(index, value)

    def detect(self, file: str | io.IOBase = None):
        raise ValueError("Not implemented")

    def read(self, content: str | io.IOBase, languages: list[str], **kwargs):
        raise ValueError("Not implemented")

    def checkContent(self, content: str | io.IOBase, **kwargs):
        if not isinstance(content, io.IOBase):
            if not not isinstance(content, str):
                raise ValueError("The content is not a unicode string or I/O stream.")
            content = io.StringIO(content)
        return content

    def save(self, filename: str, languages: list[str], **kwargs):
        raise ValueError("Not implemented")

    def makeFilename(self, filename: str, extension: str, languages: list[str] = None,
                     include_languages_in_filename: bool = True, **kwargs):
        languages = languages or [self.default_language]
        if filename.endswith(extension):
            file, _ = os.path.splitext(filename)
        else:
            file = filename
        if include_languages_in_filename:
            file = ".".join((val for val in file.split('.') if val not in languages))+"."+".".join(languages)

        return file+extension

    def getLanguagesFromFilename(self, filename):
        filename, ext = os.path.splitext(filename)
        filename = filename.split(".")
        if len(filename) > 1:
            languages = []
            for i in filename:
                try:
                    if tag_is_valid(standardize_tag(i, macro=True)):
                        languages.append(i)
                except Exception:
                    continue
            if not languages:
                return None
        else:
            return None
        return languages

    def append(self, item: Block):
        if item.end_time > self.time_length:
            self.time_length = item.end_time
        self._block_list.append(item)

    def shift_time(self, time: MT):
        for i in self:
            i.shift_time_us(time)

    def shift_start(self, time: MT):
        for i in self:
            i.shift_start_us(time)

    def shif_end(self, time: MT):
        for i in self:
            i.shift_end_us(time)

    def fromJson(self, file: str, **kwargs):
        encoding = kwargs.get("encoding") or "UTF-8"
        if not file.endswith(".json"):
            file += ".json"
        try:
            with open(file, "r", encoding=encoding) as f:
                data = json.load(f)
                self.time_length = data["time_length"]
                self.default_language = data["default_language"]
                self.filename = data["filename"]
                for key, value in data["extensions"].items():
                    setattr(FileExtensions, key, value)
                self.options = data["options"]
                self._block_list = [Block(**caption) for caption in data["block_list"]]
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")

    def toJson(self, file: str, **kwargs):
        encoding = kwargs.get("encoding") or "UTF-8"
        try:
            if not file.endswith(".json"):
                file += ".json"
            with open(file, "w", encoding=encoding) as f:
                json.dump({
                    "default_language": self.default_language,
                    "time_length": self.time_length,
                    "filename": self.filename,
                    "extensions": vars(self.extensions),
                    "options": self.options,
                    "block_list": self._block_list
                           }, f, default=vars)
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")

    def join(self, captionsFormat, add_end_time: bool = False, time: MT = None, **kwargs):
        """
        Join two CaptionsFormat instances by appending blocks from the provided format to the current format.

        Args:
            captionsFormat (CaptionsFormat): The CaptionsFormat instance to join with.
            add_end_time (bool, optional): If True, current end time is added to the time offset.
            microseconds (int, optional): Time offset by microseconds.
            miliseconds (int, optional): Time offset by milliseconds.
            seconds (int, optional): Time offset by seconds.
            minutes (int, optional): Time offset by minutes.
            hours (int, optional): Time offset by hours.
            **kwargs: Additional options for customization (e.g. file encoding).
        """
        if not isinstance(captionsFormat, CaptionsFormat):
            raise ValueError("Unsupported type. Must be an instance of `CaptionsFormat`")

        time_offset = time or MT()
        if add_end_time:
            time_offset += self.time_length 

        for caption in captionsFormat:
            self.append(caption.copy())
            self[-1].shift_end_us(time_offset)

    def joinFile(self, filename: str, add_end_time: bool = False, time: MT = None, **kwargs):
        """
        Join captions from file by appending blocks to the current format.

        Args:
            captionsFormat (CaptionsFormat): The CaptionsFormat instance to join with.
            add_end_time (bool, optional): If True, current end time is added to the time offset.
            microseconds (int, optional): Time offset by microseconds.
            miliseconds (int, optional): Time offset by milliseconds.
            seconds (int, optional): Time offset by seconds.
            minutes (int, optional): Time offset by minutes.
            hours (int, optional): Time offset by hours.
            **kwargs: Additional options for customization (e.g. file encoding).
        """
        encoding = kwargs.get("encoding") or "UTF-8"

        time_offset = time or MT()
        if add_end_time:
            time_offset += self.time_length 

        with open(filename, "r", encoding=encoding) as stream:
            if self.detect(stream):
                self.read(stream, self.getLanguagesFromFilename(filename), time_offset=time_offset)
