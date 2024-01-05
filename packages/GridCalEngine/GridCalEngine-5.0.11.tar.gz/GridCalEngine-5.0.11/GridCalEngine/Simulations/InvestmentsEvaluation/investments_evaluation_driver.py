# GridCal
# Copyright (C) 2015 - 2023 Santiago Peñate Vera
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import numpy as np
import hyperopt
import functools

from typing import List, Dict, Union
from GridCalEngine.Simulations.driver_template import DriverTemplate
from GridCalEngine.Simulations.PowerFlow.power_flow_driver import PowerFlowDriver, PowerFlowOptions
from GridCalEngine.Simulations.driver_types import SimulationTypes
from GridCalEngine.Simulations.InvestmentsEvaluation.investments_evaluation_results import InvestmentsEvaluationResults
from GridCalEngine.Core.Devices.multi_circuit import MultiCircuit
from GridCalEngine.Core.Devices.Aggregation.investment import Investment
from GridCalEngine.Core.DataStructures.numerical_circuit import NumericalCircuit
from GridCalEngine.Core.DataStructures.numerical_circuit import compile_numerical_circuit_at
from GridCalEngine.Simulations.PowerFlow.power_flow_worker import multi_island_pf_nc
from GridCalEngine.Simulations.InvestmentsEvaluation.MVRSM import MVRSM_multi_minimize
from GridCalEngine.Simulations.InvestmentsEvaluation.stop_crits import StochStopCriterion
from GridCalEngine.basic_structures import IntVec, Vec
from GridCalEngine.enumerations import InvestmentEvaluationMethod
from GridCalEngine.Simulations.InvestmentsEvaluation.investments_evaluation_options import InvestmentsEvaluationOptions


