# noqa
from dataclasses import dataclass
from typing import Union

from pycardano import Address
from pycardano import PlutusData
from pycardano import VerificationKeyHash

from cardex.dataclasses.models import Assets


@dataclass
class PlutusPartAddress(PlutusData):
    """Encode a plutus address part (i.e. payment, stake, etc)."""

    CONSTR_ID = 0
    address: bytes


@dataclass
class PlutusNone(PlutusData):
    """Placeholder for a receiver datum."""

    CONSTR_ID = 1


@dataclass
class _PlutusConstrWrapper(PlutusData):
    """Hidden wrapper to match Minswap stake address constructs."""

    CONSTR_ID = 0
    wrapped: Union["_PlutusConstrWrapper", PlutusPartAddress]


@dataclass
class PlutusFullAddress(PlutusData):
    """A full address, including payment and staking keys."""

    CONSTR_ID = 0
    payment: PlutusPartAddress
    stake: _PlutusConstrWrapper

    @classmethod
    def from_address(cls, address: Address) -> "PlutusFullAddress":
        """Parse an Address object to a PlutusFullAddress."""
        error_msg = "Only addresses with staking and payment parts are accepted."
        if None in [address.staking_part, address.payment_part]:
            raise ValueError(error_msg)
        stake = _PlutusConstrWrapper(
            _PlutusConstrWrapper(
                PlutusPartAddress(bytes.fromhex(str(address.staking_part))),
            ),
        )
        return PlutusFullAddress(
            PlutusPartAddress(bytes.fromhex(str(address.payment_part))),
            stake=stake,
        )

    def to_address(self) -> Address:
        payment_part = VerificationKeyHash(self.payment.address)
        stake_part = VerificationKeyHash(self.stake.wrapped.wrapped.address)
        return Address(payment_part=payment_part, staking_part=stake_part)


@dataclass
class AssetClass(PlutusData):
    """An asset class. Separates out token policy and asset name."""

    CONSTR_ID = 0

    policy: bytes
    asset_name: bytes

    @classmethod
    def from_assets(cls, asset: Assets) -> "AssetClass":
        """Parse an Assets object into an AssetClass object."""
        error_msg = "Only one asset may be supplied."
        if len(asset) != 1:
            raise ValueError(error_msg)

        if asset.unit() == "lovelace":
            policy = b""
            asset_name = b""
        else:
            policy = bytes.fromhex(asset.unit()[:56])
            asset_name = bytes.fromhex(asset.unit()[56:])

        return AssetClass(policy=policy, asset_name=asset_name)

    @property
    def assets(self):
        """Convert back to assets."""
        if self.policy.hex() == "":
            asset = "lovelace"
        else:
            asset = self.policy.hex() + self.asset_name.hex()

        return Assets(root={asset: 0})
