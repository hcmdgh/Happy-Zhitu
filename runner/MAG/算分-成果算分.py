import json 
from dataclasses import dataclass 
from tqdm.auto import tqdm 
import numpy as np 
import lzma 
from datetime import datetime 
from typing import Any, Optional 


@dataclass 
class Org:
    ztid: int 
    name: str
    zh_name: str 
    

@dataclass 
class Scholar:
    ztid: int 
    name: str 
    org: Org 
    paper_list: list['Paper']
    
    
@dataclass 
class Field:
    ztid: int 
    name: str
    zh_name: str 
    level: int  
    
    
@dataclass
class Paper:
    ztid: int 
    title: str 
    field_list: list[Field]
    year: int 
    citation_count: int 
    score: float 
    
    
@dataclass 
class ScholarFieldScore:
    scholar: Scholar 
    field: Field 
    paper_list: list[Paper]
    history_score: float 
    recent_score: float 
    overall_score: float 
    norm_score: float 
    norm_score_rank: int 
    increase: float 
    increase_percent: float 
    increase_percent_rank: int  
    
    
@dataclass 
class FieldScore:
    field: Field 
    scholar_field_score_list: list[ScholarFieldScore]
    
    
def compute_paper_score(citation_count: int) -> float:
    # citation_count: 0 -> score: 60
    # citation_count: 10 -> score: 80
    # citation_count: 20 -> score: 90
    # citation_count: 30 -> score: 95
    score = 60 + 40 * ( 1 - (2**0.1) ** (-citation_count) ) 
    
    return score 


def compute_recent_paper_score(paper_score_sum: float) -> float:
    # paper_score_sum: 0 -> 60
    # paper_score_sum: 10 * 70 -> 85
    # paper_score_sum: 30 * 70 -> 98
    score = 60 + 40 * ( 1 - (20**(1/2100)) ** (-paper_score_sum) ) 
    
    return score 


def compute_history_paper_score(paper_score_sum: float) -> float:
    # paper_score_sum: 0 -> 60
    # paper_score_sum: 20 * 70 -> 85
    # paper_score_sum: 60 * 70 -> 98
    score = 60 + 40 * ( 1 - (20**(1/4200)) ** (-paper_score_sum) ) 
    
    return score 


def compute_scholar_score(scholar: Scholar) -> list[ScholarFieldScore]:
    field_score_map: dict[int, ScholarFieldScore] = dict() 
    
    for paper in scholar.paper_list:
        for field in paper.field_list:
            field_id = field.ztid 
            
            if field_id not in field_score_map:
                field_score_map[field_id] = ScholarFieldScore(
                    scholar = scholar, 
                    field = field, 
                    paper_list = [paper], 
                    history_score = None, 
                    recent_score = None, 
                    overall_score = None, 
                    norm_score = None, 
                    norm_score_rank = None, 
                    increase = None, 
                    increase_percent = None, 
                    increase_percent_rank = None, 
                )
            else:
                field_score_map[field_id].paper_list.append(paper)
                
    for field_score in field_score_map.values():
        recent_paper_list = []
        history_paper_list = []

        for paper in field_score.paper_list:
            if paper.year >= 2019:
                recent_paper_list.append(paper)
            else:
                history_paper_list.append(paper)
                
        recent_score = compute_recent_paper_score(sum(paper.score for paper in recent_paper_list))
        history_score = compute_history_paper_score(sum(paper.score for paper in history_paper_list))
        overall_score = 0.6 * recent_score + 0.4 * history_score 
        
        field_score.history_score = history_score
        field_score.recent_score = recent_score 
        field_score.overall_score = overall_score 
        field_score.increase = recent_score - history_score 
        field_score.increase_percent = field_score.increase / history_score * 100
        
    # 每个学者保留1个一级领域、3个二级领域、5个三级领域
    field_score_list = list(field_score_map.values())
    field_score_list.sort(key=lambda x: -x.overall_score)
    
    filtered_field_score_list = [] 
    L1_cnt = L2_cnt = L3_cnt = 0 
    
    for field_score in field_score_list:
        if field_score.field.level == 1 and L1_cnt < 1:
            filtered_field_score_list.append(field_score) 
            L1_cnt += 1 
            
        if field_score.field.level == 2 and L2_cnt < 3:
            filtered_field_score_list.append(field_score) 
            L2_cnt += 1
            
        if field_score.field.level == 3 and L3_cnt < 5:
            filtered_field_score_list.append(field_score) 
            L3_cnt += 1  
    
    return filtered_field_score_list


def compute_norm_score(score: float, 
                       min_score: float,
                       max_score: float) -> float:
    # (10, 10, 100) -> 60
    # (60, 10, 100) -> 82 
    # (100, 10, 100) -> 100 
    if max_score - min_score > 0:
        norm_score = 60 + 40 * (score - min_score) / (max_score - min_score)
    else:
        norm_score = 80. 
    
    return norm_score 


def now_str() -> str: 
    now = datetime.now()
    s = now.strftime('%Y-%m-%d %H:%M:%S')

    return s 

    
