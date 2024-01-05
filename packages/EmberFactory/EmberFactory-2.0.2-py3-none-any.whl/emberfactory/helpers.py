import re
import logging


def colspan(content):
    """
    Adds colspan=x to html tables when x empty cells are found after a filled cell.
    Intended as a supplement to the standard processing of Markdown tables.
    Note that this might be replaced by an existing third-party extension to the markdown python library,
    https://github.com/Neepawa/cell_row_span
    The rules are the same, but the extension does a lot more and is more complex.
    In addition, this code removes any empty header cell (standard markdown does not support tables without header)
    :param content: the html to be processed
    :return:
    """
    lines = content.splitlines()
    content = ""
    nlines = len(lines)
    iline = 0
    while iline < nlines:
        line = lines[iline]
        if line[0:3] == "<td":
            ispan = 1
            nxline = lines[iline+1]
            while (iline+1) < nlines and nxline[nxline.find(">"):] == "></td>":
                iline += 1
                ispan += 1
                nxline = lines[iline + 1]
            if ispan > 1:
                line = "<td colspan=" + str(ispan) + line[3:]
        if line != "<th></th>":
            content += line + "\n"
        iline += 1
    return content


def mdcombine(basetext, addsource):
    """
    Combines two markdown texts by inserting sections from a source file where indicated in basetext.
    Used here to extract information from the file defining parameters and insert it in the documentation.
    The basetext has to include tags indicating what should be inserted and where:
    - basetext contains the requests for inserting specific sections extracted from addsource : {INSERT:section_name}
    - addsource contains the source of the insertions in the form
            <section id=section_name>Content to be inserted</section>

    (the behaviour differs from the markdown-include project because here only one file with several sections is
    used as input, not several entire files).

    :param basetext: The text in which insertions are to be done, based on tags like {INSERT:section_name}
    :param addsource: The files from which to get the text fragments to be inserted.
    :return: the combined text
    """

    # Get addtext from the source file:
    with open(addsource, "r", encoding="utf-8") as input_file:
        addtext = input_file.read()
    # Remove lines containing <del hidden>: those are about legacy parameters which are no longer shown to the user
    filtext = ""
    for text in addtext.split("\n"):
        if "<del hidden>" not in text:
            filtext += text + "\n"
    # Parse addtext as dict {section_name: section_text}
    sections = dict(re.findall(r'<section.id=[ \"\']*(.+?)[ \"\']*>(.+?)</section>', filtext, re.DOTALL))

    # Combine texts
    basesplit = basetext.split('{INSERT:')
    combined = basesplit[0]  # Text before the first Insert
    for part in basesplit[1:]:
        resplit = part.split('}')  # (Name of the first insert, text after the first insert)
        secname = resplit[0].strip()
        if secname in sections:  # If we have a section with that name, insert it here
            combined += sections[secname]
        else:
            logging.warning("Markdown documents combination: section '{}' is missing".format(secname))
        combined += resplit[1]

    return combined
