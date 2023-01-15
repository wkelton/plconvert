import re
import sys
from typing import List


def is_valid_first_line(first_line: str):
    return re.match("(#EXT3MU)|[^#<]", first_line) is not None


class M3UAttribute:
    def __init__(self, name: str, value: str = None):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        if self.value:
            return "{}:{}".format(self.name, self.value)
        return self.name


class M3UEntry:
    def __init__(self, entry: str, ext_attributes: List[M3UAttribute] = None):
        self.entry = entry
        self.ext_attributes = ext_attributes

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        if self.ext_attributes:
            return "\n".join([str(a) for a in self.ext_attributes]) + "\n" + self.entry
        return self.entry


class M3U:
    def __init__(
        self, ext_support: bool = False, ext_globals: List[M3UAttribute] = None, entries: List[M3UEntry] = None
    ):
        self.ext_support = ext_support
        self.ext_globals = ext_globals if ext_globals else []
        self.entries = entries if entries else []

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        if self.ext_support:
            return "#EXT3MU\n{}\n{}".format(
                "\n".join([str(g) for g in self.ext_globals]), "\n".join([str(e) for e in self.entries])
            )
        return "\n".join(self.entries)

    def enable_ext(self):
        self.ext_support = True

    def append_ext_global(self, ext_global: M3UAttribute):
        self.ext_globals.append(ext_global)

    def append_entry(self, entry: M3UEntry):
        self.entries.append(entry)

    def get_playlist_name(self) -> str:
        name = None
        for a in self.ext_globals:
            if a.name == "#PLAYLIST":
                return a.value
        return name

    def set_playlist_name(self, name: str):
        self.append_ext_global(M3UAttribute("#PLAYLIST", name))

    @classmethod
    def parse(self, path: str, debug: bool = False):
        ext_support = False
        playlist_name = None
        entries = []

        with open(path, "r") as p:
            index = 0
            for line in p:
                line = line.strip()

                if line == "#EXT3MU":
                    ext_support = True
                    if debug:
                        print(
                            "[M3U::parse({})]: ext support enabled".format(path),
                            file=sys.stderr,
                        )
                elif line.startswith("#"):
                    if ext_support:
                        if line.startswith("#PLAYLIST"):
                            playlist_name = line.split(":")[1]
                            if debug:
                                print(
                                    "[M3U::parse({})]: ext playlist name found: {}".format(path, playlist_name),
                                    file=sys.stderr,
                                )
                        else:
                            print("EXT3MU setting not supported: {}".format(line), file=sys.stderr)
                    else:
                        print(
                            "[M3U::parse({})]: skipping ext setting as EXT3MU not found: {}".format(path, line),
                            file=sys.stderr,
                        )
                else:
                    index += 1
                    entries.append(M3UEntry(line))
                    if debug:
                        print(
                            "[M3U::parse({})]: item found at index {}: {}".format(path, index, line),
                            file=sys.stderr,
                        )

        if debug and len(entries) == 0:
            print("[M3U::parse({})]: No items found!".format(path), file=sys.stderr)

        m3u = M3U(ext_support, None, entries)
        if playlist_name:
            m3u.set_playlist_name(playlist_name)

        return m3u
