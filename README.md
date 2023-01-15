# plconvert

Tool for converting playlists from one format to another.

Current formats supported:
* m3u
* Jellyfin xml

## Requirements
Requried Python 3 packages:
* click

## Usage

See available commands by running:
`plconvert --help`

See help usage for a specific command by providing the `--help` option to the command. Example:
`plconvert validate --help`

Example usage:
* `plconvert to-m3u /path/to/jellyfin/file`
  * Prints the input playlist in the m3u format to stdout
* `plconvert to-m3u --relativize /path /path/to/jellyfin/file`
  * Prints the input playlist in the m3u format after changing each path in the playlist to be relative to '/path' to stdout

For bash autocompletion, run:
`eval "$(./plconvert autocompletion)"`
See [Click Shell Completion docs](https://click.palletsprojects.com/en/8.1.x/shell-completion/) for details on enabling completion in other shells.
