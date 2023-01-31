from .str_util import * 

import pypinyin 

__all__ = [
    'convert_str_to_pinyin', 
    'convert_name_to_pinyin_1', 
    'convert_name_to_pinyin_2', 
    'convert_name_to_pinyins', 
]


def convert_str_to_pinyin(s: str) -> list[str]:
    """
    将字符串中每一个汉字转换成拼音，其他无法转换的字符原样返回。

    例如：
    1. "王德庆" -> ['wang', 'de', 'qing']
    2. "Wang Deqing" -> ['Wang Deqing']
    """
    pinyin_list = pypinyin.lazy_pinyin(s)
    assert isinstance(pinyin_list, list)
    assert all(isinstance(x, str) for x in pinyin_list)

    return pinyin_list


def convert_name_to_pinyin_1(name: str) -> str:
    """
    将中文姓名转换为拼音。

    例如："王德庆" -> "wangdeqing"
    """

    pinyin_list = convert_str_to_pinyin(name)

    result = normalize_str(''.join(pinyin_list), keep_space=False)
    
    return result 


def convert_name_to_pinyin_2(name: str) -> str:
    """
    将中文姓名转换为拼音。

    例如："王德庆" -> "deqingwang"
    """

    pinyin_list = convert_str_to_pinyin(name)

    if len(pinyin_list) >= 2: 
        pinyin_list = pinyin_list[1:] + pinyin_list[:1]

    result = normalize_str(''.join(pinyin_list), keep_space=False)
    
    return result 


def convert_name_to_pinyins(name: str) -> set[str]:
    """
    将中文姓名转换为几种常见拼音格式。
    例如：
      王德庆 -> {'王德庆', 'Wang Deqing', 'Deqing Wang', 'Wang De-qing'}
      王德 -> {'王德', 'Wang De-', 'De Wang', 'Wang De'}

    更新日期：2022/11/17
    """
    
    pinyin_list = convert_str_to_pinyin(name)
    
    if len(pinyin_list) == 0:
        return { name }
    elif len(pinyin_list) == 1:
        return { name, pinyin_list[0].capitalize() }
    else:
        return {
            name,
            pinyin_list[0].capitalize() + ' ' + ''.join(pinyin_list[1:]).capitalize(),
            ''.join(pinyin_list[1:]).capitalize() + ' ' + pinyin_list[0].capitalize(),
            pinyin_list[0].capitalize() + ' ' + pinyin_list[1].capitalize() + '-' + ''.join(pinyin_list[2:]),
        }
