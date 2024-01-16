"""Some utility functions used acrross the repository."""
import threading
from enum import Enum

import ipywidgets as ipw
import traitlets as tl
from aiida.plugins import DataFactory

CifData = DataFactory("core.cif")  # pylint: disable=invalid-name
StructureData = DataFactory("core.structure")  # pylint: disable=invalid-name
TrajectoryData = DataFactory("core.array.trajectory")  # pylint: disable=invalid-name

class _StatusWidgetMixin(tl.HasTraits):
    """Show temporary messages for example for status updates.
    This is a mixin class that is meant to be part of an inheritance
    tree of an actual widget with a 'value' traitlet that is used
    to convey a status message. See the non-private classes below
    for examples.
    """

    message = tl.Unicode(default_value="", allow_none=True)
    new_line = "\n"

    def __init__(self, clear_after=3, *args, **kwargs):
        self._clear_timer = None
        self._clear_after = clear_after
        self._message_stack = []
        super().__init__(*args, **kwargs)

    def _clear_value(self):
        """Set widget .value to be an empty string."""
        if self._message_stack:
            self._message_stack.pop(0)
            self.value = self.new_line.join(self._message_stack)
        else:
            self.value = ""

    def show_temporary_message(self, value, clear_after=None):
        """Show a temporary message and clear it after the given interval."""
        clear_after = clear_after or self._clear_after
        if value:
            self._message_stack.append(value)
            self.value = self.new_line.join(self._message_stack)

            # Start new timer that will clear the value after the specified interval.
            self._clear_timer = threading.Timer(self._clear_after, self._clear_value)
            self._clear_timer.start()
            self.message = None

class StatusHTML(_StatusWidgetMixin, ipw.HTML):
    """Show temporary HTML messages for example for status updates."""

    new_line = "<br>"

    # This method should be part of _StatusWidgetMixin, but that does not work
    # for an unknown reason.
    @tl.observe("message")
    def _observe_message(self, change):
        self.show_temporary_message(change["new"])


# Define the message levels as Enum
class MessageLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "danger"
    SUCCESS = "success"


def wrap_message(message, level=MessageLevel.INFO):
    """Wrap message into HTML code with the given level."""
    # mapping level to fa icon
    # https://fontawesome.com/v4.7.0/icons/
    mapping = {
        MessageLevel.INFO: "info-circle",
        MessageLevel.WARNING: "exclamation-triangle",
        MessageLevel.ERROR: "exclamation-circle",
        MessageLevel.SUCCESS: "check-circle",
    }

    # The message is wrapped into a div with the class "alert" and the icon of the given level
    return f"""
        <div class="alert alert-{level.value}" role="alert" style="margin-bottom: 0px; padding: 6px 12px;">
            <i class="fa fa-{mapping[level]}"></i>{message}
        </div>
    """