class InvestmentsEvaluationDriver(DriverTemplate):
    name = 'Investments evaluation'
    tpe = SimulationTypes.InvestmestsEvaluation_run

    def __init__(self, grid: MultiCircuit,
                 options: InvestmentsEvaluationOptions):
        """
        InputsAnalysisDriver class constructor
        :param grid: MultiCircuit instance
        :param method: InvestmentEvaluationMethod
        :param max_eval: Maximum number of evaluations
        """
        DriverTemplate.__init__(self, grid=grid)

        # options object
        self.options = options

        # results object
        self.results = InvestmentsEvaluationResults(investment_groups_names=grid.get_investment_groups_names(),
                                                    max_eval=0)

        self.__eval_index = 0

        # dictionary of investment groups
        self.investments_by_group: Dict[int, List[Investment]] = self.grid.get_investmenst_by_groups_index_dict()

        # dimensions
        self.dim = len(self.grid.investments_groups)

        # numerical circuit
        self.nc: Union[NumericalCircuit, None] = None

        # gather a dictionary of all the elements, this serves for the investments generation
        self.get_all_elements_dict = self.grid.get_all_elements_dict()

    def get_steps(self):
        """

        :return:
        """
        return self.results.get_index()

    def objective_function_old(self, combination: IntVec):
        """
        Function to evaluate a combination of investments
        :param combination: vector of investments (yes/no)
        :return: objective function value
        """

        # add all the investments of the investment groups reflected in the combination
        inv_list = list()
        for i, active in enumerate(combination):
            if active == 1:
                inv_list += self.investments_by_group[i]

        # enable the investment
        # TODO: use MultiCircuit deep copies instead of NumericalCircuit copies (try deepcopy module)
        nc_mod = self.nc.copy()
        nc_mod.set_investments_status(investments_list=inv_list, status=1)

        # do something
        res = multi_island_pf_nc(nc=nc_mod, options=self.options.pf_options)
        total_losses = np.sum(res.losses.real)
        overload_score = res.get_oveload_score(branch_prices=nc_mod.branch_data.overload_cost)
        # voltage_score = res.get_undervoltage_overvoltage_score(undervoltage_prices=self.nc.bus_data.undervoltage_cost,
        #                                                        overvoltage_prices=self.nc.bus_data.overvoltage_cost,
        #                                                        vmin=self.nc.bus_data.Vmin,
        #                                                        vmax=self.nc.bus_data.Vmax)
        voltage_score = 0.0

        capex_score = sum([inv.CAPEX for inv in inv_list]) * 0.00001

        f = total_losses + overload_score + voltage_score + capex_score

        # store the results
        self.results.set_at(eval_idx=self.__eval_index,
                            capex=sum([inv.CAPEX for inv in inv_list]),
                            opex=sum([inv.OPEX for inv in inv_list]),
                            losses=total_losses,
                            overload_score=overload_score,
                            voltage_score=voltage_score,
                            objective_function=f - capex_score,
                            combination=combination,
                            index_name="Evaluation {}".format(self.__eval_index))

        # revert to disabled
        # nc_mod.set_investments_status(investments_list=inv_list, status=0)

        # increase evaluations
        self.__eval_index += 1

        self.report_progress2(self.__eval_index, self.options.max_eval)

        return f

    def objective_function(self, combination: IntVec) -> Vec:
        """
        Function to evaluate a combination of investments
        :param combination: vector of investments (yes/no). Length = number of investment groups
        :return: objective function value
        """

        # add all the investments of the investment groups reflected in the combination
        inv_list = list()
        for i, active in enumerate(combination):
            if active == 1:
                inv_list += self.investments_by_group[i]

        # enable the investment
        self.grid.set_investments_status(investments_list=inv_list,
                                         status=True,
                                         all_elemnts_dict=self.get_all_elements_dict)

        branches = self.grid.get_branches_wo_hvdc()
        buses = self.grid.get_buses()

        # do something
        driver = PowerFlowDriver(grid=self.grid, options=self.options.pf_options)
        driver.run()
        res = driver.results

        norm = False

        overload_score = get_overload_score(res, branches, norm)
        losses_score = np.sum(res.losses.real)
        voltage_module_score = get_voltage_module_score(res, buses, norm)
        voltage_angle_score = 0.0
        capex_score = np.sum(np.array([inv.CAPEX for inv in inv_list])) * 0
        # opex_score = get_opex_score()

        f = losses_score + overload_score + voltage_module_score + capex_score

        # store the results
        self.results.set_at(eval_idx=self.__eval_index,
                            capex=sum([inv.CAPEX for inv in inv_list]),
                            opex=sum([inv.OPEX for inv in inv_list]),
                            losses=losses_score,
                            overload_score=overload_score,
                            voltage_score=voltage_module_score,
                            objective_function=f - capex_score,
                            combination=combination,
                            index_name="Evaluation {}".format(self.__eval_index))

        # revert to disabled
        self.grid.set_investments_status(investments_list=inv_list,
                                         status=False,
                                         all_elemnts_dict=self.get_all_elements_dict)

        # increase evaluations
        self.__eval_index += 1

        self.report_progress2(self.__eval_index, self.options.max_eval)

        return np.array([losses_score, overload_score, voltage_module_score, capex_score])

    def independent_evaluation(self) -> None:
        """
        Run a one-by-one investment evaluation without considering multiple evaluation groups at a time
        """
        self.report_text("Running independent investments evaluation...")
        # compile the snapshot
        self.nc = compile_numerical_circuit_at(circuit=self.grid, t_idx=None)
        self.results = InvestmentsEvaluationResults(investment_groups_names=self.grid.get_investment_groups_names(),
                                                    max_eval=len(self.grid.investments_groups) + 1)
        # disable all status
        self.nc.set_investments_status(investments_list=self.grid.investments, status=0)

        # evaluate the investments
        self.__eval_index = 0

        # add baseline
        self.objective_function(combination=np.zeros(self.results.n_groups, dtype=int))

        dim = len(self.grid.investments_groups)

        for k in range(dim):
            self.report_text("Evaluating investment group {}...".format(k))

            combination = np.zeros(dim, dtype=int)
            combination[k] = 1

            self.objective_function(combination=combination)

        self.report_done()

    def optimized_evaluation_hyperopt(self) -> None:
        """
        Run an optimized investment evaluation without considering multiple evaluation groups at a time
        """
        self.report_text("Running investments optimization with Hyperopt")
        # configure hyperopt:

        # number of random evaluations at the beginning
        rand_evals = round(self.dim * 1.5)

        # binary search space
        space = [hyperopt.hp.randint(f'x_{i}', 2) for i in range(self.dim)]

        if self.options.max_eval == rand_evals:
            algo = hyperopt.rand.suggest
        else:
            algo = functools.partial(hyperopt.tpe.suggest, n_startup_jobs=rand_evals)

        # compile the snapshot
        self.nc = compile_numerical_circuit_at(circuit=self.grid, t_idx=None)
        self.results = InvestmentsEvaluationResults(investment_groups_names=self.grid.get_investment_groups_names(),
                                                    max_eval=self.options.max_eval + 1)
        # disable all status
        self.nc.set_investments_status(investments_list=self.grid.investments, status=0)

        # evaluate the investments
        self.__eval_index = 0

        # add baseline
        self.objective_function(combination=np.zeros(self.results.n_groups, dtype=int))

        hyperopt.fmin(np.sum(self.objective_function), space, algo, self.options.max_eval)

        self.report_done()

    def optimized_evaluation_mvrsm(self) -> None:
        """
        Run an optimized investment evaluation without considering multiple evaluation groups at a time
        """
        self.report_text("Running investments optimization with MVRSM")

        # configure MVRSM:

        # number of random evaluations at the beginning
        rand_evals = round(self.dim * 1.5)
        lb = np.zeros(self.dim)
        ub = np.ones(self.dim)
        rand_search_active_prob = 0.5
        threshold = 0.001
        conf_dist = 0.0
        conf_level = 0.95
        stop_crit = StochStopCriterion(conf_dist, conf_level)
        x0 = np.random.binomial(1, rand_search_active_prob, self.dim)

        # compile the snapshot
        self.nc = compile_numerical_circuit_at(circuit=self.grid, t_idx=None)
        self.results = InvestmentsEvaluationResults(investment_groups_names=self.grid.get_investment_groups_names(),
                                                    max_eval=self.options.max_eval + 1)
        # disable all status
        self.nc.set_investments_status(investments_list=self.grid.investments, status=0)

        # evaluate the investments
        self.__eval_index = 0

        # add baseline
        self.objective_function(combination=np.zeros(self.results.n_groups, dtype=int))

        # optimize
        best_x, inv_scale, model = MVRSM_multi_minimize(obj_func=self.objective_function,
                                                        x0=x0,
                                                        lb=lb,
                                                        ub=ub,
                                                        num_int=self.dim,
                                                        max_evals=self.options.max_eval,
                                                        n_objectives=4,
                                                        rand_evals=rand_evals)

        self.report_done()

    def run(self):
        """
        run the QThread
        :return:
        """

        self.tic()

        if self.options.solver == InvestmentEvaluationMethod.Independent:
            self.independent_evaluation()

        elif self.options.solver == InvestmentEvaluationMethod.Hyperopt:
            self.optimized_evaluation_hyperopt()

        elif self.options.solver == InvestmentEvaluationMethod.MVRSM:
            self.optimized_evaluation_mvrsm()

        else:
            raise Exception('Unsupported method')

        self.toc()

    def cancel(self):
        self.__cancel__ = True


