"""命令模块。"""

from .ls import handle as handle_ls
from .new_cmd import handle as handle_new
from .resume import handle as handle_resume
from .save import handle as handle_save
from .run import handle as handle_run
from .submit import handle as handle_submit
from .next_cmd import handle as handle_next

__all__ = [
    "handle_ls",
    "handle_new",
    "handle_resume",
    "handle_save",
    "handle_run",
    "handle_submit",
    "handle_next",
]
