import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
import numpy as np 
from typing import Any, Optional 


def compute_journal_score(rank: int,
                          total: int) -> float:
    score = 40 + (1 - (rank / total) / 0.2) * 60 
    score = max(score, 40.)
    
    return score 


compute_conference_score = compute_journal_score 


def compute_papers_score(paper_list: list[dict[str, Any]]) -> float:
    if not paper_list:
        return 40. 
    
    year_list = [ paper['year'] for paper in paper_list ]
    year_cnt = max(year_list) - min(year_list) + 1 
    year_cnt = min(year_cnt, 10) 
    
    total_score = sum(paper['score'] for paper in paper_list)
    
    score = total_score / year_cnt 
    score = max(score, 50.)
    
    return score 


def main():
    journal_score_map: dict[int, float] = dict() 
    
    with open('/MAG/json/journal_ranked.json', 'r', encoding='utf-8') as fp:
        line_list = list(fp)
        total = len(line_list)
        
        for rank, line in enumerate(line_list, start=1):
            entry = json.loads(line)
            journal_id = entry['id']
            
            journal_score_map[journal_id] = compute_journal_score(
                rank = rank, 
                total = total, 
            )
            
    conference_score_map: dict[int, float] = dict() 
    
    with open('/MAG/json/conference_ranked.json', 'r', encoding='utf-8') as fp:
        line_list = list(fp)
        total = len(line_list)
        
        for rank, line in enumerate(line_list, start=1):
            entry = json.loads(line)
            conference_id = entry['id']
            
            conference_score_map[conference_id] = compute_conference_score(
                rank = rank, 
                total = total, 
            )
    
    scholar_field_paper_map: dict[int, dict[int, set[int]]] = dict()
    paper_map: dict[int, dict[str, Any]] = dict()
    
    with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=3171_8738):
            paper_entry = json.loads(line)
            paper_id = int(paper_entry['id'])
            mag_paper_entry = paper_entry['raw_data']
            scholar_list = paper_entry.get('scholar_list') 
            if not scholar_list: 
                scholar_list = []
            field_list = paper_entry.get('field_list') 
            if not field_list: 
                field_list = [] 
            journal_id = mag_paper_entry.get('journalId')
            if journal_id:
                journal_id = int(journal_id)
            else:
                journal_id = None 
            conference_id = mag_paper_entry.get('conferenceSeriesId')
            if conference_id:
                conference_id = int(conference_id)
            else:
                conference_id = None 
            
            if journal_id and journal_id in journal_score_map:
                paper_score = journal_score_map[journal_id]
            elif conference_id and conference_id in conference_score_map:
                paper_score = conference_score_map[conference_id]
            else:
                paper_score = 50.  
                
            paper_map[paper_id] = dict(
                citation_cnt = int(mag_paper_entry['citationCount']),
                year = int(mag_paper_entry['year']), 
                score = paper_score, 
            )
            
            for scholar in scholar_list:
                scholar_id = int(scholar['scholar_id'])
                
                if scholar_id not in scholar_field_paper_map:
                    scholar_field_paper_map[scholar_id] = dict()
                
                for field in field_list:
                    field_id = int(field['field_id'])
                    
                    if field_id not in scholar_field_paper_map[scholar_id]:
                        scholar_field_paper_map[scholar_id][field_id] = set()
                        
                    scholar_field_paper_map[scholar_id][field_id].add(paper_id)

    with open('/MAG/zhitu/wzm/es_scholar_performance_index.json', 'w', encoding='utf-8') as fp_performance:
        with open('/MAG/zhitu/wzm/es_scholar_history_index.json', 'w', encoding='utf-8') as fp_history:
            for scholar_id in tqdm(scholar_field_paper_map):
                for field_id in scholar_field_paper_map[scholar_id]:
                    paper_ids = scholar_field_paper_map[scholar_id][field_id]
                    paper_list = [ paper_map[paper_id] for paper_id in paper_ids ]

                    history_paper_list = [] 
                    recent_paper_list = []
                    
                    for paper in paper_list: 
                        if paper['year'] >= 2019:
                            recent_paper_list.append(paper)
                        else:
                            history_paper_list.append(paper)
                    
                    history_citation_cnt_list = [ paper['citation_cnt'] for paper in history_paper_list ] 
                    recent_citation_cnt_list = [ paper['citation_cnt'] for paper in recent_paper_list ] 

                    if history_citation_cnt_list:
                        avg_history_citation_cnt = np.mean(history_citation_cnt_list)
                    else:
                        avg_history_citation_cnt = 0. 
                        
                    if recent_citation_cnt_list:
                        avg_recent_citation_cnt = np.mean(recent_citation_cnt_list)
                    else:
                        avg_recent_citation_cnt = 0. 
                        
                    history_score = compute_papers_score(history_paper_list)
                    recent_score = compute_papers_score(recent_paper_list)
                    
                    history_entry = dict(
                        _id = f"{scholar_id}-{field_id}",
                        createTime = core.get_now_datetime_str('-'), 
                        updateTime = core.get_now_datetime_str('-'), 
                        scholarId = scholar_id, 
                        fieldId = field_id, 
                        historyIndexScore = history_score, 
                        paperScore = history_score, 
                        projectScore = 0.,
                        patentScore = 0., 
                        sciNum = 0, 
                        sciProportion = 0.,
                        coreJournalNum = 0, 
                        impactFactorAverage = 0., 
                        impactFactorMax = 0., 
                        citationAverage = avg_history_citation_cnt, 
                        firstAuthorNum = 0, 
                        paperNum = len(history_paper_list), 
                    ) 
                    json_str = json.dumps(history_entry, ensure_ascii=False).strip() 
                    print(json_str, file=fp_history) 
                    
                    recent_entry = dict(
                        _id = f"{scholar_id}-{field_id}",
                        createTime = core.get_now_datetime_str('-'), 
                        updateTime = core.get_now_datetime_str('-'), 
                        scholarId = scholar_id, 
                        fieldId = field_id, 
                        performanceIndexScore = recent_score, 
                        paperScore = recent_score, 
                        projectScore = 0.,
                        patentScore = 0., 
                        sciNum = 0, 
                        sciProportion = 0.,
                        coreJournalNum = 0, 
                        impactFactorAverage = 0., 
                        impactFactorMax = 0., 
                        citationAverage = avg_recent_citation_cnt, 
                        firstAuthorNum = 0, 
                        paperNum = len(recent_paper_list), 
                    ) 
                    json_str = json.dumps(recent_entry, ensure_ascii=False).strip() 
                    print(json_str, file=fp_performance) 
                    

if __name__ == '__main__':
    main() 
