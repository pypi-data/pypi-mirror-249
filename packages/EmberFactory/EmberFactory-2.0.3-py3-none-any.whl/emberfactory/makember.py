# -*- coding: utf-8 -*-
"""
Makember produces a full burning ember plot from colour levels read from a table (.xlsx).

The objectives are to
- facilitate reproducibility of existing figures,
- facilitate the creation of new 'ember' figures in a way that is both quick and reliable.

This version is an adaptation to the EmberMaker library, which is a separate project starting with v2.0 (2023/09)
Copyright (C) 2020  philippe.marbaix@uclouvain.be (EmberFactory version)
"""
from embermaker.embergraph import EmberGraph
from os import path
from embermaker.readembers import embers_from_xl
from embermaker import helpers as hlp
from embermaker.ember import Transition, gpsort, getgroups
from embermaker import embergraph as eg
from embermaker import parameters as param
trd = Transition  # Transition definitions

# Input file
# ----------
# This code can process 3 file formats:
# - The standard file format only contains data about the risk and confidence levels,
#   in the format from the IPCC SRCCL chap 7 supplementary material; the workbook only contains one sheet.
# - The extended file format contains the same first sheet, but one or two additional sheets provide:
#   . graphic parameters
#   . color definitions
# - The legacy "fullflex" format uses a different sheet to provide the data about the risk levels;
#   It was used for Zommers et. al (2020). The 'standard format' was made more flexible, so that this no longer needed.
#   Graphic parameters and colors are provided in the same way as in the "extended" file format above.


def makember(infile=None, outfile=None, prefcsys='CMYK', grformat='SVG', logger=None):
    """
    Reads ember data from .xlsx files, reads default values if needed, and generates an ember plot;
    in principle, this part of the plotting relates to the most 'high level' aspects that decides for the design,
    while lower level aspects are delegated to the ember module.
    :param infile: The name of the data file (.xlsx). Mandatory.
    :param outfile: An optional name for the output file (with or without extension, both ok ?)
    :param prefcsys: The prefered color system (also called mode): RGB or CMYK.
    :param grformat: The desired graphic file format
    :param logger: The logger object to which information and warning messages should be recorded.
    :return: a dict potentially containing : 'outfile' (output file path), 'width' (diagram width), 'error' (if any)
    """
    
    # Logger (there is no obligation to start it now unless one wishes to store log that will be returned to the user)
    if logger is None:
        logger = hlp.Logger()
    
    # Input file:
    if infile is None:
        return {'error': logger.addfail("No input file.")}

    # Open input file (workbook):
    wbmain = hlp.secure_open_workbook(infile)

    # Default colors (will only be open if needed):
    infdef = path.join(hlp.getpath_defaults(), "colors.xlsx")

    # Get default graph parameters
    # ----------------------------
    gp = param.ParamDict(logger=logger)

    # Open the user's data sheet and read graph parameters, if any
    # ------------------------------------------------------------
    gp.readparams(wbmain)  # Read parameters from the Excel WB, if any.

    # Read the ember's data sheet
    # ---------------------------
    lbes = embers_from_xl(wbmain, gp=gp, logger=logger)
    if isinstance(lbes, dict):  # Fatal error - reading was not possible
        return {'outfile': '', 'width': '', 'logger': logger, 'error': lbes['error']}

    # Get colours palette
    # -------------------
    cpalname = None if 'be_palette' not in gp.keys() else gp['be_palette']
    # The UI color choice overrides any choice in the user file; if the UI asks for a default palette, use default wb
    # ("standard" means that the user does not make this choice => takes whatever is selected in the file)
    if "Color definitions" not in wbmain.sheetnames or cpalname is None or "standard" not in prefcsys:
        palsource = "default palette"
        wbcol = hlp.secure_open_workbook(infdef)
    else:
        palsource = "palette from input file"
        wbcol = wbmain
    cpal = eg.ColourPalette(wbcol, prefcsys=prefcsys, cpalname=cpalname, cpalinfo=palsource)
    if "RGB" in prefcsys and cpal.csys != "RGB":  # Received palette not appropriate => needs to read again!
        palsource = "default palette because RGB requested (e.g. for SVG) but file wants CMYK"
        cpal = eg.ColourPalette(hlp.secure_open_workbook(infdef), prefcsys="RGB", cpalname="", cpalinfo=palsource)
    logger.addinfo(f"Colors: {palsource}")

    # Create the ember graph
    # ----------------------
    outfile = outfile if outfile else infile.replace('/in/', '/out/')
    egr = EmberGraph(outfile, cpal, gp, grformat=grformat, logger=logger)
    logger.addinfo(f"Graphical parameters", mestype='title')
    logger.addinfo(str(gp))

    # Sort embers according to the parameters in gp
    # ---------------------------------------------
    lbes = gpsort(lbes, gp)

    # Group embers according to their group names
    # -------------------------------------------
    gbes = getgroups(lbes)  # The result of this operation is a nested list : [groups[embers]]

    # Add groups of embers (and the embers it contains), to the graph
    # ---------------------------------------------------------------
    egr.add(gbes)

    # Actually produce the diagram
    # ----------------------------
    logger.addinfo("Drawing embers", mestype='title')
    outfile = egr.draw()

    # Rough clone of the former output, which is still needed
    odict = {'outfile': outfile, 'width': str(egr.cx.b1), 'logger': logger}
    critical = logger.getlog("CRITICAL")
    if len(critical) > 0:
        odict["error"] = ", ".join(critical)  # Legacy appraoch: 'error' actually stops the processing (see control.py)
    return odict
