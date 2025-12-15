from typing import Any, Optional

# Assuming these are available from the ml_utils module
from .ml_utils import (
    FlaxPreTrainedModel,
    PyTree,
    SaveDtype,
    TrainState,
    _save_loop_state,
    _save_model_component,
)


# Assuming sharding functions are available from a jax_utils module or similar
# Placeholder definitions for now, in a real scenario these would be imported
def get_sharding_from_model(model: FlaxPreTrainedModel, params: PyTree, mesh=None):
    """Placeholder for getting sharding from a model."""
    print(f"DEBUG: get_sharding_from_model called for {model}")
    return None  # Return None or a mock sharding object


def get_sharding_from_model_policy(
    model: FlaxPreTrainedModel, params: PyTree, mesh=None
):
    """Placeholder for getting sharding from a policy model."""
    print(f"DEBUG: get_sharding_from_model_policy called for {model}")
    return None


def get_sharding_from_model_head(model: FlaxPreTrainedModel, params: PyTree, mesh=None):
    """Placeholder for getting sharding from a model head."""
    print(f"DEBUG: get_sharding_from_model_head called for {model}")
    return None


# --- Refactored dump_state functions ---


def dump_state_single_model_root_config(
    save_dir: str,
    loop_state: Any,
    model: FlaxPreTrainedModel,
    train_state: TrainState,
    enable_save: bool,
    save_dtype: SaveDtype,
    save_train_state: bool = False,
    mesh=None,  # Assuming mesh might be passed for sharding
):
    """
    Refactored version of dump_state for a single model with config at the root save_dir.
    Original patterns:
    - Dumps loop_state to loop_state.pkl.
    - Creates output directories using create_path.
    - Saves model.config to config.json at save_dir.
    - Saves train_state (full object) or train_state.params (just parameters)
      using save_pytree to train_state.msgpack or params.msgpack.
    - Uses get_sharding_from_model.
    """
    print(f"DEBUG: Calling dump_state_single_model_root_config for {save_dir}")

    # Save loop state
    _save_loop_state(save_dir, loop_state, enable_save)

    # Save model component
    _save_model_component(
        component_name=".",  # Save to root of save_dir
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=model,
        train_state_to_save=train_state,
        save_train_state=save_train_state,
        sharding_model_source=model,
        sharding_fn=get_sharding_from_model,
    )


def dump_state_single_model_base_subdir(
    save_dir: str,
    loop_state: Any,
    model: FlaxPreTrainedModel,
    train_state: TrainState,
    enable_save: bool,
    save_dtype: SaveDtype,
    save_train_state: bool = False,
    mesh=None,  # Assuming mesh might be passed for sharding
):
    """
    Refactored version of dump_state for a single model saved in a 'base' subdirectory.
    Original patterns:
    - Dumps loop_state to loop_state.pkl.
    - Creates output directories using create_path.
    - Dumps model.config to save_dir/base/config.json.
    - Saves train_state (full object) or train_state.params (just parameters)
      into save_dir/base/train_state.msgpack or params.msgpack.
    - Uses get_sharding_from_model.
    """
    print(f"DEBUG: Calling dump_state_single_model_base_subdir for {save_dir}")

    # Save loop state
    _save_loop_state(save_dir, loop_state, enable_save)

    # Save model component in 'base' subdirectory
    _save_model_component(
        component_name="base",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=model,
        train_state_to_save=train_state,
        save_train_state=save_train_state,
        sharding_model_source=model,
        sharding_fn=get_sharding_from_model,
    )


def dump_state_base_q_head(
    save_dir: str,
    loop_state: Any,
    base_model: FlaxPreTrainedModel,
    base_train_state: TrainState,
    q_head_model: FlaxPreTrainedModel,
    q_head_train_state: TrainState,
    enable_save: bool,
    save_dtype: SaveDtype,
    save_train_state: bool = False,
    mesh=None,
):
    """
    Refactored version of dump_state for a Base + Q-head model architecture.
    """
    print(f"DEBUG: Calling dump_state_base_q_head for {save_dir}")

    _save_loop_state(save_dir, loop_state, enable_save)

    # Save base component
    _save_model_component(
        component_name="base",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=base_model,
        train_state_to_save=base_train_state,
        save_train_state=save_train_state,
        sharding_model_source=base_model,
        sharding_fn=get_sharding_from_model,
    )

    # Save q_head component
    _save_model_component(
        component_name="q_head",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=q_head_model,
        train_state_to_save=q_head_train_state,
        save_train_state=save_train_state,
        sharding_model_source=q_head_model,
        sharding_fn=get_sharding_from_model,  # Assuming get_sharding_from_model is generic enough for q_head
    )


