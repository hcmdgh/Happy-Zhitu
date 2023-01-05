import util 

from typing import Optional, Any 

__all__ = [
    'convert_mag_date_to_es', 
    'convert_mag_paper_to_es', 
]


def convert_mag_date_to_es(mag_date_str: Optional[str]) -> Optional[str]:
    if not mag_date_str:
        return None 
    
    es_date_str = mag_date_str.strip() + ' 00:00:00'

    return es_date_str 


def convert_mag_paper_to_es(mag_paper_entry: dict[str, Any],
                            author_list: Optional[list[dict[str, Any]]] = None,
                            field_list: Optional[list[dict[str, Any]]] = None,) -> dict[str, Any]:
    paper_title = mag_paper_entry['original_title'].strip() 
    norm_paper_title = util.normalize_str(paper_title)
    
    if field_list: 
        field_list = [
            dict(
                
            )
            for field in field_list 
        ]
    
    es_paper_entry = dict(
        abst = None, 
        authors = , 
        beenEi = None, 
        classCode = None,
        className = None, 
        date = convert_mag_date_to_es(mag_paper_entry['date']),
        docType = mag_paper_entry['doc_type'], 
        doi = mag_paper_entry['doi'], 
        fields 
        impactFactor = None, 
        issn = None, 
        issue = mag_paper_entry['issue'],
        keywords = None, 
        lang = None, 
        maId = str(mag_paper_entry['id']), 
        ncitation = mag_paper_entry['citation_count'],
        pageEnd = mag_paper_entry['last_page'], 
        pageStart = mag_paper_entry['first_page'], 
        publisher = mag_paper_entry['publisher'], 
        scholars 
        title = paper_title, 
        titleLowercase = norm_paper_title, 
        type = 'paper', 
        urls = None, 
        venue = mag_paper_entry['original_venue'], 
        volume = mag_paper_entry['volume'],
        year = mag_paper_entry['year'],
        update_time = util.now(), 
    )
    