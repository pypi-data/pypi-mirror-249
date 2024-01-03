from model_analyzer import analyzer  as mana
from np_reader      import np_reader as np_rdr
from logzero        import logger    as log
from rk_model       import rk_model

import rk.utilities as rkut
import math
import zfit

#---------------------------------------------
def delete_all_pars():
    d_par = zfit.Parameter._existing_params
    l_key = list(d_par.keys())

    for key in l_key:
        del(d_par[key])
#---------------------------------------------
def get_model():
    obs          = zfit.Space('x', limits=(-10, 10))
    mu           = zfit.Parameter("mu", 2.4, -1, 5)
    sg           = zfit.Parameter("sg", 1.3,  0, 5)
    ne           = zfit.Parameter('ne', 100, 0, 1000)
    gauss        = zfit.pdf.Gauss(obs=obs, mu=mu, sigma=sg)

    return gauss.create_extended(ne) 
#---------------------------------------------
def test_fit():
    model = get_model()
    
    obj                    = mana(pdf=model, d_const={'mu' : [2.4, 0.5]})
    obj.out_dir            = 'tests/model_analyzer/pulls'
    df_ini, df_val, df_err = obj.fit(nfit=10)

    delete_all_pars()
#---------------------------------------------
def test_rk():
    log.info('Getting nuisance parameters')
    rdr          = np_rdr(sys='v65', sta='v63', yld='v24')
    rdr.cache    = True
    d_eff        = rdr.get_eff()
    d_byld       = rdr.get_byields()
    d_nent       = rkut.average_byields(d_byld, l_exclude=['TIS'])
    d_rare_yld   = rkut.reso_to_rare(d_nent, kind='jpsi')

    log.info('Building model')
    mod         = rk_model(preffix='all_tos', d_eff=d_eff, d_nent=d_rare_yld, l_dset=['all_TOS'])
    mod.bdt_wp  = {'BDT_cmb' : 0.977, 'BDT_prc' : 0.480751}
    d_mod       = mod.get_model()
    d_val, d_var= mod.get_cons()
    _, mod_ee   = d_mod['all_TOS']

    d_const = { key : [val, math.sqrt(var)] for key, val, var in zip(d_val, d_val.values(), d_var.values())}

    log.info('Analyzing model')
    obj            = mana(pdf=mod_ee, d_const = d_const, nev_fac=10)
    obj.out_dir    = 'tests/model_analyzer/rk'
    df_ini, df_val, df_err = obj.fit(nfit=10)

    delete_all_pars()
#---------------------------------------------
def main():
    test_fit()
    test_rk()
#---------------------------------------------
if __name__ == '__main__':
    main()

