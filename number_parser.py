import os
import re


def get_number(filepath: str) -> str:
    """
    >>> from number_parser import get_number
    >>> get_number("/Users/Guest/AV_Data_Capture/snis-829.mp4")
    'snis-829'
    >>> get_number("/Users/Guest/AV_Data_Capture/snis-829-C.mp4")
    'snis-829'
    >>> get_number("C:¥Users¥Guest¥snis-829.mp4")
    'snis-829'
    >>> get_number("C:¥Users¥Guest¥snis-829-C.mp4")
    'snis-829'
    >>> get_number("./snis-829.mp4")
    'snis-829'
    >>> get_number("./snis-829-C.mp4")
    'snis-829'
    >>> get_number(".¥snis-829.mp4")
    'snis-829'
    >>> get_number(".¥snis-829-C.mp4")
    'snis-829'
    >>> get_number("snis-829.mp4")
    'snis-829'
    >>> get_number("snis-829-C.mp4")
    'snis-829'
    """
    filepath = os.path.basename(filepath)
    code_match_pattern1 = '[a-zA-Z]{2,5}[-_][0-9]{3,5}'
    code_match_pattern2 = '([a-zA-Z]{2,5})([0-9]{3,5})'
    re_rules1 = re.compile(code_match_pattern1, flags=re.IGNORECASE)
    re_rules2 = re.compile(code_match_pattern2, flags=re.IGNORECASE)

    file_code1 = re_rules1.findall(filepath)
    file_code2 = re_rules2.findall(filepath)
    if file_code1:
        return file_code1[0]
    elif file_code2:
        return file_code2[0][0].upper() + '-' +"{:0>3d}".format(int(file_code2[0][1]))#file_code2[0][1]
    else:
        return "UNKNOWN"

    #below is not used...

    if '-' in filepath or '_' in filepath:  # 普通提取番号 主要处理包含减号-和_的番号
        filepath = filepath.replace("_", "-")
        filepath.strip('22-sht.me').strip('-HD').strip('-hd')
        filename = str(re.sub("\[\d{4}-\d{1,2}-\d{1,2}\] - ", "", filepath))  # 去除文件名中时间
        if 'FC2' or 'fc2' in filename:
            filename = filename.replace('PPV','').replace('ppv','').replace('--','-').replace('_','-')
        file_number = "UNKNOWN"
        if re.search(r'\w+-\w+', filename, re.A) is not None:
            file_number = re.search(r'\w+-\w+', filename, re.A).group()
        return file_number
    else:  # 提取不含减号-的番号，FANZA CID
        try:
            return str(re.findall(r'(.+?)\.', str(re.search('([^<>/\\\\|:""\\*\\?]+)\\.\\w+$', filepath).group()))).strip("['']").replace('_', '-')
        except:
            return re.search(r'(.+?)\.', filepath)[0]


if __name__ == "__main__":
    import doctest
    doctest.testmod(raise_on_error=True)
