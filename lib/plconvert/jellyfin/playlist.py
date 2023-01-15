import re
import sys
import xml.etree.ElementTree

from typing import List


def is_valid_first_line(first_line: str):
    return re.match(".?<\?[xX][mM][lL]", first_line) is not None


class JFPlaylistItem:
    def __init__(self, path: str):
        self.path = path


class JFPlaylist:
    def __init__(self, name: str = None, playlist_items: List[JFPlaylistItem] = None):
        self.name = name
        self.playlist_items = playlist_items if playlist_items else []

    def get_playlist_name(self) -> str:
        return self.name

    @classmethod
    def parse(self, path: str, debug: bool = False):
        tree = xml.etree.ElementTree.parse(path)
        root = tree.getroot()

        playlist_items = []
        item_count = 0
        for item_elem in root.iter("PlaylistItem"):
            item_count += 1
            path_count = 0
            for path_elem in item_elem.iter("Path"):
                path_count += 1
                playlist_items.append(JFPlaylistItem(path_elem.text))
                if debug:
                    print(
                        "[JFPlaylist::parse({})]: path found at index {}: {}".format(path, item_count, path_elem.text),
                        file=sys.stderr,
                    )
            if debug:
                if path_count == 0:
                    print(
                        "[JFPlaylist::parse({})]: No path found for PlaylistItem at index {}: {}".format(
                            path, item_count, item_elem
                        ),
                        file=sys.stderr,
                    )
                elif path_count > 1:
                    print(
                        "[JFPlaylist::parse({})]: Too many paths for PlaylistItem at index {}: {}".format(
                            path, item_count, item_elem
                        ),
                        file=sys.stderr,
                    )

        if debug and item_count == 0:
            print("[JFPlaylist::parse({})]: No PlaylistItems found!".format(path), file=sys.stderr)

        name_elem = root.find("LocalTitle")
        name = name_elem.text if name_elem is not None else None

        if debug:
            print("[JFPlaylist::parse({})]: name={}".format(path, name), file=sys.stderr)

        return JFPlaylist(name, playlist_items)
