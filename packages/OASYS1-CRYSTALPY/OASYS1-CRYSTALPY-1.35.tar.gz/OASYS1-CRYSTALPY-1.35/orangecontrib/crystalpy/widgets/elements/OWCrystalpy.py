import numpy
import sys
from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui, congruence

from oasys.widgets.exchange import DataExchangeObject
from orangecontrib.xoppy.widgets.gui.ow_xoppy_widget import XoppyWidget


import scipy.constants as codata

import xraylib
from dabax.dabax_xraylib import DabaxXraylib

from xoppylib.crystals.tools import run_diff_pat, bragg_calc2



from PyQt5 import QtGui, QtWidgets
from oasys.util.oasys_util import EmittingStream
from silx.io.specfile import SpecFile

from crystalpy.util.calc_xcrystal import calc_xcrystal_angular_scan, calc_xcrystal_energy_scan, calc_xcrystal_alphazachariasen_scan

class OWCrystalpy(XoppyWidget):
    name = "CRYSTAL"
    id = "orange.widgets.crystalpy"
    description = "Crystal Reflectivity (perfect)"
    icon = "icons/xoppy_xcrystal.png"
    priority = 500
    category = ""
    keywords = ["xoppy", "xcrystal"]


    CRYSTAL_MATERIAL_XRAYLIB = Setting(32)
    CRYSTAL_MATERIAL_DABAX = Setting(32)
    MILLER_INDEX_H = Setting(1)
    MILLER_INDEX_K = Setting(1)
    MILLER_INDEX_L = Setting(1)
    TEMPER = Setting("1.0")
    MOSAIC = Setting(0)
    GEOMETRY = Setting(0)
    SCAN = Setting(2) # ['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)']
    UNIT = Setting(1) # ['Radians', 'micro rads', 'Degrees', 'ArcSec']
    SCANFROM = Setting(-100.0)
    SCANTO = Setting(100.0)
    SCANPOINTS = Setting(200)
    ENERGY = Setting(8000.0)
    ASYMMETRY_ANGLE = Setting(0.0)
    THICKNESS = Setting(0.7)
    IS_THICK = Setting(0)

    CALCULATION_METHOD = Setting(1)
    CALCULATION_STRATEGY_FLAG = Setting(0)
    USE_TRANSFER_MATRIX = Setting(0)

    # new crystals  #todo: add to menus?
    material_constants_library_flag = Setting(0) # 0=xraylib, 1=dabax
    dx = None # DABAX object


    def __init__(self):
        super().__init__(show_script_tab=True)

    def build_gui(self):

        box = oasysgui.widgetBox(self.controlArea, self.name + " Input Parameters", orientation="vertical", width=self.CONTROL_AREA_WIDTH-5)
        
        idx = -1 
        
        #widget index 3 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL_XRAYLIB",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=self.get_crystal_list_xraylib(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        #widget index 3
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "CRYSTAL_MATERIAL_DABAX",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=self.get_crystal_list_dabax(),
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)


        #widget index 4 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_H",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 5 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_K",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 6 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "MILLER_INDEX_L",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 8 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "TEMPER",
                     label=self.unitLabels()[idx], addSpace=False, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 

        
        #widget index 10 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "GEOMETRY",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['BRAGG: diffr beam', 'LAUE: diffr beam', 'BRAGG: transm beam', 'LAUE: transm beam'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 11 
        idx += 1 
        box1 = gui.widgetBox(box) 
        gui.comboBox(box1, self, "SCAN",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 12 
        idx += 1 
        box1 = gui.widgetBox(box) 
        self.unit_combo = gui.comboBox(box1, self, "UNIT",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Radians', 'micro rads', 'Degrees', 'ArcSec'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 13 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANFROM",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 14 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANTO",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 15 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "SCANPOINTS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 16 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ENERGY",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 17 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "ASYMMETRY_ANGLE",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1) 
        
        #widget index 18 
        idx += 1 
        box1 = gui.widgetBox(box) 
        oasysgui.lineEdit(box1, self, "THICKNESS",
                     label=self.unitLabels()[idx], addSpace=False,
                    valueType=float, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)



        #
        # advanced parameters
        #
        boxAdvanced = oasysgui.widgetBox(self.controlArea, "Advanced Parameters", orientation="vertical")#, width=self.CONTROL_AREA_WIDTH-5)

        #widget index 19
        idx += 1
        box1 = gui.widgetBox(boxAdvanced)
        gui.comboBox(box1, self, "CALCULATION_METHOD",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['Zachariasen', 'Guigay'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 19b
        idx += 1
        box1 = gui.widgetBox(box)
        gui.comboBox(box1, self, "IS_THICK",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 19
        idx += 1
        box1 = gui.widgetBox(boxAdvanced)
        gui.comboBox(box1, self, "USE_TRANSFER_MATRIX",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['No', 'Yes'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 20
        idx += 1
        box1 = gui.widgetBox(boxAdvanced)
        gui.comboBox(box1, self, "material_constants_library_flag",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['xraylib', 'dabax'],
                    valueType=int, orientation="horizontal", labelWidth=250)
        self.show_at(self.unitFlags()[idx], box1)

        #widget index 21
        idx += 1
        box1 = gui.widgetBox(boxAdvanced)
        gui.comboBox(box1, self, "CALCULATION_STRATEGY_FLAG",
                     label=self.unitLabels()[idx], addSpace=False,
                    items=['mpmath', 'numpy native [to avoid]', 'numpy truncated'],
                    valueType=int, orientation="horizontal", labelWidth=150)
        self.show_at(self.unitFlags()[idx], box1)

    def unitLabels(self):
         return ['Crystal (xraylib list):','Crystal (dabax list):','h Miller index','k Miller index','l Miller index','Temperature factor [see help]:', # 0-5
                 'Geometry:','Scan:','Scan Units:','Min Scan value:','Max Scan value:','Scan Points:', # 6-12
                 'Fix value (E[eV] or Theta[deg])','Asymmetry angle [deg] (to surf.)','Crystal Thickness [cm]:', # 13-15
                 'Calculation method', 'Thick crystal approximation', 'Use transfer matrix', 'material library', 'exp,sin,cos use']


    def unitFlags(self):
         return ['self.material_constants_library_flag == 0','self.material_constants_library_flag == 1','True','True','True','True',
                 'True','True','self.SCAN  <=  2','True','True','True',
                 'True','True','True',
                 'True','self.CALCULATION_METHOD == 1','self.CALCULATION_METHOD == 1','True', 'True']

    def get_help_name(self):
        return 'crystal'

    def check_fields(self):
        self.MILLER_INDEX_H = congruence.checkNumber(self.MILLER_INDEX_H, "Miller index H")
        self.MILLER_INDEX_K = congruence.checkNumber(self.MILLER_INDEX_K, "Miller index K")
        self.MILLER_INDEX_L = congruence.checkNumber(self.MILLER_INDEX_L, "Miller index L")
        self.TEMPER = congruence.checkNumber(self.TEMPER, "Temperature factor")

        if self.SCAN == 0 or self.SCAN == 3:
            self.SCANFROM = congruence.checkPositiveNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkStrictlyPositiveNumber(self.SCANTO, "Max Scan value")
        else:
            self.SCANFROM = congruence.checkNumber(self.SCANFROM, "Min Scan value")
            self.SCANTO = congruence.checkNumber(self.SCANTO, "Max Scan value")

        congruence.checkLessThan(self.SCANFROM, self.SCANTO, "Min Scan value", "Max Scan value")
        self.SCANPOINTS = congruence.checkStrictlyPositiveNumber(self.SCANPOINTS, "Scan points")

        if self.SCAN < 4:
            self.ENERGY = congruence.checkStrictlyPositiveNumber(self.ENERGY , "Fix value")
        else:
            self.ENERGY = congruence.checkNumber(self.ENERGY , "Fix value")

        if self.MOSAIC == 0: #perfect
            self.ASYMMETRY_ANGLE = congruence.checkNumber(self.ASYMMETRY_ANGLE, "Asymmetry angle")
            self.THICKNESS = congruence.checkStrictlyPositiveNumber(self.THICKNESS, "Crystal thickness")
        else:
            raise NotImplementedError


    def get_crystal_list_xraylib(self):
        return list(xraylib.Crystal_GetCrystalsList())


    def get_crystal_list_dabax(self):
        self.dx = DabaxXraylib()
        return self.dx.Crystal_GetCrystalsList()

    def get_units_to_degrees(self):
        # SCAN = # ['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)']
        # UNIT = # ['Radians', 'micro rads', 'Degrees', 'ArcSec']
        if self.UNIT == 0:  # RADIANS
            return 180 / numpy.pi
        elif self.UNIT == 1:  # MICRORADIANS
            return 180e-6 / numpy.pi
        elif self.UNIT == 2:  # DEGREES
            return 1.0
        elif self.UNIT == 3:  # ARCSEC
            return 1/3600.0

    def get_units_to_radians(self):
        # SCAN = # ['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)']
        # UNIT = # ['Radians', 'micro rads', 'Degrees', 'ArcSec']
        if self.UNIT == 0:  # RADIANS
            return 1
        elif self.UNIT == 1:  # MICRORADIANS
            return 1e-6
        elif self.UNIT == 2:  # DEGREES
            return numpy.pi / 180
        elif self.UNIT == 3:  # ARCSEC
            return 1/3600.0 * numpy.pi / 180

    def compute(self):
        self.setStatusMessage("Running XOPPY")

        self.progressBarInit()

        if 1: # try:
            script = self.do_xoppy_calculation_script()
            # self.script_template().format_map(dict_parameters)
            self.xoppy_script.set_code(script)


            self.xoppy_output.setText("")

            sys.stdout = EmittingStream(textWritten=self.writeStdOut)

            self.progressBarSet(20)

            self.check_fields()

            # self.calculated_data = self.calculate_with_complex_amplitude_photon()

            calculation_output = self.do_xoppy_calculation()

            self.progressBarSet(50)

            # calculation_output = None

            if calculation_output is None:
                raise Exception("Xoppy gave no result")
            else:
                self.calculated_data = self.extract_data_from_xoppy_output(calculation_output)

                self.add_specific_content_to_calculated_data(self.calculated_data)

            self.setStatusMessage("Plotting Results")


            # test output

            xoppy_data = self.calculated_data.get_content("xoppy_data")

            print(">>>> xoppy_data: ", xoppy_data.shape)
            print(">>>  titles =  " , self.getTitles())
            print(">>>  xtitles = " ,  self.getXTitles())
            print(">>>  ytitles = " ,  self.getYTitles())
            print(">>>  col X = ", self.calculated_data.get_content("plot_x_col"))
            print(">>>  col Y = ", self.calculated_data.get_content("plot_y_col"))



            for index in range(0, len(self.getTitles())):
                x_index, y_index = self.getVariablesToPlot()[index]
                log_x, log_y = self.getLogPlot()[index]
                print("   >>  ", index, x_index, y_index, log_x, log_y)


            self.plot_results(self.calculated_data, progressBarValue=60)

            self.setStatusMessage("")

            self.send("xoppy_data", self.calculated_data)

        # except Exception as exception:
        #     QtWidgets.QMessageBox.critical(self, "Error",
        #                                str(exception), QtWidgets.QMessageBox.Ok)
        #     self.setStatusMessage("Error!")
        #
        #     if self.IS_DEVELOP: raise exception

        self.progressBarFinished()

    # def do_xoppy_calculation(self):
    #     # return self.xoppy_calc_xcrystal()
    #
    #     print(">>>> do_xoppy_calculation")
    #
    #     descriptor = self.get_crystal_list()[self.CRYSTAL_MATERIAL]
    #
    #     if self.material_constants_library_flag == 0:
    #         material_constants_library = xraylib
    #     elif self.material_constants_library_flag == 1:
    #         material_constants_library = self.dx
    #     elif self.material_constants_library_flag == 2:
    #         if descriptor in xraylib.Crystal_GetCrystalsList():
    #             material_constants_library = xraylib
    #         elif descriptor in self.dx.Crystal_GetCrystalsList():
    #             material_constants_library = self.dx
    #         else:
    #             raise Exception("Descriptor not found in material constants database")
    #
    #
    #     if self.SCAN == 3:  # energy scan
    #         emin = self.SCANFROM - 1
    #         emax = self.SCANTO + 1
    #     else:
    #         emin = self.ENERGY - 100.0
    #         emax = self.ENERGY + 100.0
    #
    #     estep = (emax - emin) / 500 # the preprocessor data is limited to NMAXENER=1000
    #
    #
    #
    #     #
    #     # write python script
    #     #
    #     if isinstance(material_constants_library, DabaxXraylib):
    #         material_constants_library_txt = "DabaxXraylib()"
    #     else:
    #         material_constants_library_txt = "xraylib"
    #
    #     dict_parameters = {
    #         'CRYSTAL_DESCRIPTOR': descriptor,
    #         'MILLER_INDEX_H': self.MILLER_INDEX_H,
    #         'MILLER_INDEX_K': self.MILLER_INDEX_K,
    #         'MILLER_INDEX_L': self.MILLER_INDEX_L,
    #         'TEMPER': self.TEMPER,
    #         'GEOMETRY': self.GEOMETRY,
    #         'SCAN': self.SCAN,
    #         'UNIT': self.UNIT,
    #         'SCANFROM': self.SCANFROM,
    #         'SCANTO': self.SCANTO,
    #         'SCANPOINTS': self.SCANPOINTS,
    #         'ENERGY': self.ENERGY,
    #         'ASYMMETRY_ANGLE': self.ASYMMETRY_ANGLE,
    #         'THICKNESS': self.THICKNESS,
    #         'material_constants_library_txt': material_constants_library_txt,
    #         'emin': emin,
    #         'emax': emax,
    #         'estep': estep,
    #         }
    #
    #     print(">>>", dict_parameters)
    #
    #     # script = self.script_template().format_map(dict_parameters)
    #     # self.xoppy_script.set_code(script)
    #     script = "# script"
    #
    #     return None, "diff_pat.dat", script
    #
    # def extract_data_from_xoppy_output(self, calculation_output):
    #     spec_file_name = calculation_output
    #
    #     sf = SpecFile(spec_file_name)
    #
    #     if len(sf) == 1:
    #         #load spec file with one scan, # is comment
    #         print("Loading file:  ", spec_file_name)
    #         out = numpy.loadtxt(spec_file_name)
    #         if len(out) == 0 : raise Exception("Calculation gave no results (empty data)")
    #
    #         #get labels
    #         # txt = open(spec_file_name).readlines()
    #         # tmp = [ line.find("#L") for line in txt]
    #         # itmp = numpy.where(numpy.array(tmp) != (-1))
    #         # labels = txt[int(itmp[0])].replace("#L ","").split("  ")
    #         # print("data labels: ", labels)
    #
    #         calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
    #
    #         calculated_data.add_content("xoppy_specfile", spec_file_name)
    #         calculated_data.add_content("xoppy_data", out)
    #
    #         return calculated_data
    #     else:
    #       raise Exception("File %s contains %d scans. Cannot send it as xoppy_table" % (spec_file_name, len(sf)))


    def get_data_exchange_widget_name(self):
        return "XCRYSTAL"

    def getTitles(self):
        return ["Phase_p","Phase_s","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getXTitles(self):
        """
    SCAN = Setting(2) # ['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)']
    UNIT = Setting(1) # ['Radians', 'micro rads', 'Degrees', 'ArcSec']
        """
        if self.SCAN < 3:
            return ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                    "Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]"]
        elif self.SCAN == 3:
            return ["Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]",
                    "Energy [eV]"]
        else:
            return ["y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)",
                    "y (Zachariasen)"]


    def getYTitles(self):
        return ["phase_p [rad]","phase_s [rad]","Circ. Polariz.","p-polarized reflectivity","s-polarized reflectivity"]

    def getVariablesToPlot(self):
        """
    SCAN = Setting(2) # ['Theta (absolute)', 'Th - Th Bragg (corrected)', 'Th - Th Bragg', 'Energy [eV]', 'y (Zachariasen)']
    UNIT = Setting(1) # ['Radians', 'micro rads', 'Degrees', 'ArcSec']
        """
        if self.SCAN == 3:
            return [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]
        else:
            return [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]


    def getLogPlot(self):
        return[(False, False), (False, False), (False, False), (False, False), (False, False)]

    def plot_histo(self, x, y, progressBarValue, tabs_canvas_index, plot_canvas_index, title="", xtitle="", ytitle="", log_x=False, log_y=False):
        super().plot_histo(x, y,progressBarValue, tabs_canvas_index, plot_canvas_index, title, xtitle, ytitle, log_x, log_y)

        # ALLOW FIT BUTTON HERE
        self.plot_canvas[plot_canvas_index].fitAction.setVisible(True)

        # overwrite FWHM and peak values
        if title == "s-polarized reflectivity" or title == "p-polarized reflectivity":
            t = numpy.where(y>=max(y)*0.5)
            x_left,x_right =  x[t[0][0]], x[t[0][-1]]


            self.plot_canvas[plot_canvas_index].addMarker(x_left, 0.5, legend="G1", text="FWHM=%5.2f"%(x_right-x_left),
                                                          color="pink",selectable=False, draggable=False,
                                                          symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x_right, 0.5, legend="G2", text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)

            index_ymax = numpy.argmax(y)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax], legend="G3",
                                                          text=None, color="pink",
                                                          selectable=False, draggable=False, symbol="+", constraint=None)
            self.plot_canvas[plot_canvas_index].addMarker(x[index_ymax], y[index_ymax]-0.05, legend="G4",
                                                          text="Peak=%5.2f"%(y[index_ymax]), color="pink",
                                                          selectable=False, draggable=False, symbol=None, constraint=None)

    def do_xoppy_calculation_script(self):

        import numpy



        if self.material_constants_library_flag == 0:
            crystal_name = self.get_crystal_list_xraylib()[self.CRYSTAL_MATERIAL_XRAYLIB]  # string
        else:
            crystal_name = self.get_crystal_list_dabax()[self.CRYSTAL_MATERIAL_DABAX]


        if self.SCAN in (0,1,2):
            angle_center_flag = self.SCAN
        elif self.SCAN == 3:
            pass # raise Exception("Not implemented energy scan")
        elif self.SCAN == 4:
            angle_center_flag = 1
        else:
            raise Exception("Not implemented scan")

        if self.SCAN in (0,1,2):
            fmt_dict = {
                'crystal_name'           : crystal_name,
                'thickness'              : self.THICKNESS * 1e-2,  # meters
                'miller_h'               : self.MILLER_INDEX_H,
                'miller_k'               : self.MILLER_INDEX_K,
                'miller_l'               : self.MILLER_INDEX_L,
                'asymmetry_angle'        : numpy.radians(self.ASYMMETRY_ANGLE) ,
                'energy'                 : self.ENERGY ,
                'angle_deviation_min'    : self.SCANFROM * self.get_units_to_radians(),
                'angle_deviation_max'    : self.SCANTO * self.get_units_to_radians(),
                'angle_deviation_points' : self.SCANPOINTS,
                'angle_center_flag'      : angle_center_flag,
                'calculation_method'     : self.CALCULATION_METHOD,
                'is_thick'               : self.IS_THICK,
                'use_transfer_matrix'    : self.USE_TRANSFER_MATRIX,
                'geometry_type_index'    : self.GEOMETRY,
                'get_units_to_radians'   : self.get_units_to_radians(),
                'calculation_strategy_flag': self.CALCULATION_STRATEGY_FLAG,
            }

            script_template =  """
import numpy
from crystalpy.util.calc_xcrystal import calc_xcrystal_angular_scan, calc_xcrystal_energy_scan, calc_xcrystal_alphazachariasen_scan

bunch_out_dict, diffraction_setup, deviations = calc_xcrystal_angular_scan(
    # material_constants_library_flag=self.material_constants_library_flag,
    crystal_name              = '{crystal_name:s}',
    thickness                 = {thickness:g},
    miller_h                  = {miller_h},
    miller_k                  = {miller_k},
    miller_l                  = {miller_l},
    asymmetry_angle           = {asymmetry_angle},
    energy                    = {energy},
    angle_deviation_min       = {angle_deviation_min:g},
    angle_deviation_max       = {angle_deviation_max:g},
    angle_deviation_points    = {angle_deviation_points},
    angle_center_flag         = {angle_center_flag},
    calculation_method        = {calculation_method}, # 0=Zachariasen, 1=Guigay
    is_thick                  = {is_thick},
    use_transfer_matrix       = {use_transfer_matrix},
    geometry_type_index       = {geometry_type_index},
    calculation_strategy_flag = {calculation_strategy_flag}, # 0=mpmath 1=numpy 2=numpy-truncated
            )

tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
tmp[:, 0] = deviations / {get_units_to_radians}
tmp[:, 1] = {energy}
tmp[:, 2] = bunch_out_dict["phaseP"]
tmp[:, 3] = bunch_out_dict["phaseS"]
# tmp[:, 4] = circular polarization
tmp[:, 5] = bunch_out_dict["intensityP"]
tmp[:, 6] = bunch_out_dict["intensityS"]

from srxraylib.plot.gol import plot
plot(tmp[:,0], tmp[:,6], tmp[:,0], tmp[:,5], xtitle="angle", legend=["S-pol","P-pol"])

"""

        elif self.SCAN == 3: # energy scan
            fmt_dict = {
                'crystal_name'           : crystal_name,
                'thickness'              : self.THICKNESS * 1e-2,  # meters
                'miller_h'               : self.MILLER_INDEX_H,
                'miller_k'               : self.MILLER_INDEX_K,
                'miller_l'               : self.MILLER_INDEX_L,
                'asymmetry_angle'        : numpy.radians(self.ASYMMETRY_ANGLE) ,
                'energy'                 : self.ENERGY,
                'energy_min'             : self.SCANFROM,
                'energy_max'             : self.SCANTO,
                'energy_points'          : self.SCANPOINTS,
                'theta'                  : numpy.radians(self.ENERGY),
                'calculation_method'     : self.CALCULATION_METHOD,
                'is_thick'               : self.IS_THICK,
                'use_transfer_matrix'    : self.USE_TRANSFER_MATRIX,
                'geometry_type_index'    : self.GEOMETRY,
                'get_units_to_radians'   : self.get_units_to_radians(),
                'calculation_strategy_flag': self.CALCULATION_STRATEGY_FLAG,
            }
            script_template = """
import numpy
from crystalpy.util.calc_xcrystal import calc_xcrystal_angular_scan, calc_xcrystal_energy_scan, calc_xcrystal_alphazachariasen_scan

bunch_out_dict, diffraction_setup, energies = calc_xcrystal_energy_scan(
    # material_constants_library_flag=self.material_constants_library_flag,
    crystal_name           = '{crystal_name:s}',
    thickness              = {thickness:g},
    miller_h               = {miller_h},
    miller_k               = {miller_k},
    miller_l               = {miller_l},
    asymmetry_angle        = {asymmetry_angle},
    energy_min             = {energy_min},
    energy_max             = {energy_max},
    energy_points          = {energy_points},
    theta                  = {theta},
    calculation_method     = {calculation_method},  # 0=Zachariasen, 1=Guigay
    is_thick               = {is_thick},
    use_transfer_matrix    = {use_transfer_matrix},
    geometry_type_index    = {geometry_type_index},
    calculation_strategy_flag = {calculation_strategy_flag}, # 0=mpmath 1=numpy 2=numpy-truncated
)

tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
tmp[:, 0] = numpy.radians({energy})
tmp[:, 1] = energies
tmp[:, 2] = bunch_out_dict["phaseP"]
tmp[:, 3] = bunch_out_dict["phaseS"]
# tmp[:, 4] = circular polarization
tmp[:, 5] = bunch_out_dict["intensityP"]
tmp[:, 6] = bunch_out_dict["intensityS"]

from srxraylib.plot.gol import plot
plot(tmp[:,1], tmp[:,6], tmp[:,1], tmp[:,5], xtitle="Photon energy [eV]", legend=["S-pol","P-pol"])

"""

        elif self.SCAN == 4:  # alpha zachariasen scan
            fmt_dict = {
                'crystal_name'           : crystal_name,
                'thickness'              : self.THICKNESS * 1e-2,  # meters
                'miller_h'               : self.MILLER_INDEX_H,
                'miller_k'               : self.MILLER_INDEX_K,
                'miller_l'               : self.MILLER_INDEX_L,
                'asymmetry_angle'        : numpy.radians(self.ASYMMETRY_ANGLE) ,
                'energy'                 : self.ENERGY ,
                'angle_deviation_min'    : self.SCANFROM,
                'angle_deviation_max'    : self.SCANTO,
                'angle_deviation_points' : self.SCANPOINTS,
                'calculation_method'     : self.CALCULATION_METHOD,
                'is_thick'               : self.IS_THICK,
                'use_transfer_matrix'    : self.USE_TRANSFER_MATRIX,
                'geometry_type_index'    : self.GEOMETRY,
                'get_units_to_radians'   : self.get_units_to_radians(),
                'calculation_strategy_flag': self.CALCULATION_STRATEGY_FLAG,
            }
            script_template = """
import numpy
from crystalpy.util.calc_xcrystal import calc_xcrystal_angular_scan, calc_xcrystal_energy_scan, calc_xcrystal_alphazachariasen_scan


bunch_out_dict, diffraction_setup, deviations = calc_xcrystal_alphazachariasen_scan(
    # material_constants_library_flag=self.material_constants_library_flag,
    crystal_name           = '{crystal_name:s}',
    thickness              = {thickness:g},
    miller_h               = {miller_h},
    miller_k               = {miller_k},
    miller_l               = {miller_l},
    asymmetry_angle        = {asymmetry_angle},
    energy                 = {energy},
    angle_deviation_min    = {angle_deviation_min},
    angle_deviation_max    = {angle_deviation_max},
    angle_deviation_points = {angle_deviation_points},
    calculation_method     = {calculation_method},  # 0=Zachariasen, 1=Guigay
    is_thick               = {is_thick},
    use_transfer_matrix    = {use_transfer_matrix},
    geometry_type_index    = {geometry_type_index},
    calculation_strategy_flag = {calculation_strategy_flag}, # 0=mpmath 1=numpy 2=numpy-truncated
)

tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
tmp[:, 0] = deviations
tmp[:, 1] = {energy}
tmp[:, 2] = bunch_out_dict["phaseP"]
tmp[:, 3] = bunch_out_dict["phaseS"]
# tmp[:, 4] = circular polarization
tmp[:, 5] = bunch_out_dict["intensityP"]
tmp[:, 6] = bunch_out_dict["intensityS"]

from srxraylib.plot.gol import plot
plot(tmp[:,0], tmp[:,6], tmp[:,0], tmp[:,5], xtitle="y", legend=["S-pol","P-pol"])

"""
        else:
            raise NotImplementedError

        script = script_template.format_map(fmt_dict)
        return script

    def do_xoppy_calculation(self):

        import numpy



        if self.material_constants_library_flag == 0:
            crystal_name = self.get_crystal_list_xraylib()[self.CRYSTAL_MATERIAL_XRAYLIB]  # string
        else:
            crystal_name = self.get_crystal_list_dabax()[self.CRYSTAL_MATERIAL_DABAX]


        if self.SCAN in (0,1,2):
            angle_center_flag = self.SCAN
        elif self.SCAN == 3:
            pass # raise Exception("Not implemented energy scan")
        elif self.SCAN == 4:
            angle_center_flag = 1
        else:
            raise Exception("Not implemented scan")

        if self.SCAN in (0,1,2):
            bunch_out_dict, diffraction_setup, deviations = calc_xcrystal_angular_scan(
                # material_constants_library_flag=self.material_constants_library_flag,
                crystal_name           = crystal_name,
                thickness              = self.THICKNESS * 1e-2,  # meters
                miller_h               = self.MILLER_INDEX_H,
                miller_k               = self.MILLER_INDEX_K,
                miller_l               = self.MILLER_INDEX_L,
                asymmetry_angle        = numpy.radians(self.ASYMMETRY_ANGLE) ,
                energy                 = self.ENERGY ,
                angle_deviation_min    = self.SCANFROM * self.get_units_to_radians(),
                angle_deviation_max    = self.SCANTO * self.get_units_to_radians(),
                angle_deviation_points = self.SCANPOINTS,
                angle_center_flag      = angle_center_flag,
                calculation_method     = self.CALCULATION_METHOD,
                is_thick               = self.IS_THICK,
                use_transfer_matrix    = self.USE_TRANSFER_MATRIX,
                geometry_type_index    = self.GEOMETRY,
                calculation_strategy_flag = self.CALCULATION_STRATEGY_FLAG,
            )
            return bunch_out_dict, diffraction_setup, deviations
        elif self.SCAN == 3: # energy scan
            bunch_out_dict, diffraction_setup, energies = calc_xcrystal_energy_scan(
                # material_constants_library_flag=self.material_constants_library_flag,
                crystal_name           = crystal_name,
                thickness              = self.THICKNESS * 1e-2,  # meters
                miller_h               = self.MILLER_INDEX_H,
                miller_k               = self.MILLER_INDEX_K,
                miller_l               = self.MILLER_INDEX_L,
                asymmetry_angle        = numpy.radians(self.ASYMMETRY_ANGLE) ,
                energy_min             = self.SCANFROM,
                energy_max             = self.SCANTO,
                energy_points          = self.SCANPOINTS,
                theta                  = numpy.radians(self.ENERGY),
                calculation_method     = self.CALCULATION_METHOD,
                is_thick               = self.IS_THICK,
                use_transfer_matrix    = self.USE_TRANSFER_MATRIX,
                geometry_type_index    = self.GEOMETRY,
                calculation_strategy_flag = self.CALCULATION_STRATEGY_FLAG,
            )
            return bunch_out_dict, diffraction_setup, energies
        elif self.SCAN == 4:  # alpha zachariasen scan
            bunch_out_dict, diffraction_setup, deviations = calc_xcrystal_alphazachariasen_scan(
                # material_constants_library_flag=self.material_constants_library_flag,
                crystal_name           = crystal_name,
                thickness              = self.THICKNESS * 1e-2,  # meters
                miller_h               = self.MILLER_INDEX_H,
                miller_k               = self.MILLER_INDEX_K,
                miller_l               = self.MILLER_INDEX_L,
                asymmetry_angle        = numpy.radians(self.ASYMMETRY_ANGLE) ,
                energy                 = self.ENERGY ,
                angle_deviation_min    = self.SCANFROM,
                angle_deviation_max    = self.SCANTO,
                angle_deviation_points = self.SCANPOINTS,
                calculation_method     = self.CALCULATION_METHOD,
                is_thick               = self.IS_THICK,
                use_transfer_matrix    = self.USE_TRANSFER_MATRIX,
                geometry_type_index    = self.GEOMETRY,
                calculation_strategy_flag = self.CALCULATION_STRATEGY_FLAG,
            )
            return bunch_out_dict, diffraction_setup, deviations
        else:
            raise NotImplementedError



    def extract_data_from_xoppy_output(self, calculation_output):

        #
        # encapsulate output
        #
        calculated_data = DataExchangeObject("XOPPY", self.get_data_exchange_widget_name())
        calculated_data.add_content("plot_y_col", -1)
        calculated_data.add_content("scan_type", self.SCAN)

        if self.SCAN in (0,1,2):
            bunch_out_dict, diffraction_setup, deviations = calculation_output

            tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
            tmp[:, 0] = deviations / self.get_units_to_radians()
            tmp[:, 1] = self.ENERGY
            tmp[:, 2] = bunch_out_dict["phaseP"]
            tmp[:, 3] = bunch_out_dict["phaseS"]
            tmp[:, 4] = 2 * numpy.sqrt(bunch_out_dict["intensityP"] * bunch_out_dict["intensityS"]) * numpy.sin(bunch_out_dict["phaseP"] - bunch_out_dict["phaseS"])
            tmp[:, 5] = bunch_out_dict["intensityP"]
            tmp[:, 6] = bunch_out_dict["intensityS"]

            if self.SCAN in (1, 2):
                wavelength = codata.h * codata.c / codata.e / self.ENERGY * 1e2  # cm
                dspacing = diffraction_setup.dSpacingSI()  # todo float(bragg_dictionary["dspacing"])

                calculated_data.add_content("bragg_angle", numpy.degrees(numpy.arcsin(wavelength / (2 * dspacing))))
                calculated_data.add_content("asymmetry_angle", self.ASYMMETRY_ANGLE)

            calculated_data.add_content("plot_x_col", 0)

        elif self.SCAN == 3: # energy scan
            bunch_out_dict, diffraction_setup, energies = calculation_output

            tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
            tmp[:, 0] = numpy.radians(self.ENERGY)
            tmp[:, 1] = energies
            tmp[:, 2] = bunch_out_dict["phaseP"]
            tmp[:, 3] = bunch_out_dict["phaseS"]
            # tmp[:, 4] = circular polarization
            tmp[:, 5] = bunch_out_dict["intensityP"]
            tmp[:, 6] = bunch_out_dict["intensityS"]

            calculated_data.add_content("plot_x_col", 1)

        elif self.SCAN == 4:  # alpha zachariasen scan
            bunch_out_dict, diffraction_setup, deviations = calculation_output

            tmp = numpy.zeros((bunch_out_dict["energies"].size,7))
            tmp[:, 0] = deviations
            tmp[:, 1] = self.ENERGY
            tmp[:, 2] = bunch_out_dict["phaseP"]
            tmp[:, 3] = bunch_out_dict["phaseS"]
            # tmp[:, 4] = circular polarization
            tmp[:, 5] = bunch_out_dict["intensityP"]
            tmp[:, 6] = bunch_out_dict["intensityS"]

            calculated_data.add_content("plot_x_col", 0)

        calculated_data.add_content("xoppy_data", tmp)
        calculated_data.add_content("units_to_degrees", self.get_units_to_degrees())
        calculated_data.add_content("labels",
                                    ["Th-ThB{in} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                     "Th-ThB{out} [" + self.unit_combo.itemText(self.UNIT) + "]",
                                     "phase_p[rad]",
                                     "phase_s[rad]", "Circ Polariz",
                                     "p-polarized reflectivity",
                                     "s-polarized reflectivity"])
        calculated_data.add_content("info", "info blah blah")

        return calculated_data


if __name__ == "__main__":
    # calc_xcrystal_angular_scan()


    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = OWCrystalpy()
    w.show()
    app.exec()
    w.saveSettings()