def dump_state_policy_value_head(
    save_dir: str,
    loop_state: Any,
    policy_model: FlaxPreTrainedModel,
    policy_train_state: TrainState,
    value_head_model: FlaxPreTrainedModel,
    value_head_train_state: TrainState,
    enable_save: bool,
    save_dtype: SaveDtype,
    save_train_state: bool = False,
    mesh=None,
):
    """
    Refactored version of dump_state for a Policy + Value-head model architecture.
    """
    print(f"DEBUG: Calling dump_state_policy_value_head for {save_dir}")

    _save_loop_state(save_dir, loop_state, enable_save)

    # Save policy component
    _save_model_component(
        component_name="policy",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=policy_model,
        train_state_to_save=policy_train_state,
        save_train_state=save_train_state,
        sharding_model_source=policy_model,
        sharding_fn=get_sharding_from_model_policy,
    )

    # Save value_head component
    _save_model_component(
        component_name="value_head",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=value_head_model,
        train_state_to_save=value_head_train_state,
        save_train_state=save_train_state,
        sharding_model_source=value_head_model,
        sharding_fn=get_sharding_from_model_head,
    )


def dump_state_complex_architecture(
    save_dir: str,
    loop_state: Any,
    base_model: FlaxPreTrainedModel,
    base_train_state: TrainState,
    target_base_params: Optional[PyTree],
    q_head_model: FlaxPreTrainedModel,
    q1_head_train_state: TrainState,
    q2_head_train_state: TrainState,
    q1_target_head_params: Optional[PyTree],
    q2_target_head_params: Optional[PyTree],
    v_head_model: FlaxPreTrainedModel,
    v_head_train_state: TrainState,
    enable_save: bool,
    save_dtype: SaveDtype,
    save_train_state: bool = False,
    mesh=None,
):
    """
    Refactored version of dump_state for a complex model architecture
    (Base, Q1/Q2-head, V-head, Target Base, Q1/Q2 Target-head).
    """
    print(f"DEBUG: Calling dump_state_complex_architecture for {save_dir}")

    _save_loop_state(save_dir, loop_state, enable_save)

    # Save base component
    _save_model_component(
        component_name="base",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=base_model,
        train_state_to_save=base_train_state,
        save_train_state=save_train_state,
        sharding_model_source=base_model,
        sharding_fn=get_sharding_from_model,
    )

    # Save target_base component
    if target_base_params is not None:
        _save_model_component(
            component_name="target_base",
            save_dir=save_dir,
            enable_save=enable_save,
            save_dtype=save_dtype,
            model_config_source=base_model,  # config source is still base_model
            pytree_to_save=target_base_params,
            sharding_model_source=base_model,
            sharding_fn=get_sharding_from_model,
            target_params_component=True,  # Indicate this is a target params type
        )

    # Save q1_head component
    _save_model_component(
        component_name="q1_head",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=q_head_model,
        train_state_to_save=q1_head_train_state,
        save_train_state=save_train_state,
        sharding_model_source=q_head_model,
        sharding_fn=get_sharding_from_model,
    )

    # Save q2_head component
    _save_model_component(
        component_name="q2_head",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=q_head_model,
        train_state_to_save=q2_head_train_state,
        save_train_state=save_train_state,
        sharding_model_source=q_head_model,
        sharding_fn=get_sharding_from_model,
    )

    # Save v_head component
    _save_model_component(
        component_name="v_head",
        save_dir=save_dir,
        enable_save=enable_save,
        save_dtype=save_dtype,
        model_config_source=v_head_model,
        train_state_to_save=v_head_train_state,
        save_train_state=save_train_state,
        sharding_model_source=v_head_model,
        sharding_fn=get_sharding_from_model,  # Assuming get_sharding_from_model is generic enough for v_head
    )

    # Save q1_target_head component
    if q1_target_head_params is not None:
        _save_model_component(
            component_name="q1_target_head",
            save_dir=save_dir,
            enable_save=enable_save,
            save_dtype=save_dtype,
            model_config_source=q_head_model,
            pytree_to_save=q1_target_head_params,
            sharding_model_source=q_head_model,
            sharding_fn=get_sharding_from_model,
            target_params_component=True,
        )

    # Save q2_target_head component
    if q2_target_head_params is not None:
        _save_model_component(
            component_name="q2_target_head",
            save_dir=save_dir,
            enable_save=enable_save,
            save_dtype=save_dtype,
            model_config_source=q_head_model,
            pytree_to_save=q2_target_head_params,
            sharding_model_source=q_head_model,
            sharding_fn=get_sharding_from_model,
            target_params_component=True,
        )
