from dataclasses import dataclass 
from alias import * 

__all__ = [
    'ScholarPublish', 
]


@dataclass
class ScholarPublish:
    class Metadata:
        database = 'zhitu_calculation'
        collection = 'scholar_publish'
        
    _id: Str = None 

    created_time: Str = None 

    scholar_id: Int = None 

    scholar_name: Str = None 

    org_name: Str = None 

    # 论文、专利、项目id
    publish_id: Int = None 

    publish_type: Str = None 

    field_list: Optional[list[dict[str, Any]]] = None 
