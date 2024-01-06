# Copyright (c) 2023 Arista Networks, Inc.
# Use of this source code is governed by the Apache License 2.0
# that can be found in the LICENSE file.
"""
BGP test functions
"""
# Mypy does not understand AntaTest.Input typing
# mypy: disable-error-code=attr-defined
from __future__ import annotations

from ipaddress import IPv4Address, IPv6Address
from typing import Any, List, Optional, Union, cast

from pydantic import BaseModel, PositiveInt, model_validator

from anta.custom_types import Afi, Safi
from anta.models import AntaCommand, AntaTemplate, AntaTest
from anta.tools.get_value import get_value

# Need to keep List for pydantic in python 3.8


def _check_bgp_vrfs(bgp_vrfs: dict[str, Any]) -> dict[str, Any]:
    """
    Parse the output of the `show bgp <address family> unicast summary vrf <vrf>` 'vrfs' key
    and returns a dictionary with the following structure:

    {
        <vrf>: {
            <peer>:
                {
                    "peerState": <state>,
                    "inMsgQueue": <count>,
                    "outMsgQueue": <count>,
                }
        }
    }

    Args:
        bgp_vrfs: Output of the `show bgp <address family> unicast summary vrf <vrf>` 'vrfs' key
    """
    state_issue: dict[str, Any] = {}
    for vrf in bgp_vrfs:
        for peer in bgp_vrfs[vrf]["peers"]:
            if (
                (bgp_vrfs[vrf]["peers"][peer]["peerState"] != "Established")
                or (bgp_vrfs[vrf]["peers"][peer]["inMsgQueue"] != 0)
                or (bgp_vrfs[vrf]["peers"][peer]["outMsgQueue"] != 0)
            ):
                vrf_dict = state_issue.setdefault(vrf, {})
                vrf_dict.update(
                    {
                        peer: {
                            "peerState": bgp_vrfs[vrf]["peers"][peer]["peerState"],
                            "inMsgQueue": bgp_vrfs[vrf]["peers"][peer]["inMsgQueue"],
                            "outMsgQueue": bgp_vrfs[vrf]["peers"][peer]["outMsgQueue"],
                        }
                    }
                )

    return state_issue


def _add_bgp_failures(failures: dict[tuple[str, Union[str, None]], dict[str, Any]], afi: Afi, safi: Optional[Safi], vrf: str, issue: Any) -> None:
    """
    Add a BGP failure entry to the given `failures` dictionary.

    Note: This function modifies `failures` in-place.

    Parameters:
        failures (dict): The dictionary to which the failure will be added.
        afi (Afi): The address family identifier.
        vrf (str): The VRF name.
        safi (Safi, optional): The subsequent address family identifier.
        issue (Any): A description of the issue. Can be of any type.

    The `failures` dictionnary will have the following structure:
        {
            ('afi1', 'safi1'): {
                'afi': 'afi1',
                'safi': 'safi1',
                'vrfs': {
                    'vrf1': issue1,
                    'vrf2': issue2
                }
            },
            ('afi2', None): {
                'afi': 'afi2',
                'vrfs': {
                    'vrf1': issue3
                }
            }
        }
    """
    key = (afi, safi)

    if safi:
        failure_entry = failures.setdefault(key, {"afi": afi, "safi": safi, "vrfs": {}})
    else:
        failure_entry = failures.setdefault(key, {"afi": afi, "vrfs": {}})

    failure_entry["vrfs"][vrf] = issue


def _check_peer_issues(peer_data: Optional[dict[str, Any]]) -> dict[str, Any]:
    """
    Check for issues in BGP peer data.

    Parameters:
        peer_data (dict, optional): The BGP peer data dictionary nested in the `show bgp <afi> <safi> summary` command.

    Returns:
        dict: Dictionary with keys indicating issues or an empty dictionary if no issues.

    Example:
        {"peerNotFound": True}
        {"peerState": "Idle", "inMsgQueue": 2, "outMsgQueue": 0}
        {}

    Raises:
        ValueError: If any of the required keys ("peerState", "inMsgQueue", "outMsgQueue") are missing in `peer_data`, i.e. invalid BGP peer data.
    """
    if peer_data is None:
        return {"peerNotFound": True}

    if any(key not in peer_data for key in ["peerState", "inMsgQueue", "outMsgQueue"]):
        raise ValueError("Provided BGP peer data is invalid.")

    if peer_data["peerState"] != "Established" or peer_data["inMsgQueue"] != 0 or peer_data["outMsgQueue"] != 0:
        return {"peerState": peer_data["peerState"], "inMsgQueue": peer_data["inMsgQueue"], "outMsgQueue": peer_data["outMsgQueue"]}

    return {}


