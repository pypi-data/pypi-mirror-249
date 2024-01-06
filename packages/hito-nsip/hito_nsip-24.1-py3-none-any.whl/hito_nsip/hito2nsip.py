#!/usr/bin/env python
"""
Script that updates in NSIP the team an agent belongs too, based on Hito. Produces a CSV with
the required updates. Requires that NSIP and Hito team names have been synchronised first with
fix_nsip_team_names.py
"""

import argparse
import os
import re
from typing import Set

from hito_tools.agents import (
    Agent,
    ascii_lower,
    get_nsip_agents,
    match_hito_agent_name,
    name_mapping_exceptions,
    read_hito_agents,
)
from hito_tools.core import GlobalParams
from hito_tools.exceptions import OptionMissing
from hito_tools.nsip import nsip_session_init
from hito_tools.teams import NSIP_NO_TEAM_ID, get_nsip_team_ids
from hito_tools.utils import get_config_path_default, load_config_file, load_email_fixes
from prettytable import PrettyTable

LAB_EMAIL_DOMAIN = "ijclab.in2p3.fr"
LAB_ALIAS_DOMAINS_PATTERN = r".*@(csnsm|imnc|ipn|lal)\.in2p3\.fr"


class NSIPChangeOperation:
    def __init__(
        self,
        firstname: str,
        lastname: str,
        reseda_email: str,
        new_team_id: str,
        new_team_name: str = "",
        current_team_name: str = "",
        current_contact_email: str = None,
        new_contact_email: str = None,
        current_offices: str = set(),
        new_offices: str = set(),
        current_phones: str = set(),
        new_phones: str = set(),
    ) -> None:
        self.firstname = firstname
        self.lastname = lastname
        self.reseda_email = reseda_email
        if new_contact_email is None:
            self.new_contact_email = self.reseda_email
        else:
            self.new_contact_email = new_contact_email
        self.current_contact_email = current_contact_email
        self.new_team_id = new_team_id
        self.new_team_name = new_team_name
        self.current_team_name = current_team_name
        self.current_offices = current_offices
        self.new_offices = new_offices
        self.current_phones = current_phones
        self.new_phones = new_phones

    def get_current_contact_email(self):
        return self.current_contact_email

    def get_current_offices(self):
        return self.current_offices

    def get_current_phones(self):
        return self.current_phones

    def get_current_team(self):
        return self.current_team_name

    def get_reseda_email(self):
        return self.reseda_email

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_new_contact_email(self):
        return self.new_contact_email

    def get_new_offices(self):
        return self.new_offices

    def get_new_phones(self):
        return self.new_phones

    def get_new_team(self):
        return self.new_team_id, self.new_team_name


