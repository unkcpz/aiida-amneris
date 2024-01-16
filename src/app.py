import solara
import aiida
import ipywidgets as ipw

from aiida_amneris.computational_resource import ComputationalResourcesWidget
from aiida_amneris.control import DaemonControlPage, StatusControlPage, ProfileControlPage

from IPython.display import display, clear_output

aiida.load_profile()

@solara.component
def Page():
    correspondance = {
        "Daemon": DaemonControlPage,
        "Status": StatusControlPage,
        "Profile": ProfileControlPage,
    }

    toc = ipw.ToggleButtons(
        options=correspondance.keys(),
        value=None,
        orientation="vertical",
        layout=ipw.Layout(width='200px')
    )



    output = ipw.Output()

    def update_output(value={"new": "Group"}):
        if value['new'] in correspondance:
            with output:
                clear_output()
                display(correspondance[value['new']]())


    toc.observe(update_output, names="value")

    toc.value = "Daemon"

    display(ipw.HBox([toc, output]))


    # The computation resources widget.
    crw = ComputationalResourcesWidget()
    display(crw)