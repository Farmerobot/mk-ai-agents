import pytest
from src.game.game_engine import GameEngine
from src.game.players.base_player import PlayerRole
from src.game.players.ai import AIPlayer
from src.game.players.human import HumanPlayer
from src.game.utils import get_impostor_tasks


def test_load_human_players():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    player3 = HumanPlayer(name="Player 3")
    game_engine.load_players([player1, player2, player3], impostor_count=1)
    assert len(game_engine.state.players) == 3
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], HumanPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], HumanPlayer)
    assert game_engine.state.players[2].name == "Player 3"
    assert isinstance(game_engine.state.players[2], HumanPlayer)


# Mocking ChatOpenAI and ChatGoogleGenerativeAI using pytest-mock
def test_load_ai_players():
    game_engine = GameEngine()
    player1 = AIPlayer(name="Player 1", llm_model_name="gpt-4o-mini")
    player2 = AIPlayer(name="Player 2", llm_model_name="gpt-4o-mini")
    player3 = AIPlayer(name="Player 3", llm_model_name="gpt-4o-mini")

    # Loading the AI players
    game_engine.load_players([player1, player2, player3], impostor_count=1)

    # Assertions
    assert len(game_engine.state.players) == 3
    assert game_engine.state.players[0].name == "Player 1"
    assert isinstance(game_engine.state.players[0], AIPlayer)
    assert game_engine.state.players[1].name == "Player 2"
    assert isinstance(game_engine.state.players[1], AIPlayer)
    assert game_engine.state.players[2].name == "Player 3"
    assert isinstance(game_engine.state.players[2], AIPlayer)


def test_load_human_players_with_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    player3 = HumanPlayer(name="Player 3")
    game_engine.load_players([player1, player2, player3], impostor_count=1)
    assert len(game_engine.state.players) == 3
    impostors = [player for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR]
    assert len(impostors) == 1


def test_load_human_players_no_impostor():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    player3 = HumanPlayer(name="Player 3")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3], impostor_count=0)


def test_load_few_players_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2])


def test_load_imbalanced_team_raises_error():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    player3 = HumanPlayer(name="Player 3")
    player4 = HumanPlayer(name="Player 4")
    with pytest.raises(ValueError):
        game_engine.load_players([player1, player2, player3, player4], impostor_count=2)


def test_load_ten_players_four_impostors():
    game_engine = GameEngine()
    players = [HumanPlayer(name=f"Player {i}") for i in range(1, 11)]
    game_engine.load_players(players, impostor_count=4)
    assert len(game_engine.state.players) == 10
    impostors = [player for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR]
    assert len(impostors) == 4


def test_one_impostor_when_impostor_count_is_one():
    game_engine = GameEngine()
    player1 = HumanPlayer(name="Player 1")
    player2 = HumanPlayer(name="Player 2")
    player3 = HumanPlayer(name="Player 3")
    player4 = HumanPlayer(name="Player 4", role=PlayerRole.IMPOSTOR)
    game_engine.load_players([player1, player2, player3, player4], impostor_count=1)
    impostors = [player for player in game_engine.state.players if player.role == PlayerRole.IMPOSTOR]
    assert len(impostors) == 1