class VerifyBGPPeerCount(AntaTest):
    """
    This test verifies the count of BGP peers for a given address family.

    It supports multiple types of address families (AFI) and subsequent service families (SAFI).
    Please refer to the Input class attributes below for details.

    Expected Results:
        * success: If the count of BGP peers matches the expected count for each address family and VRF.
        * failure: If the count of BGP peers does not match the expected count, or if BGP is not configured for an expected VRF or address family.
    """

    name = "VerifyBGPPeerCount"
    description = "Verifies the count of BGP peers."
    categories = ["routing", "bgp"]
    commands = [
        AntaTemplate(template="show bgp {afi} {safi} summary vrf {vrf}"),
        AntaTemplate(template="show bgp {afi} summary"),
    ]

    class Input(AntaTest.Input):  # pylint: disable=missing-class-docstring
        address_families: List[BgpAfi]
        """
        List of BGP address families (BgpAfi)
        """

        class BgpAfi(BaseModel):  # pylint: disable=missing-class-docstring
            afi: Afi
            """BGP address family (AFI)"""
            safi: Optional[Safi] = None
            """Optional BGP subsequent service family (SAFI).

            If the input `afi` is `ipv4` or `ipv6`, a valid `safi` must be provided.
            """
            vrf: str = "default"
            """
            Optional VRF for IPv4 and IPv6. If not provided, it defaults to `default`.

            If the input `afi` is not `ipv4` or `ipv6`, e.g. `evpn`, `vrf` must be `default`.
            """
            num_peers: PositiveInt
            """Number of expected BGP peer(s)"""

            @model_validator(mode="after")
            def validate_inputs(self: BaseModel) -> BaseModel:
                """
                Validate the inputs provided to the BgpAfi class.

                If afi is either ipv4 or ipv6, safi must be provided.

                If afi is not ipv4 or ipv6, safi must not be provided and vrf must be default.
                """
                if self.afi in ["ipv4", "ipv6"]:
                    if self.safi is None:
                        raise ValueError("'safi' must be provided when afi is ipv4 or ipv6")
                elif self.safi is not None:
                    raise ValueError("'safi' must not be provided when afi is not ipv4 or ipv6")
                elif self.vrf != "default":
                    raise ValueError("'vrf' must be default when afi is not ipv4 or ipv6")
                return self

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        commands = []
        for afi in self.inputs.address_families:
            if template == VerifyBGPPeerCount.commands[0] and afi.afi in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, safi=afi.safi, vrf=afi.vrf, num_peers=afi.num_peers))
            elif template == VerifyBGPPeerCount.commands[1] and afi.afi not in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, vrf=afi.vrf, num_peers=afi.num_peers))
        return commands

    @AntaTest.anta_test
    def test(self) -> None:
        self.result.is_success()

        failures: dict[tuple[str, Any], dict[str, Any]] = {}

        for command in self.instance_commands:
            peer_count = 0
            command_output = command.json_output

            afi = cast(Afi, command.params.get("afi"))
            safi = cast(Optional[Safi], command.params.get("safi"))
            afi_vrf = cast(str, command.params.get("vrf"))
            num_peers = cast(PositiveInt, command.params.get("num_peers"))

            if not (vrfs := command_output.get("vrfs")):
                _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue="Not Configured")
                continue

            if afi_vrf == "all":
                for vrf_data in vrfs.values():
                    peer_count += len(vrf_data["peers"])
            else:
                peer_count += len(command_output["vrfs"][afi_vrf]["peers"])

            if peer_count != num_peers:
                _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue=f"Expected: {num_peers}, Actual: {peer_count}")

        if failures:
            self.result.is_failure(f"Failures: {list(failures.values())}")


