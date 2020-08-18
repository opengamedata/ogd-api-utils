# include libraries
import abc
import typing
from datetime import date
# include local files
import utils
from schemas.Schema import Schema

## @class FileExports
#  Completely dumb struct that just enforces the names of the three kinds of file we can output.
#  @param dump Bool stating whether to output a dump file or not.
#  @param raw  Bool stating whether to output a raw file or not.
#  @param proc Bool stating whether to output a processed feature file or not.
class ExportFiles:
    def __init__(self, dump:bool = True, raw:bool = True, proc:bool = True):
        self.dump = dump
        self.raw = raw
        self.proc = proc

## @class Request
#  Dumb struct to hold data related to requests for data export.
#  This way, we've at least got a list of what is available in a request.
#  Acts as a base class for more specific types of request.
class Request(abc.ABC):
    ## Constructor for the request base class.
    #  Just stores whatever data is given. No checking done to ensure we have all
    #  necessary data, this can be checked wherever Requests are actually used.
    #  @param game_id An identifier for the game from which we want to extract data.
    #                 Should correspond to the app_id in the database.
    #  @param start_date   The starting date for our range of data to process.
    #  @param end_date     The ending date for our range of data to process.
    #  @param max_sessions Maximum number of sessions to be processed.
    #  @param min_moves    The minimum number of moves (events) per session.
    #                      Any session with fewer moves is ignored.
    # TODO: Not actually sure if I ever set up code to ignore sessions with < min_moves.
    def __init__(self, game_id: str = None, max_sessions: int = None, min_moves: int = None, export_files: ExportFiles = ExportFiles()):
        self.export_files = export_files
        self.game_id = game_id
        self.max_sessions = max_sessions
        self.min_moves = min_moves

    ## Abstract method to retrieve the list of IDs for all sessions covered by
    #  the request.
    @abc.abstractmethod
    def retrieveSessionIDs(self, db_cursor, db_settings) -> typing.List:
        pass

## Class representing a request that includes a range of dates to be retrieved
#  for the given game.
class DateRangeRequest(Request):
    def __init__(self, game_id: str = None, max_sessions: int = None, min_moves: int = None,
                 start_date: date = None, end_date: date = None, export_files: ExportFiles = ExportFiles()):
        Request.__init__(self, game_id=game_id, max_sessions=max_sessions, min_moves=min_moves, export_files=export_files)
        self.start_date = start_date
        self.end_date = end_date

    ## String representation of a request. Just gives game id, and date range.
    def __str__(self):
        fmt = "%Y%m%d"
        return f"{self.game_id}: {self.start_date.strftime(fmt)}-{self.end_date.strftime(fmt)}"

    ## Method to retrieve the list of IDs for all sessions covered by
    #  the request.
    def retrieveSessionIDs(self, db_cursor, db_settings) -> typing.List:
        # We grab the ids for all sessions that have 0th move in the proper date range.
        if self.game_id == "LAKELAND":
            supported_vers = Schema(schema_name="LAKELAND.json").schema()['config']['SUPPORTED_VERS']
        elif self.game_id == "JOWILDER":
            supported_vers = Schema(schema_name="JOWILDER.json").schema()['config']['SUPPORTED_VERS']
        else:
            supported_vers = []
        ver_filter = f" AND `app_version` in ({','.join([str(x) for x in supported_vers])}) " if supported_vers else ''
        filt = "`app_id`=\"{}\" AND `session_n`='0' AND (`server_time` BETWEEN '{}' AND '{}'){}".format( \
                        self.game_id, self.start_date.isoformat(), self.end_date.isoformat(), ver_filter)
        session_ids_raw = utils.SQL.SELECT(cursor=db_cursor, db_name=db_settings["DB_NAME_DATA"], table=db_settings["table"],
                                columns=["`session_id`"], filter=filt,
                                sort_columns=["`session_id`"], sort_direction="ASC", distinct=True, limit=self.max_sessions)
        return [sess[0] for sess in session_ids_raw]

## Class representing a request for a specific list of session IDs.
class IDListRequest(Request):
    def __init__(self, game_id: str = None, max_sessions: int = None, min_moves: int = None,
                    session_ids = [], export_files: ExportFiles = ExportFiles()):
        Request.__init__(self, game_id=game_id, max_sessions=max_sessions, min_moves=min_moves, export_files=export_files)
        self._session_ids = session_ids

    ## Method to retrieve the list of IDs for all sessions covered by
    #  the request. Should just be the original request list.
    def retrieveSessionIDs(self, db_cursor, db_settings) -> typing.List:
        return self._session_ids

class FileRequest(Request):
    def __init__(self, file_path, game_id: str = None, export_files: ExportFiles = ExportFiles(), max_sessions: int = None, min_moves: int = None):
        Request.__init__(self, game_id=game_id, max_sessions=max_sessions, min_moves=min_moves, export_files=export_files)
        self.file_path = file_path

    def retrieveSessionIDs(self, db_cursor, db_settings) -> typing.List:
        return []