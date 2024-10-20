from game.game_engine import GameEngine
from game.players.base_player import Player
from game.models.engine import GamePhase
from game.players.base_player import PlayerRole

game = GameEngine()

impostor = Player("Warcin", agent="human")
impostor.set_role(PlayerRole.IMPOSTOR)

players = [
    Player("Wateusz", agent="ai", model_name="gpt-4o-mini"),
    Player("Waciej", agent="ai", model_name="gpt-4o-mini"),
    Player("Warek", agent="ai", model_name="gpt-4o-mini"),
    Player("Wikolaj", agent="ai", model_name="gpt-4o-mini"),
    impostor,
]
game.load_players(players, force_crewmate_to_impostor=False)
game.init_game()

game.enter_main_game_loop()
