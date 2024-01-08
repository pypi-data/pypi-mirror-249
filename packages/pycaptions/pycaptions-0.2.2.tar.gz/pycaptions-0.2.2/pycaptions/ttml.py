import io
import os

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT
from bs4 import BeautifulSoup


EXTENSIONS = [".ttml", ".dfxp", ".xml"]


@staticmethod
def detectTTML(content: str | io.IOBase) -> bool:
    """
    Used to detect Timed Text Markup Language caption format.

    It returns True if:
     - the first line starts with `<?xml` and contains `<tt xml` OR
     - the first line starts with `<tt xml` OR
     - the second line starts with `<tt xml`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    first = content.readline().lstrip()
    if (first.startswith("<tt xml") or first.startswith("<?xml") and "<tt xml" in first
        or content.readline().lstrip().startswith("<tt xml")
    ):
        content.seek(offset)
        return True
    content.seek(offset)
    return False

# ttp:frameRate, ttp:frameRateMultiplier, ttp:subFrameRate, ttp:tickRate, ttp:timeBase
def readTTML(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, **kwargs)
    time_offset = kwargs.get("time_offset") or 0
    content = BeautifulSoup(content, "xml")
    if not languages:
        if not content.tt.get("xml:lang"):
            languages = [self.default_language]
        else:
            languages = [content.tt.get("xml:lang")]
    self.setDefaultLanguage(languages[0])
    for index, langs in enumerate(content.body.find_all("div")):
        lang = langs.get("xml:lang")
        p_start, p_end = MT.fromTTMLTime(langs.get("begin"), langs.get("dur"), langs.get("end"))
        for block, line in enumerate(langs.find_all("p")):
            start, end = MT.fromTTMLTime(line.get("begin"), line.get("dur"), line.get("end"))
            start += p_start
            if start > p_end:
                start = p_end
                end = p_end
            elif end > p_end:
                end = p_end
            if index == 0:
                caption = Block(BlockType.CAPTION, start_time=start, end_time=end)
            else:
                caption = self[block]
            for l, text in enumerate(line.get_text().strip().split("\n")):
                if len(languages) > 1:
                    caption.append(text, lang or languages[l])
                else:
                    caption.append(text, lang or languages[0])
            caption.shift_time(time_offset)
            if index == 0:
                self.append(caption)


def saveTTML(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.TTML,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
            pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class TTML(CaptionsFormat):
    """
    Timed Text Markup Language

    Read more about it https://www.w3.org/TR/ttml/

    Example:

    with TTML("path/to/file.ttml") as ttml:
        ttml.saveSRT("file")
    """
    detect = staticmethod(detectTTML)
    _read = readTTML
    _save = saveTTML

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .vtt import saveVTT
