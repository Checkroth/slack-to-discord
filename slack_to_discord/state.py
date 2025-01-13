from pathlib import Path
from dataclasses import dataclass
import json

DEFAULT_STATE_FILE_PATH = Path("slack_to_discord_import_state.json")
class InvalidStateFile(Exception):
    pass

@dataclass
class Message:
    # Mix of information about a message that we can combine to
    # reasonably assume that it wouldn't ever be duplicated
    text: str
    date: str
    time: str

@dataclass
class ChannelImportState:
    channel_name: str
    last_message: Message | None
    completed: bool

def _establish_path(state_file_path: str | None):
    if not state_file_path:
        state_file_path = DEFAULT_STATE_FILE_PATH
    else:
        state_file_path = Path(state_file_path)
    return state_file_path
    

def load_import_state(state_file_path: str | None):
    state_file_path = _establish_path(state_file_path)
    if not state_file_path.exists():
        return {}
    
    with open(state_file_path, 'r') as inf:
        try:
            state = json.loads(inf.read())
        except json.JSONEncoder:
            raise InvalidStateFile


def store_import_state(state_file_path: str, state: dict[str, ChannelImportState]):
    state_file_path = _establish_path(state_file_path)
    with open(state_file_path, 'w') as outf:
        outf.write(json.dumps(state))
