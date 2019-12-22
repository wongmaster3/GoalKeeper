import re

tag_regex = re.compile('#[a-zA-Z0-9][a-zA-Z0-9 ]*')
tag_lst_regex = re.compile('(#[a-zA-Z0-9][a-zA-Z0-9 ]*)*$')

def get_tags(tagstr):
    """Returns a list of valid tags or None if the given string contains invalid tags"""
    if(tag_lst_regex.match(tagstr.strip())):
        taglst = tagstr.strip().split('#')
        output = []
        for tag in taglst:
            if tag_regex.match('#' + tag.strip()) is not None:
                output.append('#' + tag.strip())
        return output
    return None

def is_tag_str(tagstr):
    """Determines if a given string is a valid list of tags"""
    return tag_lst_regex.match(tagstr.strip()) is not None

def is_tag(str):
    """Determines if a given string is a valid tag"""
    return tag_regex.match(str) is not None

def get_tag_text(tag):
    """Gets the text from a valid tag (just the text without the leading #)"""
    return tag[1:]
