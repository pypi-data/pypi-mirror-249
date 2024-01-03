import fileinput
import re
import sys
from argparse import ArgumentParser, Namespace
from os import chdir
from os import rename, scandir
from os.path import splitext
from typing import TextIO

"""
Generates page index for a wiki
"""


file_exclusion_re: re.Pattern
dash_to_space: dict
underscore_to_space: dict
start_marker: str
end_marker: str
untagged_after: bool


def _setup():
    global file_exclusion_re
    global dash_to_space
    global underscore_to_space
    global start_marker
    global end_marker

    # excludes files and folders that start with a dot, like .git or .DS_Store
    # also excludes _Sidebar.md, _Footer.md, and Home.md
    file_exclusion_re = re.compile(r"^\..*$|^_Sidebar\.md$|^_Footer.md$|Home.md")

    # translation tables for str.translate
    dash_to_space = str.maketrans("-", " ")
    underscore_to_space = str.maketrans("_", " ")

    start_marker = "<!--start Page Index-->\n"
    end_marker = "<!--end Page Index-->\n"


def _parse_args(args_list: list[str]) -> Namespace:
    global untagged_after

    parser = ArgumentParser(description="Generate a Page Index for a GitHub Wiki. ")
    parser.add_argument("wiki_dir", help="Path to the clone of your GitHub Wiki")
    parser.add_argument(
        "-i",
        "--insert",
        help="Automatically insert the Page Index into your Home.md file",
        action="store_true",
    )
    parser.add_argument(
        "-u",
        "--untagged-after",
        help="Place untagged pages at the end of the index (default is at the start)",
        action="store_true",
    )
    result = parser.parse_args(args=args_list)
    untagged_after = result.untagged_after

    return result


def insert_page_index():
    """Generate the Page Index and place the text into the Home.md file.

    If the HTML comments <!--start Page Index--> and <!--end Page Index-->
    exist then the Page Index will be inserted between them. Otherwise, the
    Page Index will be placed at the start of the file and the comments will
    be added. Text above the start marker and text below the end marker will
    be preserved.
    """
    rename("Home.md", "Home.md.old")
    with open("Home.md", "w") as new_home_md:
        with open("Home.md.old", "r") as old_home_md:
            _insert_page_index(old_home_md, new_home_md)


def _insert_page_index(old_home_md: TextIO, new_home_md: TextIO) -> None:
    # Read and dump out text before the Page Index
    while one_line := old_home_md.readline():
        if one_line == start_marker:
            # We reached the top of the old Page Index
            break
        else:
            # We haven't reached the top of the old Page Index yet so
            # transfer the old content to the new file.
            new_home_md.write(one_line)

    if len(one_line) == 0:
        # reached EOF without finding an existing Page Index
        # Put the Page Index at the beginning of the file, then
        # rewind and put the rest of the old home page's content
        # after that.
        # This is slightly inefficient, but good enough for this purpose
        new_home_md.seek(0)
        new_home_md.write(generate_page_index())
        old_home_md.seek(0)
        for existing_line in old_home_md:
            new_home_md.write(existing_line)
        return

    # We found the old Page Index, so skip lines until the end of the old Page Index
    while one_line := old_home_md.readline():
        if one_line == end_marker:
            break

    # Either we found the old Page Index and skipped to the bottom of it,
    # or we never found the bottom marker and skipped all of the rest
    # of the file.
    # In either case write the new Page Index
    new_home_md.write(generate_page_index())

    # Read and dump out text after the Page Index
    while one_line := old_home_md.readline():
        new_home_md.write(one_line)


def _get_file_tags() -> tuple[str, list[str]]:
    files_in_dir = scandir()
    files_to_scan = [
        f.name
        for f in files_in_dir
        if f.is_file() and not file_exclusion_re.match(f.name)
    ]

    # errors="replace" is to handle files with screwed up Unicode encoding, otherwise
    # fileinput crashes
    with fileinput.input(files_to_scan, errors="replace") as f:
        for one_line in f:
            fn = fileinput.filename()
            tags_list = _scan_line_for_tags(one_line)
            yield fn, tags_list
            fileinput.nextfile()


