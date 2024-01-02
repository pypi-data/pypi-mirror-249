# __init__.py

# Import modules and classes to make them accessible when importing the package
from .system.novum import Novum
from .system.gates import Hadamard
import system.gates as gates
from .algorithms.grover import Grover
from .algorithms.deutschjozsa import DeutschJozsa


__all__ = ['Novum', 'gates', 'Grover', 'DeutschJozsa']
def learn():
    print("You can learn all about quantum computing for free or for money based on an valuation test by contacting aminalogai@aol.com")