class NSIPUpdates:
    def __init__(self, nsip_session, verbose) -> None:
        self.nsip_session = nsip_session
        self.team_changes = []
        self.verbose = verbose

    def add_change(
        self,
        firstname: str,
        lastname: str,
        reseda_email: str,
        new_team_id: str,
        new_team_name: str = "",
        current_team_name: str = "",
        current_contact_email: str = None,
        new_contact_email: str = None,
        current_offices: str = set(),
        new_offices: str = set(),
        current_phones: str = set(),
        new_phones: str = set(),
    ) -> None:
        """
        Change the team of an agent

        :param firstname: agent firstname
        :param lastname: agent lastname
        :param reseda_email: agent RESEDA email
        :param new_team_id: new team id
        :param new_team_name: new team name, optional, only for easier debugging
        :param current_team_name: current team name, optional, only for easier debugging
        :param new_contact_email: new contact email
        :param current_offices: current list of offices
        :param new_offices: new list of offices
        :param current_phones: current list of phones
        :param new_phones: new list of phones
        :return: None
        """

        self.team_changes.append(
            NSIPChangeOperation(
                firstname,
                lastname,
                reseda_email,
                new_team_id,
                new_team_name,
                current_team_name,
                current_contact_email,
                new_contact_email,
                current_offices,
                new_offices,
                current_phones,
                new_phones,
            )
        )

    def get_list(self):
        """
        Return a list of tuples for each list operation. Tuple is:
                (firstaname, lastname, new_team_id, new_team_name)

        :return: list of tuples
        """

        return self.team_changes

    def get_number(self):
        """
        Return the number of change operation queued

        :return: number of queued changes
        """

        return len(self.team_changes)

    def apply(self) -> None:
        """
        Apply updates using NSIP API.

        :return: none
        """

        updated_agents = []
        failed_agents = {}

        for change in sorted(self.team_changes, key=lambda x: x.lastname):
            new_team_id, new_team_name = change.get_new_team()
            if new_team_name == change.get_current_team():
                new_team_id = None
            new_email = change.get_new_contact_email()
            if new_email is None or new_email == change.get_current_contact_email():
                new_email = None
            new_offices = change.get_new_offices()
            if new_offices is None or ",".join(new_offices) == ",".join(
                change.get_current_offices()
            ):
                new_offices = None
            new_phones = change.get_new_phones()
            if new_phones is None or ",".join(new_phones) == ",".join(change.get_current_phones()):
                new_phones = None
            agent_id = change.reseda_email
            status, http_status, http_reason = self.nsip_session.update_agent(
                agent_id,
                new_team_id,
                new_email,
                new_phones,
                new_offices,
            )
            if status == 0:
                updated_agents.append(agent_id)
                if self.verbose:
                    print(f"Agent {agent_id} successfully updated")
            else:
                failed_agents[agent_id] = f"{http_status}/{http_reason}"
                if self.verbose:
                    print(
                        (
                            f"Update of agent {agent_id} failed (HTTP status={http_status},"
                            " HTTP reason={http_reason})"
                        )
                    )

        print()
        print("-------------- Update Summary ---------------")
        print(f"Successfull updates: {len(updated_agents)}")
        print(f"Failed updates: {len(failed_agents.keys())}")
        if len(updated_agents) > 0:
            print(f"Agents successfully updated: {', '.join(updated_agents)}")
        if len(failed_agents.keys()) > 0:
            failed_agent_strings = []
            for id, reason in failed_agents.items():
                failed_agent_strings.append(f"{id} ({reason})")
            print(f"Failed agents: {', '.join(failed_agent_strings)}")
        print("---------------------------------------------")
        print()

        return


def ijclab_email_alias(agent, email_fixes=None):
    """
    Return the email alias for an agent, built from its firstname and lastname. An optional
    list of exceptions can be used to override the computed value.

    :param agent: agent object
    :param email_fixes: list of exceptions to the computed values
    :return: email alias for the agent
    """

    ijclab_alias = (
        f"{ascii_lower(agent.firstname)}." f"{ascii_lower(agent.lastname)}@{LAB_EMAIL_DOMAIN}"
    )
    if ijclab_alias in email_fixes:
        ijclab_alias = email_fixes[ijclab_alias]

    return ijclab_alias


def generate_alias_check(filename: str, agent_list: Set[Agent]) -> None:
    """
    Add to the output file the required Zimbra command to check if the agent email if it matching
    the local domain and the agent email alias (e.g. firstname.lastname@ijclab.in2p3.fr)
    exist in Zimbra.

    :param file: SQL scrip file name
    :param agent_list: set of agent object
    :return: none
    """

    try:
        file = open(filename, "w", encoding="utf-8", newline="")
    except Exception:
        print(f"ERROR: failed to create the alias check script file ({filename})")
        raise

    print("#!/bin/bash", file=file)

    for agent in sorted(agent_list, key=lambda x: x.lastname):
        name = agent.fullname
        agent_emails = set([agent.email])
        if agent.email_alias is not None:
            agent_emails.add(agent.email_alias)

        for email in agent_emails:
            if not re.match(rf".*@{LAB_EMAIL_DOMAIN}$", email) and not re.match(
                LAB_ALIAS_DOMAINS_PATTERN, email
            ):
                continue
            print(
                (
                    f'if [ -n "$(/usr/bin/sudo /opt/zadm/bin/zmprov.sh ga'
                    f' {email} cn 2>/dev/null)" ]; then'
                ),
                file=file,
            )
            print(f'    echo "{name}\'s email ({email}): OK"', file=file)
            print("else", file=file)
            print(f'    echo "{name}\'s email ({email}): ERROR"', file=file)
            print("fi", file=file)

    print()
    print(f"Alias check script generated ({filename})")


