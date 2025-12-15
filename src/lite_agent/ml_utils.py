import json
import os
import pickle
from typing import Any, Callable, Optional

# Assuming these imports from jax, flax, and custom utils
from flax.training import train_state
from jax.experimental import jax_utils

# Placeholder for project-specific types if they are not standard Flax/JAX types
# from .some_module import TrainState, FlaxPreTrainedModel, PyTree, SaveDtype

# For the purpose of this implementation, we'll define some placeholder types
# based on the context provided in previous turns. In a real scenario, these
# would be imported from the actual project.


# Placeholder for FlaxPreTrainedModel (assuming it has a .config attribute with .to_json_string())
class FlaxPreTrainedModel:
    def __init__(self, config):
        self.config = config


class ModelConfig:
    def to_json_string(self):
        return json.dumps(self.__dict__)


# Placeholder for PyTree (JAX PyTree type)
PyTree = Any

# Placeholder for TrainState (Flax TrainState)
TrainState = train_state.TrainState

# Placeholder for SaveDtype (jax_utils.SaveDtype)
SaveDtype = Any  # This should ideally be jax_utils.SaveDtype

# --- Placeholder for project-specific utility functions ---
# These functions (create_path, get_enabled_save_path) are assumed to exist
# elsewhere in the 'lite_agent' module or a common 'utils' file.
# If they don't exist, they would need to be implemented or their actual source found.


def create_path(path: str):
    """Placeholder for creating directories recursively."""
    os.makedirs(path, exist_ok=True)


def get_enabled_save_path(
    base_dir: str, component_name: str, enable_save: bool
) -> Optional[str]:
    """
    Placeholder for determining the save path.
    If component_name is empty or ".", it implies saving to the base_dir directly.
    """
    if not enable_save:
        return None
    if not component_name or component_name == ".":
        return base_dir
    return os.path.join(base_dir, component_name)


# --- End of Placeholder section ---


def _save_loop_state(save_dir: str, loop_state: Any, enable_save: bool):
    """
    Encapsulates the common logic for saving loop_state using pickle.
    """
    if enable_save:
        loop_state_path = os.path.join(save_dir, "loop_state.pkl")
        create_path(os.path.dirname(loop_state_path))
        with open(loop_state_path, "wb") as f:
            pickle.dump(loop_state, f)
        print(
            f"Loop state saved to {loop_state_path}"
        )  # Added for verbosity during implementation


def _save_experiment_config(save_path: str, config: Any, enable_save: bool):
    """
    Encapsulates the common logic for saving a model's configuration.
    Assumes config object has a .to_json_string() method.
    """
    if enable_save:
        create_path(os.path.dirname(save_path))
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(config.to_json_string())
        print(
            f"Experiment config saved to {save_path}"
        )  # Added for verbosity during implementation


def _save_model_component(
    component_name: str,
    save_dir: str,
    enable_save: bool,
    save_dtype: SaveDtype,
    model_config_source: Optional[FlaxPreTrainedModel] = None,
    pytree_to_save: Optional[PyTree] = None,
    train_state_to_save: Optional[TrainState] = None,
    save_train_state: bool = False,
    sharding_model_source: Optional[FlaxPreTrainedModel] = None,
    sharding_fn: Optional[Callable] = None,
    target_params_component: bool = False,
) -> None:
    """
    A generic utility to handle the saving of various model components (base, q-head, policy, target params, etc.).
    This function will be called for each distinct component that needs saving.
    """
    component_save_path = get_enabled_save_path(save_dir, component_name, enable_save)

    if component_save_path:
        # 1. Save Config
        if model_config_source:
            _save_experiment_config(
                os.path.join(component_save_path, "config.json"),
                model_config_source.config,
                True,
            )

        # 2. Prepare PyTree for Saving
        params_to_save: Optional[PyTree] = None
        if pytree_to_save is not None:
            params_to_save = pytree_to_save
        elif train_state_to_save is not None:
            if save_train_state and not target_params_component:
                params_to_save = train_state_to_save
            else:
                params_to_save = train_state_to_save.params

        # 3. Determine Filename
        filename = "params.msgpack"
        if (
            params_to_save is not None
            and isinstance(params_to_save, TrainState)
            and save_train_state
            and not target_params_component
        ):
            filename = "train_state.msgpack"

        # 4. Save PyTree
        if params_to_save is not None:
            sharding = None
            if sharding_model_source and sharding_fn:
                # Assuming sharding_fn takes the model source and returns sharding info
                # The actual arguments to sharding_fn might vary, adjust as needed.
                sharding = sharding_fn(sharding_model_source)

            # Ensure the directory for saving the pytree exists
            create_path(component_save_path)

            jax_utils.save_pytree(
                params_to_save,
                os.path.join(component_save_path, filename),
                save_dtype,
                sharding=sharding,
            )
            print(
                f"Component '{component_name}' PyTree saved to {os.path.join(component_save_path, filename)}"
            )  # Added for verbosity during implementation
