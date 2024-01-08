# -*- coding: utf-8 -*-
"""
EmberGraphs stores the general information on a graphic containing embers.
"""
import numpy as np
from embermaker import helpers as hlp
from embermaker.helpers import norm, isempty
from embermaker.drawinglib import canvas
from embermaker.drawinglib.helpers import mm
from embermaker.graphbase import Element, Coord, vaxis
from embermaker.legend import LegendBox, drawlegend
from embermaker import __version__
import embermaker.parameters as param
from embermaker.ember import Ember
from embermaker.ember import getgroups
from os import path


class EmberGraph(Element):
    """
    EmberGraphs stores the general information on a graphic containing embers,
    and provides methods for drawing such graphs (except for the embers themselves, which are dealt with
    in the Ember class)
    We have included the creation of the drawing canvas here because we want to perfom some intialisation
    before the main program can access the canvas. This sets the colour space to RGB or CMYK once and for all.
    """

    def __init__(self, outfile, cpal=None, gp=None, size=(1, 1), circular=False, grformat="PDF", logger=None):
        """
        :param outfile: the intended outfile path
        :param cpal: a dict defining a color palette
        :param gp: a dict of graphic parameters
        :param circular: draws a 'circular' version of the embers; the distance to the center represents 'hazard',
                         and the coulour gradients remain identical to what they are in the 'straight ember' version;
                         this differs from a polar diagram, in which distance to the center may represent risk.
                         Circular diagrams are at alpha dev. stage for the moment.
        :param grformat:
        :param logger:
        """
        super().__init__()
        self.logger = hlp.Logger() if logger is None else logger

        if cpal:
            self.cpal = cpal
        else:
            colfile = path.join(path.dirname(hlp.__file__), "defaults/colors.xlsx")
            self.cpal = ColourPalette(colfile, prefcsys="RGB", cpalname="")
        self.csys = cpal.csys if cpal else "RGB"
        self.gp = gp if gp else param.ParamDict()  # Default graph parameters

        self.circular = circular
        self.glen = 10  # Default number of embers in the current group; needed for circular diagrams.

        # Define the drawing canvas
        self.c = canvas.get_canvas(outfile, colorsys=self.csys, size=size, grformat=grformat)  # drawing canvas
        self.colors = self.c.colors

        # fixed graphic parameters
        self.txspace = min(0.05 * self.gp['scale_x'], 1*mm)  # Spacing between tick or grid line and text
        self.lxticks = min(0.1 * self.gp['scale_x'], 2*mm)   # Length of ticks

    def isdefined(self, gpname):
        """
        Returns True if gp (Graphical Parameter) gpname is defined AND is not empty (not an empty list, etc.)
        In particulars, returns False if the gp is a blank string (' '), but True for any number, including 0.
        :param gpname: the name of the gp to check.
        :return:
        """
        if gpname not in self.gp:
            return False
        else:
            return not isempty(self.gp[gpname])

    def hx1to2(self, haz1):
        """
        Experimental service fct for the secondary axis, TBD
        :param haz1:
        :return:
        """
        return self.gp['haz_axis2_factor'] * haz1 + self.gp['haz_axis2_shift']

    def hx2to1(self, haz2):
        """
        Experimental service fct for the secondary axis, TBD
        :param haz2:
        :return:
        """
        return (haz2 - self.gp['haz_axis2_shift']) / self.gp['haz_axis2_factor']

    def add(self, cel):
        """
        Add elements (= groups or xy-plots) to the embergraph (= egr, the root graph element).
        Elements are not directly added to egr: lines of elements are created, then elements are added to them
        :param cel: a graph element (at this level, a group or plot) or list of graph elements.
        :return:
        """
        gp = self.gp

        if gp["max_gr_line"] < 1:
            raise Exception("max_gr_line must be > 0, as it is the max number of groups per line")

        if type(cel) is not list:  # Simplify the processing below by getting a list in all cases (even if one element)
            cel = [cel]
        if type(cel[0]) is Ember:  # Simplify usage by creating groups automatically if that is not done yet
            cel = getgroups(cel)

        ili: int = 0
        nuli = 1  # Number of the line within this graph
        gline = None
        nf = 0
        while ili < len(cel):
            if len(self.elements) > 0:
                # There is at least one graphline; get the number 'free seats' in it
                gline = self.elements[-1]
                nf = gline.numfree()
            if nf < 1:
                # No graphline or no free seats => create a new graphline
                grl = GraphLine(max_gr_line=gp["max_gr_line"], name=f"Line #{nuli}")
                nuli += 1
                self.elements.append(grl)
                continue
            gline.add(cel[ili: ili+nf])
            ili += nf

    def attach(self, egr=None):
        """
        All 'attach' methods 'propagate' the reference to egr to child elements (see graphbase.Element).
        In addition, when relevant,
        - bounding boxes and coordinates (graphbase.Coord) are defined for the element
        - some switches about the presence of axes, etc. may be defined to affect placement and drawing consistently
        The actions on coordinates & switches *possibly* move to specific methods, like set_cy, in the future.
        :param egr:
        :return:
        """
        super().attach()
        gp = self.gp
        mar_x1 = 0
        mar_x2 = 0
        mar_y1 = 0

        # Position the legend
        # The ember groups form a "grid". The legend can be
        # - centered at the right of the entire grid (leg_pos = right), and vertical
        # - centered under the entire grid (leg_pos = under), and horizontal
        # - inside the grid, as an additional ember group (leg_pos = in-grid-horizontal or in-grid-vertical)
        #   => this last case is delegated to the GraphLine, as it is part of it (as a "group")
        if gp('leg_pos') == "under":
            mar_y1 = gp['leg_bot_y'] + gp['leg_y'] + gp['leg_top_y']
        elif norm(gp['leg_pos']) == "right":
            mar_x2 = 16 * gp('fnt_size')  # Might be further improved; see also legend > drawlegend > ltot_x

        # Set the y-coordinate and bounding box for the lines within this Ember
        cur_y = mar_y1
        max_x = 0
        for li in reversed(self.elements):  # Traverse lines from bottom to top, because bottom is (0,0)
            cur_y = li.set_cy(cur_y)  # Sets the coordinate for this line, and gets cur_y for the next one
            max_x = max(max_x, li.cx.b1)
        max_x += gp["gr_int_x"] / 2.0

        # If the legend is under the graph, take care that it has enough width (for small graphs):
        if gp('leg_pos') == "under":
            add_x = gp['leg_x'] * 1.2 - (mar_x1 + max_x + mar_x2)
            if add_x > 0:
                mar_x2 += add_x/2
                mar_x1 += add_x/2
        else:
            add_x = 0

        self.cx = Coord(0, mar_x1, max_x, mar_x2)
        self.cy = Coord(0, mar_y1, cur_y-mar_y1, 0)

        if gp('leg_pos') == "under" and add_x > 0:
            for li in self.elements:
                li.relpos_x(self.cx.c0)

        self.c.set_page_size((self.cx.b1, self.cy.b1))

    def draw(self):
        """
        The top-level draw function
        :return:
        """
        # Attach all graphical elements (in the list of elements) to this EmberGraph before drawing
        self.attach()
        super().draw()

        # Draw legend, if it is placed at the top (EmberGraph) level
        if self.gp('leg_pos') == "right":
            drawlegend(self, self.cx.c1, self.cy.b0, self.cx.m2, self.cy.b)
        elif self.gp('leg_pos') == "under":
            drawlegend(self, self.cx.b0, self.cy.b0, self.cx.b, self.cy.m1)

        # If there were critical errors, 'stamp' the *first* critical error message on the diagram
        if self.logger.getlog("critical"):
            msg = "Critical issue! this diagram may be unreliable. Please investigate. " \
                  + self.logger.getlog("critical")[0] + " (...)"
            pp = (2 * mm, self.cy.b1 - 22 * mm)
            self.c.rect(*pp, 72 * mm, 20 * mm, fill="ltransluscent", stroke=None)
            self.c.paragraph(pp[0], pp[1] + 20 * mm, msg, font=("Helvetica", 9),
                             color="red", width=70 * mm, valign="top")

        # Set metadata: keywords = warning messages
        if len(self.logger.getlog("warning")) == 0 and len(self.logger.getlog("critical")) == 0:
            self.c.set_keywords(["No warning messages: perfect"])
            pass
        else:
            pass
            self.c.set_keywords(["Warnings: "] + self.logger.getlog("warning") + self.logger.getlog("critical")
                                + [f"Palette: {self.cpal.name}"])

        # Set other metadata
        self.c.set_creator(f"EmberMaker {__version__}")
        try:  # Inelegant way to get the group name of the first ember (until improvement of elements and groups?)
            self.c.set_title(self.elements[0].elements[0].elements[0].group[:100])
        except IndexError:
            pass
        outfile = self.c.save()

        return outfile