def main():
    field_map: dict[int, Field] = dict() 
    org_map: dict[str, Org] = dict() 
    paper_map: dict[int, Paper] = dict() 
    scholar_map: dict[int, Scholar] = dict() 
    field_score_map: dict[int, FieldScore] = dict() 
    
    with open('/MAG/zhitu/field_map_L012_enriched.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp):
            entry = json.loads(line)
            field_id = int(entry['field_zhituid']) 
            field_map[field_id] = Field(
                ztid = field_id, 
                name = entry['field_name'].strip(),
                zh_name = entry['field_zh_name'].strip(),
                level = int(entry['field_level']) + 1, 
            )
            
    with open('/MAG/zhitu/mag_zhitu_org_map.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp):
            entry = json.loads(line)
            org_id = int(entry['zhitu_zh_org_id']) 
            org_name = entry['org_name'].strip()
            org_zh_name = entry['org_zh_name'].strip()
            
            org_map[org_name] = Org(
                ztid = org_id, 
                name = org_name, 
                zh_name = org_zh_name, 
            )
            
    with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as fp:
        for line in tqdm(fp, total=3171_8738):
            entry = json.loads(line)
            
            field_id_set = { int(field['field_id']) for field in entry['field_list'] }
            field_list = [ field_map[field_id] for field_id in field_id_set if field_id in field_map ]

            paper = Paper(
                ztid = int(entry['id']),
                title = entry['title'].strip(), 
                field_list = field_list, 
                year = int(entry['raw_data']['year']),
                citation_count = int(entry['raw_data']['citationCount']),
                score = compute_paper_score(int(entry['raw_data']['citationCount'])), 
            )
            paper_map[paper.ztid] = paper 

            for scholar in entry['scholar_list']:
                scholar_id = int(scholar['scholar_id'])
                scholar_name = scholar['scholar_name'].strip() 
                scholar_org = scholar['scholar_org'].strip() 

                if scholar_id not in scholar_map:
                    scholar_map[scholar_id] = Scholar(
                        ztid = scholar_id, 
                        name = scholar_name, 
                        org = org_map[scholar_org], 
                        paper_list = [paper], 
                    )
                else:
                    scholar_map[scholar_id].paper_list.append(paper)

    for scholar in tqdm(scholar_map.values()):
        scholar_score_list = compute_scholar_score(scholar)
        
        for scholar_field_score in scholar_score_list:
            field = scholar_field_score.field 
            field_id = field.ztid 
            
            if field_id not in field_score_map: 
                field_score_map[field_id] = FieldScore(
                    field = field, 
                    scholar_field_score_list = [scholar_field_score], 
                )        
            else:
                field_score_map[field_id].scholar_field_score_list.append(scholar_field_score)
                
    for field_score in tqdm(field_score_map.values()):
        field_score.scholar_field_score_list.sort(key=lambda x: -x.overall_score)
        min_score = field_score.scholar_field_score_list[-1].overall_score
        max_score = field_score.scholar_field_score_list[0].overall_score
        
        for rank, scholar_field_score in enumerate(field_score.scholar_field_score_list):
            rank = rank + 1 
            
            scholar_field_score.norm_score_rank = rank     
            scholar_field_score.norm_score = compute_norm_score(
                score = scholar_field_score.overall_score, 
                min_score = min_score, 
                max_score = max_score, 
            )
            
        field_score.scholar_field_score_list.sort(key=lambda x: -x.increase_percent)

        for rank, scholar_field_score in enumerate(field_score.scholar_field_score_list):
            rank = rank + 1 
            
            scholar_field_score.increase_percent_rank = rank  
            
    with lzma.open('/MAG/zhitu/wzm/es/es_scholar_max_index.json.xz', 'wt', encoding='utf-8') as fp:
        for field_score in tqdm(field_score_map.values()):
            entry = dict(
                _id = f"{field_score.field.ztid}-1", 
                c1 = 0,
                c2 = 0,
                c3 = 0,
                c4 = 0,
                c5 = 0,
                c6 = 0,
                c7 = 0,
                c8 = 0,
                c9 = 0,
                c10 = 0,
                citationAverage = 0.,
                coreJournalNum = 0, 
                fieldId = field_score.field.ztid,
                firstAuthorNum = 0,
                impactFactorAverage = 0.,
                impactFactorMax = 0.,   
                indexScore = 0., 
                indexType = "HISTORY", 
                internationalNum = 0, 
                inventionApp3YearsRate = 0., 
                inventionAppNum = 0, 
                inventionGrant3YearsRate = 0., 
                inventionGrantNum = 0, 
                paperNum = 0, 
                rankScore = 0, 
                sciNum = 0, 
                sciProportion = 0., 
                utilityApp3YearsRate = 0., 
                utilityAppNum = 0, 
                utilityGrant3YearsRate = 0., 
                utilityGrantNum = 0, 
            )
            
            json_str = json.dumps(entry, ensure_ascii=False).strip() 
            print(json_str, file=fp)
            
            entry = dict(
                _id = f"{field_score.field.ztid}-2", 
                c1 = 0,
                c2 = 0,
                c3 = 0,
                c4 = 0,
                c5 = 0,
                c6 = 0,
                c7 = 0,
                c8 = 0,
                c9 = 0,
                c10 = 0,
                citationAverage = 0.,
                coreJournalNum = 0, 
                fieldId = field_score.field.ztid,
                firstAuthorNum = 0,
                impactFactorAverage = 0.,
                impactFactorMax = 0.,   
                indexScore = 0., 
                indexType = "PERFORMANCE", 
                internationalNum = 0, 
                inventionApp3YearsRate = 0., 
                inventionAppNum = 0, 
                inventionGrant3YearsRate = 0., 
                inventionGrantNum = 0, 
                paperNum = 0, 
                rankScore = 0, 
                sciNum = 0, 
                sciProportion = 0., 
                utilityApp3YearsRate = 0., 
                utilityAppNum = 0, 
                utilityGrant3YearsRate = 0., 
                utilityGrantNum = 0, 
            )
            
            json_str = json.dumps(entry, ensure_ascii=False).strip() 
            print(json_str, file=fp)
            
    with lzma.open('/MAG/zhitu/wzm/es/es_scholar_index.json.xz', 'wt', encoding='utf-8') as scholar_index_fp:
        with lzma.open('/MAG/zhitu/wzm/es/es_scholar_history_index.json.xz', 'wt', encoding='utf-8') as scholar_history_index_fp:
            with lzma.open('/MAG/zhitu/wzm/es/es_scholar_performance_index.json.xz', 'wt', encoding='utf-8') as scholar_performance_index_fp:
                for field_score in tqdm(field_score_map.values()):
                    for scholar_field_score in field_score.scholar_field_score_list:
                        scholar_index_entry = dict(
                            _id = f"{scholar_field_score.scholar.ztid}-{scholar_field_score.field.ztid}",
                            createTime = now_str(), 
                            updateTime = now_str(),
                            scholarId = scholar_field_score.scholar.ztid, 
                            scholarName = scholar_field_score.scholar.name,
                            awardValue = 30,
                            basicIndex = 40.,
                            orgId = scholar_field_score.scholar.org.ztid, 
                            orgName = scholar_field_score.scholar.org.zh_name,
                            fieldId = scholar_field_score.field.ztid, 
                            fieldName = scholar_field_score.field.zh_name, 
                            level = scholar_field_score.field.level,
                            originIndex = scholar_field_score.overall_score, 
                            innovationIndex = scholar_field_score.norm_score, 
                            increase = scholar_field_score.increase,
                            increasePercentage = scholar_field_score.increase_percent, 
                            rankInnovation = scholar_field_score.norm_score_rank, 
                            rankPercentage = scholar_field_score.increase_percent_rank, 
                            priority = scholar_field_score.field.level,
                            scholarHistoryIndex = scholar_field_score.history_score,
                            scholarPerformanceIndex = scholar_field_score.recent_score,
                        ) 
                        
                        json_str = json.dumps(scholar_index_entry, ensure_ascii=False).strip() 
                        print(json_str, file=scholar_index_fp)

                        paper_list = scholar_field_score.paper_list 
                        paper_cnt = len(paper_list)
                        mean_citation_count = np.mean([ paper.citation_count for paper in paper_list ])
                        
                        scholar_history_index_entry = dict(
                            _id = f"{scholar_field_score.scholar.ztid}-{scholar_field_score.field.ztid}",
                            createTime = now_str(), 
                            updateTime = now_str(),
                            scholarId = scholar_field_score.scholar.ztid, 
                            fieldId = scholar_field_score.field.ztid, 
                            historyindexScore = scholar_field_score.history_score,
                            paperScore = scholar_field_score.history_score,
                            patentScore = 0., 
                            projectScore = 0.,
                            sciNum = 0, 
                            sciProportion = 0., 
                            coreJournalNum = 0, 
                            impactFactorAverage = 0., 
                            impactFactorMax = 0., 
                            citationAverage = mean_citation_count, 
                            firstAuthorNum = 0, 
                            paperNum = paper_cnt, 
                        )
                        
                        json_str = json.dumps(scholar_history_index_entry, ensure_ascii=False).strip() 
                        print(json_str, file=scholar_history_index_fp)
                        
                        scholar_performance_index_entry = dict(
                            _id = f"{scholar_field_score.scholar.ztid}-{scholar_field_score.field.ztid}",
                            createTime = now_str(), 
                            updateTime = now_str(),
                            scholarId = scholar_field_score.scholar.ztid, 
                            fieldId = scholar_field_score.field.ztid, 
                            performanceindexScore = scholar_field_score.recent_score,
                            paperScore = scholar_field_score.recent_score,
                            patentScore = 0., 
                            projectScore = 0.,
                            sciNum = 0, 
                            sciProportion = 0., 
                            coreJournalNum = 0, 
                            impactFactorAverage = 0., 
                            impactFactorMax = 0., 
                            citationAverage = mean_citation_count, 
                            firstAuthorNum = 0, 
                            paperNum = paper_cnt, 
                        )
                        
                        json_str = json.dumps(scholar_performance_index_entry, ensure_ascii=False).strip() 
                        print(json_str, file=scholar_performance_index_fp)
                
                
if __name__ == '__main__':
    main() 
