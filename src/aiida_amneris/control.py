import ipywidgets as ipw
from aiida import engine, manage

from IPython.display import clear_output

import subprocess

class DaemonControlPage(ipw.VBox):
    def __init__(self, *args, **kwargs):
        self._daemon = engine.daemon.get_daemon_client()
        self._status = ipw.Output()

        # Start daemon.
        start_button = ipw.Button(description="Start daemon", button_style="info")
        start_button.on_click(self._start_daemon)

        # Stop daemon.
        stop_button = ipw.Button(description="Stop daemon", button_style="danger")
        stop_button.on_click(self._stop_daemon)

        # Restart daemon.
        restart_button = ipw.Button(description="Restart daemon", button_style="warning")
        restart_button.on_click(self._restart_daemon)

        self.info=ipw.HTML()
        self._update_status()
        super().__init__(children=[self.info, self._status, ipw.HBox([start_button, stop_button, restart_button])])

    def _restart_daemon(self, _=None):
        self._clear_status()
        self.info.value = "Restarting the daemon..."
        response = self._daemon.restart_daemon()
        self.info.value = ""
        self._update_status()
        return response

    def _start_daemon(self, _=None):
        self._clear_status()
        self.info.value = "Starting the daemon..."
        response = self._daemon.start_daemon()
        self.info.value = ""
        self._update_status()
        return response

    def _stop_daemon(self, _=None):
        self._clear_status()
        self.info.value = "Stopping the daemon..."
        response = self._daemon.stop_daemon()
        self.info.value = ""
        self._update_status()
        return response

    def _update_status(self, _=None):
        self._clear_status()
        with self._status:
            result = subprocess.run(["verdi", "daemon", "status"], capture_output=True, text=True)
            print(result.stdout, result.stderr)

    def _clear_status(self):
        with self._status:
            clear_output()


class StatusControlPage(ipw.HTML):
    def __init__(self):
        print("AiiDA status")
        print(subprocess.run(["verdi", "status"], capture_output=True, text=True).stdout)
        super().__init__()


class Profile(ipw.HBox):
    def __init__(self, profile):
        self.profile = profile
        self.name = ipw.HTML(f"""<font size="3"> * {self.profile.name}</font>""")
        self.make_default = ipw.Button(description="Make default", button_style="info")
        self.delete = ipw.Button(description="Delele", button_style="danger")
        super().__init__(children=[self.name, self.make_default, self.delete])


class ProfileControlPage(ipw.VBox):
    def __init__(self):
        text = ipw.HTML(value="<h3> List of profiles </h3>")
        children = [Profile(p) for p in manage.get_config().profiles]
        super().__init__(children=children)
