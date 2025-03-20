from typing import Dict

from fastapi_sa_orm_filter.operators import Operators as Ops

receipts_filters: Dict[str, list] = {
    "payment_type": [Ops.eq, Ops.in_],
    "total": [Ops.between, Ops.eq, Ops.gt, Ops.lt, Ops.in_],
    "created_at": [Ops.between, Ops.eq, Ops.gt, Ops.lt, Ops.in_],
}
