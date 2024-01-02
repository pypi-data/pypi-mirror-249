import ROOT
import zfit
import numpy
import math

from rk_model    import rk_model
from logzero     import logger    as log
from mc_reader   import mc_reader as mc_rdr
from np_reader   import np_reader as np_rdr
from cs_reader   import cs_reader as cs_rdr
from zutils.plot import plot      as zfp

import matplotlib.pyplot as plt
import zutils.utils      as zut
import rk.utilities      as rkut
import pytest
import pprint
import os

#------------------------------------
def plot(shape, label, mass_window=(4500, 6000), d_const=None):
    plot_dir = f'tests/rk_model/{label}'
    os.makedirs(plot_dir, exist_ok=True)

    obj   = zfp(data=shape.arr_mass, model=shape)
    obj.plot(nbins=50, stacked=True)

    log.info(f"saving plot to {plot_dir}/pdf.png")
    plt.savefig(f'{plot_dir}/pdf.png')
    plt.close()

    zut.print_pdf(shape, d_const=d_const, txt_path=f'{plot_dir}/pdf.txt')
#-----------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#----------------------------------------------------
def rename_keys(d_data, use_txs=True):
    d_rename = {}
    if use_txs:
        d_rename[  'r1_TOS'] = d_data['d1']
        d_rename[  'r1_TIS'] = d_data['d1']

        d_rename['r2p1_TOS'] = d_data['d2']
        d_rename['r2p1_TIS'] = d_data['d2']

        d_rename['2017_TOS'] = d_data['d3']
        d_rename['2017_TIS'] = d_data['d3']

        d_rename['2018_TOS'] = d_data['d4']
        d_rename['2018_TIS'] = d_data['d4']
    else:
        d_rename[  'r1']     = d_data['d1']
        d_rename['r2p1']     = d_data['d2']
        d_rename['2017']     = d_data['d3']
        d_rename['2018']     = d_data['d4']

    return d_rename
#-----------------------------
def skip_test():
    try:
        uname = os.environ['USER']
    except:
        pytest.skip()

    if uname in ['angelc', 'campoverde']:
        return

    pytest.skip()
#----------------------
def test_simple():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='simple', d_eff=d_eff, d_nent=d_nent, l_dset=['all_TOS', 'all_TIS'])
    mod.out_dir = 'tests/rk_model/simple'
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def test_all_tos():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='all_tos', d_eff=d_eff, d_nent=d_nent, l_dset=['all_TOS'])
    d_mod       = mod.get_model()
    d_val, d_var= mod.get_cons()
    _, mod_ee   = d_mod['all_TOS']

    mod_ee.arr_mass = mod_ee.create_sampler(fixed_params=False)

    d_const = { key : [val, math.sqrt(var)] for key, val, var in zip(d_val, d_val.values(), d_var.values())}

    plot(mod_ee, 'all_tos', d_const=d_const)

    delete_all_pars()
#----------------------
def test_wp():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e4, 'd2' :          1e4, 'd3' :          1e4, 'd4' :          1e4}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='wp_ap', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    mod.bdt_wp  = {'BDT_cmb' : 0.9, 'BDT_prc' : 0.7}
    mod.out_dir = 'tests/rk_model/wp/ap'
    d_mod       = mod.get_model()

    delete_all_pars()

    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e4, 'd2' :          1e4, 'd3' :          1e4, 'd4' :          1e4}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='wp_no', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    mod.out_dir = 'tests/rk_model/wp/no'
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def test_kind():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='kind', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    mod.kind    = 'cmb_ee:use_etos'
    mod.out_dir = 'tests/rk_model/kind'
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def test_all_years():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='allyears', d_eff=d_eff, d_nent=d_nent, l_dset=['all_TOS'])
    mod.out_dir = 'tests/rk_model/all_years'
    d_mod       = mod.get_model()

    delete_all_pars()
#----------------------
def test_data():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='data', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    d_mod       = mod.get_data()

    delete_all_pars()
#----------------------
def test_rseed():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}
    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod_1   = rk_model(preffix='data1', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    d_dat_1 = mod_1.get_data(rseed=0)

    mod_2   = rk_model(preffix='data2', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    d_dat_2 = mod_2.get_data(rseed=0)

    plt_dir = f'tests/rk_model/rseed'
    os.makedirs(plt_dir, exist_ok=True)
    for index in [0, 1]:
        kind = 'mm' if index == 0 else 'ee'
        for key in d_dat_1:
            arr_dat_1 = d_dat_1[key][index].numpy().flatten()
            arr_dat_2 = d_dat_2[key][index].numpy().flatten()

            close = numpy.allclose(arr_dat_1, arr_dat_2, atol=1e-5)
            assert(close)

            min_x, max_x = min(arr_dat_1), max(arr_dat_1)

            plt.hist(arr_dat_1, bins=30, range=(min_x, max_x), histtype='step', linestyle='-', label='First')
            plt.hist(arr_dat_2, bins=30, range=(min_x, max_x), histtype='step', linestyle=':', label='Second')
            plt.legend()
            plt.savefig(f'{plt_dir}/{key}_{kind}.png')
            plt.close('all')

    delete_all_pars()
#----------------------
def test_cons():
    d_eff = {'d1' :   (0.5, 0.4), 'd2' :   (0.4, 0.3), 'd3' :   (0.3, 0.2), 'd4' :   (0.2, 0.1)}
    d_nent= {'d1' :          1e3, 'd2' :          1e3, 'd3' :          1e3, 'd4' :          1e3}

    d_eff =rename_keys(d_eff)
    d_nent=rename_keys(d_nent, use_txs=False)

    mod         = rk_model(preffix='cons', d_eff=d_eff, d_nent=d_nent, l_dset=['2018_TOS'])
    d_mod       = mod.get_cons()

    delete_all_pars()
#----------------------
def main():
    test_all_tos()
    test_simple()
    test_kind()
    test_wp()
    test_data()
    test_cons()
    test_rseed()
    test_all_years()
#----------------------
if __name__ == '__main__':
    main()

