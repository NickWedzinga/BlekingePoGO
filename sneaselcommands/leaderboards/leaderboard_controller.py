from datetime import datetime
from typing import Union, Dict

import discord

from common import constants
from utils.database_connector import execute_statement, create_select_top_x_scores_query, \
    get_ranking_of_user


class LeaderboardController:
    def __init__(self, leaderboard: str):
        self.leaderboard = leaderboard

    @staticmethod
    def validate_score(score: str) -> bool:
        """Validates submitted score"""
        return score.isnumeric()

    def get_previous_top_3(self) -> Dict:
        """Gets the top 3 scores in a leaderboard sorted by order from first to third"""
        return execute_statement(create_select_top_x_scores_query(table_name=self.leaderboard, limit=3)).all(
            as_dict=True)

    def insert_score(self, score: str, interaction: discord.Interaction):
        """Inserts submitted score"""
        execute_statement(
            f"INSERT INTO leaderboard__{self.leaderboard} (name, score, submit_date) "
            f"VALUES ('{interaction.user.display_name}', {score}, DATE '{datetime.now().date()}')")

    async def congratulate(self, interaction: discord.Interaction, previous_top_3: Dict):
        """Sends a congratulations message custom to which ranking the user got"""
        current_top_3 = execute_statement(
            create_select_top_x_scores_query(table_name=self.leaderboard, limit=3)).all(as_dict=True)

        name = interaction.user.display_name

        # if submission made top 3
        if any(name == entry.get("name") for entry in current_top_3):
            for index, user in enumerate(current_top_3):
                # new rank 1
                if index == 0 and name == user.get("name") and not name == previous_top_3[0].get("name"):
                    await interaction.response.send_message(
                        f":crown: :first_place: CONGRATULATIONS {interaction.user.mention} on your new #{index + 1} placement in the {self.leaderboard} leaderboard!"
                        f"\nPlease send an in-game screenshot to any admin for verification.", ephemeral=True)
                # new top 3
                elif name == user.get("name") and not any(
                        name == user_entry.get("name") for user_entry in previous_top_3):
                    await interaction.response.send_message.send(
                        f":crown: Congratulations {interaction.user.mention} on your #{index + 1} placement in the "
                        f"{self.leaderboard} leaderboard! \n"
                        f"Please send an in-game screenshot to any admin for verification.", ephemeral=True)
                elif name == user.get("name"):
                    await interaction.response.send_message(
                        f":crown: Congratulations {interaction.user.mention} on your #{index + 1} position in the "
                        f"{self.leaderboard} leaderboard!", ephemeral=True)
        # submission not top 3
        else:
            record_collection = execute_statement(create_select_top_x_scores_query(self.leaderboard))
            ranking = get_ranking_of_user(name=name, record_collection=record_collection)
            await interaction.response.send_message(
                f"Nice work {interaction.user.mention} on your #{ranking} position in the "
                f"{self.leaderboard} leaderboard, keep it up!", ephemeral=True)

    def create_leaderboard_embed(self, user: Union[discord.User, discord.Member]):
        """Creates the leaderboard embed"""
        score_dict = execute_statement(
            create_select_top_x_scores_query(table_name=self.leaderboard)).all(as_dict=True)
        embed = discord.Embed(title=f"Leaderboard Blekinge: {self.leaderboard.capitalize()} \n", color=0xff9900,
                              description=f"Submit your score by clicking a button and selecting submit")
        embed.set_thumbnail(
            url=f"https://static.wikia.nocookie.net/pokemongo/images/{constants.MEDAL_ICON_URLS.get(self.leaderboard)}")
        embed.set_footer(text=f"Showing top 10 scores, highlighting your score")
        embed.add_field(name="\u200b", value="\u200b", inline=False)

        for index, score_entry in enumerate(score_dict[:10]):
            name = score_entry.get('name')
            name_score_text = f"{index + 1}. {name} \nScore: {score_entry.get('score')}"
            if name == user.display_name:
                name_score_text = ":reminder_ribbon: " + name_score_text
            embed.add_field(
                name=name_score_text,
                value=f"Updated: {score_entry.get('submit_date')}", inline=True)
        embed = self.__add_user_field_to_embed(embed, score_dict, user)
        return embed

    def __add_user_field_to_embed(self, embed: discord.Embed, score_dict: dict,
                                  user: Union[discord.User, discord.Member]) -> discord.Embed:
        # if user has submitted at least one score, we find score and index and then print
        if any(user.display_name == entry.get("name") for entry in score_dict):
            for index, score_entry in enumerate(score_dict):
                if score_entry.get('name') == user.display_name:
                    embed.add_field(
                        name=f":reminder_ribbon: (YOU) {index + 1}. {user.display_name} \nScore: {score_entry.get('score')}",
                        value=f"Updated: {score_entry.get('submit_date')}", inline=True)
        # print message that user has not posted yet
        else:
            embed.add_field(
                name=f":grey_question: (YOU) {user.display_name} - MISSING",
                value=f"You have not yet submitted a score to {self.leaderboard}, please submit a score to be listed",
                inline=True)

        return embed
