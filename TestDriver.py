from tests.t_HelloAPI import t_HelloAPI
from tests.t_GameStateAPI import t_GameStateAPI

# test_Hello = t_HelloAPI()
# print("***\nRunning test_Hello:")
# test_Hello.RunAll()
# print("Done\n***")
test_GameState = t_GameStateAPI()
print("***\nRunning test_GameState:\n")
test_GameState.RunAll()
print("Done\n***")