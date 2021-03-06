__author__ = 'richard'
import os
import pickle

import score_y

from roboskeeter.io import i_o

reload(score_y)
reload(kinematics)

EXPERIMENT_PATH = i_o.get_directory('EXPERIMENT_PATH')


def store_mosquito_pickle():
    MOSQUITOES = kinematics.ExperimentalKinematics()
    MOSQUITOES.experiment_data_to_DF(experimental_condition='CONTROL_EXP_PATH')  # load the experimental data
    pickle.dump(MOSQUITOES, open(os.path.join(EXPERIMENT_PATH, "controlsY.p"), "wb"))

    ref_data = score_y.get_data(MOSQUITOES)
    experimental_bins_dict = score_y.calc_bins(ref_data)
    experimental_KDEs_dict = score_y.calc_kde(ref_data)
    experimental_vals_dict = score_y.evaluate_kdes(experimental_KDEs_dict, experimental_bins_dict)

    pickle.dump(experimental_bins_dict, open(os.path.join(EXPERIMENT_PATH, "experimental_bins_dictY.p"), "wb"))
    pickle.dump(experimental_vals_dict, open(os.path.join(EXPERIMENT_PATH, "experimental_vals_dictY.p"), "wb"))
    print "Pickles dumped."


def load_mosquito_trajectory_pickle():
    return pickle.load(open(os.path.join(EXPERIMENT_PATH, "controlsY.p"), "rb"))


def load_mosquito_kde_data_dicts():
    bins = pickle.load(open(os.path.join(EXPERIMENT_PATH, "experimental_bins_dictY.p"), "rb"))
    vals = pickle.load(open(os.path.join(EXPERIMENT_PATH, "experimental_vals_dictY.p"), "rb"))

    return bins, vals


if __name__ is '__main__':
    store_mosquito_pickle()
