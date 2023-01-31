from ..util import * 

import requests

__all__ = [
    'match_scholar_with_publish', 
    'match_scholar_with_paper',
    'match_scholar_with_patent',
    'match_scholar_with_project',
]


def match_scholar_with_publish(name: str,
                               org: str) -> dict[str, set[int]]:
    """
    根据学者的姓名和机构匹配成果（姓名和机构均为中文形式），返回成果id。
    
    返回值：
    {
      paper -> 匹配的论文id
      patent -> 匹配的专利id
      project -> 匹配的项目id
    }
    
    更新日期：2022/11/15
    """
    
    return {
        'paper': match_scholar_with_paper(name=name, org=org),
        'patent': match_scholar_with_patent(name=name, org=org),
        'project': match_scholar_with_project(name=name, org=org),
    }


def match_scholar_with_project(name: str,
                               org: str) -> set[int]:
    """
    根据学者的姓名和机构匹配项目（姓名和机构均为中文形式），返回项目id。

    更新日期：2022/11/15
    """
    resp = requests.get(url='http://192.168.0.90:9200/project/_search',
                        json={
                            'query': {
                                'bool': {
                                    'must': [
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'match': {
                                                            'authors.scholarName': name 
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'leader': name 
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'scholars.scholarName': name 
                                                        }
                                                    },
                                                ]
                                            }
                                        },
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'match': {
                                                            'org': org  
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'scholars.orgName': org  
                                                        }
                                                    },
                                                ]
                                            }
                                        },
                                    ]
                                }
                            },
                            'size': 999,
                        })
    
    assert resp.status_code == 200
    
    resp_json = resp.json()
    
    project_ids = {
        int(item['_id'])
        for item in resp_json['hits']['hits']
    }

    return project_ids


def match_scholar_with_patent(name: str,
                              org: str) -> set[int]:
    """
    根据学者的姓名和机构匹配专利（姓名和机构均为中文形式），返回专利id。
    
    更新日期：2022/11/15
    """
    resp = requests.get(url='http://192.168.0.90:9200/patent/_search',
                        json={
                            'query': {
                                'bool': {
                                    'must': [
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'match': {
                                                            'authors.scholarName': name 
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'inventorName': name 
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'scholars.scholarName': name 
                                                        }
                                                    },
                                                ]
                                            }
                                        },
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'match': {
                                                            'applicantName': org  
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'scholars.orgName': org  
                                                        }
                                                    },
                                                ]
                                            }
                                        },
                                    ]
                                }
                            },
                            'size': 999,
                        })
    
    assert resp.status_code == 200
    
    resp_json = resp.json()
    
    patent_ids = {
        int(item['_id'])
        for item in resp_json['hits']['hits']
    }

    return patent_ids


def match_scholar_with_paper(name: str,
                             org: str) -> set[int]:
    """
    根据学者的姓名和机构匹配论文（姓名和机构均为中文形式），返回论文id。
    
    更新日期：2022/11/15
    """
    pinyin_names = convert_name_to_pinyins(name)
    
    resp = requests.get(url='http://192.168.0.90:9200/paper/_search',
                        json={
                            'query': {
                                'bool': {
                                    'must': [
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'match': {
                                                            'scholars.orgName': org,     
                                                        }
                                                    },
                                                    {
                                                        'match': {
                                                            'authors.orgName': org,     
                                                        }
                                                    }
                                                ]
                                            }
                                        },
                                        {
                                            'bool': {
                                                'should': [
                                                    {
                                                        'terms': {
                                                            'scholars.scholarName': list(pinyin_names),     
                                                        }
                                                    },
                                                    {
                                                        'terms': {
                                                            'authors.scholarName': list(pinyin_names),     
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    ]
                                }    
                            },
                            'size': 999,
                        })
    
    assert resp.status_code == 200
    
    resp_json = resp.json()
    
    paper_ids = {
        int(item['_id'])
        for item in resp_json['hits']['hits']
    }

    return paper_ids
