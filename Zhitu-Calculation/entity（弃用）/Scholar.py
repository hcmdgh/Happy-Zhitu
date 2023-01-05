from dataclasses import dataclass 
from alias import * 

__all__ = [
    'Scholar', 
]


@dataclass
class Scholar: 
    class Metadata:
        database = 'zhitu_calculation'
        collection = 'scholar'
    
    _id: Int = None 
    
    created_time: Str = None 

    scholar_id: Int = None 

    name: Str = None 

    gender: Str = None 

    birth_year: Int = None 

    org_id: Int = None 

    org_name: Str = None 

    department: Str = None 

    sub_department: Str = None 

    major: Str = None 

    education: Str = None 

    position: Str = None 

    title: Str = None 

    email: Str = None 

    phone: Str = None 

    # 获得国家荣誉值
    award_value: Int = None 

    # 学者基本分
    basic_score: Float = None 
