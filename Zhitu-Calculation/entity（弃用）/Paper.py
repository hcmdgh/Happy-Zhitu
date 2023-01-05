from dataclasses import dataclass 
from alias import * 

__all__ = [
    'Paper', 
]


@dataclass
class Paper:
    class Metadata:
        database = 'zhitu_calculation'
        collection = 'paper'
        
    _id: Int = None 

    type: Str = None 

    abstract: Str = None 

    year: Int = None 

    title: Str = None 

    norm_title: Str = None 

    date: Str = None 

    citation_count: Int = None 

    author_list: Optional[list[dict[str, Any]]] = None 

    field_list: Optional[list[dict[str, Any]]] = None 

    doc_type: Str = None 
    doi: Str = None 
    lang: Str = None 
    venue: Str = None 
    publisher: Str = None 
    issue: Str = None 
    volume: Str = None 
    page_start: Str = None 
    page_end: Str = None 
    issn: Str = None 
    isbn: Str = None 
    class_code: Str = None 
    impact_factor: Float = None 
    class_name: Str = None 

    is_ei: Bool = None 

    keywords: Optional[list[str]] = None 