def add_user_email(file: str, firstname: str, lastname: str, email: str) -> None:
    """
    Add to the output file the user lastname, firstname and email

    :param file: SQL scrip file name
    :param firstname: first name of the user
    :param lastname: last name of the user
    :param email: email of the user
    :return: none
    """
    try:
        if add_user_email.f:
            pass
    except AttributeError:
        add_user_email.f = open(file, "w", encoding="utf-8", newline="")
        print("Lastname;Firstname;email", file=add_user_email.f)
    except Exception:
        print(f"ERROR: failed to create the list of IJCLab emails ({file})")
        raise

    print(f"{lastname};{firstname};{email}", file=add_user_email.f)


def set_options(
    options=None,
    check_emails_script=None,
    config_file=None,
    email_fixes=None,
    email_list=None,
    execute=None,
    hito_agents_csv=None,
    hito_reseda_mappings=None,
    match_warning=None,
    show_approximate_mappings=None,
    show_change_details=None,
    show_missing_agents=None,
    show_missing_offices=None,
    show_missing_phones=None,
    show_missing_teams=None,
    show_updates=None,
    wrong_connection_emails=None,
):
    """
    Function to initialize/update options. Basically mimics what is done by argparser in main().
    Not ideal but allows to call this application as a module rather than a command.
    Be sure to maintain the consistency with what argparser does in main().

    :param options: existing options from the parser
    :param check_emails_script: overrides --aliases-check-script
    :param config_file: overrides --configuration-file
    :param email_fixes: overrides --email-fixes
    :param email_list: overrides --email-list
    :param execute: overrides --execute
    :param hito_agents_csv: overrides --hito-agents-csv
    :param hito_reseda_mappings: overrides --hito-reseda-mappings
    :param match_warning: overrides --match-worning
    :param show_approximate_mappings: overrides --show-approximate-mappings
    :param show_change_details: overrides --show-change-details
    :param show_missing_agents: overrides --show-missing-agents
    :param show_missing_offices: overrides --show-missing-offices
    :param show_missing_phones: overrides --show-missing-phones
    :param show_missing_teams: overrides --show-missing-teams
    :param show_updates: overrides --show-updates
    :param wrong_connection_emails: overrides --wrong-connection-details
    :return: argparse.Namespace() object with all the appropriate options set
    """

    # For clarity, define default values here. Note that they cannot be defined as default values
    # of arguments as it would become impossible to distingish between a specified and unspecified
    # argument and make impossible to call this function multiple times without affecting all
    # the options.
    check_emails_script_default = None
    email_fixes_default = None
    email_list_default = None
    execute_default = False
    hito_reseda_mappings_default = None
    match_warning_default = False
    show_approximate_mappings_default = False
    show_change_details_default = False
    show_missing_agents_default = False
    show_missing_offices_default = False
    show_missing_phones_default = False
    show_missing_teams_default = False
    show_updates_default = False
    wrong_connection_emails_default = False

    # Initialize options if None
    if not options:
        options = argparse.Namespace()

    # Apply specified or default values for all options
    if hito_agents_csv:
        options.hito_agents_csv = hito_agents_csv
    elif "hito_agents_csv" not in options or options.hito_agents_csv is None:
        raise Exception("Hito agents file not specified")
    if check_emails_script:
        options.aliases_check_script = check_emails_script
    elif "aliases_check_script" not in options:
        options.aliases_check_script = check_emails_script_default
    if config_file:
        options.configuration_file = config_file
    elif "configuration_file" not in options or options.configuration_file is None:
        options.configuration_file = get_config_path_default(
            os.path.dirname(options.hito_agents_csv),
            __file__,
        )[0]
    if email_fixes:
        options.email_fixes = email_fixes
    elif "email_fixes" not in options:
        options.email_fixes = email_fixes_default
    if email_list:
        options.email_list = email_list
    elif "email_list" not in options:
        options.email_list = email_list_default
    if execute:
        options.execute = execute
    elif "execute" not in options:
        options.execute = execute_default
    if hito_reseda_mappings:
        options.hito_reseda_mappings = hito_reseda_mappings
    elif "hito_reseda_mappings" not in options:
        options.hito_reseda_mappings = hito_reseda_mappings_default
    if match_warning:
        options.match_warning = match_warning
    elif "match_warning" not in options:
        options.match_warning = match_warning_default
    if show_approximate_mappings:
        options.show_approximate_mappings = show_approximate_mappings
    elif "show_approximate_mappings" not in options:
        options.show_approximate_mappings = show_approximate_mappings_default
    if show_change_details:
        options.show_change_details = show_change_details
    elif "show_change_details" not in options:
        options.show_change_details = show_change_details_default
    if show_missing_agents:
        options.show_missing_agents = show_missing_agents
    elif "show_missing_agents" not in options:
        options.show_missing_agents = show_missing_agents_default
    if show_missing_offices:
        options.show_missing_offices = show_missing_offices
    elif "show_missing_offices" not in options:
        options.show_missing_offices = show_missing_offices_default
    if show_missing_phones:
        options.show_missing_phones = show_missing_phones
    elif "show_missing_phones" not in options:
        options.show_missing_phones = show_missing_phones_default
    if show_missing_teams:
        options.show_missing_teams = show_missing_teams
    elif "show_missing_teams" not in options:
        options.show_missing_teams = show_missing_teams_default
    if show_updates:
        options.show_updates = show_updates
    elif "show_updates" not in options:
        options.show_updates = show_updates_default
    if wrong_connection_emails:
        options.wrong_connection_emails = wrong_connection_emails
    elif "wrong_connection_emails" not in options:
        options.wrong_connection_emails = wrong_connection_emails_default

    if options.email_fixes is None:
        raise OptionMissing("email_fixes")
    if options.hito_reseda_mappings is None:
        raise OptionMissing("hito_reseda_mappings")

    return options


