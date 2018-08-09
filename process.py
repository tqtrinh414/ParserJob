import pandas as pd
from autocorrect import spell
import re
import nltk
from nltk import word_tokenize
import pandas as pd



PATTERN_FUNC = {
    "sales": ["sales", "account", "accounts", "business development"], 
    "finance": ["accounting", "finance"], 
    "it": ["programmer", "engineer", "developer", "tester", "it ", "web"],
    "marketing": ["marketing"]
}
PATTERN_LEVEL = {
    "manager": ["manager", "assistant manager"],
    "directors": ["director", "associate director"]
}


def remove_special_character(str):
    return(re.sub('[^A-Za-z]+', ' ',str))


def preprocessing(path = "Sample_data.csv"):
    df = pd.read_csv(path)
    title = [remove_special_character(str(s)).lower().strip() for s in df['Title']]
    df['Title'] = title
    df = df.drop(['Function', 'Level'], axis = 1)
    return(df)


def get_unique(df, pattern_func, pattern_level):
    uni_title = set(list(df['Title']))
    dct = {}
    for title in uni_title:
        dct[title] = ["",""]
    
    for title in uni_title:
        flag = 1
        for x in pattern_func:
            pf = pattern_func[x]
            for yf in pf:
                if title.find(yf) != -1:
                    dct[title][0] = x
                    flag = 0
        for x in pattern_level:
            pl = pattern_level[x]
            for yl in pl:
                if title.find(yl) != -1:
                    dct[title][1] = x
                    flag = 0
        
        if (len(title.split(" ")) == 2 and flag): # title co 2 tu va khong trong pattern
            temp_title = title.split()
            dct[title] = (temp_title[0],temp_title[1])
            cout += 1
    return dct


def get_result(df,dct):
    funcs = []
    levels = []
    for x in df['Title']:
        func = dct[x][0]
        lvl = dct[x][1]
        if (func != ""):
            funcs.append(func)
        else:
            funcs.append(x)
        if (lvl != ""):
            levels.append(lvl)
        else:
            levels.append(x)

    df['Function'] = funcs
    df['Level'] = levels
    df.to_csv("test.csv")


def input_pattern_func():
    dctPatFunc = {}
    print ("input pattern cho function: ")
    s = ""
    while s != "0":
        print ("function (nhap 0 de nhap function khac) ")
        s = input()
        s2 = ""
        lst = []
        while s != "0" and s2 != "0":
            print ("keyword (nhap 0 de dung):")
            s2 = input()
            if s2 != "0":
                lst.append(s2)
        if s!= "0":
            dctPatFunc[s] = lst
    return dctPatFunc


def input_pattern_level():
    dctPatLevel = {}
    print ("input pattern cho level: ")
    s = ""
    while s != "0":
        print ("level (nhap 0 de nhap level khac) ")
        s = input()
        s2 = ""
        lst = []
        while s != "0" and s2 != "0":
            print ("keyword (nhap 0 de dung):")
            s2 = input()
            if s2 != "0":
                lst.append(s2)
        if s!= "0":
            dctPatLevel[s] = lst
    return dctPatLevel


def main():
    #print (input_pattern_func())
    #print (input_pattern_level())

    df = preprocessing()
    dct = get_unique(df, PATTERN_FUNC, PATTERN_LEVEL)
    get_result(df, dct)

if __name__ == "__main__":
    main()