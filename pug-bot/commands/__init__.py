from .help import help
from .create import create
from .owner import owner
from .join import join
from .leave import leave
from .cancel import cancel
from .start import start
from .stop import stop
from .close import close
from .reset import reset
from .refresh import refresh
from .remove import remove
from .random import random
from .team import team
from .captain import captain
from .rename import rename
from .pick import pick
from .kick import kick
from .channel import channel
from .win import win

commands = globals()

# Aliases
commands["👢"] = commands["remove"]
