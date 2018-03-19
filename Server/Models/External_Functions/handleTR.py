#-*-coding:utf-8-*-
def handle_tr(str_):
    str_ = str_.replace("İ", "I").replace("Ç", "C").replace("Ş", "S").replace("Ü", "U").replace("Ö", "O").replace("Ğ",
                                                                                                                  "G")
    str_ = str_.replace("ı", "i").replace("ç", "c").replace("ş", "s").replace("ü", "u").replace("ö", "o").replace("ğ",
                                                                                                                  "g")
    return str_