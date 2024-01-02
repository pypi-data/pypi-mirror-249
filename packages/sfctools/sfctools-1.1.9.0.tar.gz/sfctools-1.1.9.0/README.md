# sfctools - A toolbox for stock-flow consistent, agent-based models

Sfctools is a lightweight and easy-to-use Python framework for agent-based macroeconomic, stock-flow consistent (ABM-SFC) modeling. It concentrates on agents in economics and helps you to construct agents, helps you to manage and document your model parameters, assures stock-flow consistency, and facilitates basic economic data structures (such as the balance sheet). For more documentation, see https://sfctools-framework.readthedocs.io/en/latest/.

## Installation

We recommend to install sfctools in a fresh Python 3.8 environment. For example, with conda, do

    conda create --name sfcenv python=3.8
    conda activate sfcenv
    conda install pip

Then, in a terminal of your choice, type:

    pip install sfctools

see https://pypi.org/project/sfctools/

## Usage with Graphical User Interface 'Attune'

Type

    python -m sfctools attune

to start the GUI.

## Usage inside Python

Try out this simple example:

```python
from sfctools import Agent, World 

class SomeAgent(Agent):
    def __init__(self, a):
        super().__init__()
        self.some_attribute = a

my_agent = SomeAgent(a='Hello')
your_agent = SomeAgent(a='World')

my_agents = World().get_agents_of_type("SomeAgent")
my_message = my_agents[0].some_attribute
your_message = my_agents[1].some_attribute

print("%s says %s, %s says %s" % (my_agent, my_message, your_agent, your_message))
```

The resulting output will be

```console 
SomeAgent__00001 says Hello, SomeAgent__00002 says World
```

## More Examples

Have a look at the [documentation page](https://sfctools-framework.readthedocs.io/en/latest/doc_api_examples/examples_framework.html) for more examples. 


## Cite this Software

You can cite the software as follows: 

Baldauf, T., (2023). sfctools - A toolbox for stock-flow consistent, agent-based models. Journal of Open Source Software, 8(87), 4980, https://doi.org/10.21105/joss.04980


You can cite the software repository as follows:

Thomas Baldauf. (2023). sfctools - A toolbox for stock-flow consistent, agent-based models (1.1.0.2b). Zenodo. https://doi.org/10.5281/zenodo.8118870


-----------------------------------

| Corresponding author: Thomas Baldauf, German Aerospace Center (DLR), Curiestr. 4 70563 Stuttgart | thomas.baldauf@dlr.de |