def update_nsip(options=None):
    """

    :param options: configuration parameters
    :return: None
    """

    global_params = GlobalParams()

    # Initialize options if they were not defined, applying defaults.
    # After this point, the application will behave the same whether it was called as a
    # command or as a module.
    options = set_options(options)

    global_params.this_script = os.path.basename(__file__)

    if options.configuration_file:
        config = load_config_file(options.configuration_file)
    else:
        config = {}
    if "nsip" in config:
        nsip_session = nsip_session_init(config["nsip"])
    else:
        print("Configuration to connect NSIP missing")
        return 1

    # If --execute is not specified, show what would be done
    if not options.execute:
        options.show_change_details = True

    # Use sets except when duplicates are unexpected and should be identified
    missing_hito_agents = []
    disabled_nsip_agents = set()
    approximate_mappings = {}
    missing_offices = set()
    missing_phones = set()
    matched_hito_names = set()
    wrong_connection_emails = set()
    # missing_teams is a dict where the key is a Hito team name and the value a list of the
    # agents belonging to the team
    missing_teams = {}
    # Set of agents used for building the alias check script: basically the hito agent list
    # with only one entry per agent
    agents_to_check = set()

    # Read agents from Hito export
    agent_list = read_hito_agents(options.hito_agents_csv, ignore_if_no_team=True)

    # Read teams defined in NSIP
    team_list = get_nsip_team_ids(nsip_session)
    team_id2names = {}
    for team in team_list.values():
        team_id2names[team.id] = team.name

    # Read email fixes
    email_fixes = load_email_fixes(options.email_fixes)

    # Read special cases for mapping Hito names to RESEDA names
    hito_reseda_exceptions = name_mapping_exceptions(options.hito_reseda_mappings)

    # Retrieve NSIP agents
    nsip_agent_list = get_nsip_agents(nsip_session, context="DIRECTORY")

    # and add a team change operation if needed
    agent_updates = NSIPUpdates(nsip_session, options.show_updates)
    for agent in sorted(nsip_agent_list.values(), key=lambda x: x.fullname):
        nsip_name = agent.fullname
        nsip_email, nsip_reseda_email = agent.get_emails()
        hito_name, approximate_match, match_criteria = match_hito_agent_name(
            agent, agent_list, hito_reseda_exceptions
        )

        if hito_name:
            if agent.disabled:
                disabled_nsip_agents.add(agent_list[hito_name])
            else:
                matched_hito_names.add(hito_name)
                if approximate_match:
                    approximate_mappings[nsip_name] = [hito_name, match_criteria]

                agent_hito_team = agent_list[hito_name].team
                hito_reseda_email = agent_list[hito_name].reseda_email
                if hito_reseda_email.lower() != nsip_reseda_email.lower():
                    wrong_connection_emails.add((agent_list[hito_name], nsip_reseda_email))
                agent_list[hito_name].email_alias = ijclab_email_alias(
                    agent_list[hito_name], email_fixes
                )

                if len(agent.offices) > 0:
                    nsip_offices = agent.offices
                else:
                    missing_offices.add(agent_list[hito_name])
                    nsip_offices = set()

                if len(agent.phones) > 0:
                    nsip_phones = agent.phones
                else:
                    missing_phones.add(agent_list[hito_name])
                    nsip_phones = set()

                change_needed = False
                # '-' is a special value to disable NSIP email update
                if agent_list[hito_name].email_alias == "-":
                    print(
                        (
                            f"INFO: NSIP email definition disabled for"
                            f" {agent_list[hito_name].firstname}"
                            f" {agent_list[hito_name].lastname}"
                        )
                    )
                    agent_list[hito_name].email_alias = nsip_email
                elif agent_list[hito_name].email_alias != nsip_email:
                    change_needed = True

                if len(agent_list[hito_name].offices) != len(nsip_offices) or len(
                    agent_list[hito_name].offices | nsip_offices
                ) != len(nsip_offices):
                    new_offices = agent_list[hito_name].offices
                    change_needed = True
                else:
                    new_offices = nsip_offices

                if len(agent_list[hito_name].phones) != len(nsip_phones) or len(
                    agent_list[hito_name].phones | nsip_phones
                ) != len(nsip_phones):
                    new_phones = agent_list[hito_name].phones
                    change_needed = True
                else:
                    new_phones = nsip_phones

                if agent_hito_team == "":
                    change_needed = True
                    new_team_id = NSIP_NO_TEAM_ID
                    new_team_name = "None"
                    current_team_name = "None"
                elif agent_hito_team in team_list:
                    current_nsip_team_id = agent.team_id
                    new_team_id = team_list[agent_hito_team].id
                    new_team_name = team_list[agent_hito_team].name
                    if new_team_id != current_nsip_team_id:
                        change_needed = True
                else:
                    if agent_hito_team not in missing_teams:
                        missing_teams[agent_hito_team] = []
                    missing_teams[agent_hito_team].append(nsip_name)
                    current_team_name = agent_hito_team
                    new_team_id = None
                    new_team_name = ""

                if change_needed:
                    agent_updates.add_change(
                        agent.firstname,
                        agent.lastname,
                        hito_reseda_email,
                        new_team_id,
                        new_team_name,
                        current_team_name,
                        nsip_email,
                        agent_list[hito_name].email_alias,
                        nsip_offices,
                        new_offices,
                        nsip_phones,
                        new_phones,
                    )

                if options.email_list:
                    agent_email, _ = agent_list[hito_name].get_emails()
                    add_user_email(
                        options.email_list,
                        agent_list[hito_name].firstname,
                        agent_list[hito_name].lastname,
                        agent_email,
                    )

                agents_to_check.add(agent_list[hito_name])

        else:
            if not agent.disabled:
                missing_hito_agents.append(agent)

    # Check agents present in Hito and not in NSIP and add them to the alias check list if enabled
    # Take care that each agent is present twice in agent_list: one with its fullname and once
    # with the ASCII version of his fullname.
    missing_nsip_agents = set()
    for agent in sorted(agent_list.values(), key=lambda x: x.lastname):
        if agent.fullname not in matched_hito_names:
            if options.aliases_check_script and agent not in missing_nsip_agents:
                agent.email_alias = ijclab_email_alias(agent, email_fixes)
                agents_to_check.add(agent)
            missing_nsip_agents.add(agent)

    # Write summary and reports
    print()
    print("----------------- SUMMARY -----------------")
    print(f"Number of Hito agents: {int(len(agent_list.keys())/2)}")
    print(f"Number of NSIP agents: {int(len(nsip_agent_list))}")
    print(f"Number of teams: {len(team_list.keys())}")
    print(f"Number of agents with changes: {agent_updates.get_number()}")
    print(f"Number of agents found in NSIP but missing in Hito: {len(missing_hito_agents)}")
    print(f"Number of agents found in Hito but not in NSIP: {len(missing_nsip_agents)}")
    print(f"Number of missing teams in NSIP: {len(missing_teams.keys())}")
    print(
        f"Number of approximate matches between Hito and NSIP: {len(approximate_mappings.keys())}"
    )
    print(f"Number of agents without an office number: {len(missing_offices)}")
    print(f"Number of agents without a phone number: {len(missing_phones)}")
    print(f"Number of agents with a wrong connection email in Hito: {len(wrong_connection_emails)}")

    team_change_pt = PrettyTable()
    team_change_pt.field_names = [
        "Agent Name",
        "Current NSIP Team",
        "NSIP New Team Name",
        "NSIP New Team ID",
    ]
    team_change_pt.align = "l"
    team_change_num = 0
    for change in sorted(agent_updates.get_list(), key=lambda x: x.lastname):
        new_team_id, new_team_name = change.get_new_team()
        current_team_name = change.get_current_team()
        if current_team_name != new_team_name:
            team_change_num += 1
            team_change_pt.add_row(
                [
                    f"{change.lastname} {change.firstname}",
                    current_team_name,
                    new_team_name,
                    new_team_id,
                ]
            )
    print(f"Number of team changes: {team_change_num}")

    email_change_pt = PrettyTable()
    email_change_pt.field_names = [
        "Agent Name",
        "Current Contact Email",
        "NSIP New Contact Email",
    ]
    email_change_pt.align = "l"
    email_change_num = 0
    for change in sorted(agent_updates.get_list(), key=lambda x: x.lastname):
        new_contact_email = change.get_new_contact_email()
        current_contact_email = change.get_current_contact_email()
        if current_contact_email != new_contact_email:
            email_change_num += 1
            email_change_pt.add_row(
                [
                    f"{change.lastname} {change.firstname}",
                    current_contact_email,
                    new_contact_email,
                ]
            )
    print(f"Number of email changes: {email_change_num}")

    office_change_pt = PrettyTable()
    office_change_pt.field_names = ["Agent Name", "Current Offices", "NSIP New Offices"]
    office_change_pt.align = "l"
    office_change_num = 0
    for change in sorted(agent_updates.get_list(), key=lambda x: x.lastname):
        new_offices = change.get_new_offices()
        current_offices = change.get_current_offices()
        if len(current_offices) != len(new_offices) or len(current_offices | new_offices) != len(
            current_offices
        ):
            office_change_num += 1
            office_change_pt.add_row(
                [
                    f"{change.lastname} {change.firstname}",
                    " | ".join(current_offices),
                    " | ".join(new_offices),
                ]
            )
    print(f"Number of office changes: {office_change_num}")

    phone_change_pt = PrettyTable()
    phone_change_pt.field_names = [
        "Agent Name",
        "Current Phones",
        "NSIP New Phones",
    ]
    phone_change_pt.align = "l"
    phone_change_num = 0
    for change in sorted(agent_updates.get_list(), key=lambda x: x.lastname):
        new_phones = change.get_new_phones()
        current_phones = change.get_current_phones()
        if len(current_phones) != len(new_phones) or len(current_phones | new_phones) != len(
            current_phones
        ):
            phone_change_num += 1
            phone_change_pt.add_row(
                [
                    f"{change.lastname} {change.firstname}",
                    " | ".join(current_phones),
                    " | ".join(new_phones),
                ]
            )
    print(f"Number of phone changes: {phone_change_num}")

    # SUMMARY end
    print("-------------------------------------------")
    print()

    if (
        options.show_approximate_mappings
        or options.show_missing_agents
        or options.show_missing_teams
        or options.show_missing_offices
        or options.show_missing_phones
        or options.show_change_details
    ):
        print()
        print("----------------- DETAILS -----------------")

        if options.show_approximate_mappings:
            if len(approximate_mappings.keys()):
                print()
                print(
                    f"++++++ Approximate match list ({len(approximate_mappings.keys())}) +++++++++"
                )
            for project_agent_name, hito_agent_params in approximate_mappings.items():
                print(
                    (
                        f"WARNING: approximate match found ({hito_agent_params[1]}) in Hito"
                        f" for project agent '{project_agent_name}': {hito_agent_params[0]}"
                    )
                )

        if options.show_missing_agents:
            if len(missing_hito_agents):
                print()
                print(f"++++++ Agents missing in Hito ({len(missing_hito_agents)}) +++++++++")
                for agent in sorted(missing_hito_agents, key=lambda x: x.lastname):
                    print(f"ERROR: '{agent.fullname}' not found in Hito: ignoring it.")
            if len(missing_nsip_agents):
                print()
                print(f"++++++ Agents missing in NSIP ({len(missing_nsip_agents)}) +++++++++")
                for agent in sorted(missing_nsip_agents, key=lambda x: x.lastname):
                    print(
                        (
                            f"ERROR: '{agent.fullname}' present in Hito but not found"
                            f" in NSIP: ignoring it."
                        )
                    )
            if len(disabled_nsip_agents):
                print()
                print(
                    (
                        f"++++++ Agents found in NSIP but disabled ({len(disabled_nsip_agents)})"
                        f" +++++++++"
                    )
                )
                for agent in sorted(disabled_nsip_agents, key=lambda x: x.lastname):
                    print(f"ERROR: '{agent.fullname}' disabled in NSIP: ignoring it.")

        if options.show_missing_teams:
            if len([missing_teams.keys()]):
                print()
                print(
                    (
                        f"++++++ Agents with no team defined in NSIP"
                        f" ({len(missing_teams.keys())}) +++++++++"
                    )
                )
                for team in sorted(missing_teams.keys()):
                    print(
                        (
                            f"ERROR: team '{team}' missing in NSIP, cannot check/update NSIP"
                            f" entry for {', '.join(missing_teams[team])}"
                        )
                    )

        if options.show_missing_offices:
            if len(missing_offices) > 0:
                print()
                print(f"++++++ Agents without offices ({len(missing_offices)}) +++++++++")
                for agent in sorted(missing_offices, key=lambda x: x.lastname):
                    print(agent.fullname)

        if options.show_missing_phones:
            if len(missing_phones) > 0:
                print()
                print(f"++++++ Agents without phones ({len(missing_phones)}) +++++++++")
                for agent in sorted(missing_phones, key=lambda x: x.lastname):
                    print(agent.fullname)

        if options.wrong_connection_emails and len(wrong_connection_emails) > 0:
            print()
            wrong_connection_emails_pt = PrettyTable()
            wrong_connection_emails_pt.field_names = [
                "Agent Name",
                "Current Hito Connection Email",
                "Actual RESEDA email",
            ]
            wrong_connection_emails_pt.align = "l"
            for e in sorted(wrong_connection_emails, key=lambda x: x[0].lastname):
                wrong_connection_emails_pt.add_row([e[0].fullname, e[0].reseda_email, e[1]])
            print(
                (
                    f"++++++ Agents with a wrong connection email in Hito"
                    f" ({len(wrong_connection_emails)}) +++++++++"
                )
            )
            print(wrong_connection_emails_pt)

        if options.show_change_details:
            print()
            print(f"++++++ Agents with team changes ({team_change_num}) +++++++++")
            print(team_change_pt)

            print()
            print(f"++++++ Agents with email changes ({email_change_num}) +++++++++")
            print(email_change_pt)

            print()
            print(f"++++++ Agents with office changes ({office_change_num}) +++++++++")
            print(office_change_pt)

            print()
            print(f"++++++ Agents with phone changes ({phone_change_num}) +++++++++")
            print(phone_change_pt)

    # Write the alias check script if requested
    if options.aliases_check_script:
        generate_alias_check(options.aliases_check_script, agents_to_check)

    # Update directory if --execute has been specified
    if options.execute:
        print()
        updates_num = agent_updates.get_number()
        if updates_num > 0:
            print(f"Starting agent updates ({updates_num})")
            agent_updates.apply()
        else:
            print()
            print("No agent update needed")
    else:
        print()
        print("Use --execute option to apply updates")


