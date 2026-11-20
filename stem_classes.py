# stem_classes.py
NO_RULE = "-"

PREFIX_MATRIX = {
    # 1st Person Singular
    ("1sg", "2sg"): {"C": "kon",  "A": "kony", "I": "kon",  "E": "kony", "O": "kony"},
    ("1sg", "3m"):  {"C": "ri",   "A": "riy",  "I": "r",    "E": "riy",  "O": "riy"},
    ("1sg", "3f"):  {"C": "khe",  "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "3pl.m"): {"C": "khe", "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "3pl.f"): {"C": "khe", "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "1du.in"): {"C": "keni", "A": "ky",   "I": "ken",  "E": "ken",  "O": "ken"},
    ("1sg", "1pl.in"): {"C": "kwa",  "A": "kw",   "I": "kwen", "E": "kw",   "O": "ky"},
    ("1sg", "3i"): {"C": "ken", "A": "ken", "I": "ken", "E": "ken", "O": "ken"},


    # 2nd Person Singular
    ("2sg", "1sg"): {"C": "take", "A": "takw", "I": "tak",  "E": "tak",  "O": "tak"},
    ("2sg", "3m"):  {"C": "etshe","A": "etsh", "I": "etsh", "E": "etsh", "O": "etsh"},
    ("2sg", "3f"):  {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "3pl.m"): {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "3pl.f"): {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "2du"): {"C": "takwa","A": "takw", "I": "takwen","E": "takw", "O": "taky"},
    ("2sg", "3i"): {"C": "hsen", "A": "hsen", "I": "hsen", "E": "hsen", "O": "hsen"},

    # 3rd Person Masculine
    ("3m", "1sg"):  {"C": "rake", "A": "rakw", "I": "rak",  "E": "rakw", "O": "rak"},
    ("3m", "2sg"):  {"C": "hya",  "A": "hy",   "I": "hyen", "E": "hyay", "O": "hyay"},
    ("3m", "3m"):   {"C": "ro",   "A": "ro",   "I": "ro",   "E": "raw",  "O": "ra"},
    ("3m", "3f"):   {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "3pl.m"): {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "3pl.f"): {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "1du.in"):  {"C": "hshonkeni","A": "hshonky","I": "hshonken","E": "hshonken","O": "hshonken"},
    ("3m", "1pl.in"):  {"C": "hshonkwa","A": "hshonkw","I": "hshonkwen","E": "hshonkw","O": "hshonky"},
    ("3m", "3i"): {"C": "ra", "A": "ra", "I": "ra", "E": "ra", "O": "ra"},

    # 3rd Person Feminine
    ("3f", "1sg"):  {"C": "yonke", "A": "yonkw", "I": "yonk", "E": "yonkw", "O": "yonk"},
    ("3f", "2sg"):  {"C": "yesa",  "A": "yes",   "I": "yesen","E": "yes",  "O": "yesay"},
    ("3f", "3m"):   {"C": "ronwa", "A": "ronw",  "I": "ronwen","E": "ronw", "O": "ronway"},
    ("3f", "3f"):   {"C": "yontate","A": "yontat","I": "yontat","E": "yontat","O": "yontat"},
    ("3f", "3pl.m"): {"C": "ronwati","A": "ronwan","I": "ronwat","E": "ronwat","O": "ronwan"},
    ("3f", "3pl.f"): {"C": "konwati","A": "konwan","I": "konwat","E": "konwat","O": "konwan"},
    ("3f", "1du.in"):  {"C": "yonkhi", "A": "yonkhiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "1pl.in"):  {"C": "yonkhi", "A": "yonkhiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "2du"):  {"C": "yetshi", "A": "yetshiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "3i"): {"C": "ye", "A": "ye", "I": "ye", "E": "ye", "O": "ye"},

    # 3rd Person Inanimate
    ("3i", "1sg"):  {"C": "wake",  "A": "wak",   "I": "wak",  "E": "wak",  "O": "wak"},
    ("3i", "2sg"):  {"C": "sa",    "A": "s",     "I": "sen",  "E": "s",    "O": "s"},
    ("3i", "3m"):   {"C": "ro",    "A": "ro",    "I": "ro",   "E": "raw",  "O": "ra"},
    ("3i", "3f"):   {"C": "yako",  "A": "yako",  "I": "yako", "E": "yakaw","O": "yaka"},
    ("3i", "3i"):   {"C": "yo",    "A": "yo",    "I": "yo",   "E": "yo",   "O": "yo"},
    ("3i", "1du.in"):  {"C": "yokeni","A": "yonsky", "I": "yonken","E": "yonken","O": "yonken"},
    ("3i", "1pl.in"):  {"C": "yonkwa","A": "yonkw", "I": "yonkwen","E": "yonkw","O": "yonky"},
    ("3i", "2du"):  {"C": "seni",  "A": "tsy",   "I": "sen",  "E": "sen",  "O": "sen"},

    # 1st Person Dual/Plural
    ("1du.in", "3i"):  {"C": "teni",  "A": "ty",    "I": "ten",  "E": "ten",  "O": "ten"},
    ("1du.ex", "3i"):  {"C": "yakeni","A": "yaky",  "I": "yaken","E": "yaken","O": "yaken"},
    ("1pl.in", "3i"):  {"C": "tewa",  "A": "tew",   "I": "tewen","E": "tew",  "O": "ty"},
    ("1pl.ex", "3i"):  {"C": "yakwa", "A": "yakw",  "I": "yakwen","E": "yakw","O": "yaky"},
    
    # 2nd Person Dual/Plural
    ("2du", "3i"):    {"C": "seni",  "A": "tsy",   "I": "sen",  "E": "sen",  "O": "sen"},
    ("2du.m", "3i"):  {"C": "hni",   "A": "hy",    "I": "hn",   "E": "hn",   "O": "hn"},
    ("2du.f", "3i"):  {"C": "keni",  "A": "ky",    "I": "ken",  "E": "ken",  "O": "ken"},
    ("2pl", "3i"):    {"C": "sewa",  "A": "sew",   "I": "sewen","E": "sew",  "O": "tsy"},

    # 3rd Person Plural
    ("3pl.m", "3i"):  {"C": "rati",  "A": "ron",   "I": "rat",  "E": "ronn", "O": "ronn"},
    ("3pl.f", "3i"):  {"C": "konti", "A": "kon",   "I": "kont", "E": "konn", "O": "konn"},
    ("3pl.m", "1sg"):   {"C": "shakoti", "A": "shakon", "I": "shakot", "E": "shakon", "O": "shakotiy"},
    ("3pl.f", "1sg"):   {"C": "yakoti",  "A": "yakon",  "I": "yakot",  "E": "yakon",  "O": "yakotiy"},
    ("3pl.m", "3f"):    {"C": "shakoti", "A": "shakon", "I": "shakot", "E": "shakon", "O": "shakotiy"},
    ("3pl.f", "3f"):    {"C": "yakoti",  "A": "yakon",  "I": "yakot",  "E": "yakon",  "O": "yakotiy"},
    ("3pl.f", "2sg"):   {"C": "yesa", "A": "yes", "I": "yesen", "E": "yes", "O": "yesay"},
    ("3pl.f", "3m"):    {"C": "ronwa", "A": "ronw", "I": "ronwen", "E": "ronw", "O": "ronway"},

    # 3i -> 3n (inanimate subject -> neuter object)
    ("3i", "3n"): {"C": "yon", "A": "yon", "I": "yon", "E": "yon", "O": "yon"},

    # 3i -> 2du.m and 2du.f
    ("3i", "2du.m"): {"C": "roti", "A": "roti", "I": "roti", "E": "roti", "O": "roti"},
    ("3i", "2du.f"): {"C": "yoti", "A": "yoti", "I": "yoti", "E": "yoti", "O": "yoti"},
}

PURPLE_PREFIX_MATRIX = {
    # 1st Person Singular
    ("1sg", "2sg"): {"C": "kon",  "A": "kony", "I": "kon",  "E": "kony", "O": "kony"},
    ("1sg", "3m"):  {"C": "ri",   "A": "riy",  "I": "r",    "E": "riy",  "O": "riy"},
    ("1sg", "3f"):  {"C": "khe",  "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "3pl.m"): {"C": "khe", "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "3pl.f"): {"C": "khe", "A": "khey", "I": "khe",  "E": "khey", "O": "khey"},
    ("1sg", "1du.in"): {"C": "keni", "A": "ky",   "I": "ken",  "E": "ken",  "O": "ken"},
    ("1sg", "1pl.in"): {"C": "kwa",  "A": "kw",   "I": "kwen", "E": "kw",   "O": "ky"},
    ("1sg", "3i"): {"C": "ken", "A": "ken", "I": "ken", "E": "ken", "O": "ken"},

    # 2nd Person Singular
    ("2sg", "1sg"): {"C": "take", "A": "takw", "I": "tak",  "E": "tak",  "O": "tak"},
    ("2sg", "3m"):  {"C": "etshe","A": "etsh", "I": "etsh", "E": "etsh", "O": "etsh"},
    ("2sg", "3f"):  {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "3pl.m"): {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "3pl.f"): {"C": "hshe", "A": "hshey","I": "hshe", "E": "hshey","O": "hshey"},
    ("2sg", "2du"): {"C": "takwa","A": "takw", "I": "takwen","E": "takw", "O": "taky"},
    ("2sg", "3i"): {"C": "hsen", "A": "hsen", "I": "hsen", "E": "hsen", "O": "hsen"},

    # 3rd Person Masculine
    ("3m", "1sg"):  {"C": "rake", "A": "rakw", "I": "rak",  "E": "rakw", "O": "rak"},
    ("3m", "2sg"):  {"C": "hya",  "A": "hy",   "I": "hyen", "E": "hyay", "O": "hyay"},
    ("3m", "3m"):   {"C": "ro",   "A": "ro",   "I": "ro",   "E": "raw",  "O": "ra"},
    ("3m", "3f"):   {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "3pl.m"): {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "3pl.f"): {"C": "hshako","A": "hshako","I": "hshako","E": "hshakaw","O": "hshaka"},
    ("3m", "1du.in"):  {"C": "hshonkeni","A": "hshonky","I": "hshonken","E": "hshonken","O": "hshonken"},
    ("3m", "1pl.in"):  {"C": "hshonkwa","A": "hshonkw","I": "hshonkwen","E": "hshonkw","O": "hshonky"},
    ("3m", "3i"): {"C": "ra", "A": "ra", "I": "ra", "E": "ra", "O": "ra"},

    # 3rd Person Feminine
    ("3f", "1sg"):  {"C": "yonke", "A": "yonkw", "I": "yonk", "E": "yonkw", "O": "yonk"},
    ("3f", "2sg"):  {"C": "yesa",  "A": "yes",   "I": "yesen","E": "yes",  "O": "yesay"},
    ("3f", "3m"):   {"C": "ronwa", "A": "ronw",  "I": "ronwen","E": "ronw", "O": "ronway"},
    ("3f", "3f"):   {"C": "yontate","A": "yontat","I": "yontat","E": "yontat","O": "yontat"},
    ("3f", "3pl.m"): {"C": "ronwati","A": "ronwan","I": "ronwat","E": "ronwat","O": "ronwan"},
    ("3f", "3pl.f"): {"C": "konwati","A": "konwan","I": "konwat","E": "konwat","O": "konwan"},
    ("3f", "1du.in"):  {"C": "yonkhi", "A": "yonkhiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "1pl.in"):  {"C": "yonkhi", "A": "yonkhiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "2du"):  {"C": "yetshi", "A": "yetshiy","I": "yetsh", "E": "yetshiy","O": "yetshiy"},
    ("3f", "3i"): {"C": "ye", "A": "ye", "I": "ye", "E": "ye", "O": "ye"},

    # 3rd Person Inanimate
    ("3i", "1sg"):  {"C": "wake",  "A": "wak",   "I": "wak",  "E": "wak",  "O": "wak"},
    ("3i", "2sg"):  {"C": "sa",    "A": "s",     "I": "sen",  "E": "s",    "O": "s"},
    ("3i", "3m"):   {"C": "ro",    "A": "ro",    "I": "ro",   "E": "raw",  "O": "ra"},
    ("3i", "3f"):   {"C": "yako",  "A": "yako",  "I": "yako", "E": "yakaw","O": "yaka"},
    ("3i", "3i"):   {"C": "ka",    "A": "ka",    "I": "ka",   "E": "ka",   "O": "ka"},

    # 1st Person Dual/Plural
    ("1du.in", "3i"):  {"C": "teni",  "A": "ty",    "I": "ten",  "E": "ten",  "O": "ten"},
    ("1du.ex", "3i"):  {"C": "yakeni","A": "yaky",  "I": "yaken","E": "yaken","O": "yaken"},
    ("1pl.in", "3i"):  {"C": "tewa",  "A": "tew",   "I": "tewen","E": "tew",  "O": "ty"},
    ("1pl.ex", "3i"):  {"C": "yakwa", "A": "yakw",  "I": "yakwen","E": "yakw","O": "yaky"},

    # 2nd Person Dual/Plural
    ("2du", "3i"):    {"C": "seni",  "A": "tsy",   "I": "sen",  "E": "sen",  "O": "sen"},
    ("2du.m", "3i"):  {"C": "hni",   "A": "hy",    "I": "hn",   "E": "hn",   "O": "hn"},
    ("2du.f", "3i"):  {"C": "keni",  "A": "ky",    "I": "ken",  "E": "ken",  "O": "ken"},
    ("2pl", "3i"):    {"C": "sewa",  "A": "sew",   "I": "sewen","E": "sew",  "O": "tsy"},

    # 3rd Person Plural
    ("3pl.m", "3i"):  {"C": "rati",  "A": "ron",   "I": "rat",  "E": "ronn", "O": "ronn"},
    ("3pl.f", "3i"):  {"C": "konti", "A": "kon",   "I": "kont", "E": "konn", "O": "konn"},
    ("3pl.m", "1sg"):   {"C": "shakoti", "A": "shakon", "I": "shakot", "E": "shakon", "O": "shakotiy"},
    ("3pl.f", "1sg"):   {"C": "yakoti",  "A": "yakon",  "I": "yakot",  "E": "yakon",  "O": "yakotiy"},
    ("3pl.m", "3f"):    {"C": "shakoti", "A": "shakon", "I": "shakot", "E": "shakon", "O": "shakotiy"},
    ("3pl.f", "3f"):    {"C": "yakoti",  "A": "yakon",  "I": "yakot",  "E": "yakon",  "O": "yakotiy"},
    ("3pl.f", "2sg"):   {"C": "yesa", "A": "yes", "I": "yesen", "E": "yes", "O": "yesay"},
    ("3pl.f", "3m"):    {"C": "ronwa", "A": "ronw", "I": "ronwen", "E": "ronw", "O": "ronway"},
    ("3i", "3n"): {"C": "yon", "A": "yon", "I": "yon", "E": "yon", "O": "yon"},
    ("3i", "2du.m"): {"C": "roti", "A": "roti", "I": "roti", "E": "roti", "O": "roti"},
    ("3i", "2du.f"): {"C": "yoti", "A": "yoti", "I": "yoti", "E": "yoti", "O": "yoti"},
}
