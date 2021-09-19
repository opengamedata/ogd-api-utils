from tests.t_HelloAPI import t_HelloAPI
from tests.t_GameStateAPI import t_GameStateAPI
from tests.t_PlayerAPI import t_PlayerAPI
from tests.t_config import EnabledTests


if EnabledTests['HELLO']:
    test_Hello = t_HelloAPI()
    print("***\nRunning test_Hello:")
    test_Hello.RunAll()
    print("Done\n***")
if EnabledTests['PLAYER']:
    test_Player = t_PlayerAPI()
    print("***\nRunning test_Player:\n")
    test_Player.RunAll()
    print("Done\n***")
if EnabledTests['GAME_STATE']:
    test_GameState = t_GameStateAPI()
    print("***\nRunning test_GameState:\n")
    test_GameState.RunAll()
    print("Done\n***")