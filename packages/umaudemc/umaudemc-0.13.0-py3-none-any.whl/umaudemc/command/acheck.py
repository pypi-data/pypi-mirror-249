#
# Admissibility checking subcommand
#

import os

from ..common import parse_initial_data, usermsgs
# Meter las herramientas en backends y usar la misma estrategia que en otros contextos

def acheck(args):
	"""Admissibility check subcommand"""

	# Parse the module data
	data = parse_initial_data(args, only_module=True)

	if data is None:
		return 1

	print(data.module)

	return 0