def generate_page_index() -> str:
    """Scan the wiki pages and produce a Page Index.

    :return: Markdown-formatted Page Index
    """
    result: str = f"{start_marker}\n# Page Index\n\n"
    tag_tree: dict = {"untagged": set()}

    for filename, tags_list in _get_file_tags():
        if len(tags_list) > 0:
            # if one of the tags is "noindex", then skip the page
            # this is useful for archiving or otherwise ignoring
            # pages.
            if "noindex" not in tags_list:
                # otherwise, add the page to the tags dict
                for one_tag in tags_list:
                    _add_page_to_tag_dict(filename, one_tag, tag_tree)
        else:
            # the page is untagged
            tag_tree["untagged"].add(filename)

    result += _render_tag_tree(tag_tree) + end_marker

    return result


def _scan_line_for_tags(line_to_scan: str) -> list[str]:
    """Scan a single line for tags.

    This is a line that looks like:
    Tags: Tag_One Tag_Two Tag_Three-Sub_Tag_A

    :param line_to_scan: line to be scanned
    :return: list of tags in that line
    """
    if line_to_scan.startswith("Tags: "):
        # return a list of tags, without the initial Tags: indicator
        return line_to_scan.split()[1:]

    else:
        return []


def _add_page_to_tag_dict(page: str, tag_seq: str, tag_dict: dict[str, any]) -> None:
    """Add the filename to the tag dict.

    The dict structure looks like:
    {
        "untagged": {"page1", "page2", "page3"}
        "tag1": {
            "untagged": ["page4"]
        }
        "tag2": {
            "untagged": {}
            "tag3": {
                "untagged": {"page5", "page6"}
            }
        }
        "tag4": {
            "untagged": {"page5"}
        }
    }

    :param page: name of the page to be added to the tag_dict
    :param tag_seq: list of tags to be added
    :param tag_dict: dictionary where the tags will be added
    """
    current_dict = tag_dict
    for current_level in tag_seq.split("-"):
        current_dict = current_dict.setdefault(current_level, {"untagged": set()})
    current_dict.setdefault("untagged", set()).add(page)


def _render_tag_tree(tag_tree: dict, level: int = 2) -> str:
    """Render the tag tree into a string with links to the pages.

    :param tag_tree: dict containing the tags
    :param level: how many #'s to put in front of tag headings
    :return: tag tree rendered as Markdown
    """

    def _insert_untagged():
        nonlocal result
        nonlocal level

        for one_filename in sorted(list(tag_tree["untagged"])):
            # strip off the extension then change dashes to spaces
            # Prefix link with 'wiki/' so that it works right
            # This is a GitHub bug
            stripped_filename = splitext(one_filename)[0]
            munged_filename = stripped_filename.translate(dash_to_space)
            result += f"[{munged_filename}](wiki/{stripped_filename})\n\n"

    result = ""

    if not untagged_after or level != 2:
        _insert_untagged()

    sub_tags = sorted(tag_tree.keys())
    sub_tags.remove("untagged")
    for one_tag in sub_tags:
        result += f"{'#' * level} {one_tag.translate(underscore_to_space)}\n\n"
        result += _render_tag_tree(tag_tree[one_tag], level + 1)

    if untagged_after and level == 2:
        result += "## Untagged Pages\n\n"
        _insert_untagged()

    return result


if __name__ == "__main__":
    _setup()
    args = _parse_args(sys.argv[1:])
    chdir(args.wiki_dir)

    if args.insert:
        print("Generating Page Index and inserting into Home.md")
        insert_page_index()
    else:
        print("Generating Page Index and printing to stdout")
        print(generate_page_index())
