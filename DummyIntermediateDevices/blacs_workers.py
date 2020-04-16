"""This is where BLACS really connects to the hardware.

Everything elso is just sending it here.
"""
from blacs.tab_base_classes import Worker


class DummyIntermediateDeviceWorker(Worker):
    def init(self):
        pass

    def program_manual(self, front_panel_values):
        return front_panel_values

    def transition_to_buffered(self, device_name, h5file, initial_values, fresh):
        return initial_values

    def transition_to_manual(self,abort = False):
        return True

    def abort_transition_to_buffered(self):
        return self.transition_to_manual(True)

    def abort_buffered(self):
        return self.transition_to_manual(True)

    def shutdown(self):
        pass
