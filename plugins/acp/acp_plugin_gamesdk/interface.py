from dataclasses import dataclass
from enum import Enum
from typing import List, Literal, Optional, Dict, Any

from virtuals_acp.models import ACPJobPhase

@dataclass
class AcpOffering:
    name: str
    price: float

    def __str__(self) -> str:
        output = (
            f"Offering(name={self.name}, price={self.price})"
        )
        return output

class AcpJobPhasesDesc(str, Enum):
    REQUEST = "request"
    NEGOTIATION = "pending_payment"
    TRANSACTION = "in_progress"
    EVALUATION = "evaluation"
    COMPLETED = "completed"
    REJECTED = "rejected"

ACP_JOB_PHASE_MAP: Dict[ACPJobPhase, AcpJobPhasesDesc] = {
    ACPJobPhase.REQUEST: AcpJobPhasesDesc.REQUEST,
    ACPJobPhase.NEGOTIATION: AcpJobPhasesDesc.NEGOTIATION,
    ACPJobPhase.TRANSACTION: AcpJobPhasesDesc.TRANSACTION,
    ACPJobPhase.EVALUATION: AcpJobPhasesDesc.EVALUATION,
    ACPJobPhase.COMPLETED: AcpJobPhasesDesc.COMPLETED,
    ACPJobPhase.REJECTED: AcpJobPhasesDesc.REJECTED,
}

@dataclass
class AcpRequestMemo:
    id: int

    def __repr__(self) -> str:
        return f"Memo(ID: {self.id})"
    
@dataclass
class ITweet:
    type: Literal["buyer", "seller"]
    tweet_id: str
    content: str
    created_at: int

@dataclass
class IAcpJob:
    jobId: Optional[int]
    clientName : Optional[str]
    providerName: Optional[str]
    desc: str
    price: str
    providerAddress: Optional[str]
    phase: AcpJobPhasesDesc
    memo: List[AcpRequestMemo]
    tweetHistory: List[ITweet] | List

    def __repr__(self) -> str:
        output =(
            f"Job ID: {self.jobId}, "
            f"Client Name: {self.clientName}, "
            f"Provider Name: {self.providerName}, "
            f"Description: {self.desc}, "
            f"Price: {self.price}, "
            f"Provider Address: {self.providerAddress}, "
            f"Phase: {self.phase.value}, "
            f"Memo: {self.memo}, "
            f"Tweet History: {self.tweetHistory}, "
        ) 
        return output

@dataclass
class IDeliverable:
    type: str
    value: str
    clientName: Optional[str]
    providerName: Optional[str]
@dataclass
class IInventory(IDeliverable):
    jobId: int
    clientName: Optional[str]
    providerName: Optional[str]

@dataclass
class AcpJobsSection:
    asABuyer: List[IAcpJob]
    asASeller: List[IAcpJob]

    def __str__(self) -> str:
        buyer_jobs = ""
        for index, job in enumerate(self.asABuyer):
            buyer_jobs += f"#{index+1} {str(job)} \n"

        seller_jobs = ""
        for index, job in enumerate(self.asASeller):
            seller_jobs += f"#{index+1} {str(job)} \n"

        output = (
            f"As Buyer:\n{buyer_jobs}\n"
            f"As Seller:\n{seller_jobs}\n"
        )
        return output

@dataclass
class AcpJobs:
    active: AcpJobsSection
    completed: List[IAcpJob]
    cancelled: List[IAcpJob]

    def __str__(self) -> str:
        output = (
            f"💻 Jobs\n"
            f"🌕 Active Jobs:\n{self.active}\n"
            f"🟢 Completed:\n{self.completed}\n"
            f"🔴 Cancelled:\n{self.cancelled}\n"
        )
        return output
    
@dataclass
class AcpInventory:
    acquired: List[IInventory]
    produced: Optional[List[IInventory]]

    def __str__(self) -> str:
        output = (
            f"💼 Inventory\n"
            f"Acquired: {self.acquired}\n"
            f"Produced: {self.produced}\n"
        )
        return output

@dataclass
class AcpState:
    inventory: AcpInventory
    jobs: AcpJobs

    def __str__(self) -> str:
        output = (
            f"🤖 Agent State".center(50, '=') + "\n" + \
            f"{str(self.inventory)}\n" + \
            f"{str(self.jobs)}\n" + \
            f"State End".center(50, '=') + "\n"
        )
        return output