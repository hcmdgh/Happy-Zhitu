import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
import numpy as np 
from typing import Any, Optional 

journal_score_map: dict[int, float] = dict() 
conference_score_map: dict[int, float] = dict() 
org_map: dict[str, dict[str, Any]] = dict()


def compute_paper_score(journal_id: Optional[int] = None, 
                        conference_id: Optional[int] = None) -> float:
    def compute_journal_score(rank: int,
                            total: int) -> float:
        score = 40 + (1 - (rank / total) / 0.2) * 60 
        score = max(score, 40.)
        
        return score 

    compute_conference_score = compute_journal_score 
    
    if not journal_score_map:
        with open('/MAG/json/journal_ranked.json', 'r', encoding='utf-8') as fp:
            line_list = list(fp)
            total = len(line_list)
            
            for rank, line in enumerate(line_list, start=1):
                entry = json.loads(line)
                journal_id = int(entry['id']) 

                journal_score_map[journal_id] = compute_journal_score(
                    rank = rank, 
                    total = total, 
                )
            
    if not conference_score_map:
        with open('/MAG/json/conference_ranked.json', 'r', encoding='utf-8') as fp:
            line_list = list(fp)
            total = len(line_list)
            
            for rank, line in enumerate(line_list, start=1):
                entry = json.loads(line)
                conference_id = int(entry['id']) 
                
                conference_score_map[conference_id] = compute_conference_score(
                    rank = rank, 
                    total = total, 
                )
                
    if journal_id and journal_id in journal_score_map:
        paper_score = journal_score_map[journal_id]
    elif conference_id and conference_id in conference_score_map:
        paper_score = conference_score_map[conference_id]
    else:
        paper_score = 0.
        
    paper_score = max(paper_score, 40.)
    
    return paper_score 


def translate_org_name(org_name: str) -> tuple[int, str]:
    if not org_map:
        with open('/MAG/zhitu/mag_zhitu_org_map.json', 'r', encoding='utf-8') as fp: 
            for line in fp:
                org_entry = json.loads(line)
                org_name = org_entry['org_name']
                org_map[org_name] = org_entry 
                
    org_id = org_map[org_name]['zhitu_zh_org_id']
    org_zh_name = org_map[org_name]['org_zh_name'] 

    return org_id, org_zh_name 


def compute_history_recent(paper_list: list[dict[str, Any]]) -> tuple:
    def compute_paper_list_score(paper_list: list[dict[str, Any]]) -> tuple[float, float]:
        if not paper_list:
            return 40., 40. 
        
        year_list = [ paper['year'] for paper in paper_list ]
        year_cnt = max(year_list) - min(year_list) + 1 
        year_cnt = min(year_cnt, 10) 
        
        sum_score = sum(paper['score'] for paper in paper_list)
        avg_score = sum_score / year_cnt 
        sum_score = max(sum_score, 50.)
        avg_score = max(avg_score, 50.)
        
        return sum_score, avg_score 
    
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
        history_avg_citation_cnt = np.mean(history_citation_cnt_list)
    else:
        history_avg_citation_cnt = 0. 
        
    if recent_citation_cnt_list:
        recent_avg_citation_cnt = np.mean(recent_citation_cnt_list)
    else:
        recent_avg_citation_cnt = 0. 
    
    recent_paper_cnt = len(recent_paper_list)
    history_paper_cnt = len(history_paper_list)
    recent_sum_score, recent_avg_score = compute_paper_list_score(recent_paper_list)
    history_sum_score, history_avg_score = compute_paper_list_score(history_paper_list)

    return recent_sum_score, recent_avg_score, history_sum_score, history_avg_score, recent_avg_citation_cnt, history_avg_citation_cnt, recent_paper_cnt, history_paper_cnt 


