import numpy as np
from compression.lpc.cameo import simplify_by_sip, simplify_by_sip_cr
from compression.lpc.vw import simplify_by_vw
from compression.lpc.pip import simplify_by_pip
from compression.lpc.tp import simplify_by_tp
from compression.lpc.swab import swab, bottom_up
from compression.hpc.hp_agg_cameo import simplify_by_agg_sip
from compression.hpc.hp_agg_pip import simplify_by_agg_pip
from compression.hpc.hp_agg_tp import simplify_by_agg_tp
from compression.hpc.hp_agg_vw import simplify_by_agg_vw
from compression.fgc.fg_agg_cameo import simplify_by_fg_agg_sip
from compression.fgc.fg_cameo import simplify_by_fg_sip, simplify_by_fg_sip_cr



def compute_error(args):
    x_1, x_2, function, raw_acf, dist = args
    return dist(raw_acf, function(x_1, x_2))


class LineSimplification(object):
    sip_error_bounds = np.round(np.concatenate([np.linspace(0.001, 0.09, 5), np.linspace(0.01, 0.1, 10)]), 3)
    agg_sip_error_bounds = np.round(np.concatenate([np.linspace(0.0001, 0.0009, 5), np.linspace(0.001, 0.01, 5)]), 4)
    solar_sip_error_bounds = np.round(np.concatenate([np.linspace(0.00001, 0.00009, 5), np.linspace(0.0001, 0.001, 5)]), 5)
    pedestrian_mae_error_bounds = np.round([0.001, 0.003, 0.005, 0.007, 0.01], 4)
    pedestrian_rmse_error_bounds = np.round([1e-6, 3e-6, 5e-6, 1e-7, 1e-5], 4)
    pedestrian_cheb_error_bounds = np.round([0.01, 0.03, 0.05, 0.07, 0.1], 4)
    name_map_coef = {'ped_mae_cameo': pedestrian_mae_error_bounds, 'ped_rmse_cameo': pedestrian_rmse_error_bounds, 'ped_cheb_cameo': pedestrian_cheb_error_bounds}
    targets = []

    def __init__(self):
        self.x = None
        self.n = None
        self.target = None
        self.min_cr = None
        self.error_bound = None
        self.kappa = None
        self.threads = None
        self.nlags = None
        self.blocking = None
        self.no_removed_indices = None
        self.swab_windows_size = 0.5

    def set_target(self, target):
        self.target = target

    def simplify_vw(self):
        self.no_removed_indices = simplify_by_vw(self.x[:, 0].astype(int), 
                                                 self.x[:, 1], 
                                                 self.nlags, 
                                                 self.error_bound)

    def simplify_pip(self):
        self.no_removed_indices = simplify_by_pip(self.x[:, 1], 
                                                  self.nlags, 
                                                  self.error_bound)

    def simplify_tp(self):
        self.no_removed_indices = simplify_by_tp(self.x[:, 1], 
                                                 self.nlags, 
                                                 self.error_bound)

    def simplify_sip(self):
        self.no_removed_indices = simplify_by_sip(self.x[:, 1], 
                                                  self.blocking, 
                                                  self.nlags, 
                                                  self.error_bound)
    
    def simplify_mae_sip(self):
        self.no_removed_indices = simplify_by_sip(self.x[:, 1], 
                                                  int(100*np.log(self.x.shape[0])), 
                                                  self.nlags, 
                                                  self.error_bound)
    
    def simplify_rmse_sip(self):
        self.no_removed_indices = simplify_by_rmse_sip(self.x[:, 1], 
                                                       int(100*np.log(self.x.shape[0])), 
                                                       self.nlags, 
                                                       self.error_bound)
    
    def simplify_cheb_sip(self):
        self.no_removed_indices = simplify_by_cheb_sip(self.x[:, 1], 
                                                       int(100*np.log(self.x.shape[0])), 
                                                       self.nlags, 
                                                       self.error_bound)
        
    def simplify_fgc_sip_cr(self):
        self.no_removed_indices = simplify_by_fg_sip_cr(self.x[:, 1], 
                                                        self.blocking, 
                                                        self.nlags, 
                                                        self.min_cr, 
                                                        self.threads)

    def simplify_lpc_sip_cr(self):
        self.no_removed_indices = simplify_by_sip_cr(self.x[:, 1], 
                                                        self.blocking, 
                                                        self.nlags, 
                                                        self.min_cr) 

    def simplify_agg_sip(self):
        self.no_removed_indices = simplify_by_agg_sip(self.x[:, 1], 
                                                      self.blocking, 
                                                      self.nlags, 
                                                      self.kappa, 
                                                      self.error_bound)
    
    def simplify_swab(self):
        self.no_removed_indices = swab(self.x[:, 0].astype(int), 
                                       self.x[:, 1], 
                                       self.error_bound, 
                                       self.swab_windows_size)
        self.no_removed_indices[-1] = True
        
    
    def simplify_agg_vw(self):
        self.no_removed_indices = simplify_by_agg_vw(self.x[:, 0].astype(int), self.x[:, 1], self.nlags, self.kappa, self.error_bound)

    def simplify_agg_pip(self):
        self.no_removed_indices = simplify_by_agg_pip(self.x[:, 1], self.nlags, self.kappa, self.error_bound)

    def simplify_agg_tp(self):
        self.no_removed_indices = simplify_by_agg_tp(self.x[:, 1], self.nlags, self.kappa, self.error_bound)


    def from_acf_threshold(self):
        pos = np.where(self.no_removed_indices)[0]
        return self.x[pos]

    def compress(self, pts, error_bound, nlags=None, blocking=None, kappa=None, threads=1):
        x = list(range(len(pts)))
        self.x = np.asarray(list(zip(x, pts)))
        self.n = self.x.shape[0]
        self.kappa = kappa
        self.nlags = nlags
        self.threads = threads
        self.blocking = blocking
        if kappa and self.n % kappa != 0.:
            raise Exception("Data length must be multiple of kappa")

        if self.target in ['lpc_sip_cr', 'fgc_sip_cr']:	
            self.min_cr = error_bound

        self.error_bound = error_bound
        self.no_removed_indices = np.zeros(self.n, dtype=int)
        if kappa is None:
            if self.target == 'sip':
                self.simplify_sip()
            elif self.target == 'vw':
                self.simplify_vw()
            elif self.target == 'pip':
                self.simplify_pip()
            elif self.target == 'tp':
                self.simplify_tp()
            elif self.target == 'swab':
                self.simplify_swab()
            elif self.target == 'fgc_sip_cr':
                self.simplify_fgc_sip_cr()
            elif self.target == 'lpc_sip_cr':
                self.simplify_lpc_sip_cr()
            elif self.target == 'ped_mae_cameo':
                self.simplify_sip()
            elif self.target == 'ped_rmse_cameo':
                self.simplify_rmse_sip()
            elif self.target == 'ped_cheb_cameo':
                self.simplify_cheb_sip()
            else:
                raise Exception(f"{self.target} target not defined...")
        else:
            if self.target == 'sip':
                self.simplify_agg_sip()
            elif self.target == 'vw':
                self.simplify_agg_vw()
            elif self.target == 'pip':
                self.simplify_agg_pip()
            elif self.target == 'tp':
                self.simplify_agg_tp()
            elif self.target == 'swab':
                self.simplify_swab()
            else:
                raise Exception(f"{self.target} taget not defined...")


        remaining_points = self.from_acf_threshold()
        return remaining_points

    def decompress(self, remaining_points):
        x = np.arange(0, int(remaining_points[-1, 0])+1)
        return np.interp(x, remaining_points[:, 0], remaining_points[:, 1])


