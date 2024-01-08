# This file contains 'conversion' rules for variables (units)

# hazard (such as temperature)
# Rules are provided as <new variable name>-><old variable name> = (<factor>, <constant>)
# where new_variable = old_variable * factor + constant
conv_haz = {
    'SST->GMST': (1.44, 0),  # Following SROCC SPM footnote 29; discussed w. experts in 2021: ok within uncertainties
    'GSST->GMST': (1.44, 0),  # Potential synonyms of (global) SST
    'GMSST->GMST': (1,44, 0),
    'GM-SST->GMST': (1.44, 0),
}