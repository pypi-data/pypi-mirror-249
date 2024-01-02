
from .singleton import Singleton
from .world import World
from ..datastructs.balance import BalanceEntry

from enum import Enum 
from collections import defaultdict 
import pandas as pd 


class BMEntry(Enum):
    A = 0
    L = 1

class BalanceMatrix(Singleton):
    """
    The balance matrix conatins the flows between agents and the stock-flow consistency. It has the following structure:

    +----------------------------------------------------------------------------+
    | Balance Matrix                                                             |
    +===============+=========================+==================================+
    |               |     Agent 1             |           Agent 2                |
    +---------------+-----------+-------------+----------------+-----------------+
    |               |     A     |  L          |            A   | L               |
    +---------------+-----------+-------------+----------------+-----------------+
    | d(Deposits)   |    dx1    |             |          dx2   |                 |
    +---------------+-----------+-------------+----------------+-----------------+
    | d(Loans)      |           |  dy1        |                |                 |
    +---------------+-----------+-------------+----------------+-----------------+
    | d(Net Worth)  |           |  dnw1       |                |  dnw2           |
    +---------------+-----------+-------------+----------------+-----------------+
    | TOTAL         |    dx1    |  dy1 + dnw1 |           dx2  |  dnw2           |
    +---------------+-----------+-------------+----------------+-----------------+
    | Residual      |           | d(A1)-d(L1) |                | d(A2)-d(L2)     |
    +---------------+-----------+-------------+----------------+-----------------+
    """

    reset_count = 0

    def __init__(self):
        # constructor of the balance matrix

        if hasattr(self, "initialized"):  # only initialize once
            return
        
        self.initialized = True # initialized flag

        self.agents = []
        self.rows = [] 

        self.group = None 

        self._data = {}  # has two keys, A (Assets) and L (Liabilities), set reset() method
        self._start_data = {}  

        self.reset()     # defaultdict will take care of missing keys here

    
    def reset(self, verbose=False):
        """
        reset the data
        :param verbose: boolean (default False), triggers a reset warning if True
        """

        # starting data        
        self._start_data[BMEntry.A] = defaultdict(lambda: defaultdict(float))
        self._start_data[BMEntry.L] = defaultdict(lambda: defaultdict(float))

        # data to compare starting data with 
        self._data[BMEntry.A] = defaultdict(lambda: defaultdict(float))
        self._data[BMEntry.L] = defaultdict(lambda: defaultdict(float))

        if self.__class__.reset_count > 1:

            # warn the user every time this is being reset!
            if verbose:
                warnings.warn("BalanceMatrix has been reset")
        
        else:
            self.__class__.reset_count += 1


    def init_data(self, group=True):
        """
        fill the balance sheet matrix with starting values (= balances at current point in time)
        """
        agents = World().agent_registry
        self.group = group 
        
        for k, v in agents.items():
            for agent in v:
                
                if self.group:
                    classname = agent.__class__.__name__ 
                else:
                    classname = str(agent)

                try:
                    for name, vals_dict in dict(agent.balance_sheet.raw_data).items():
                    
                        self._start_data[BMEntry.A][name][classname] += vals_dict[BalanceEntry.ASSETS]
                        self._start_data[BMEntry.L][name][classname] += vals_dict[BalanceEntry.LIABILITIES]
                        self._start_data[BMEntry.L][name][classname] += vals_dict[BalanceEntry.EQUITY]

                        if name not in self.rows:
                            self.rows.append(name)

                    if classname not in self.agents:
                        self.agents.append(classname)
                except:
                    pass # ignore the 'NoAgents'
        

    def fill_data(self):
        """
        fill the balance sheet matrix with the balances at the current point in time
        """

        agents = World().agent_registry
        
        for k, v in agents.items():
            for agent in v:
                
                if self.group:
                    classname = agent.__class__.__name__ 
                else:
                    classname = str(agent)

                try:
                    for name, vals_dict in dict(agent.balance_sheet.raw_data).items():
                        
                        self._data[BMEntry.A][name][classname] += vals_dict[BalanceEntry.ASSETS]
                        self._data[BMEntry.L][name][classname] += vals_dict[BalanceEntry.LIABILITIES]
                        self._data[BMEntry.L][name][classname] += vals_dict[BalanceEntry.EQUITY]

                        if name not in self.rows:
                            self.rows.append(name)

                    if classname not in self.agents:
                        self.agents.append(classname)

                except:
                    pass # ignore the 'NoAgents'
                
    def to_dataframe(self, add_residual=False):
        """
        returns a pandas DataFrame representation of the balance matrix
        
        :param add_residual: add a residual calculation to the data frame (at the bottom) if set True (default False)
        """
        # print("agent, rows", self.rows, self.agents)

        for a in ["NetWorth", "Net Worth", "NetWealth", "Net Wealth"]:
            if a in self.rows:
                self.rows.remove(a)
                self.rows.append(a) # append at the end 
        
        all_data = []

        for agent in self.agents:
            data = defaultdict(lambda: {"A": [], "L":[] })
            for row in self.rows:
                data[row]["A"] = self._data[BMEntry.A][row][agent] - self._start_data[BMEntry.A][row][agent]  
                data[row]["L"] = self._data[BMEntry.L][row][agent] - self._start_data[BMEntry.L][row][agent] 
            data_i = pd.DataFrame(data).T
            
            if add_residual:
                data_i.loc["Residual"] = {"A": "  ", "L": data_i["A"].sum() - data_i["L"].sum()}
                
            all_data.append(data_i)
    
        df = pd.concat(all_data, axis=1, keys=self.agents)
        df["Total"] = df.sum(axis=1)
        return df

    def to_string(self, replace_zeros=True,justify="right", add_residual=False, round=2):
        """
        returns a string representation of the balance matrix
        """

        if replace_zeros:
            s = self.to_dataframe(add_residual=add_residual).round(round).replace(0.0, " .- ").to_string(justify=justify)
        else:
            s = self.to_dataframe(add_residual=add_residual).round(round).to_string(justify=justify)
        
        return s