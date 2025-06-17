#!/usr/bin/env python3

import sys
import tabulate

print('Python path:', sys.executable)
print('Virtual env:', sys.prefix)
print('Tabulate version:', tabulate.__version__)
print('Tabulate location:', tabulate.__file__)