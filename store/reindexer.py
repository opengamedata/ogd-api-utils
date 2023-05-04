# Rudolph, the red-nosed reindexer...
# import libraries
import argparse
import json
import logging
import os
import pandas as pd
import zipfile
from pathlib import Path
from typing import Dict
# local imports
from config.config import settings as settings

def meta_to_index(meta:Dict, data_dir:Path):
    # raw_stat = os.stat(raw_csv_full_path)
    # sessions_stat = os.stat(sessions_csv_full_path)
    pop_file  = meta['population_file'].split('/')[-1] if meta.get("population_file") is not None else None
    play_file = meta['players_file'].split('/')[-1]    if meta.get('players_file')    is not None else None
    sess_file = meta['sessions_file'].split('/')[-1]   if meta.get('sessions_file')   is not None else None
    raw_file  = meta['raw_file'].split('/')[-1]        if meta.get('raw_file')        is not None else None
    evt_file  = meta['events_file'].split('/')[-1]     if meta.get('events_file')     is not None else None
    return {
        "population_file"     : str(data_dir / pop_file)  if pop_file  is not None else None,
        "players_file"        : str(data_dir / play_file) if play_file is not None else None,
        "sessions_file"       : str(data_dir / sess_file) if sess_file is not None else None,
        "events_file"         : str(data_dir / evt_file)  if evt_file  is not None else None,
        "raw_file"            : str(data_dir / raw_file)  if raw_file  is not None else None,
        "population_template" : meta.get('population_template', "") if pop_file  is not None else None,
        "players_template"    : meta.get('players_template', "")    if play_file is not None else None,
        "sessions_template"   : meta.get('sessions_template', "")   if sess_file is not None else None,
        "events_template"     : meta.get('events_template', "")     if evt_file  is not None else None,
        "ogd_revision"        : meta.get('ogd_revision', None),
        "start_date"          : meta.get('start_date', None),
        "end_date"            : meta.get('end_date', None),
        "date_modified"       : meta.get('date_modified', None),
        "sessions"            : meta.get('sessions', None)
    }

def index_meta(root:Path, name:str, indexed_files:Dict):
    next_meta : Dict = {}
    with open(root / name, 'r') as next_file:
        next_meta = json.load(next_file)
    next_game  = next_meta['game_id']
    next_id    = next_meta['dataset_id']
    next_mod   = next_meta['date_modified']
    if not next_game in indexed_files.keys():
        indexed_files[next_game] = {}
    # if we already indexed something with this dataset id, and this was older, do nothing..
    if next_id in indexed_files[next_game].keys() and next_mod < indexed_files[next_game][next_id]['date_modified']:
        return indexed_files
    else:
        indexed_files[next_game][next_id] = meta_to_index(meta=next_meta, data_dir=root)
    return indexed_files

