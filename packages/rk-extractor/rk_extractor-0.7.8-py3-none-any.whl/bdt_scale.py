import os
import re
import glob
import ROOT
import tqdm
import math
import numpy
import pprint
import pandas            as pnd
import utils_noroot      as utnr
import matplotlib.pyplot as plt
import read_selection    as rs

from importlib.resources import files
from scipy.interpolate   import griddata as spy_grid
from logzero             import logger   as log

#------------------------------------------------------------
class scale_maker:
    '''
    Class used to get and store efficiencies under different BDT working points
    '''
    #--------------------------
    def __init__(self, wp=None, step_size=None, dset=None, trig=None):
        '''
        Parameters
        --------------------------
        wp (dict): Stores working point ends for the scan, i.e. {'BDT_cmb' : (0.5, 1.0)} 
        step_size (float): Size of step to scan BDT score, e.g. 1e-2

        dset (str): Dataset, e.g. r1
        trig (str): Trigger, e.g. MTOS
        '''
        self._d_wp        = wp 
        self._step_size   = step_size
        self._dset        = dset
        self._trig        = trig

        self._xvar        = None
        self._yvar        = None
        self._cas_dir     = None
        self._out_dir     = None
        self._plt_dir     = None
        self._df_dat      = None
        self._size        = None
        self._version     = None
        self._proc        = 'sign'
        self._vers        = 'v10.21p2'
        self._jdir        = 'bdt_scales'

        self._initialized = False 
    #--------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._cas_dir = os.environ['CASDIR']
        self._check_wp()

        low_x, hig_x  = self._d_wp[self._xvar]
        low_y, hig_y  = self._d_wp[self._yvar]
        self._nstep_x = int((hig_x - low_x) / self._step_size)
        self._nstep_y = int((hig_y - low_y) / self._step_size)

        self._out_dir = files('extractor_data').joinpath(f'bdt_eff/{self._version}')
        os.makedirs(self._out_dir, exist_ok=True)

        self._plt_dir = f'{self._out_dir}/{self._dset}_{self._trig}' 
        os.makedirs(self._plt_dir, exist_ok=True)

        self._initialized = True
    #--------------------------
    def _check_wp(self):
        if len(self._d_wp) != 2:
            log.error(f'Not found only 2 variable in d_wp:')
            pprint.pprint(self._d_wp)
            raise

        self._xvar, self._yvar = self._d_wp.keys()
    #--------------------------
    def _get_data_paths(self):
        if   self._dset == 'r1':
            dat_dir_1 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2011_{self._trig}'
            dat_dir_2 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2012_{self._trig}'
            l_dat_dir = [dat_dir_1, dat_dir_2]
        elif self._dset == 'r2p1':
            dat_dir_1 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2015_{self._trig}'
            dat_dir_2 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2016_{self._trig}'
            l_dat_dir = [dat_dir_1, dat_dir_2]
        elif self._dset == 'all':
            dat_dir_1 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2011_{self._trig}'
            dat_dir_2 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2012_{self._trig}'
            dat_dir_3 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2015_{self._trig}'
            dat_dir_4 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2016_{self._trig}'
            dat_dir_5 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2017_{self._trig}'
            dat_dir_6 = f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/2018_{self._trig}'
            l_dat_dir = [dat_dir_1, dat_dir_2, dat_dir_3, dat_dir_4, dat_dir_5, dat_dir_6]
        else:
            l_dat_dir = [f'{self._cas_dir}/tools/apply_selection/{self._jdir}/{self._proc}/{self._vers}/{self._dset}_{self._trig}']

        l_l_path = [ glob.glob(f'{dat_dir}/*.root') for dat_dir in l_dat_dir ] 
        l_fpath  = [ fpath for l_path in l_l_path for fpath in l_path ]

        if len(l_fpath) == 0:
            log.error(f'No ROOT file found in: {l_dat_dir}')
            raise

        log.info(f'Picking up data from: {l_dat_dir}')

        return l_fpath
    #--------------------------
    def _get_data(self):
        l_fpath      = self._get_data_paths()
        rdf          = ROOT.RDataFrame(self._trig, l_fpath)
        rdf          = rdf.Define('year', 'int(yearLabbel)')

        l_var        = [self._xvar, self._yvar, 'year']
        d_arr        = { var : rdf.AsNumpy(l_var)[var].tolist() for var in l_var} 
        df           = pnd.DataFrame(d_arr) 
        df['weight'] = df.year.apply(self._weight_from_year)

        for var in df.columns:
            self._plot_var(var, df)

        log.info(f'Picking {self._size} entries with {l_var} vars from {len(l_fpath)} files from {self._trig}')


        self._size = df.weight.sum() 

        return df
    #--------------------------
    def _weight_from_year(self, year):
        d_lumi = {2011 : 1, 2012 : 2, 2015 : 0.3, 2016 : 1.6, 2017 : 1.7, 2018 : 2.1}

        if year not in d_lumi:
            log.error(f'Year {year} not valid')
            raise

        return d_lumi[year]
    #--------------------------
    def _get_efficiency(self, xval=None, yval=None):
        xvar, yvar = self._xvar, self._yvar

        df = self._df_dat
        df = df[df[xvar] > xval]
        df = df[df[yvar] > yval]

        npas = df.weight.sum() 
        eff  = npas / self._size

        if not (0 <= eff <= 1):
            log.error(f'Invalid efficiency: {eff:.3f} = {npas}/{self._size}')
            raise

        return eff
    #--------------------------
    def _get_efficiencies(self):
        low_x, hig_x = self._d_wp[self._xvar]
        low_y, hig_y = self._d_wp[self._yvar]

        l_xval = numpy.linspace(low_x, hig_x, num=int(self._nstep_x))
        l_yval = numpy.linspace(low_y, hig_y, num=int(self._nstep_y))

        l_xgrid= []
        l_ygrid= []
        l_zgrid= []
        for xval in tqdm.tqdm(l_xval, ascii=' -'):
            for yval in l_yval:
                zval = self._get_efficiency(xval=xval, yval=yval)
                l_xgrid.append(xval)
                l_ygrid.append(yval)
                l_zgrid.append(zval)

        df = pnd.DataFrame({self._xvar : l_xgrid, self._yvar : l_ygrid, 'Efficiency' : l_zgrid})

        return df 
    #--------------------------
    def _plot_var(self, varname, df):
        if self._out_dir is None:
            return

        plot_path = f'{self._plt_dir}/{varname}.png'

        if varname != 'weight':
            plt.hist(df[varname], weights=df.weight, bins=30)
        else:
            plt.hist(df[varname],                     bins=30)

        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------
    def _plot_eff(self, df, interpolate=None):
        if not self._out_dir:
            return

        fig = plt.figure(figsize=(15, 10))
        if interpolate:
            self._plot_interpolated(df)
        else:
            self._plot_true(df)

        plt.colorbar()
        plot_path = f'{self._plt_dir}/eff_int.png' if interpolate else f'{self._plt_dir}/eff_raw.png'
        log.info(f'Saving to: {plot_path}')
        plt.xlabel(self._xvar)
        plt.ylabel(self._yvar)
        plt.title(f'{self._dset}, {self._trig}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------
    def _plot_interpolated(self, df):
        low_x, hig_x   = self._d_wp[self._xvar]
        low_y, hig_y   = self._d_wp[self._yvar]
        grid_x, grid_y = numpy.mgrid[low_x:hig_x:1000j, low_y:hig_y:1000j]
        
        x_arr, y_arr   = df[self._xvar].values, df[self._yvar].values
        arr_point      = numpy.array([x_arr, y_arr]).T
        z_arr          = df['Efficiency'] 

        grid_z         = spy_grid(arr_point, z_arr, (grid_x, grid_y), method='cubic')
        
        plt.imshow(grid_z.T, extent=(low_x, hig_x, low_y, hig_y), origin='lower')
    #--------------------------
    def _plot_true(self, df):
        arr_xvar         = df[self._xvar].values
        arr_yvar         = df[self._yvar].values
        arr_zvar         = df['Efficiency'].values

        plt.hist2d(x=arr_xvar, y=arr_yvar, weights=arr_zvar, bins=[self._nstep_x, self._nstep_y])
    #--------------------------
    def save_efficiencies(self, version=None):
        if version is None:
            log.error(f'Invalid version: {version}')
            raise
        else:
            self._version = version

        self._initialize()

        jsn_path= f'{self._out_dir}/eff_{self._dset}_{self._trig}.json'

        if os.path.isfile(jsn_path):
            log.warning(f'Output already found, not remaking it: {jsn_path}')
            df = pnd.read_json(jsn_path)
            self._plot_eff(df, interpolate=False)
            self._plot_eff(df, interpolate=True)
            return df

        self._df_dat = self._get_data()

        df_eff = self._get_efficiencies()
        df_eff.to_json(jsn_path, indent=4)

        self._plot_eff(df_eff, interpolate=False)
        self._plot_eff(df_eff, interpolate=True)

        return df_eff
#------------------------------------------------------------
class scale_reader:
    '''
    Class used to read efficiencies under different BDT working points and
    return scale factor
    '''
    #--------------------------
    def __init__(self, wp=None, version=None, dset=None, trig=None):
        '''
        Parameters
        --------------------------
        wp (dict): Stores working point ends for the scan, i.e. {'BDT_cmb' : (0.5, 1.0)} 
        version (str): Version of efficiency file

        dset (str): Dataset, e.g. r1
        trig (str): Trigger, e.g. MTOS
        '''
        self._d_wp        = wp 
        self._dset        = dset
        self._trig        = trig
        self._vers        = version

        self._arr_bdt     = None
        self._arr_eff     = None

        self._cmb_nom     = None
        self._prc_nom     = None

        self._cmb_new     = self._d_wp['BDT_cmb'] 
        self._prc_new     = self._d_wp['BDT_prc'] 
        self._regex       = 'BDT_cmb > ([\.,\d]+) && BDT_prc > ([\.,\d]+)'

        self._initialized = False
    #--------------------------
    def _initialize(self):
        if self._initialized:
            return

        self._read_nominal_wp()
        self._load_data()

        self._initialized = True 
    #--------------------------
    def _read_nominal_wp(self):
        selection = rs.get('bdt', self._trig, q2bin='high', year = 'none')
        mch = re.match(self._regex, selection)
        if not mch:
            log.error(f'Cannot find WP in: {selection}')
            raise

        [cmb_str, prc_str] = mch.groups()

        self._cmb_nom = float(cmb_str)
        self._prc_nom = float(prc_str)

        log.debug(f'Using nominal WP: {self._cmb_nom:.3f}, {self._prc_nom:.3f}')
    #--------------------------
    def _load_data(self):
        file_path = files('extractor_data').joinpath(f'bdt_eff/{self._vers}/eff_{self._dset}_{self._trig}.json')
        if not os.path.isfile(file_path):
            log.error(f'File not found: {file_path}')
            raise

        df     = pnd.read_json(file_path)

        arr_cmb = df.BDT_cmb.values
        arr_prc = df.BDT_prc.values

        self._arr_bdt = numpy.array([arr_cmb, arr_prc]).T
        self._arr_eff = df.Efficiency.values
    #--------------------------
    def _read_eff(self, cmb=None, prc=None):
        [eff] = spy_grid(self._arr_bdt, self._arr_eff, [cmb, prc], method='cubic')

        if math.isnan(eff):
            log.error(f'Found nan efficiency at: {cmb:.3f}, {prc:.3f}')
            raise
        else:
            log.debug(f'{eff:.3f}-> [{cmb:.3f},{prc:.3f}]')

        return eff
    #--------------------------
    def get_scale(self):
        '''
        Returns
        -------------------
        scale (float): Efficiency ratio between WP and nominal.
        '''
        self._initialize()

        eff_nom = self._read_eff(cmb=self._cmb_nom, prc=self._prc_nom)
        eff_new = self._read_eff(cmb=self._cmb_new, prc=self._prc_new)
        scale   = eff_new / eff_nom
        log.debug(f'{scale:.3f}= {eff_new:.3f}/{eff_nom:.3f}')

        return scale
#------------------------------------------------------------