class VerifyBGPPeersHealth(AntaTest):
    """
    This test verifies the health of BGP peers.

    It will validate that all BGP sessions are established and all message queues for these BGP sessions are empty for a given address family.

    It supports multiple types of address families (AFI) and subsequent service families (SAFI).
    Please refer to the Input class attributes below for details.

    Expected Results:
        * success: If all BGP sessions are established and all messages queues are empty for each address family and VRF.
        * failure: If there are issues with any of the BGP sessions, or if BGP is not configured for an expected VRF or address family.
    """

    name = "VerifyBGPPeersHealth"
    description = "Verifies the health of BGP peers"
    categories = ["routing", "bgp"]
    commands = [
        AntaTemplate(template="show bgp {afi} {safi} summary vrf {vrf}"),
        AntaTemplate(template="show bgp {afi} summary"),
    ]

    class Input(AntaTest.Input):  # pylint: disable=missing-class-docstring
        address_families: List[BgpAfi]
        """
        List of BGP address families (BgpAfi)
        """

        class BgpAfi(BaseModel):  # pylint: disable=missing-class-docstring
            afi: Afi
            """BGP address family (AFI)"""
            safi: Optional[Safi] = None
            """Optional BGP subsequent service family (SAFI).

            If the input `afi` is `ipv4` or `ipv6`, a valid `safi` must be provided.
            """
            vrf: str = "default"
            """
            Optional VRF for IPv4 and IPv6. If not provided, it defaults to `default`.

            If the input `afi` is not `ipv4` or `ipv6`, e.g. `evpn`, `vrf` must be `default`.
            """

            @model_validator(mode="after")
            def validate_inputs(self: BaseModel) -> BaseModel:
                """
                Validate the inputs provided to the BgpAfi class.

                If afi is either ipv4 or ipv6, safi must be provided.

                If afi is not ipv4 or ipv6, safi must not be provided and vrf must be default.
                """
                if self.afi in ["ipv4", "ipv6"]:
                    if self.safi is None:
                        raise ValueError("'safi' must be provided when afi is ipv4 or ipv6")
                elif self.safi is not None:
                    raise ValueError("'safi' must not be provided when afi is not ipv4 or ipv6")
                elif self.vrf != "default":
                    raise ValueError("'vrf' must be default when afi is not ipv4 or ipv6")
                return self

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        commands = []
        for afi in self.inputs.address_families:
            if template == VerifyBGPPeersHealth.commands[0] and afi.afi in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, safi=afi.safi, vrf=afi.vrf))
            elif template == VerifyBGPPeersHealth.commands[1] and afi.afi not in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, vrf=afi.vrf))
        return commands

    @AntaTest.anta_test
    def test(self) -> None:
        self.result.is_success()

        failures: dict[tuple[str, Any], dict[str, Any]] = {}

        for command in self.instance_commands:
            command_output = command.json_output

            afi = cast(Afi, command.params.get("afi"))
            safi = cast(Optional[Safi], command.params.get("safi"))
            afi_vrf = cast(str, command.params.get("vrf"))

            if not (vrfs := command_output.get("vrfs")):
                _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue="Not Configured")
                continue

            for vrf, vrf_data in vrfs.items():
                if not (peers := vrf_data.get("peers")):
                    _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue="No Peers")
                    continue

                peer_issues = {}
                for peer, peer_data in peers.items():
                    issues = _check_peer_issues(peer_data)

                    if issues:
                        peer_issues[peer] = issues

                if peer_issues:
                    _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=vrf, issue=peer_issues)

        if failures:
            self.result.is_failure(f"Failures: {list(failures.values())}")