def index_zip(root:Path, name:str, indexed_files):
    # for reference, here's how the indices of a tsv file should look, if we're not dealing with a "cycle" game.
    PIECE_INDICES = {'name':0, 'start_date':1, 'to':2, 'end_date':3, 'id':4, 'file_type':5}
    top = name.split('.')
    pieces = top[0].split('_')
    game_id = pieces[0] if pieces[0] != 'CYCLE' else f"{pieces[0]}_{pieces[1]}"
    start_date = pieces[-5]
    end_date = pieces[-3]
    dataset_id  = f"{game_id}_{start_date}_to_{end_date}"
    kind = pieces[-1]
    if not game_id in indexed_files.keys():
        indexed_files[game_id] = {}
    # if we already indexed something with this dataset id, then only update if this one is newer.
    # else, just stick this new meta in the index.
    file_path = root / name
    if not dataset_id in indexed_files[game_id].keys():
        # after getting info from filename on the game id, start/end dates, etc. we can peek at the file and count the rows, *if* it's a session file.
        session_ct = None
        if kind == "session-features":
            with zipfile.ZipFile(file_path, 'r') as zip:
                data = pd.read_csv(zip.open(f"{dataset_id}/{top[0]}.tsv"), sep='\t')
                session_ct = len(data.index)
        logging.log(msg=f"Indexing {file_path}", level=logging.INFO)
        indexed_files[game_id][dataset_id] = {
            "population_file"     : str(file_path) if kind == 'population-features' else None,
            "population_template" : f'/tree/{game_id}' if kind == 'population-features' else None,
            "players_file"        : str(file_path) if kind == 'player-features' else None,
            "players_template"    : f'/tree/{game_id}' if kind == 'players-features' else None,
            "sessions_file"       : str(file_path) if kind == 'session-features' else None,
            "sessions_template"   : f'/tree/{game_id}' if kind == 'sessions-features' else None,
            "raw_file"            : str(file_path) if kind == 'raw' else None,
            "events_file"         : str(file_path) if kind == 'events' else None,
            "events_template"     : f'/tree/{game_id}' if kind == 'events' else None,
            "ogd_revision"        : None,
            "start_date"          : start_date,
            "end_date"            : end_date,
            "date_modified"       : None,
            "sessions"            : session_ct
        }
    else:
        # handle population file
        if indexed_files[game_id][dataset_id]["population_file"] == None and kind == 'population-features':
            logging.log(msg=f"Updating index with {file_path}", level=logging.INFO)
            indexed_files[game_id][dataset_id]["population_file"] = str(file_path)
            indexed_files[game_id][dataset_id]["population_template"] = ''
        # handle players file
        if indexed_files[game_id][dataset_id]["players_file"] == None and kind == 'player-features':
            logging.log(msg=f"Updating index with {file_path}", level=logging.INFO)
            indexed_files[game_id][dataset_id]["players_file"] = str(file_path)
            indexed_files[game_id][dataset_id]["players_template"] = ''
        # handle sessions file
        if indexed_files[game_id][dataset_id]["sessions_file"] == None and kind == 'session-features':
            logging.log(msg=f"Updating index with {file_path}", level=logging.INFO)
            indexed_files[game_id][dataset_id]["sessions_file"] = str(file_path)
            indexed_files[game_id][dataset_id]["sessions_template"] = ''
        # handle events file
        if indexed_files[game_id][dataset_id]["events_file"] == None and kind == 'events':
            logging.log(msg=f"Updating index with {file_path}", level=logging.INFO)
            indexed_files[game_id][dataset_id]["events_file"] = str(file_path)
            indexed_files[game_id][dataset_id]["events_template"] = ''
        # handle raw file
        if indexed_files[game_id][dataset_id]["raw_file"] == None and kind == 'raw':
            logging.log(msg=f"Updating index with {file_path}", level=logging.INFO)
            indexed_files[game_id][dataset_id]["raw_file"] = str(file_path)
    return indexed_files

def generate_index(walk_data):
    indexed_files = {}
    zips = []
    for root, subdirs, files in walk_data:
        for name in files:
            root_path = Path(root)
            if not 'BACKUP' in root:
                ext = name.split('.')[-1]
                if (ext == 'meta'):
                    logging.log(msg=f"Indexing {root_path / name}", level=logging.INFO)
                    indexed_files = index_meta(root_path, name, indexed_files)
                elif (ext == 'zip'):
                    logging.log(msg=f"Reserving {root_path / name}", level=logging.DEBUG)
                    zips.append((root_path, name))
                else:
                    logging.log(msg=f"Doing nothing with {root_path / name}", level=logging.DEBUG)
            else:
                logging.log(msg=f"Doing nothing with {root_path / name}", level=logging.DEBUG)
    for root_path,name in zips:
        indexed_files = index_zip(root_path, name, indexed_files)
    return indexed_files

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-l", "--level", help="Set the logging level to DEBUG, INFO, or WARN", type=str, choices=['DEBUG', 'INFO', 'WARN'])
args = arg_parser.parse_args()
if args.level == 'WARN':
    logging.basicConfig(level=logging.WARN)
elif args.level == 'INFO':
    logging.basicConfig(level=logging.INFO)
elif args.level == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG)
data_dirs = os.walk("./data/")
indexed_files = generate_index(data_dirs)
if not "CONFIG" in indexed_files.keys():
    indexed_files["CONFIG"] = {
        "files_base"     : settings.get("FILE_INDEXING", {}).get("REMOTE_URL", None),
        "templates_base" : settings.get("FILE_INDEXING", {}).get("TEMPLATES_URL", None)
    }
# print(f"Final set of indexed files: {indexed_files}")
with open(Path("./data/file_list.json"), "w+") as indexed_zips_file:
    indexed_zips_file.write(json.dumps(indexed_files, indent=4, sort_keys=True))
    indexed_zips_file.close()
