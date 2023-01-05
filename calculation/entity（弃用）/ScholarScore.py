from dataclasses import dataclass 
from alias import * 

__all__ = [
    'ScholarScore', 
]


@dataclass
class ScholarScore:
    class Metadata:
        database = 'zhitu_calculation'
        collection = 'scholar_score'
    
    _id: Str = None 
    
    created_time: Str = None 

    scholar_id: Int = None 

    scholar_name: Str = None 

    scholar_gender: Str = None 

    scholar_birth_year: Int = None 

    scholar_title: Str = None 

    # 获得国家荣誉值
    award_value: Int = None 

    # 学者基本分
    basic_score: Float = None 

    org_id: Int = None 

    org_name: Str = None 

    department: Str = None 

    field_id: Int = None 
    field_name: Str = None  
    field_level: Int = None 

    # 是否自己创建 
    is_original: Bool = None 

    # 原始分数 
    original_score: Float = None 

    # 原始分数公式 
    origin_score_formula: Str = None 

    # 归一化分数
    innovation_score: Float = None 

    # 归一化分数公式
    innovation_score_formula: Str = None 

    # 涨幅
    increase: Float = None 

    # 涨幅百分比
    increase_percentage: Float = None 

    # 排名
    rank_innovation: Int = None 

    # 涨幅排名
    rank_percentage: Int = None 

    # 领域优先顺序
    priority: Int = None 

    # 历史得分
    scholar_history_score: Float = None 

    # 当前得分
    scholar_performance_score: Float = None 

    province: Str = None 
    city: Str = None 
    district: Str = None 
    org_type: Str = None 
    is_high_tech_ent: Bool = None 
    org_code: Str = None 
    email: Str = None 

    last_rank_innovation: Int = None 
