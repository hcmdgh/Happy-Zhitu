import json 


def main():
    journal_list = []
    
    with open('/MAG/json/journal.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            
            journal_list.append(
                dict(
                    id = int(entry['id']), 
                    name = entry['display_name'].strip(), 
                    rank = int(entry['rank']), 
                    citation_count = int(entry['citation_count']), 
                )
            )
            
    journal_list.sort(key=lambda entry: entry['rank']) 
            
    conference_list = [] 
    
    with open('/MAG/json/conference.json', 'r', encoding='utf-8') as fp:
        for line in fp:
            entry = json.loads(line)
            
            conference_list.append(
                dict(
                    id = int(entry['id']), 
                    name = entry['display_name'].strip(), 
                    abbr = entry['normalized_name'].strip(), 
                    rank = int(entry['rank']), 
                    citation_count = int(entry['citation_count']), 
                )
            )
            
    conference_list.sort(key=lambda entry: entry['rank']) 

    with open('/MAG/json/journal_ranked.json', 'w', encoding='utf-8') as fp:
        for i, entry in enumerate(journal_list, start=1):
            percentage = f"{i} / {len(journal_list)} = {i/len(journal_list):.4f}"
            entry['percentage'] = percentage 
            
            json_str = json.dumps(entry, ensure_ascii=False).strip()
            print(json_str, file=fp)
            
    with open('/MAG/json/conference_ranked.json', 'w', encoding='utf-8') as fp:
        for i, entry in enumerate(conference_list, start=1):
            percentage = f"{i} / {len(conference_list)} = {i/len(conference_list):.4f}"
            entry['percentage'] = percentage 
            
            json_str = json.dumps(entry, ensure_ascii=False).strip()
            print(json_str, file=fp)
    

if __name__ == '__main__':
    main() 
