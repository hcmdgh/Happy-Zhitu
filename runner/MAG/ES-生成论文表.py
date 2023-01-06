import os 
import sys 
os.chdir(os.path.dirname(__file__))
sys.path.append('../..')

import core 

import json 
from tqdm.auto import tqdm 
from typing import Any, Optional 


def main():
    journal_map: dict[int, str] = dict()
    
    with open('/MAG/json/journal.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            journal_id = int(entry['id'])
            journal_name = entry['display_name'].strip() 
            
            journal_map[journal_id] = journal_name 
            
    conference_map: dict[int, str] = dict()
    
    with open('/MAG/json/conference.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            conference_id = int(entry['id'])
            conference_name = entry['display_name'].strip() 
            
            conference_map[conference_id] = conference_name 
            
    org_map: dict[str, dict[str, Any]] = dict()
    
    with open('/MAG/zhitu/mag_zhitu_org_map.json', 'r', encoding='utf-8') as fp: 
        for line in fp:
            org_entry = json.loads(line)
            org_name = org_entry['org_name']
            org_map[org_name] = org_entry 
    
    with open('/MAG/zhitu/wzm/es_paper.json', 'w', encoding='utf-8') as writer:
        with open('/MAG/zhitu/wzm/paper_author_field.json', 'r', encoding='utf-8') as reader:
            for line in tqdm(reader, total=3171_8738):
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
                    
                if journal_id:
                    venue = journal_map[journal_id]
                elif conference_id:
                    venue = conference_map[conference_id]
                else:
                    venue = mag_paper_entry['originalVenue'] 

                author_list = [
                    dict(
                        scholarName = entry['scholar_name'], 
                        orgName = org_map[entry['scholar_org']]['org_zh_name'], 
                    )
                    for entry in scholar_list
                ]

                scholar_list = [
                    dict(
                        scholarId = entry['scholar_id'],
                        scholarName = entry['scholar_name'], 
                        orgId = org_map[entry['scholar_org']]['zhitu_zh_org_id'],
                        orgName = org_map[entry['scholar_org']]['org_zh_name'],
                    )
                    for entry in scholar_list
                ]
                
                field_list = [
                    dict(
                        fieldId = entry['field_id'], 
                        fieldName = core.translate_field_name_to_zh(entry['field_name']), 
                        level = entry['field_level'] + 1,
                    ) 
                    for entry in field_list
                ]

                entry = dict(
                    _id = f"{paper_id}",
                    createTime = core.get_now_datetime_str('-'),
                    updateTime = core.get_now_datetime_str('-'),
                    type = 'paper',
                    year = int(mag_paper_entry['year']) if mag_paper_entry['year'] else None, 
                    title = mag_paper_entry['originalTitle'],
                    titleLowercase = core.normalize_str(mag_paper_entry['originalTitle'], keep_space=True),
                    date = mag_paper_entry['date'] if mag_paper_entry['date'] else None,
                    ncitation = int(mag_paper_entry['citationCount']) if mag_paper_entry['citationCount'] else None, 
                    authors = author_list, 
                    fields = field_list, 
                    scholars = scholar_list, 
                    docType = 'conference' if conference_id else 'journal',
                    doi = mag_paper_entry['doi'], 
                    venue = venue, 
                    publisher = mag_paper_entry['publisher'],
                    issue = mag_paper_entry['issue'],
                    volume = mag_paper_entry['volume'],
                    pageStart = mag_paper_entry['firstPage'],
                    pageEnd = mag_paper_entry['lastPage'],
                )
                
                json_str = json.dumps(entry, ensure_ascii=False).strip() 
                print(json_str, file=writer)
                        
    
if __name__ == '__main__':
    main() 
