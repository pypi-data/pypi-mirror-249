from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from typing import Dict, Callable, Any, Tuple, TYPE_CHECKING, MutableMapping

import mosaik_api
import pandas as pd

from vessim._util import Clock

if TYPE_CHECKING:
    from vessim.cosim.environment import Microgrid


class Controller(ABC):

    def __init__(self, step_size: int):
        self.step_size = step_size
        self.microgrid = None
        self.grid_signals = None
        self.clock = None

    def start(self, microgrid: "Microgrid", clock: Clock, grid_signals: Dict):
        self.microgrid = microgrid
        self.clock = clock
        self.grid_signals = grid_signals

    def custom_init(self):
        """TODO document"""

    @abstractmethod
    def step(self, time: int, p_delta: float, actors: Dict) -> None:
        pass  # TODO document

    def finalize(self) -> None:
        """This method can be overridden clean-up after the simulation finished."""


class Monitor(Controller):

    def __init__(self, step_size: int, monitor_storage=True, monitor_grid_signals=True):
        super().__init__(step_size=step_size)
        self.monitor_storage = monitor_storage
        self.monitor_grid_signals = monitor_grid_signals
        self.monitor_log: Dict[datetime, Dict] = defaultdict(dict)
        self.custom_monitor_fns = []

    def custom_init(self):
        if self.monitor_storage:
            self.add_monitor_fn(lambda _: {"storage": self.microgrid.storage.state()})
        if self.monitor_grid_signals:
            for signal_name, signal_api in self.grid_signals.items():
                self.add_monitor_fn(lambda time: {
                    signal_name: self.grid_signals[signal_name].actual(
                        self.clock.to_datetime(time)
                    )
                })

    def add_monitor_fn(self, fn: Callable[[float], Dict[str, Any]]):
        self.custom_monitor_fns.append(fn)

    def step(self, time: int, p_delta: float, actors: Dict) -> None:
        self.monitor(time, p_delta, actors)

    def monitor(self, time: int, p_delta: float, actors: Dict) -> None:
        log_entry = dict(
            p_delta=p_delta,
            actors=actors,
        )
        for monitor_fn in self.custom_monitor_fns:
            log_entry.update(monitor_fn(time))
        self.monitor_log[self.clock.to_datetime(time)] = log_entry

    def monitor_log_to_csv(self, out_path: str):
        df = pd.DataFrame({k: flatten_dict(v) for k, v in self.monitor_log.items()}).T
        df.to_csv(out_path)


def flatten_dict(d: MutableMapping, parent_key: str = '') -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + "." + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, str(new_key)).items())
        else:
            items.append((new_key, v))
    return dict(items)


class ControllerSim(mosaik_api.Simulator):
    META = {
        "type": "time-based",
        "models": {
            "Controller": {
                "public": True,
                "any_inputs": True,
                "params": ["controller"],
                "attrs": [],
            },
        },
    }

    def __init__(self):
        super().__init__(self.META)
        self.eid = "Controller"
        self.step_size = None
        self.controller = None

    def init(self, sid, time_resolution=1., **sim_params):
        self.step_size = sim_params["step_size"]
        return self.meta

    def create(self, num, model, **model_params):
        assert num == 1, "Only one instance per simulation is supported"
        self.controller = model_params["controller"]
        return [{"eid": self.eid, "type": model}]

    def step(self, time, inputs, max_advance):
        self.controller.step(time, *_parse_controller_inputs(inputs[self.eid]))
        return time + self.step_size

    def get_data(self, outputs):
        return {}  # TODO so far unused

    def finalize(self) -> None:
        """Stops the api server and the collector thread when the simulation finishes."""
        self.controller.finalize()


def _parse_controller_inputs(inputs: Dict[str, Dict[str, Any]]) -> Tuple[float, Dict]:
    try:
        p_delta = _get_val(inputs, "p_delta")
    except KeyError:
        p_delta = None  # in case there has not yet been any power reported by actors
    actor_keys = [k for k in inputs.keys() if k.startswith("actor")]
    actors = defaultdict(dict)
    for k in actor_keys:
        _, actor_name, attr = k.split(".")
        actors[actor_name][attr] = _get_val(inputs, k)
    return p_delta, dict(actors)


def _get_val(inputs: Dict, key: str) -> Any:
    return list(inputs[key].values())[0]
