from io import StringIO

from pytest import fixture

import src.github_wiki_page_index.generate_wiki_page_index as generate_wiki_page_index
from src.github_wiki_page_index.generate_wiki_page_index import (
    _add_page_to_tag_dict,
    _parse_args,
    _scan_line_for_tags,
    _render_tag_tree,
    generate_page_index,
    _insert_page_index,
)


@fixture
def example_tag_dict():
    return {
        "foo": {
            "bar": {"baz": {"untagged": {"test-page"}}, "untagged": set()},
            "untagged": set(),
        },
        "untagged": set(),
    }


@fixture
def example_page_index():
    return """<!--start Page Index-->

# Page Index

[file1](wiki/file1)

## tag

[file3](wiki/file3)

### subtag

[file2](wiki/file2)

<!--end Page Index-->
"""


@fixture
def example_page_index_2():
    return """<!--start Page Index-->

# Page Index

## tag

[file3](wiki/file3)

### subtag

[file2](wiki/file2)

## Untagged Pages

[file1](wiki/file1)

<!--end Page Index-->
"""


@fixture
def example_home_page_md():
    return """Welcome to the wikitest wiki!

Barrau was born in Carcassonne. He was a student of Alexandre Falguière and 
started at the Salon in 1874. He received awards in 1879, 1880, 1889, and 
became a Chevalier of the Legion of Honor in 1892. He died in Paris.

<!--start Page Index-->

# Page Index

[A Restructured Text Page](wiki/A-Restructured-Text-Page)

<!--end Page Index-->

Drilling is a cutting process that uses a drill bit to cut a hole of circular cross-section in solid materials. The
drill bit is usually a rotary cutting tool, often multi-point. The bit is pressed against the work-piece and rotated at
rates from hundreds to thousands of revolutions per minute. This forces the cutting edge against the work-piece, cutting
off chips (swarf) from the hole as it is drilled.
"""


@fixture
def run_setup():
    generate_wiki_page_index.untagged_after = False
    generate_wiki_page_index._setup()


def test_add_page_to_tag_dict(example_tag_dict):
    tag_dict = {"untagged": set()}
    tag_to_add = "foo-bar-baz"
    page_name = "test-page"

    _add_page_to_tag_dict(page_name, tag_to_add, tag_dict)
    assert tag_dict == example_tag_dict


def test_parse_args():
    namespace = _parse_args(["./wiki", "--insert", "--untagged-after"])

    assert namespace.wiki_dir == "./wiki"
    assert namespace.insert is True
    assert namespace.untagged_after is True


def test_scan_line_for_tags():
    tags_list = _scan_line_for_tags("Tags: foo foo-bar blah baz")
    assert tags_list == ["foo", "foo-bar", "blah", "baz"]


def test_scan_line_for_tags_2():
    tags_list = _scan_line_for_tags("foo foo-bar blah baz")
    assert tags_list == []


def test_render_tag_tree(example_tag_dict, run_setup):
    rendered_tree = _render_tag_tree(example_tag_dict)

    assert (
        rendered_tree
        == """## foo

### bar

#### baz

[test page](wiki/test-page)

"""
    )


def test_generate_page_index(monkeypatch, run_setup, example_page_index):
    def return_dummy_tag_list():
        return [
            ("file1", []),
            ("file2", ["tag-subtag"]),
            ("file3", ["tag"]),
            ("file4", ["tag", "noindex"]),
        ]

    monkeypatch.setattr(
        generate_wiki_page_index, "_get_file_tags", return_dummy_tag_list
    )

    result = generate_page_index()

    assert result == example_page_index


def test_generate_page_index_2(monkeypatch, run_setup, example_page_index_2):
    def return_dummy_tag_list():
        return [
            ("file1", []),
            ("file2", ["tag-subtag"]),
            ("file3", ["tag"]),
            ("file4", ["tag", "noindex"]),
        ]

    monkeypatch.setattr(
        generate_wiki_page_index, "_get_file_tags", return_dummy_tag_list
    )
    generate_wiki_page_index.untagged_after = True

    result = generate_page_index()

    assert result == example_page_index_2


def test_insert_page_index(monkeypatch, example_page_index, example_home_page_md):
    def return_dummy_index():
        return example_page_index

    monkeypatch.setattr(
        generate_wiki_page_index, "generate_page_index", return_dummy_index
    )

    input_io = StringIO(example_home_page_md)

    output_io = StringIO()

    _insert_page_index(input_io, output_io)
    assert (
        output_io.getvalue()
        == """Welcome to the wikitest wiki!

Barrau was born in Carcassonne. He was a student of Alexandre Falguière and 
started at the Salon in 1874. He received awards in 1879, 1880, 1889, and 
became a Chevalier of the Legion of Honor in 1892. He died in Paris.

<!--start Page Index-->

# Page Index

[file1](wiki/file1)

## tag

[file3](wiki/file3)

### subtag

[file2](wiki/file2)

<!--end Page Index-->

Drilling is a cutting process that uses a drill bit to cut a hole of circular cross-section in solid materials. The
drill bit is usually a rotary cutting tool, often multi-point. The bit is pressed against the work-piece and rotated at
rates from hundreds to thousands of revolutions per minute. This forces the cutting edge against the work-piece, cutting
off chips (swarf) from the hole as it is drilled.
"""
    )


def test_insert_page_index_2(monkeypatch, example_page_index):
    def return_dummy_index():
        return example_page_index

    monkeypatch.setattr(
        generate_wiki_page_index, "generate_page_index", return_dummy_index
    )

    input_io = StringIO(
        """Welcome to the wikitest wiki!

Barrau was born in Carcassonne. He was a student of Alexandre Falguière and 
started at the Salon in 1874. He received awards in 1879, 1880, 1889, and 
became a Chevalier of the Legion of Honor in 1892. He died in Paris.

Drilling is a cutting process that uses a drill bit to cut a hole of circular cross-section in solid materials. The
drill bit is usually a rotary cutting tool, often multi-point. The bit is pressed against the work-piece and rotated at
rates from hundreds to thousands of revolutions per minute. This forces the cutting edge against the work-piece, cutting
off chips (swarf) from the hole as it is drilled.
"""
    )

    output_io = StringIO()

    _insert_page_index(input_io, output_io)
    assert (
        output_io.getvalue()
        == """<!--start Page Index-->

# Page Index

[file1](wiki/file1)

## tag

[file3](wiki/file3)

### subtag

[file2](wiki/file2)

<!--end Page Index-->
Welcome to the wikitest wiki!

Barrau was born in Carcassonne. He was a student of Alexandre Falguière and 
started at the Salon in 1874. He received awards in 1879, 1880, 1889, and 
became a Chevalier of the Legion of Honor in 1892. He died in Paris.

Drilling is a cutting process that uses a drill bit to cut a hole of circular cross-section in solid materials. The
drill bit is usually a rotary cutting tool, often multi-point. The bit is pressed against the work-piece and rotated at
rates from hundreds to thousands of revolutions per minute. This forces the cutting edge against the work-piece, cutting
off chips (swarf) from the hole as it is drilled.
"""
    )
