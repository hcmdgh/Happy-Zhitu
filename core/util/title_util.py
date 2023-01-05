from typing import Any, Optional

__all__ = [
    'merge_title', 
]


def merge_title(title1: Optional[str],
                title2: Optional[str]) -> str:
    if not title1:
        title1 = ''
    if not title2:
        title2 = ''
        
    title_set_1 = set(title1.split())
    title_set_2 = set(title2.split())

    merged_title_set = title_set_1 | title_set_2 
    
    # [BEGIN] 分级
    if '教授' in merged_title_set:
        merged_title_set -= {'副教授', '讲师', '助理教授'}
    if '副教授' in merged_title_set:
        merged_title_set -= {'讲师', '助理教授'}
    if '讲师' in merged_title_set:
        merged_title_set -= {'助理教授'}
    
    if '研究员' in merged_title_set:
        merged_title_set -= {'副研究员', '助理研究员'}
    if '副研究员' in merged_title_set:
        merged_title_set -= {'助理研究员'}
    # [END]
    
    merged_title = ' '.join(merged_title_set)
    
    return merged_title
