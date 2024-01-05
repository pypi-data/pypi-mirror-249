"""pyaslengine.patch.states"""

from attrs import define, field

from pyaslengine.data import StateInput, StateOutput, JSON
from pyaslengine.states import State
from pyaslengine.log import get_logger

logger = get_logger(__name__)


@define
class StatePatch:
    """Class to patch the behavior of Workflow States during execution.

    Some patches are direct, e.g. `.next` which will override `State.next` if defined in
    the patch.  Similarly, `run_override()` will completely override the `State.run` method
    requiring handling of input, state logic, and returning of output data.

    Other methods, like `post_input_process_hook()` are not direct overrides of State or
    Workflow behavior, but instead, allow for injecting code and logic at intermediate
    stages during execution.  This can be particularly helpful for debugging data and
    logic of a State while it's executing, or even manipulating the input and output
    payloads as they are constructed.
    """

    # State field overrides
    @property
    def field_overrides(self) -> dict:
        return {}

    def run_override(
        self, state: State, state_input: StateInput, registered_resources: dict
    ) -> tuple[str, StateOutput]:
        """Override to define State run logic."""
        logger.info(f"StatePatch: {state.state_id}.run_override")
        raise NotImplementedError()

    def pre_input_process_hook(
        self, state_input: StateInput, current_state: State
    ) -> tuple[StateInput, State]:
        """Override to run method BEFORE input data processed."""
        logger.info(f"StatePatch: {current_state.state_id}.pre_input_process_hook")
        raise NotImplementedError()

    def post_input_process_hook(
        self, state_input: StateInput, current_state: State, original_data: JSON
    ) -> tuple[StateInput, State, JSON]:
        """Override to run method AFTER input data processed."""
        logger.info(f"StatePatch: {current_state.state_id}.post_input_process_hook")
        raise NotImplementedError()

    def pre_output_process_hook(
        self, state_output: StateOutput, current_state: State, original_data: JSON
    ) -> tuple[StateOutput, State, JSON]:
        """Override to run method BEFORE output data processed."""
        logger.info(f"StatePatch: {current_state.state_id}.pre_output_process_hook")
        raise NotImplementedError()

    def post_output_process_hook(
        self, state_output: StateOutput, current_state: State, original_data: JSON
    ) -> tuple[StateOutput, State, JSON]:
        """Override to run method AFTER output data processed."""
        logger.info(f"StatePatch: {current_state.state_id}.post_output_process_hook")
        raise NotImplementedError()

    def hook_defined(self, hook):
        """Return boolean if hook is overridden"""
        return getattr(self, hook).__func__ is not getattr(StatePatch, hook)