def main():
    field_scholar_map: dict[int, dict[int, dict[str, Any]]] = dict()
    
    with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=3171_8738):
            paper_entry = json.loads(line)
            paper_id = int(paper_entry['id'])
            mag_paper_entry = paper_entry['raw_data']
            paper_year = int(mag_paper_entry['year'])
            paper_citation_cnt = int(mag_paper_entry['citationCount'])
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
                
            paper_score = compute_paper_score(
                journal_id = journal_id, 
                conference_id = conference_id, 
            )
            
            for field in field_list:
                field_id = int(field['field_id']) 
                field_name = core.translate_field_name_to_zh(field['field_name'])
                field_level = int(field['field_level']) + 1 

                if field_id not in field_scholar_map: 
                    field_scholar_map[field_id] = dict()
                
                for scholar in scholar_list: 
                    scholar_id = int(scholar['scholar_id'])
                    scholar_name = scholar['scholar_name'].strip() 
                    org_id, org_name = translate_org_name(scholar['scholar_org'])  

                    if scholar_id not in field_scholar_map[field_id]:
                        field_scholar_map[field_id][scholar_id] = dict() 

                    entry = field_scholar_map[field_id][scholar_id] 
                    
                    entry['scholar_id'] = scholar_id 
                    entry['scholar_name'] = scholar_name
                    entry['org_name'] = org_name 
                    entry['org_id'] = org_id 
                    entry['field_id'] = field_id 
                    entry['field_name'] = field_name 
                    entry['field_level'] = field_level 
                    
                    if 'paper_list' not in entry: 
                        entry['paper_list'] = []  

                    entry['paper_list'].append(
                        dict(
                            id = paper_id, 
                            score = paper_score, 
                            year = paper_year, 
                            citation_cnt = paper_citation_cnt, 
                        )
                    )
    
    for field_id in tqdm(field_scholar_map): 
        for scholar_id in field_scholar_map[field_id]:
            entry = field_scholar_map[field_id][scholar_id] 
            
            paper_list = entry['paper_list']
            recent_sum_score, recent_avg_score, history_sum_score, history_avg_score, recent_avg_citation_cnt, history_avg_citation_cnt, recent_paper_cnt, history_paper_cnt = compute_history_recent(paper_list)
            score = history_sum_score * 0.4 + recent_sum_score * 0.6 
            growth = recent_avg_score - history_avg_score 
            growth_percent = growth / history_avg_score * 100. 
            
            entry['recent_sum_score'] = recent_sum_score
            entry['recent_avg_score'] = recent_avg_score
            entry['history_sum_score'] = history_sum_score
            entry['history_avg_score'] = history_avg_score
            entry['recent_avg_citation_cnt'] = recent_avg_citation_cnt
            entry['history_avg_citation_cnt'] = history_avg_citation_cnt
            entry['history_paper_cnt'] = history_paper_cnt
            entry['recent_paper_cnt'] = recent_paper_cnt
            entry['score'] = score
            entry['growth'] = growth  
            entry['growth_percent'] = growth_percent 
         
    with open('/MAG/zhitu/wzm/es_scholar_performance_index.json', 'w', encoding='utf-8') as fp_performance:
        with open('/MAG/zhitu/wzm/es_scholar_history_index.json', 'w', encoding='utf-8') as fp_history:   
            with open('/MAG/zhitu/wzm/es_scholar_index.json', 'w', encoding='utf-8') as fp_total:   
                for field_id in tqdm(field_scholar_map): 
                    sorted_entry_list = sorted(
                        field_scholar_map[field_id].values(), 
                        key = lambda x: -x['score'], 
                    )
                    
                    N = len(sorted_entry_list)
                    
                    for rank, entry in enumerate(sorted_entry_list): 
                        entry['rank'] = rank + 1 
                        entry['norm_score'] = 40 + (N - rank - 1) / N * 60
                        
                    sorted_entry_list.sort(
                        key = lambda x: -x['growth_percent'], 
                    )
                    
                    for rank, entry in enumerate(sorted_entry_list): 
                        entry['growth_rank'] = rank + 1 
                        
                    for entry in sorted_entry_list:
                        history_entry = dict(
                            _id = f"{entry['scholar_id']}-{entry['field_id']}",
                            createTime = core.get_now_datetime_str('-'), 
                            updateTime = core.get_now_datetime_str('-'), 
                            scholarId = entry['scholar_id'], 
                            fieldId = entry['field_id'], 
                            historyIndexScore = entry['history_avg_score'], 
                            paperScore = entry['history_sum_score'],
                            projectScore = 0.,
                            patentScore = 0., 
                            sciNum = 0, 
                            sciProportion = 0.,
                            coreJournalNum = 0, 
                            impactFactorAverage = 0., 
                            impactFactorMax = 0., 
                            citationAverage = entry['history_avg_citation_cnt'], 
                            firstAuthorNum = 0, 
                            paperNum = entry['history_paper_cnt'], 
                        ) 
                        json_str = json.dumps(history_entry, ensure_ascii=False).strip() 
                        print(json_str, file=fp_history) 
                        
                        recent_entry = dict(
                            _id = f"{entry['scholar_id']}-{entry['field_id']}",
                            createTime = core.get_now_datetime_str('-'), 
                            updateTime = core.get_now_datetime_str('-'), 
                            scholarId = entry['scholar_id'],
                            fieldId = entry['field_id'], 
                            performanceIndexScore = entry['recent_avg_score'], 
                            paperScore = entry['recent_sum_score'],
                            projectScore = 0.,
                            patentScore = 0., 
                            sciNum = 0, 
                            sciProportion = 0.,
                            coreJournalNum = 0, 
                            impactFactorAverage = 0., 
                            impactFactorMax = 0., 
                            citationAverage = entry['recent_avg_citation_cnt'],
                            firstAuthorNum = 0, 
                            paperNum = entry['recent_paper_cnt'], 
                        ) 
                        json_str = json.dumps(recent_entry, ensure_ascii=False).strip() 
                        print(json_str, file=fp_performance) 
                        
                        total_entry = dict(
                            _id = f"{entry['scholar_id']}-{entry['field_id']}",
                            createTime = core.get_now_datetime_str('-'), 
                            updateTime = core.get_now_datetime_str('-'), 
                            scholarId = entry['scholar_id'],
                            scholarName = entry['scholar_name'],
                            awardValue = 30, 
                            basicIndex = 40.,
                            orgId = entry['org_id'],
                            orgName = entry['org_name'],
                            fieldId = entry['field_id'], 
                            fieldName = entry['field_name'],
                            level = entry['field_level'],
                            originIndex = entry['score'], 
                            innovationIndex = entry['norm_score'], 
                            increase = entry['growth'], 
                            increasePercentage = entry['growth_percent'],
                            rankInnovation = entry['rank'], 
                            rankPercentage = entry['growth_rank'], 
                            priority = entry['field_level'],
                            scholarHistoryIndex = entry['history_avg_score'],
                            scholarPerformanceIndex = entry['recent_avg_score'],
                        )
                        json_str = json.dumps(total_entry, ensure_ascii=False).strip() 
                        print(json_str, file=fp_total)
                        

if __name__ == '__main__':
    main() 
