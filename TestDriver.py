from tests.t_HelloAPI import t_HelloAPI
from tests.t_GameStateAPI import t_GameStateAPI

test_Hello = t_HelloAPI()
# print("Running test_Hello:")
# test_Hello.RunAll()
# print("Done")
test_GameState = t_GameStateAPI()
print("Running test_GameState:")
test_GameState.RunAll()
print("Done")