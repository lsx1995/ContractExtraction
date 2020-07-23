import json
def OCRtext2Text(file_path):
    '''
    将OCR文本转换成规则可迭代list
    :return:
    '''
    text = []
    f = open(file_path, 'r', encoding='utf8')
    for line in f:
        if line != '':
            text.append("".join(line.split()[1:]))
    text = ''.join(text)
    text = text.replace('_', "")
    text = text.replace(' ', "")
    return text

def deletePattern(item,patten,flag):
    '''

    :param item: 字段名
    :param patten: 正则表达式或约束词
    :param flag: 0正则 其他为约数词
    :return:
    '''
    if flag == 0:
        file_path = ".\\data\\pattern.json"
    else:
        file_path = ".\\data\\limit_phrase.json"
    try:
        with open(file_path, 'r', encoding="utf-8")as f:
            dict = json.load(f)
            if dict[item]:
                dict[item].remove(patten)
            else:
                print("字段的正则表达式或限制词不存在，删除失败！！！")
                return
            with open(file_path, 'w', encoding="utf-8")as f:
                dict = json.dumps(dict)
                f.write(dict)
                print("删除成功！！！")
    except json.decoder.JSONDecodeError:
        print("文件为空或无该字段，删除失败！！！")
        return

def addPattern(item,patten,flag):
    '''

    :param item:
    :param patten:
    :param file_path: ".\\data\\limit_phrase.json"
    :return:
    '''
    if flag==0:
        file_path=".\\data\\pattern.json"
    else:
        file_path = ".\\data\\limit_phrase.json"
    try:
        with open(file_path, 'r', encoding="utf-8")as f:
            dict = json.load(f)
            if dict[item]:
                dict[item].append(patten)
            else:
                dict[item] = [patten]
            with open(file_path, 'w', encoding="utf-8")as f:
                dict = json.dumps(dict)
                f.write(dict)
                print("追加内容成功！！！！")
    except json.decoder.JSONDecodeError:
        print("文件为空，现在载入第一条数据")
        with open(file_path, 'w', encoding="utf-8")as f:
            dict = {item: [patten]}
            dict = json.dumps(dict)
            f.write(dict)
# deletePattern("CONTRACT_NAME","编号：",1)
# import re
# list=[i.start() for i in re.finditer('\\\\', 'C:\\Users\\aaa\\computer\\flicker\\01213.jpg')]
# print(list)