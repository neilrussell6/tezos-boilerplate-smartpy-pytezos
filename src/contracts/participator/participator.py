"""Participator Tezos smart contract"""
import vendor.SmartPyBasic.smartpy as sp  # noqa: N813
from src.contracts.participator.participator_constants import (
    ERROR_CANNOT_ADD_DUPLICATE_PARTICIPANT,
    ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT,
    ERROR_ONLY_REGISTERED_PARTICIPANTS_CAN_PARTICIPATE,
)


class Participator(sp.Contract):
    def __init__(self, owner):
        self.init(
            participants=sp.bigMap(tkey=sp.TAddress, tvalue=sp.TMutez),
            owner=sp.address(owner),
        )

    @sp.entryPoint
    def add_participant(self, address):
        sp.verify(sp.sender == self.data.owner, False, ERROR_ONLY_OWNER_CAN_ADD_PARTICIPANT)
        sp.verify(~self.data.participants.contains(address), False, ERROR_CANNOT_ADD_DUPLICATE_PARTICIPANT)
        self.data.participants[address] = sp.amount

    @sp.entryPoint
    def participate(self, address):
        sp.verify(
            self.data.participants.contains(sp.sender),
            False,
            ERROR_ONLY_REGISTERED_PARTICIPANTS_CAN_PARTICIPATE,
        )
        self.data.participants[sp.sender] += sp.amount
