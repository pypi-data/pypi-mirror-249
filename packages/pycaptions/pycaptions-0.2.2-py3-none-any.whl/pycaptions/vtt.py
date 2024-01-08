import io
import re

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT
from cssutils import CSSParser


EXTENSIONS = [".vtt"]
STYLE_PATERN = re.compile(r"::cue\((#[^)]+)\)")


@staticmethod
def detectVTT(content: str | io.IOBase) -> bool:
    """
    Used to detect WebVTT caption format.

    It returns True if:
     - the first line matches `WebVTT`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().rstrip().startswith("WEBVTT"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readVTT(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0

    if not self.options.get("blocks"):
        self.options["blocks"] = []
    metadata = Block(BlockType.METADATA)
    content.readline()
    line = content.readline().strip()
    while line:
        line = line.split(": ", 1)
        metadata.options[line[0]] = line[1]
        line = content.readline().strip()
    self.options["blocks"].append(metadata)

    if not self.options.get("style"):
        self.options["style"] = dict()
    if not self.options["style"].get("identifier_to_original"):
        self.options["style"]["identifier_to_original"] = dict()
    if not self.options["style"].get("identifier_to_new"):
        self.options["style"]["identifier_to_new"] = dict()
    if not self.options["style"].get("style_id_counter"):
        self.options["style"]["style_id_counter"] = 0

    line = content.readline()
    while line:
        line = line.strip()
        if line.startswith("NOTE"):
            temp = line.split(" ", 1)
            comment = Block(BlockType.COMMENT)
            if len(temp) > 1:
                comment.append(temp[1])
            line = content.readline().strip()
            while line:
                comment.append(line)
                line = content.readline().strip()
            self.options["blocks"].append(comment)
        elif line == "STYLE":
            style = ""
            line = content.readline().strip()
            while line:
                style += line
                line = content.readline().strip()

            def replace_style(match):
                if match.group(1).startswith("#"):
                    if match.group(1) in self.options["style"]["identifier_to_new"]:
                        return self.options["style"]["identifier_to_new"][match.group(1)]
                    self.options["style"]["style_id_counter"] += 1
                    style_name = f"#style{self.options['style']['style_id_counter']}"
                    self.options["style"]["identifier_to_original"][style_name] = match.group(1)
                    self.options["style"]["identifier_to_new"][match.group(1)] = style_name
                    return style_name
                return match.group(1)
            parser = CSSParser(validate=False)
            style = parser.parseString(
                        cssText=re.sub(STYLE_PATERN, replace_style, style),
                        encoding="UTF-8"
                    )
            self.options["blocks"].append(Block(BlockType.STYLE, style=style))
        elif line == "REGION":
            line = content.readline().strip()
            temp = dict()
            while line:
                line = line.split(":", 1)
                temp[line[0]] = line[1]
                line = content.readline().strip()
            self.options["blocks"].append(Block(BlockType.LAYOUT, layout=temp))
        else:
            break
        line = content.readline()

    while line:
        if line.startswith("NOTE"):
            temp = line.split(" ", 1)
            comment = Block(BlockType.COMMENT)
            if len(temp) > 1:
                comment.append(temp[1])
            line = content.readline().strip()
            while line:
                comment.append(line)
                line = content.readline().strip()
            self.append(comment)
        else:
            caption = Block(BlockType.CAPTION)
            if "-->" not in line:
                caption.options["indentificator"] = line.strip()
                line = content.readline().strip()
            start, end = line.split(" --> ", 1)
            end = end.split(" ", 1)
            if len(end) > 1:
                caption.options["style"] = end[1]
            end = end[0]
            caption.start_time = MT.fromVTTTime(start)
            caption.end_time = MT.fromVTTTime(end)
            counter = 1
            line = content.readline().strip()
            if line.startswith("{"):
                caption.block_type = BlockType.METADATA
            while line:
                if len(languages) > 1:
                    caption.append(line, languages[counter])
                    counter += 1
                else:
                    caption.append(line, languages[0])
                line = content.readline().strip()
            caption.shift_time(time_offset)
            self.append(caption)
        line = content.readline()


def saveVTT(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.VTT,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
            file.write("WEBVTT\n\n")
            index = 1
            for data in self:
                if data.block_type != BlockType.CAPTION:
                    continue
                elif index != 1:
                    file.write("\n\n")
                file.write(f"{data.start_time.toVTTTime()} --> {data.end_time.toVTTTime()}\n")
                file.write("\n".join(data.get(i) for i in languages))
                index += 1
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")


class WebVTT(CaptionsFormat):
    """
    Web Video Text Tracks

    Read more about it: https://www.speechpad.com/captions/webvtt
    Full specification: https://www.w3.org/TR/webvtt/

    Example:

    with WebVTT("path/to/file.vtt") as vtt:
        vtt.saveSRT("file")
    """
    detect = staticmethod(detectVTT)
    _read = readVTT
    _save = saveVTT

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
