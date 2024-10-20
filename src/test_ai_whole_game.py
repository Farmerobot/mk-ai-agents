from game.game_engine import GameEngine
from game.players.base_player import Player
from game.models.engine import GamePhase, PlayerRole

n = 1
for i in range(n):
    print(f"Test {i} of {n}")

    game = GameEngine()

    players = [
        Player("Wateusz", agent="ai", model_name="gpt-4o"),
        Player("Waciej", agent="ai", model_name="gpt-4o"),
        Player("Warek", agent="ai", model_name="gpt-4o"),
        Player("Wikolaj", agent="ai", model_name="gpt-4o"),
        Player("Warcin", agent="ai", model_name="gpt-4o", role=PlayerRole.IMPOSTOR),
    ]
    game.load_players(players, force_crewmate_to_impostor=False)
    game.init_game()
    game.DEBUG = True
    game.save_playthrough = f"whole_game_test__new_{i}.txt"
    game.enter_main_game_loop()
    crewmates_won = game.check_crewmates_win()
    impostor_won = game.check_impostors_win()
    print("Crewmates won" if crewmates_won else "Impostor won")
    print("End of test")
