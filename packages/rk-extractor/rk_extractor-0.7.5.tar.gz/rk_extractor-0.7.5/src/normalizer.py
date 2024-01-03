from logzero import logger as log

import os
import glob
import ROOT
import math
import numpy
import pprint
import utils_noroot      as utnr
import zutils.utils      as zut
import matplotlib.pyplot as plt

from zutils.plot   import plot     as zfp
from fitter        import zfitter

#--------------------------------------
class normalizer:
    '''
    Class used to find normalizations for combinatorial and PRec components
    in the high-q2 signal model
    '''
    #--------------------------------------
    def __init__(self, dset=None, trig=None, model=None, d_val=None, d_var=None):
        self._dset    = dset
        self._trig    = trig
        self._model   = model 
        self._d_val   = d_val
        self._d_var   = d_var

        self._l_flt_par= ['lm_cb', 'mu_cb', 'ncb', 'npr_ee']
        self._dat_path = f'{os.environ["CASDIR"]}/tools/apply_selection/blind_fits/data/v10.21p2'

        self._d_const  = {}
        self._nbins    = 60
        self._hig_mm   = 5360, 5600
        self._low_mm   = 5180, 5200 
        self._hig_ee   = 5450, 5950 
        self._low_ee   = 4450, 5000 

        self._out_dir     = None
        self._d_bdt_wp    = None
        self._initialized = False 
    #--------------------------------------
    def _initialize(self):
        if self._initialized:
            return

        os.makedirs(f'{self._out_dir}/pdf', exist_ok=True)
        self._d_const= self._prepare_model(self._model)

        self._initialized = True 
    #--------------------------------------
    @property
    def bdt_wp(self):
        return self._d_bdt_wp

    @bdt_wp.setter
    def bdt_wp(self, value):
        '''
        If used, will use a new WP for the sideband data 

        Parameters:
        value (dict): Dictionary mapping BDT to new WP, e.g. {'BDT_cmb' : 0.1, 'BDT_prc' : 0.6}
        '''
        self._d_bdt_wp = value
    #--------------------------------------
    def _get_data_paths(self):
        if   self._dset == 'r1':
            l_dset = [f'{self._dat_path}/2011_{self._trig}', f'{self._dat_path}/2012_{self._trig}']
        elif self._dset == 'r2p1':
            l_dset = [f'{self._dat_path}/2015_{self._trig}', f'{self._dat_path}/2016_{self._trig}']
        elif self._dset == 'all':
            l_dset = [f'{self._dat_path}/{year}_{self._trig}' for year in [2011, 2012, 2015, 2016, 2017, 2018] ]
        else:
            l_dset = [f'{self._dat_path}/{self._dset}_{self._trig}']

        l_wc = [f'{dset}/*.root' for dset in l_dset]

        l_l_path = [ glob.glob(wc) for wc in l_wc ]
        for l_path, wc in zip(l_l_path, l_wc):
            if len(l_path) == 0:
                log.error(f'No file found in {wc}')
                raise

        return l_wc
    #-------------------------------------
    def _filter(self, rdf):
        if self._d_bdt_wp is None:
            log.info('Using nominal BDT WP')
            return rdf
        else:
            log.info('Updating BDT WP')
            pprint.pprint(self._d_bdt_wp)

        cmb_wp = self._d_bdt_wp['BDT_cmb']
        prc_wp = self._d_bdt_wp['BDT_prc']

        rdf = rdf.Filter(f'BDT_cmb > {cmb_wp}', 'CMB')
        rdf = rdf.Filter(f'BDT_prc > {prc_wp}', 'PRC')

        rep = rdf.Report()
        rep.Print()

        return rdf
    #-------------------------------------
    def _get_mass(self, l_dpath):
        rdf = ROOT.RDataFrame(self._trig, l_dpath)
        rdf = self._filter(rdf)

        arr_mass = rdf.AsNumpy(['B_M'])['B_M']

        if self._trig != 'MTOS':
            low, high   = self._low_ee[1], self._hig_ee[0]
            arr_mass_lo = arr_mass[(arr_mass < low)]
            arr_mass_hi = arr_mass[(arr_mass > hig)]

            arr_mass_cn = arr_mass[(arr_mass > low) & (arr_mass < hig)]
            arr_mass_cn = numpy.random.uniform(low=low, high=hig, size=arr_mass_cn.shape)

            arr_mass = numpy.concatenate([arr_mass_lo, arr_mass_cn, arr_mass_hi])
        else:
            log.warning(f'Unblinding: {self._trig}')

        return arr_mass
    #--------------------------------------
    def _get_data(self):
        dat_path = f'{self._out_dir}/data/{self._dset}_{self._trig}.json'
        if os.path.isfile(dat_path):
            log.info(f'Loading cached data from: {dat_path}')
            l_dat = utnr.load_json(dat_path)
            return numpy.array(l_dat)

        os.makedirs(f'{self._out_dir}/data', exist_ok=True)

        l_dpath = self._get_data_paths()
        arr_dat = self._get_mass(l_dpath)

        log.info(f'Saving to: {dat_path}')
        utnr.dump_json(arr_dat.tolist(), dat_path) 
        self._plot_data(arr_dat)

        return arr_dat
    #--------------------------------------
    def _plot_data(self, arr_mass):
        if not self._out_dir:
            return

        rng_ee = 4800, 6000
        rng_mm = 5100, 5600
        rng = rng_mm if self._trig == 'MTOS' else rng_ee
        plt.hist(arr_mass, range=rng, bins=50, histtype='step')
        plot_path = f'{self._out_dir}/data/{self._dset}_{self._trig}.png'
        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------------------
    def _prepare_model(self, pdf):
        s_par = pdf.get_params()
        for par in s_par:
            par.floating = False

        d_const = {}
        for par in s_par:
            for flt_par in self._l_flt_par:
                if par.name.startswith(flt_par):
                    par.floating = True
                else:
                    continue

                if par.name in self._d_val:
                    var = self._d_var[par.name]
                    val = self._d_val[par.name]
                    d_const[par.name] = val, math.sqrt(var)

        return d_const
    #--------------------------------------
    @property
    def out_dir(self):
        return self._out_dir

    @out_dir.setter
    def out_dir(self, value):
        try:
            os.makedirs(value, exist_ok=True)
        except:
            log.error(f'Cannot create directory: {value}')
            raise

        self._out_dir = value
    #--------------------------------------
    def _plot_fit(self, data=None, name=None, result=None, l_range=None, stacked=None):
        if self._trig == 'MTOS':
            l_range = None
            log.warning(f'Plotting unblinded data for {self._trig}')

        obj= zfp(data=data, model=self._model, result=result)
        obj.plot(nbins=self._nbins, ranges=l_range, stacked=stacked)

        if   '_all_' not in name and 'MTOS' in name:
            obj.axs[0].set_ylim(0,  70)
        elif '_all_' not in name and 'ETOS' in name:
            obj.axs[0].set_ylim(0,  30)
        elif '_all_' not in name and 'GTIS' in name:
            obj.axs[0].set_ylim(0,  20)

        obj.axs[1].set_ylim(-5, 5)
        obj.axs[1].axhline(0, color='r')

        os.makedirs(f'{self._out_dir}/fits', exist_ok=True)
        plot_path = f'{self._out_dir}/fits/{name}.png'
        log.info(f'Saving to: {plot_path}')
        plt.savefig(plot_path)
        plt.close('all')
    #--------------------------------------
    def get_fit_result(self):
        self._initialize()

        arr_mass= self._get_data()

        low   = self._low_mm if self._trig == 'MTOS' else self._low_ee
        hig   = self._hig_mm if self._trig == 'MTOS' else self._hig_ee

        zut.print_pdf(self._model, txt_path=f'{self._out_dir}/pdf/pre_{self._dset}_{self._trig}.txt', d_const=self._d_const)
        obj   = zfitter(self._model, arr_mass)
        res   = obj.fit(ranges=[low, hig], d_const=self._d_const)
        zut.print_pdf(self._model, txt_path=f'{self._out_dir}/pdf/pos_{self._dset}_{self._trig}.txt', d_const=self._d_const)

        self._plot_fit(data=arr_mass, name=f'{self._trig}_{self._dset}_stk', result=res, l_range=[low, hig], stacked= True)
        self._plot_fit(data=arr_mass, name=f'{self._trig}_{self._dset}_ovr', result=res, l_range=[low, hig], stacked=False)

        res.hesse()
        res.freeze()
        print(res)

        return res
#--------------------------------------

