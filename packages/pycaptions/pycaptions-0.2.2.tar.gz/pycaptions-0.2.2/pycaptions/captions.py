import io
from .captionsFormat import CaptionsFormat


class Captions(CaptionsFormat):
    """
    Captions

    A generic class to read different types of caption formats.

    Example:

    with Captions("path/to/file.srt") as captions:
        captions.saveSRT("file")
    """
    def __init__(self, filename: str = None, default_language: str = "und", **options):
        super().__init__(filename, default_language, **options)

    from .sami import detectSAMI, saveSAMI, readSAMI
    from .srt import detectSRT, saveSRT, readSRT
    from .sub import detectSUB, saveSUB, readSUB
    from .ttml import detectTTML, saveTTML, readTTML
    from .vtt import detectVTT, saveVTT, readVTT

    readers = {
        "sami": readSAMI,
        "srt": readSRT,
        "sub": readSUB,
        "ttml": readTTML,
        "vtt": readVTT
    }

    savers = {
        "sami": saveSAMI,
        "srt": saveSRT,
        "sub": saveSUB,
        "ttml": saveTTML,
        "vtt": saveVTT
    }

    def get_format(self, file: str | io.IOBase) -> str | None:
        if self.detectSAMI(file):
            self.fileFormat = "sami"
        elif self.detectSRT(file):
            self.fileFormat = "srt"
        elif self.detectSUB(file):
            self.fileFormat = "sub"
        elif self.detectTTML(file):
            self.fileFormat = "ttml"
        elif self.detectVTT(file):
            self.fileFormat = "vtt"
        return self.fileFormat

    def detect(self, content: str | io.IOBase) -> bool:
        if not self.get_format(content):
            return False
        return True

    def read(self, content: str | io.IOBase, languages: list[str] = None, **kwargs):
        format = self.get_format(content)
        if not format:
            return
        self.readers[format](self, content, languages, **kwargs)

    def save(self, filename: str, languages: list[str] = None, output_format: str = None, **kwargs):
        output_format = output_format or self.fileFormat
        if output_format not in self.savers:
            raise ValueError("Incorect output format")
        self.savers[output_format](self, filename=filename, languages=languages, **kwargs)
