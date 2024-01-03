from bdt_scale import scale_reader as scl_rdr

#------------------------------------------------
def test_simple():
    d_wp             = {}
    d_wp['BDT_prc']  = 0.481
    d_wp['BDT_cmb']  = 0.831

    obj = scl_rdr(wp=d_wp, version='v1', dset='2011', trig='ETOS')
    scl = obj.get_scale()

    print(scl)
#------------------------------------------------
def main():
    test_simple()
#------------------------------------------------
if __name__ == '__main__':
    main()

