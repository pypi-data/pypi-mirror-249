
###---------------### YEAR CHECKER ###--------------- ###

def sintxcs_year(uid):
    D = "20??"
    E = "2023"
    C = "2009"
    B = uid
    if len(B) == 15:
        if str(B)[:10] in ["1000000000"]:
            get_year = C
        elif str(B)[:9] in ["100000000"]:
            get_year = C
        elif str(B)[:8] in ["10000000"]:
            get_year = C
        elif str(B)[:7] in [
            "1000000",
            "1000001",
            "1000002",
            "1000003",
            "1000004",
            "1000005",
        ]:
            get_year = C
        elif str(B)[:7] in ["1000006", "1000007", "1000008", "1000009"]:
            get_year = "2010"
        elif str(B)[:6] in ["100001"]:
            get_year = "2010-2011"
        elif str(B)[:6] in ["100002", "100003"]:
            get_year = "2011-2012"
        elif str(B)[:6] in ["100004"]:
            get_year = "2012-2013"
        elif str(B)[:6] in ["100005", "100006"]:
            get_year = "2013-2014"
        elif str(B)[:6] in ["100007", "100008"]:
            get_year = "2014-2015"
        elif str(B)[:6] in ["100009"]:
            get_year = "2015"
        elif str(B)[:5] in ["10001"]:
            get_year = "2015-2016"
        elif str(B)[:5] in ["10002"]:
            get_year = "2016-2017"
        elif str(B)[:5] in ["10003"]:
            get_year = "2018-2019"
        elif str(B)[:5] in ["10004"]:
            get_year = "2019-2020"
        elif str(B)[:5] in ["10005"]:
            get_year = "2020"
        elif str(B)[:5] in ["10006", "10007"]:
            get_year = "2021"
        elif str(B)[:5] in ["10008"]:
            get_year = "2022"
        elif str(B)[:5] in ["10009"]:
            get_year = E
        else:
            get_year = D
    elif len(B) == 14:
        get_year = E
    elif len(B) in [9, 10]:
        get_year = " 2008-2009 "
    elif len(B) == 8:
        get_year = " 2007-2008 "
    elif len(B) == 7:
        get_year = " 2006-2007 "
    else:
        get_year = D
    return get_year