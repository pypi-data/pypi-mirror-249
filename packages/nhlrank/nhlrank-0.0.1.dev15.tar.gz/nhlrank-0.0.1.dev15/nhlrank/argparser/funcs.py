# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:26:28 2023

@author: shane
"""
import argparse
from typing import Any

from nhlrank.core import (
    func_projections,
    func_standings,
    func_standings_team_details,
    func_team_details,
    func_teams_list,
    process_csv,
)
from nhlrank.models import Game, Team
from nhlrank.models.helpers import get_team_name
from nhlrank.sheetutils import cache_csv_games_file, get_google_sheet
from nhlrank.utils import print_title


def parser_func_download(
    **kwargs: dict[str, Any]  # pylint: disable=unused-argument
) -> tuple[int, None]:
    """Default function for download parser"""
    cache_csv_games_file(
        _csv_bytes_output=get_google_sheet(),
    )
    return 0, None


def parser_func_teams(
    args: argparse.Namespace,
) -> tuple[int, None]:
    """Default function for teams parser, prints all teams and their abbreviations"""

    # Load the teams from main CSV file
    _, teams = process_csv()

    # Print them out
    func_teams_list(
        teams=teams,
        abbrev=args.abbrev,
        abbrev_only=args.abbrev_only,
        group_teams_by=args.group_teams_by,
    )

    return 0, None


def parser_func_team_details(
    args: argparse.Namespace,
) -> tuple[int, tuple[list[Game], dict[str, Team]]]:
    """Default function for team parser"""

    # Load games and teams from main CSV file
    games, teams = process_csv()

    # Print out team details/summary
    func_team_details(
        games=games,
        teams=teams,
        team_name=args.team,
        num_games_last=args.num_games_last,
        num_games_next=args.num_games_next,
    )

    return 0, (games, teams)


def parser_func_standings(
    args: argparse.Namespace,
) -> tuple[int, tuple[list[Game], dict[str, Team]]]:
    """Default function for rank parser"""

    # FIXME: make this into an annotation function?  Easy to reuse & test that way?
    if not args.skip_dl:  # pragma: no cover
        cache_csv_games_file(
            _csv_bytes_output=get_google_sheet(),
        )

    # Build games and team objects
    games, teams = process_csv()

    # Print standings
    # TODO: skip this if only printing team details
    func_standings(
        games=games,
        teams=teams,
        col_sort_by=args.sort_column.lower() if args.sort_column else str(),
        # reverse=args.reverse,
        group_standings_by=args.group_standings_by,
    )

    # Optionally print team details
    if args.team:
        print_title("Team details")
        func_standings_team_details(
            team_name=args.team,
            games=games,
            teams=teams,
            num_games_last=args.num_games_last,
            num_games_next=args.num_games_next,
        )
        # func_up_coming_games()

    # Optionally print match ups
    # if args.matches:
    #     func_match_ups(teams=teams)

    return 0, (games, teams)


def parser_func_projections(
    args: argparse.Namespace,
) -> tuple[int, tuple[list[Game], dict[str, Team]]]:
    """Default function for projection parser"""

    if not args.skip_dl:  # pragma: no cover
        cache_csv_games_file(
            _csv_bytes_output=get_google_sheet(),
        )

    # Build games and team objects
    games, teams = process_csv()

    # Print projections
    func_projections(
        games=games,
        teams=teams,
        # col_sort_by=args.sort_column.lower() if args.sort_column else str(),
        # group_projections_by=args.group_projections_by,
    )

    # TODO: Optionally print team details, e.g. list of game outcomes

    return 0, (games, teams)


def parser_func_match_ups(
    args: argparse.Namespace,
) -> tuple[int, tuple[list[Game], dict[str, Team]]]:
    """Default function for match ups parser"""

    if not args.skip_dl:  # pragma: no cover
        cache_csv_games_file(
            _csv_bytes_output=get_google_sheet(),
        )

    # Build games and team objects
    games, teams = process_csv()

    # Decide which teams to print match ups for
    if args.teams:
        team_names = [get_team_name(x) for x in args.teams]
        teams_selected = [teams[team_name] for team_name in team_names]
    else:
        teams_selected = list(sorted(teams.values(), key=lambda x: x.name))

    for team in teams_selected:
        print(team)

    print("NOTE: Function not fully implemented yet!")
    return 0, (games, teams)
