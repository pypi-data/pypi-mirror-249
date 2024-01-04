import numpy as np
import pandas as pd


def features_icp(x, f, triples, n=16):
    vm_ic = ela.vmap.VMIC(x, f, triples)
    eps, ic, icp = vm_ic.run_all_1d(np.linspace(vm_ic._eps_min, vm_ic.eps_max, n // 2))
    return ic, icp


def features_seg(x, f, triples, n=None):
    vm = ela.VMSegment(x, f, triples)
    if n is None:  # 7 output features
        gamma, seg_p = vm.run_all(sectors=[0, 30, 45, 60, 90, 120, 135, 150, 180])
    else:
        gamma, seg_p = vm.run_all(n_sectors=n + 2)
    return seg_p[1:-1].tolist()


def features_gic(x, f, triples, n=16):
    vm_ic = ela.vmap.VMIC(x, f, triples)
    eps_values = np.linspace(vm_ic._eps_min, vm_ic.eps_max, int(np.sqrt(n)))
    return vm_ic.run_all_2d(eps_values, eps_values)[1]


def features_ic(x, f, triples, n=8):
    vm_ic = ela.vmap.VMIC(x, f, triples)
    eps_values = np.linspace(vm_ic._eps_min, vm_ic.eps_max, n // 2)
    ic_max_eps1 = [
        vm_ic.run_all_2d(eps_i, np.geomspace(vm_ic._eps_min, vm_ic.eps_max, 100))[
            1
        ].max()
        for eps_i in eps_values
    ]
    ic_max_eps2 = [
        vm_ic.run_all_2d(np.geomspace(vm_ic._eps_min, vm_ic.eps_max, 100), eps_i)[
            1
        ].max()
        for eps_i in eps_values
    ]
    return np.hstack((ic_max_eps1, ic_max_eps2)).tolist()


def features_segic(x, f, triples):
    # return features_seg(x, f, triples, n=11), features_ic(x, f, triples, n=16) # features_old analogue
    return features_seg(x, f, triples, n=None), features_ic(x, f, triples, n=8)


def features_old(x, f, triples):
    vm = ela.VMSegment(x, f, triples)
    features1 = vm.run_all(13)[1][1:-1]

    vm_ic = ela.vmap.VMIC(x, f, triples)
    eps_values = np.linspace(vm_ic._eps_min, vm_ic.eps_max, 8)
    ic1 = [
        vm_ic.run_all_2d(e, np.geomspace(vm_ic._eps_min, vm_ic.eps_max, 100))[1].max()
        for e in eps_values
    ]
    ic2 = [
        vm_ic.run_all_2d(np.geomspace(vm_ic._eps_min, vm_ic.eps_max, 100), e)[1].max()
        for e in eps_values
    ]
    features2 = np.hstack((ic1, ic2))

    return features1.tolist(), features2.tolist()
