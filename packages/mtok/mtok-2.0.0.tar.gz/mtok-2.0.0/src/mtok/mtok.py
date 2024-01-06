"""

    """

import json
from dataclasses import dataclass
from pathlib import Path

import requests

# GitHub username
gu = 'imahdimir'

class Const :
    # local GitHub token filename
    lg = '.gt.json'

    # local directories for GitHub token json file
    ld = {
            'mac'     : '/Users/mahdi/' ,
            'hetzner' : '/root/'
            }

@dataclass
class KeyVal :
    key: str
    val: str

def find_local_github_token_fpn() -> Path :
    k = Const()
    for dyr in k.ld.values() :
        fp = Path(dyr) / k.lg
        if fp.exists() :
            return fp

def ret_val_by_key_fr_json(fp , key) -> KeyVal :
    with open(fp , 'r') as f :
        dc = json.load(f)
    return KeyVal(key = key , val = dc[key])

def get_all_tokens_fr_tokens_repo(gtok_fp) -> dict :
    """ Gets all tokens from the private tokens repo """
    tok = ret_val_by_key_fr_json(gtok_fp , gu)
    url = ret_github_url_for_private_access_to_file(tok.key ,
                                                    tok.val ,
                                                    tok.key ,
                                                    'tokens' ,
                                                    'main' ,
                                                    'main.json')
    r = requests.get(url)
    j = r.json()
    return j

def ret_github_url_for_private_access_to_file(user ,
                                              token ,
                                              target_usr ,
                                              target_repo ,
                                              branch ,
                                              filename
                                              ) -> str :
    """ Makes a raw GitHub url for private access to a file in a repo """
    return f'https://{user}:{token}@raw.githubusercontent.com/{target_usr}/{target_repo}/{branch}/{filename}'

def get_token(key = None) -> str :
    """ Gets the token by a key from the private tokens repo on my GitHub"""

    fp = find_local_github_token_fpn()

    if fp is None :
        raise ValueError(f'{gu} GitHub Token Not Found.')

    # If key is None, return the GitHub token
    if key is None :
        return ret_val_by_key_fr_json(fp , gu).val

    # Get all tokens from the private tokens repo
    all_toks = get_all_tokens_fr_tokens_repo(fp)

    wanted_tok = all_toks[key]

    return wanted_tok
