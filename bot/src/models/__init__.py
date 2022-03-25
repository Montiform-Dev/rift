from .account import *
from .alliance_settings import *
from .audit import *
from .audit_log import *
from .audit_log_config import *
from .auto_role import *
from .blitz import *
from .blitz_target import *
from .build import *
from .condition import *
from .embassy import *
from .embassy_config import *
from .grant import *
from .guild_role import *
from .guild_settings import *
from .inactive_alert import *
from .interview import *
from .mention import *
from .menu import *
from .pnw import *
from .reminder import *
from .resources import *
from .role import *
from .roster import *
from .server import *
from .server_submission import *
from .subscription import *
from .tag import *
from .target_config import *
from .target_rater import *
from .target_reminder import *
from .ticket import *
from .ticket_config import *
from .transaction import *
from .user import *
from .war_room import *
from .war_room_config import *
from .webhook import *

# types = {
#     "integer": "int",
#     "text": "str",
#     "boolean": "bool",
#     "smallint": "ENUM",
#     "resources": "models.Resources",
#     "numeric": "decimal.Decimal",
#     "timestamp with time zone": "datetime.datetime",
#     "bigint": "int",
#     "GENERATED BY DEFAULT AS IDENTITY": "int",
#     "interval": "datetime.timedelta",
#     "json": dict[str, Any],
# }


# def table(text: str) -> None:
#     lines = [i.strip() for i in text.split(",")]
#     lines = [i.split('"') for i in lines]
#     for line in lines:
#         if line[2].endswith("[]"):
#             print(f"    {line[1]}: list[{types.get(line[2].strip()[:-2], 'UNKNOWN')}]")
#         else:
#             print(f"    {line[1]}: {types.get(line[2].strip(), 'UNKNOWN')}")