class VerifyBGPSpecificPeers(AntaTest):
    """
    This test verifies the health of specific BGP peer(s).

    It will validate that the BGP session is established and all message queues for this BGP session are empty for the given peer(s).

    It supports multiple types of address families (AFI) and subsequent service families (SAFI).
    Please refer to the Input class attributes below for details.

    Expected Results:
        * success: If the BGP session is established and all messages queues are empty for each given peer.
        * failure: If the BGP session has issues or is not configured, or if BGP is not configured for an expected VRF or address family.
    """

    name = "VerifyBGPSpecificPeers"
    description = "Verifies the health of specific BGP peer(s)."
    categories = ["routing", "bgp"]
    commands = [
        AntaTemplate(template="show bgp {afi} {safi} summary vrf {vrf}"),
        AntaTemplate(template="show bgp {afi} summary"),
    ]

    class Input(AntaTest.Input):  # pylint: disable=missing-class-docstring
        address_families: List[BgpAfi]
        """
        List of BGP address families (BgpAfi)
        """

        class BgpAfi(BaseModel):  # pylint: disable=missing-class-docstring
            afi: Afi
            """BGP address family (AFI)"""
            safi: Optional[Safi] = None
            """Optional BGP subsequent service family (SAFI).

            If the input `afi` is `ipv4` or `ipv6`, a valid `safi` must be provided.
            """
            vrf: str = "default"
            """
            Optional VRF for IPv4 and IPv6. If not provided, it defaults to `default`.

            `all` is NOT supported.

            If the input `afi` is not `ipv4` or `ipv6`, e.g. `evpn`, `vrf` must be `default`.
            """
            peers: List[Union[IPv4Address, IPv6Address]]
            """List of BGP IPv4 or IPv6 peer"""

            @model_validator(mode="after")
            def validate_inputs(self: BaseModel) -> BaseModel:
                """
                Validate the inputs provided to the BgpAfi class.

                If afi is either ipv4 or ipv6, safi must be provided and vrf must NOT be all.

                If afi is not ipv4 or ipv6, safi must not be provided and vrf must be default.
                """
                if self.afi in ["ipv4", "ipv6"]:
                    if self.safi is None:
                        raise ValueError("'safi' must be provided when afi is ipv4 or ipv6")
                    if self.vrf == "all":
                        raise ValueError("'all' is not supported in this test. Use VerifyBGPPeersHealth test instead.")
                elif self.safi is not None:
                    raise ValueError("'safi' must not be provided when afi is not ipv4 or ipv6")
                elif self.vrf != "default":
                    raise ValueError("'vrf' must be default when afi is not ipv4 or ipv6")
                return self

    def render(self, template: AntaTemplate) -> list[AntaCommand]:
        commands = []
        for afi in self.inputs.address_families:
            if template == VerifyBGPSpecificPeers.commands[0] and afi.afi in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, safi=afi.safi, vrf=afi.vrf, peers=afi.peers))
            elif template == VerifyBGPSpecificPeers.commands[1] and afi.afi not in ["ipv4", "ipv6"]:
                commands.append(template.render(afi=afi.afi, vrf=afi.vrf, peers=afi.peers))
        return commands

    @AntaTest.anta_test
    def test(self) -> None:
        self.result.is_success()

        failures: dict[tuple[str, Any], dict[str, Any]] = {}

        for command in self.instance_commands:
            command_output = command.json_output

            afi = cast(Afi, command.params.get("afi"))
            safi = cast(Optional[Safi], command.params.get("safi"))
            afi_vrf = cast(str, command.params.get("vrf"))
            afi_peers = cast(List[Union[IPv4Address, IPv6Address]], command.params.get("peers", []))

            if not (vrfs := command_output.get("vrfs")):
                _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue="Not Configured")
                continue

            peer_issues = {}
            for peer in afi_peers:
                peer_ip = str(peer)
                peer_data = get_value(dictionary=vrfs, key=f"{afi_vrf}_peers_{peer_ip}", separator="_")
                issues = _check_peer_issues(peer_data)
                if issues:
                    peer_issues[peer_ip] = issues

            if peer_issues:
                _add_bgp_failures(failures=failures, afi=afi, safi=safi, vrf=afi_vrf, issue=peer_issues)

        if failures:
            self.result.is_failure(f"Failures: {list(failures.values())}")
