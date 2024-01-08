# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This file defines the run utils.
"""

import os
from typing import Union

from .constants import UNKNOWN_VALUE
from ..model_selector.constants import RunDetailsConstants


def calculate_per_node_process_count() -> Union[int, str]:
    """Calculate the process count from run properties."""
    try:
        # in case of MaaP, number_of_gpu_to_use_finetuning is passed as input to pipeline component
        # Need to deduce the value in finetune component
        from azureml.core import Run
        run_details = Run.get_context().get_details()
        total_process_count = run_details[
            RunDetailsConstants.RUN_DEFINITION][
            RunDetailsConstants.PYTORCH_DISTRIBUTION][
            RunDetailsConstants.PROCESS_COUNT]
        node_count = run_details[RunDetailsConstants.RUN_DEFINITION][RunDetailsConstants.NODE_COUNT]
        return total_process_count // node_count
    except Exception:
        try:
            # in case of MaaS, the number_of_gpu_to_use_finetuning is passed as input to both pipeline and finetune
            # component
            return os.environ["AZUREML_PARAMETER_number_of_gpu_to_use_finetuning"]
        except Exception:
            return UNKNOWN_VALUE
