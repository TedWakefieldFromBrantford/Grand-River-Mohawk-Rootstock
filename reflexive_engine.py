# reflexive_engine.py
"""
Reflexive (Someone ... Themself) and Reciprocal (Each other) matrices.
Based on Onkwawenna Kentyohkwa Unit 2, Page 47.
"""

REFLEXIVE_MATRIX = {
    ("1sg", "1sg"): {"C": "katate", "A": "katate", "I": "katate", "E": "katate", "O": "katate"},
    ("2sg", "2sg"): {"C": "hsatate", "A": "hsatate", "I": "hsatate", "E": "hsatate", "O": "hsatate"},
    ("3m", "3m"):   {"C": "ratate", "A": "ratate", "I": "ratate", "E": "ratate", "O": "ratate"},
    ("3f", "3f"):   {"C": "yontate", "A": "yontate", "I": "yontate", "E": "yontate", "O": "yontate"},
    ("3i", "3i"):   {"C": "watate", "A": "watate", "I": "watate", "E": "watate", "O": "watate"},
    
    ("1du.in", "1du.in"): {"C": "yatate", "A": "yatate", "I": "yatate", "E": "yatate", "O": "yatate"}, 
    ("1du.ex", "1du.ex"): {"C": "yakyatate", "A": "yakyatate", "I": "yakyatate", "E": "yakyatate", "O": "yakyatate"}, 
    ("2du", "2du"):       {"C": "tsyatate", "A": "tsyatate", "I": "tsyatate", "E": "tsyatate", "O": "tsyatate"}, 
    ("2du.m", "2du.m"):   {"C": "hyatate", "A": "hyatate", "I": "hyatate", "E": "hyatate", "O": "hyatate"}, 
    ("2du.f", "2du.f"):   {"C": "kyatate", "A": "kyatate", "I": "kyatate", "E": "kyatate", "O": "kyatate"}, 
    
    ("1pl.in", "1pl.in"): {"C": "tewatate", "A": "tewatate", "I": "tewatate", "E": "tewatate", "O": "tewatate"},
    ("1pl.ex", "1pl.ex"): {"C": "yakwatate", "A": "yakwatate", "I": "yakwatate", "E": "yakwatate", "O": "yakwatate"}, 
    ("2pl", "2pl"):       {"C": "sewatate", "A": "sewatate", "I": "sewatate", "E": "sewatate", "O": "sewatate"}, 
    
    ("3pl.m", "3pl.m"):   {"C": "ronatate", "A": "ronatate", "I": "ronatate", "E": "ronatate", "O": "ronatate"}, 
    ("3pl.f", "3pl.f"):   {"C": "konatate", "A": "konatate", "I": "konatate", "E": "konatate", "O": "konatate"}, 
    
    ("1sg", "2sg"): {"C": "kontatate", "A": "kontatate", "I": "kontatate", "E": "kontatate", "O": "kontatate"}, 
}

RECIPROCAL_MATRIX = {
    ("1du.in", "1du.in"): {"C": "teyakyatate", "A": "teyakyatate", "I": "teyakyatate", "E": "teyakyatate", "O": "teyakyatate"},
    ("1du.ex", "1du.ex"): {"C": "teyakyatate", "A": "teyakyatate", "I": "teyakyatate", "E": "teyakyatate", "O": "teyakyatate"},
    ("2du", "2du"):       {"C": "tesyatate",   "A": "tesyatate",   "I": "tesyatate",   "E": "tesyatate",   "O": "tesyatate"},
    ("2du.m", "2du.m"):   {"C": "tehyatate",   "A": "tehyatate",   "I": "tehyatate",   "E": "tehyatate",   "O": "tehyatate"},
    ("2du.f", "2du.f"):   {"C": "tekyatate",   "A": "tekyatate",   "I": "tekyatate",   "E": "tekyatate",   "O": "tekyatate"},
    ("1pl.in", "1pl.in"): {"C": "tetewatate",  "A": "tetewatate",  "I": "tetewatate",  "E": "tetewatate",  "O": "tetewatate"},
    ("1pl.ex", "1pl.ex"): {"C": "teyakwatate", "A": "teyakwatate", "I": "teyakwatate", "E": "teyakwatate", "O": "teyakwatate"},
    ("2pl", "2pl"):       {"C": "tesewatate",  "A": "tesewatate",  "I": "tesewatate",  "E": "tesewatate",  "O": "tesewatate"},
    ("3pl.m", "3pl.m"):   {"C": "tehonatate",  "A": "tehonatate",  "I": "tehonatate",  "E": "tehonatate",  "O": "tehonatate"},
    ("3pl.f", "3pl.f"):   {"C": "tekonatate",  "A": "tekonatate",  "I": "tekonatate",  "E": "tekonatate",  "O": "tekonatate"},
}