def get_overload_score(results, branches, norm):
    branches_cost = np.array([e.Cost for e in branches], dtype=float)
    branches_loading = np.abs(results.loading)

    # get lines where loading is above 1 -- why 1 ?
    branches_idx = np.where(branches_loading > 1)[0]

    cost = branches_cost[branches_idx] * branches_loading[branches_idx]

    if norm:
        return get_normalized_score(cost)
    return np.sum(cost)


def get_voltage_module_score(results, buses, norm):
    bus_cost = np.array([e.Vm_cost for e in buses], dtype=float)
    vmax = np.array([e.Vmax for e in buses], dtype=float)
    vmin = np.array([e.Vmin for e in buses], dtype=float)
    vm = np.abs(results.voltage)
    vmax_diffs = np.array(vm - vmax).clip(min=0)
    vmin_diffs = np.array(vmin - vm).clip(min=0)
    cost = (vmax_diffs + vmin_diffs) * bus_cost

    if norm:
        return get_normalized_score(cost)
    return np.sum(cost)


def get_opex_score(inv_list):
    for inv in inv_list:
        opex = inv.OPEX


def get_normalized_score(array):
    if len(array) < 1:
        return 0.0

    max_value = np.max(array)

    if max_value != 0:
        return np.sum(array) / max_value

    return 0.0