class GraphLine(Element):
    """
    A line of ember groups and possibly other types of diagrams.
    The graph line sets the y-coordinate for its elements.
    """
    parent_type = "EmberGraph"

    def __init__(self, max_gr_line=100, name=""):
        super().__init__()
        self.name = name
        self.maxgr = int(max_gr_line)

    def add(self, cel):
        super().add(cel)
        for el in cel:
            el.cy = self.cy  # in a line, all child elements share the same y-coordinate.

    def numfree(self) -> int:
        """
        The number of "free seats" in the graphline
        :return: # free seats
        """
        return self.maxgr - len(self.elements)

    def attach(self, egr=None):
        super().attach(egr)
        self.has_vaxis = "line-line" in egr.gp['haz_axis_grid']
        self.has_vgrid = self.has_vaxis
        self.has_axis_name = self.has_vaxis
        self.has_axis2_name = egr.gp['haz_axis2'] in ["True", "Right"] and self.has_vaxis

        # Legend, when it is an element in the GraphLine
        # Note: this is only permitted if it makes senses, i.e. there is a graph line that is not entirely filled
        if "in-grid" in egr.gp['leg_pos']:
            if len(self.elements) < egr.gp["max_gr_line"]:
                lbox = LegendBox()
                super().add(lbox)
                lbox.attach(egr)

        # Vertical axis
        # If this line has no vaxis, then the first group within this line has a vaxis:
        # (this could be done within groups, but we should 'tell' them when they are 'first in line';
        #  has we are dealing with line elements (=groups) below anyway, we kept this code here)
        self.elements[0].has_vaxis = self.elements[0].has_vaxis or not self.has_vaxis
        self.elements[0].has_axis_name = self.elements[0].has_vaxis
        self.elements[-1].has_vaxis2 = (self.elements[-1].has_vaxis2
                                        or (egr.gp['haz_axis2'] in ["True", "Right"] and not self.has_vaxis))
        self.elements[-1].has_axis2_name = self.elements[-1].has_vaxis2

        # x-coordinates and bounding box, including for the elements (groups; y for the line is set by EmberGraph)
        marg1 = self.has_vaxis * (egr.gp["haz_name_x"] + egr.gp["scale_x"])
        cur_x = marg1

        for el in self.elements:  # Loop over groups in the line
            cur_x = el.set_cx(cur_x)  # Sets the coordinate for this group, and gets cur_x for the next one

        self.cx = Coord(0, marg1, cur_x-marg1, 0)

    def set_cy(self, base_y):
        gp = self.egr.gp
        self.cy = Coord(base_y, self.egr.gp['be_bot_y'], self.egr.gp['be_y'], gp['be_top_y'], gp=gp)
        for el in self.elements:
            el.prop_cy(self.cy)  # Propagate to each group a reference to the cy coordinate/box
        return self.cy.b1  # Top of this line => for use as bottom of next line above

    def draw(self):
        # Draw the vertical axis and grid lines, if it applies to the entire line
        if self.has_vaxis or self.has_vgrid:
            vaxis(self)

        super().draw()


