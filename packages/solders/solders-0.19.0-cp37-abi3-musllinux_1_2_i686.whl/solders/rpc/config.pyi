from typing import List, Optional, Sequence, Union

from solders.account_decoder import UiAccountEncoding, UiDataSliceConfig
from solders.commitment_config import CommitmentLevel
from solders.hash import Hash
from solders.pubkey import Pubkey
from solders.rpc.filter import Memcmp
from solders.signature import Signature
from solders.transaction_status import TransactionDetails, UiTransactionEncoding

class RpcSignatureStatusConfig:
    def __init__(self, search_transaction_history: bool): ...
    @property
    def search_transaction_history(self) -> bool: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSignatureStatusConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSignatureStatusConfig": ...

class RpcSendTransactionConfig:
    def __init__(
        self,
        skip_preflight: bool = False,
        preflight_commitment: Optional[CommitmentLevel] = None,
        encoding: Optional[UiTransactionEncoding] = None,
        max_retries: Optional[int] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def skip_preflight(self) -> bool: ...
    @property
    def preflight_commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def encoding(self) -> Optional[UiTransactionEncoding]: ...
    @property
    def max_retries(self) -> Optional[int]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSendTransactionConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSendTransactionConfig": ...
    @staticmethod
    def default() -> "RpcSendTransactionConfig": ...

class RpcSimulateTransactionAccountsConfig:
    def __init__(
        self, addresses: Sequence[Pubkey], encoding: Optional[UiAccountEncoding] = None
    ): ...
    @property
    def addresses(self) -> List[Pubkey]: ...
    @property
    def encoding(self) -> Optional[UiAccountEncoding]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(
        self, other: "RpcSimulateTransactionAccountsConfig", op: int
    ) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSimulateTransactionAccountsConfig": ...
    @staticmethod
    def default() -> "RpcSimulateTransactionAccountsConfig": ...

class RpcSimulateTransactionConfig:
    def __init__(
        self,
        sig_verify: bool = False,
        replace_recent_blockhash: bool = False,
        commitment: Optional[CommitmentLevel] = None,
        accounts: Optional[RpcSimulateTransactionAccountsConfig] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def sig_verify(self) -> bool: ...
    @property
    def replace_recent_blockhash(self) -> bool: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def accounts(self) -> Optional[RpcSimulateTransactionAccountsConfig]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSimulateTransactionConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSimulateTransactionConfig": ...
    @staticmethod
    def default() -> "RpcSimulateTransactionConfig": ...

class RpcRequestAirdropConfig:
    def __init__(
        self,
        recent_blockhash: Optional[Hash] = None,
        commitment: Optional[CommitmentLevel] = None,
    ): ...
    @property
    def recent_blockhash(self) -> Optional[Hash]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcRequestAirdropConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcRequestAirdropConfig": ...
    @staticmethod
    def default() -> "RpcRequestAirdropConfig": ...

class RpcLeaderScheduleConfig:
    def __init__(
        self,
        identity: Optional[Pubkey] = None,
        commitment: Optional[CommitmentLevel] = None,
    ): ...
    @property
    def identity(self) -> Optional[Pubkey]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcLeaderScheduleConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcLeaderScheduleConfig": ...
    @staticmethod
    def default() -> "RpcLeaderScheduleConfig": ...

class RpcBlockProductionConfigRange:
    def __init__(self, first_slot: int, last_slot: Optional[int]): ...
    @property
    def first_slot(self) -> int: ...
    @property
    def last_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcBlockProductionConfigRange", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcBlockProductionConfigRange": ...

class RpcBlockProductionConfig:
    def __init__(
        self,
        identity: Optional[Pubkey] = None,
        range: Optional[RpcBlockProductionConfigRange] = None,
        commitment: Optional[CommitmentLevel] = None,
    ): ...
    @property
    def identity(self) -> Optional[Pubkey]: ...
    @property
    def range(self) -> Optional[RpcBlockProductionConfigRange]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcBlockProductionConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcBlockProductionConfig": ...
    @staticmethod
    def default() -> "RpcBlockProductionConfig": ...

class RpcGetVoteAccountsConfig:
    def __init__(
        self,
        vote_pubkey: Optional[Pubkey] = None,
        commitment: Optional[CommitmentLevel] = None,
        keep_unstaked_delinquents: Optional[bool] = None,
        delinquent_slot_distance: Optional[int] = None,
    ): ...
    @property
    def vote_pubkey(self) -> Optional[Pubkey]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def keep_unstaked_delinquents(self) -> Optional[bool]: ...
    @property
    def delinquent_slot_distance(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcGetVoteAccountsConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcGetVoteAccountsConfig": ...
    @staticmethod
    def default() -> "RpcGetVoteAccountsConfig": ...

class RpcLargestAccountsFilter:
    Circulating: "RpcLargestAccountsFilter"
    NonCirculating: "RpcLargestAccountsFilter"
    def __int__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, o: object) -> bool: ...

class RpcLargestAccountsConfig:
    def __init__(
        self,
        commitment: Optional[CommitmentLevel] = None,
        filter: Optional[RpcLargestAccountsFilter] = None,
    ): ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def filter(self) -> Optional[RpcLargestAccountsFilter]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcLargestAccountsConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcLargestAccountsConfig": ...
    @staticmethod
    def default() -> "RpcLargestAccountsConfig": ...

class RpcSupplyConfig:
    def __init__(
        self,
        exclude_non_circulating_accounts_list: bool,
        commitment: Optional[CommitmentLevel] = None,
    ): ...
    @property
    def exclude_non_circulating_accounts_list(self) -> bool: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSupplyConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSupplyConfig": ...
    @staticmethod
    def default() -> "RpcSupplyConfig": ...

class RpcEpochConfig:
    def __init__(
        self,
        epoch: Optional[int] = None,
        commitment: Optional[CommitmentLevel] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def epoch(self) -> Optional[int]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcEpochConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcEpochConfig": ...
    @staticmethod
    def default() -> "RpcEpochConfig": ...

class RpcAccountInfoConfig:
    def __init__(
        self,
        encoding: Optional[UiAccountEncoding] = None,
        data_slice: Optional[UiDataSliceConfig] = None,
        commitment: Optional[CommitmentLevel] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def encoding(self) -> Optional[UiAccountEncoding]: ...
    @property
    def data_slice(self) -> Optional[UiDataSliceConfig]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcAccountInfoConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcAccountInfoConfig": ...
    @staticmethod
    def default() -> "RpcAccountInfoConfig": ...

class RpcProgramAccountsConfig:
    def __init__(
        self,
        account_config: RpcAccountInfoConfig,
        filters: Optional[Sequence[Union[int, Memcmp]]] = None,
        with_context: Optional[bool] = None,
    ): ...
    @property
    def account_config(self) -> RpcAccountInfoConfig: ...
    @property
    def filters(self) -> Optional[Sequence[Union[int, Memcmp]]]: ...
    @property
    def with_context(self) -> Optional[bool]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcProgramAccountsConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcProgramAccountsConfig": ...
    @staticmethod
    def default() -> "RpcProgramAccountsConfig": ...

class RpcTransactionLogsFilter:
    All: "RpcTransactionLogsFilter"
    AllWithVotes: "RpcTransactionLogsFilter"
    def __int__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, o: object) -> bool: ...

class RpcTransactionLogsFilterMentions:
    def __init__(self, pubkey: Pubkey): ...
    def __richcmp__(
        self, other: "RpcTransactionLogsFilterMentions", op: int
    ) -> bool: ...
    def __repr__(self) -> str: ...
    @property
    def pubkey(self) -> Pubkey: ...

class RpcTransactionLogsConfig:
    def __init__(self, commitment: Optional[CommitmentLevel] = None): ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcTransactionLogsConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcTransactionLogsConfig": ...

class RpcTokenAccountsFilterMint:
    def __init__(self, mint: Pubkey): ...
    def __richcmp__(self, other: "RpcTokenAccountsFilterMint", op: int) -> bool: ...
    def __repr__(self) -> str: ...
    @property
    def mint(self) -> Pubkey: ...

class RpcTokenAccountsFilterProgramId:
    def __init__(self, program_id: Pubkey): ...
    def __richcmp__(
        self, other: "RpcTokenAccountsFilterProgramId", op: int
    ) -> bool: ...
    def __repr__(self) -> str: ...
    @property
    def program_id(self) -> Pubkey: ...

class RpcSignatureSubscribeConfig:
    def __init__(
        self,
        commitment: Optional[CommitmentLevel] = None,
        enable_received_notification: Optional[bool] = None,
    ): ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def enable_received_notification(self) -> Optional[bool]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSignatureSubscribeConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSignatureSubscribeConfig": ...
    @staticmethod
    def default() -> "RpcSignatureSubscribeConfig": ...

class RpcBlockSubscribeFilter:
    All: "RpcBlockSubscribeFilter"
    def __int__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __eq__(self, o: object) -> bool: ...

class RpcBlockSubscribeFilterMentions:
    def __init__(self, pubkey: Pubkey): ...
    def __richcmp__(
        self, other: "RpcBlockSubscribeFilterMentions", op: int
    ) -> bool: ...
    def __repr__(self) -> str: ...
    @property
    def pubkey(self) -> Pubkey: ...

class RpcBlockSubscribeConfig:
    def __init__(
        self,
        commitment: Optional[CommitmentLevel] = None,
        encoding: Optional[UiTransactionEncoding] = None,
        transaction_details: Optional[TransactionDetails] = None,
        show_rewards: Optional[bool] = None,
        max_supported_transaction_version: Optional[int] = None,
    ): ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def encoding(self) -> Optional[UiTransactionEncoding]: ...
    @property
    def transaction_details(self) -> Optional[TransactionDetails]: ...
    @property
    def show_rewards(self) -> Optional[bool]: ...
    @property
    def max_supported_transaction_version(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcBlockSubscribeConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcBlockSubscribeConfig": ...
    @staticmethod
    def default() -> "RpcBlockSubscribeConfig": ...

class RpcSignaturesForAddressConfig:
    def __init__(
        self,
        before: Optional[Signature] = None,
        until: Optional[Signature] = None,
        limit: Optional[int] = None,
        commitment: Optional[CommitmentLevel] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def before(self) -> Optional[Signature]: ...
    @property
    def until(self) -> Optional[Signature]: ...
    @property
    def limit(self) -> Optional[int]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcSignaturesForAddressConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcSignaturesForAddressConfig": ...
    @staticmethod
    def default() -> "RpcSignaturesForAddressConfig": ...

class RpcBlockConfig:
    def __init__(
        self,
        encoding: Optional[UiTransactionEncoding] = None,
        transaction_details: Optional[TransactionDetails] = None,
        rewards: Optional[bool] = None,
        commitment: Optional[CommitmentLevel] = None,
        max_supported_transaction_version: Optional[int] = None,
    ): ...
    @property
    def encoding(self) -> Optional[UiTransactionEncoding]: ...
    @property
    def transaction_details(self) -> Optional[TransactionDetails]: ...
    @property
    def rewards(self) -> Optional[bool]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def max_supported_transaction_version(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcBlockConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcBlockConfig": ...
    @staticmethod
    def default() -> "RpcBlockConfig": ...
    @staticmethod
    def rewards_only() -> "RpcBlockConfig": ...
    @staticmethod
    def rewards_with_commitment(
        commitment: Optional[CommitmentLevel] = None,
    ) -> "RpcBlockConfig": ...

class RpcTransactionConfig:
    def __init__(
        self,
        encoding: Optional[UiTransactionEncoding] = None,
        commitment: Optional[CommitmentLevel] = None,
        max_supported_transaction_version: Optional[int] = None,
    ): ...
    @property
    def encoding(self) -> Optional[UiTransactionEncoding]: ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def max_supported_transaction_version(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcTransactionConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcTransactionConfig": ...
    @staticmethod
    def default() -> "RpcTransactionConfig": ...

class RpcContextConfig:
    def __init__(
        self,
        commitment: Optional[CommitmentLevel] = None,
        min_context_slot: Optional[int] = None,
    ): ...
    @property
    def commitment(self) -> Optional[CommitmentLevel]: ...
    @property
    def min_context_slot(self) -> Optional[int]: ...
    def __bytes__(self) -> bytes: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __richcmp__(self, other: "RpcContextConfig", op: int) -> bool: ...
    def to_json(self) -> str: ...
    @staticmethod
    def from_json(raw: str) -> "RpcContextConfig": ...
    @staticmethod
    def default() -> "RpcContextConfig": ...