def main():
    # Search the config file in the current directory first
    config_file_path, config_file_name = get_config_path_default()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--aliases-check-script",
        required=False,
        help="Script to test aliases on Zimbra",
    )
    parser.add_argument(
        "--configuration-file",
        required=False,
        help="Configuration file (D: {} in the CSV directory or {})".format(
            config_file_name, config_file_path
        ),
    )
    parser.add_argument(
        "--email-list",
        required=False,
        help="CSV file name with the @ijclab email for each person in Hito",
    )
    parser.add_argument(
        "--email-fixes",
        required=True,
        help="CSV file with correct email address for those improperly built from Hito",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Apply updates",
    )
    parser.add_argument(
        "--hito-agents-csv",
        required=True,
        help="CSV file describing the main team an agent belongs to. If absent, NSIP API is used",
    )
    parser.add_argument(
        "--hito-reseda-mappings",
        required=True,
        help="CSV file defining the Hito to RESEDA name mapping for special cases",
    )
    parser.add_argument(
        "--match-warning",
        action="store_true",
        default=False,
        help="Display a message when agent match between Hito and NSIP is not an exact match",
    )
    parser.add_argument(
        "--show-approximate-mappings",
        action="store_true",
        default=False,
        help="Show the list of approximate matches between Hito and project aggents",
    )
    parser.add_argument(
        "--show-change-details",
        action="store_true",
        default=False,
        help="Display the changes for each agent affected",
    )
    parser.add_argument(
        "--show-missing-agents",
        action="store_true",
        default=False,
        help="Display the list of agents missing in Hito or NSIP",
    )
    parser.add_argument(
        "--show-missing-offices",
        action="store_true",
        default=False,
        help="Display the list of agents without an office number",
    )
    parser.add_argument(
        "--show-missing-phones",
        action="store_true",
        default=False,
        help="Display the list of agents without a phone number",
    )
    parser.add_argument(
        "--show-missing-teams",
        action="store_true",
        default=False,
        help="Display the list of Hito teams missing in NSIP",
    )
    parser.add_argument(
        "--show-updates",
        action="store_true",
        default=False,
        help="Log a message for each update with its status (verbose update)",
    )
    parser.add_argument(
        "--wrong-connection-emails",
        action="store_true",
        default=False,
        help="List of agents with a wrong connection email in Hito",
    )
    options = parser.parse_args()

    update_nsip(options)


if __name__ == "__main__":
    exit(main())