class ColourPalette:
    """
    Reads the color palette. Importantly, this also defines the "risk scale" (sequence of risk indexes & colours).
    The palette is defined by:
     - its color system (RGB, CMYK...): csys
     - names of risk levels associated to colors : cnames (see Excel sheet)
     - a risk level index: cdefs[0] (1D numpy array of risk indexes)
     - the color densities for each color corresponding to a risk index :
         cdefs[i] (1D numpy array of color densities for each risk index, given i=#color within the color system)
     - the set of transitions that it defines: transnames_risk is a dict linking transition names to risk levels,
         such as {"high to very high": (2, 1)}, which means that this transition extends from risk index 2 to index 2+1
    Todo: further improve this class, which is a quick conversion from the former function (getcpal)
    """

    def __init__(self, wbcol, prefcsys=None, cpalname=None, cpalinfo=None, logger=None):
        """
        Creates an EmberFactory colour palette by reading it from an Excel workbook
        :param wbcol: an Excel workbook from openpyxl, OR the name of such an Excel workbook
        :param prefcsys: a colour system choice from the user, among (RGB, CMYK, *standard);
                        'RGB' or 'CMYK' will use *default* palettes defined below;
                        'standard' means that the user makes no choice in the UI;
    -                    When 'standard' is included, it will go through several steps to get a palette, using
                        1) cpalname if set (this should come from the parameter in the spreadsheet),
                        2) 'ACTIVE-P' if it is set; if is also unavailable,
                        3) revert to the internal default (RGB-SRCCL-C7).
                        ACTIVE-P is a legacy parameter which may be provided in the 'colour' spreadsheet (read here).
                        Note: this is cluttered due to legacy support; ACTIVE-P might be dropped in the future.
        :param cpalname: the name of the desired palette, used only if the color sheet does not set 'ACTIVE-P'
        :param cpalinfo:
        :param logger:
        """
        if logger is None:
            logger = hlp.Logger()
        if type(wbcol) is str:
            wbcol = hlp.secure_open_workbook(wbcol)
        self.info = cpalinfo
        self.cnames = []
        self.csys = None
        self.cdefs = None
        read = False
        ctmp = []
        cref = 1.0  # Reference (max) value of the color range (optional parameter)
        sht = wbcol["Color definitions"]
        # Default palette (if no palette defined in the color sheet or provided as cpalname
        if prefcsys == 'RGB':  # if prefcsys is set to RGB or CMYK, it gets the priority over any parameter
            cpalname = 'RGB-SRCCL-C7'
        elif prefcsys == 'CMYK':
            cpalname = 'CMYK-IPCC'
        elif not cpalname:
            # if prefcsys did not specify a colour system and cpalname is not set,
            # then we set a default here and will overwrite it below if 'ACTIVE-P' is found
            cpalname = 'RGB-SRCCL-C7'

        for row in sht.rows:
            key = hlp.stripped(row[0].value)
            name = hlp.stripped(row[1].value)
            inda = [acell.value for acell in row[2:]]  # input data
            if key == 'ACTIVE-P' and 'standard' in prefcsys:
                cpalname = name  # ACTIVE-P is a legacy parameter
            elif key == 'PALETTE' and cpalname == name:
                logger.addinfo('Will use color palette: ' + cpalname)
                read = True
            elif key == '' or key is None:
                read = False
            elif key == 'HEADERS' and read:
                if inda[1:4] == ['Red', 'Green', 'Blue']:
                    self.csys = 'RGB'
                elif inda[1:5] == ['Cyan', 'Magenta', 'Yellow', 'Black']:
                    self.csys = 'CMYK'
                else:
                    raise Exception("Unknown color system (see colors in sheet 'Color definitions').")
            elif key == 'DATA' and read:
                self.cnames.append(name)
                ctmp.append(inda[:1 + len(self.csys)])
            elif key == 'REFERENCE' and read:
                # The "reference" is an arbitrary number that is the maximum of colour values, typically 1, 100, or 255.
                # (default value is 1, see above)
                try:
                    cref = float(inda[0])
                except ValueError:
                    raise ValueError("REFERENCE value for the colors is wrong or misplaced "
                                     "(must be 3rd col in palette definition)")
        if len(self.cnames) < 2:
            raise Exception("Colour palette '{}' could not be found or was incorrectly defined.".format(cpalname))
        cdiv = [1.0] + ([cref] * (len(ctmp[0]) - 1))  # We need to divide each line by the ref, but not element 0
        self.cdefs = (np.array(ctmp) / cdiv).transpose()  # color definitions array
        del ctmp
        logger.addinfo(f"Palette risk levels and colors: {self.cdefs}")
        self.name = cpalname

        # transnames_risk is a dict linking transition names to their (base risk level, risk level change),
        # such as {"high to very high": (2, 1)}, which means that this transition extends from index 2 to index 2+1
        self.transnames_risk = {}
        ridx = self.cdefs[0]
        for ibeg in range(len(self.cnames)-1):
            transname = norm(self.cnames[ibeg]) + " to " + norm(self.cnames[ibeg+1])
            self.transnames_risk[transname] = (ridx[ibeg], ridx[ibeg+1] - ridx[ibeg])

            # Downward risk transitions (including for increasing benefits <0 risk index)
            transname = norm(self.cnames[ibeg+1]) + " to " + norm(self.cnames[ibeg])
            self.transnames_risk[transname] = (ridx[ibeg+1], ridx[ibeg] - ridx[ibeg+1])
