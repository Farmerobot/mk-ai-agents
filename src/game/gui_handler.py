from typing import Any, List, Dict, Optional
import streamlit as st
from game.game_state import GameState
from pydantic import BaseModel, Field
from game.players.base_player import Player, PlayerRole
from streamlit.delta_generator import DeltaGenerator

from game.models.history import PlayerState


class GUIHandler(BaseModel):
    player_states_placeholders: List[DeltaGenerator] = Field(default_factory=list)
    game_log_placeholder: Optional[DeltaGenerator] = None
    game_log_json: Optional[DeltaGenerator] = None
    cols: List[DeltaGenerator] = Field(default_factory=list)
    model_config = {"arbitrary_types_allowed": True}
    sidebar: List[DeltaGenerator] = Field(default_factory=list)
    
    def init_gui(self, game_state: GameState):
        num_players = len(game_state.players)
        if not self.cols:
            self.cols = [col.empty() for col in st.columns(num_players)]
            for col in self.cols:
                self.player_states_placeholders.append(col.empty())
            # self.player_states_placeholders = [st.empty() for _ in range(num_players)]
        if not self.sidebar:
            sidebar = st.sidebar
            with sidebar:
                for _ in game_state.players:
                    self.sidebar.append(st.empty())
        if not self.game_log_placeholder:
            self.game_log_placeholder = st.empty()
        if not self.game_log_json:
            self.game_log_json = st.empty()
        

    def update_gui(self, game_state: GameState):
        self.init_gui(game_state)
        for i, (player, col) in enumerate(zip(game_state.players, self.cols)):
            with col:
                self._display_player_info(player, self.player_states_placeholders[i])
                
        for i, (player, sidebar) in enumerate(zip(game_state.players, self.sidebar)):
            with sidebar:
                self._display_short_player_info(player, st)
        with self.game_log_placeholder.container(height=500):
            st.text("\n".join(game_state.playthrough))
        self.game_log_json.json(game_state.to_dict(), expanded=True)
        
    def _display_short_player_info(self, player: Player, placeholder: DeltaGenerator):
        with placeholder.container(border=True): 
            self._display_name_role_status(player)
            self._display_tasks_progress(player)
        

    def _display_player_info(self, player: Player, placeholder: DeltaGenerator):
        with placeholder.container():  # Clear previous content
            st.subheader(player.name)
            self._display_status(player)
            self._display_role(player)
            self._display_tasks_progress(player)
            self._display_tasks(player)
            self._display_location(player)
            self._display_action_taken(player)
            self._display_action_result(player)
            self._display_recent_actions(player)


    def _display_name_role_status(self, player: Player):
        status_icon = "✅" if player.state.life == PlayerState.ALIVE else "❌"
        role_icon = "😈" if player.role == PlayerRole.IMPOSTOR else "👤"
        complete_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        if player.role == PlayerRole.IMPOSTOR:
            st.write(f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon} ⏳{player.kill_cooldown}")
        else:
            st.write(f"{status_icon} {player.name} - ({complete_tasks}/{len(player.state.tasks)}) {role_icon}")

    def _display_status(self, player: Player):
        status_icon = "✅" if player.state.life == PlayerState.ALIVE else "❌"
        st.write(f"Status: {status_icon} {player.state.life.value}")

    def _display_role(self, player: PlayerRole):
        role_icon = "😈" if player.role == PlayerRole.IMPOSTOR else "👤"
        st.write(f"Role: {role_icon} {player.role.value}")

    def _display_tasks_progress(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.progress(completed_tasks / total_tasks if total_tasks > 0 else 0) #Handle division by zero
        
    def _display_tasks(self, player: Player):
        completed_tasks = sum(1 for task in player.state.tasks if "DONE" in str(task))
        total_tasks = len(player.state.tasks)
        st.write(f"Tasks: {completed_tasks}/{total_tasks}")
        st.write("Tasks:")
        for task in player.state.tasks:
            st.write(f"- {task}")
        

    def _display_location(self, player: Player):
        st.write(f"Location: {player.state.location.value} {player.state.player_in_room}")
        
    def _display_action_taken(self, player: Player):
        action = player.history.rounds[-1].response
        if action.isdigit():
            st.write(f"Action Taken: {player.history.rounds[-1].actions[int(action)]}")
        else:
            st.write(f"Action Taken: {action}")
        
    def _display_action_result(self, player: Player):
        st.write(f"Action Result: {player.history.rounds[-1].action_result}")

    def _display_recent_actions(self, player: Player):
        st.write("Seen Actions:")
        for action in player.history.rounds[-1].seen_actions:
            st.write(f"- {action}")

