from __future__ import annotations

import logging
import math
import os
import sys
from collections import OrderedDict
from typing import TYPE_CHECKING, Iterable, Optional, Union

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import torch

from neuralprophet import utils_torch
from neuralprophet.hdays_utils import get_country_holidays
from neuralprophet.logger import ProgressBar

if TYPE_CHECKING:
    from neuralprophet.configure import ConfigEvents, ConfigLaggedRegressors, ConfigSeasonality, Train

log = logging.getLogger("NP.utils")


def save(forecaster, path: str):
    """save a fitted np model to a disk file.

    Parameters
    ----------
        forecaster : np.forecaster.NeuralProphet
            input forecaster that is fitted
        path : str
            path and filename to be saved. filename could be any but suggested to have extension .np.
    Examples
    --------
    After you fitted a model, you may save the model to save_test_model.np
        >>> from neuralprophet import save
        >>> save(forecaster, "test_save_model.np")
    """
    # Remove the Lightning trainer since it does not serialise correcly with torch.save
    attrs_to_remove = ["trainer"]
    removed_attrs = {}
    for attr in attrs_to_remove:
        removed_attrs[attr] = getattr(forecaster, attr)
        setattr(forecaster, attr, None)
    torch.save(forecaster, path)

    # Restore the Lightning trainer
    for attr in attrs_to_remove:
        setattr(forecaster, attr, removed_attrs[attr])


def load(path: str):
    """retrieve a fitted model from a .np file that was saved by save.

    Parameters
    ----------
        path : str
            path and filename to be saved. filename could be any but suggested to have extension .np.

    Returns
    -------
        np.forecaster.NeuralProphet
            previously saved model

    Examples
    --------
    Saved model could be loaded from disk file test_save_model.np
        >>> from neuralprophet import load
        >>> model = load("test_save_model.np")
    """
    m = torch.load(path)
    m.restore_trainer()
    return m


def reg_func_abs(weights):
    """Regularization of weights to induce sparcity

    Parameters
    ----------
        weights : torch.Tensor
            Model weights to be regularized towards zero

    Returns
    -------
        torch.Tensor
            Regularization loss
    """
    return torch.mean(torch.abs(weights)).squeeze()


def reg_func_trend(weights, threshold=None):
    """Regularization of weights to induce sparcity

    Parameters
    ----------
        weights : torch.Tensor
            Model weights to be regularized towards zero
        threshold : float
            Value below which not to regularize weights

    Returns
    -------
        torch.Tensor
            regularization loss
    """
    # weights dimensions:
    # local: quantiles, num_time_series, segments + 1
    # global: quantiles, segments + 1
    # we do the average of all the sum of weights per time series and per quantile. equivalently
    abs_weights = torch.abs(weights)
    if threshold is not None and not math.isclose(threshold, 0):
        abs_weights = torch.clamp(abs_weights - threshold, min=0.0)
    reg = torch.mean(torch.sum(abs_weights, dim=-1)).squeeze()
    return reg


def reg_func_season(weights):
    return reg_func_abs(weights)


def _regularize_weights(weights, reg_lambda):
    """
    Regularization of weights

    Parameters
    ----------
        weights : torch.Tensor
            Model weights to be regularized towards zero
        reg_lambda : float
            Regularization strength

    Returns
    -------
        torch.Tensor
            Regularization loss
    """
    reg_loss = 0.0
    if reg_lambda is not None:
        for offset in weights.keys():
            reg_loss += reg_lambda * reg_func_abs(weights[offset])
    return reg_loss


def reg_func_events(config_events: Optional[ConfigEvents], config_country_holidays, model):
    """
    Regularization of events coefficients to induce sparcity

    Parameters
    ----------
        config_events : configure.ConfigEvents
            Configurations (upper, lower windows, regularization) for user specified events
        config_country_holidays : configure.ConfigCountryHolidays
            Configurations (holiday_names, upper, lower windows, regularization)
            for country specific holidays
        model : TimeNet
            The TimeNet model object

    Returns
    -------
        scalar
            Regularization loss
    """

    reg_events_loss = 0.0
    if config_events is not None:
        for event, configs in config_events.items():
            reg_events_loss += _regularize_weights(model.get_event_weights(event), configs.reg_lambda)

    if config_country_holidays is not None:
        for holiday in config_country_holidays.holiday_names:
            reg_events_loss += _regularize_weights(model.get_event_weights(holiday), config_country_holidays.reg_lambda)

    return reg_events_loss


def reg_func_covariates(config_lagged_regressors: ConfigLaggedRegressors, model):
    """
    Regularization of lagged covariates to induce sparsity

    Parameters
    ----------
        config_lagged_regressors : configure.ConfigLaggedRegressors
            Configurations for lagged regressors
        model : TimeNet
            TimeNet model object

    Returns
    -------
        scalar
            Regularization loss
    """
    reg_covariate_loss = 0.0
    weights = model.get_covar_weights()
    for covariate, configs in config_lagged_regressors.items():
        reg_lambda = configs.reg_lambda
        if reg_lambda is not None:
            loss = torch.mean(utils_torch.penalize_nonzero(weights[covariate])).squeeze()
            reg_covariate_loss += reg_lambda * loss

    return reg_covariate_loss


def reg_func_regressors(config_regressors, model):
    """
    Regularization of regressors coefficients to induce sparsity

    Parameters
    ----------
        config_regressors : configure.ConfigFutureRegressors
            Configurations for user specified regressors
        model : TimeNet
            TimeNet model object

    Returns
    -------
        scalar
            Regularization loss
    """
    reg_regressor_loss = 0.0
    for regressor, configs in config_regressors.items():
        reg_lambda = configs.reg_lambda
        if reg_lambda is not None:
            weight = model.future_regressors.get_reg_weights(regressor)
            reg_regressor_loss += reg_lambda * reg_func_abs(weight)

    return reg_regressor_loss


def check_for_regularization(configs: list):
    """
    Check if any regularization is specified in the configs

    Parameters
    ----------
        configs : list
            List of configurations

    Returns
    -------
        bool
            True if any regularization is specified
    """
    reg_sum = 0
    for config in [c for c in configs if c is not None]:
        if hasattr(config, "reg_lambda"):
            if config.reg_lambda is not None:
                reg_sum += config.reg_lambda
    return reg_sum > 0


def symmetric_total_percentage_error(values, estimates):
    """Compute STPE

    Parameters
    ----------
        values : np.array
            Input values
        estimates : np.array
            Respective estimates of input values

    Returns
    -------
        float
            Symmetric total percentage error
    """
    sum_abs_diff = np.sum(np.abs(estimates - values))
    sum_abs = np.sum(np.abs(estimates) + np.abs(values))
    return 100 * sum_abs_diff / (10e-9 + sum_abs)


def config_seasonality_to_model_dims(config_seasonality: ConfigSeasonality):
    """Convert the NeuralProphet seasonal model configuration to input dims for TimeNet model.

    Parameters
    ----------
        config_seasonality : configure.ConfigSeasonality
            NeuralProphet seasonal model configuration

    Returns
    -------
        dict(int)
            Input dims for TimeNet model
    """
    if config_seasonality is None or len(config_seasonality.periods) < 1:
        return None
    seasonal_dims = OrderedDict({})
    for name, period in config_seasonality.periods.items():
        resolution = period.resolution
        if config_seasonality.computation == "fourier":
            resolution = 2 * resolution
        seasonal_dims[name] = resolution
    return seasonal_dims


def get_holidays_from_country(country: Union[str, Iterable[str]], df=None):
    """
    Return all possible holiday names of given country

    Parameters
    ----------
        country : str, list
            List of country names to retrieve country specific holidays
        df : pd.Dataframe
            Dataframe from which datestamps will be retrieved from

    Returns
    -------
        set
            All possible holiday names of given country
    """
    if df is None:
        years = np.arange(1995, 2045)
    else:
        dates = df["ds"].copy(deep=True)
        years = list({x.year for x in dates})
    # support multiple countries
    if isinstance(country, str):
        country = [country]

    holidays = {}
    for single_country in country:
        holidays_country = get_country_holidays(single_country, years)
        # only add holiday if it is not already in the dict
        holidays.update(holidays_country)
    holiday_names = holidays.values()
    return set(holiday_names)


def config_events_to_model_dims(config_events: Optional[ConfigEvents], config_country_holidays):
    """
    Convert user specified events configurations along with country specific
        holidays to input dims for TimeNet model.

    Parameters
    ----------
        config_events : configure.ConfigEvents
            Configurations (upper, lower windows, regularization) for user specified events
        config_country_holidays : configure.ConfigCountryHolidays
            Configurations (holiday_names, upper, lower windows, regularization) for country specific holidays

    Returns
    -------
        OrderedDict
            input dims for TimeNet model

            Note
            ----

            This dictionaries' keys correspond to individual holidays and contains configs such as the mode,
            list of event delims of the event corresponding to the offsets and
            indices in the input dataframe corresponding to each event.
    """
    if config_events is None and config_country_holidays is None:
        return None
    additive_events_dims = pd.DataFrame(columns=["event", "event_delim"])
    multiplicative_events_dims = pd.DataFrame(columns=["event", "event_delim"])

    if config_events is not None:
        for event, configs in config_events.items():
            mode = configs.mode
            for offset in range(configs.lower_window, configs.upper_window + 1):
                event_delim = create_event_names_for_offsets(event, offset)
                if mode == "additive":
                    additive_events_dims = pd.concat(
                        [
                            additive_events_dims,
                            pd.DataFrame([{"event": event, "event_delim": event_delim}]),
                        ],
                        ignore_index=True,
                    )
                else:
                    multiplicative_events_dims = pd.concat(
                        [multiplicative_events_dims, pd.DataFrame([{"event": event, "event_delim": event_delim}])],
                        ignore_index=True,
                    )

    if config_country_holidays is not None:
        lower_window = config_country_holidays.lower_window
        upper_window = config_country_holidays.upper_window
        mode = config_country_holidays.mode
        for country_holiday in config_country_holidays.holiday_names:
            for offset in range(lower_window, upper_window + 1):
                holiday_delim = create_event_names_for_offsets(country_holiday, offset)
                if mode == "additive":
                    additive_events_dims = pd.concat(
                        [
                            additive_events_dims,
                            pd.DataFrame([{"event": country_holiday, "event_delim": holiday_delim}]),
                        ],
                        ignore_index=True,
                    )
                else:
                    multiplicative_events_dims = pd.concat(
                        [
                            multiplicative_events_dims,
                            pd.DataFrame([{"event": country_holiday, "event_delim": holiday_delim}]),
                        ],
                        ignore_index=True,
                    )

    # sort based on event_delim
    event_dims = pd.DataFrame()
    if not additive_events_dims.empty:
        additive_events_dims = additive_events_dims.sort_values(by="event_delim").reset_index(drop=True)
        additive_events_dims["mode"] = "additive"
        event_dims = additive_events_dims

    if not multiplicative_events_dims.empty:
        multiplicative_events_dims = multiplicative_events_dims.sort_values(by="event_delim").reset_index(drop=True)
        multiplicative_events_dims["mode"] = "multiplicative"
        event_dims = pd.concat([event_dims, multiplicative_events_dims])

    event_dims_dic = OrderedDict({})
    # convert to dict format
    for event, row in event_dims.groupby("event"):
        event_dims_dic[event] = {
            "mode": row["mode"].iloc[0],
            "event_delim": list(row["event_delim"]),
            "event_indices": list(row.index),
        }
    return event_dims_dic


def create_event_names_for_offsets(event_name, offset):
    """
    Create names for offsets of every event

    Parameters
    ----------
        event_name : str
            Name of the event
        offset : int
            Offset of the event

    Returns
    -------
        str
            Name created for the offset of the event
    """
    sign = "+" if offset >= 0 else "-"
    offset_name = f"{event_name}_{sign}{abs(offset)}"
    return offset_name


def config_regressors_to_model_dims(config_regressors):
    """
    Convert the NeuralProphet user specified regressors configurations to input dims for TimeNet model.

    Parameters
    ----------
        config_regressors : configure.ConfigFutureRegressors
            Configurations for user specified regressors

    Returns
    -------
        OrderedDict
            Input dims for TimeNet model.

            Note
            ----

            This dictionaries' keys correspond to individual regressor and values in a dict containing the mode
            and the indices in the input dataframe corresponding to each regressor.
    """
    if config_regressors is None:
        return None
    else:
        additive_regressors = []
        multiplicative_regressors = []

        if config_regressors is not None:
            for regressor, configs in config_regressors.items():
                mode = configs.mode
                if mode == "additive":
                    additive_regressors.append(regressor)
                else:
                    multiplicative_regressors.append(regressor)

        # sort based on event_delim
        regressors_dims = pd.DataFrame()
        if additive_regressors:
            additive_regressors = sorted(additive_regressors)
            additive_regressors_dims = pd.DataFrame(data=additive_regressors, columns=["regressors"])
            additive_regressors_dims["mode"] = "additive"
            regressors_dims = additive_regressors_dims

        if multiplicative_regressors:
            multiplicative_regressors = sorted(multiplicative_regressors)
            multiplicative_regressors_dims = pd.DataFrame(data=multiplicative_regressors, columns=["regressors"])
            multiplicative_regressors_dims["mode"] = "multiplicative"
            regressors_dims = pd.concat([regressors_dims, multiplicative_regressors_dims])

        regressors_dims_dic = OrderedDict({})
        # convert to dict format
        for index, row in regressors_dims.iterrows():
            regressors_dims_dic[row["regressors"]] = {"mode": row["mode"], "regressor_index": index}
        return regressors_dims_dic


def set_auto_seasonalities(df, config_seasonality: ConfigSeasonality):
    """Set seasonalities that were left on auto or set by user.

    Note
    ----
    Turns on yearly seasonality if there is >=2 years of history.

    Turns on weekly seasonality if there is >=2 weeks of history, and the
    spacing between dates in the history is <7 days.

    Turns on daily seasonality if there is >=2 days of history, and the
    spacing between dates in the history is <1 day.

    Parameters
    ----------
        df : pd.Dataframe
            Dataframe from which datestamps will be retrieved from
        config_seasonality : configure.ConfigSeasonality
            NeuralProphet seasonal model configuration, as after __init__
    Returns
    -------
        configure.ConfigSeasonality
            Processed NeuralProphet seasonal model configuration

    """
    dates = df["ds"].copy(deep=True)

    log.debug(f"seasonality config received: {config_seasonality}")
    first = dates.min()
    last = dates.max()
    dt = dates.diff()
    min_dt = dt.iloc[dt.values.nonzero()[0]].min()
    auto_disable = {
        "yearly": last - first < pd.Timedelta(days=730),
        "weekly": ((last - first < pd.Timedelta(weeks=2)) or (min_dt >= pd.Timedelta(weeks=1))),
        "daily": ((last - first < pd.Timedelta(days=2)) or (min_dt >= pd.Timedelta(days=1))),
    }
    for name, period in config_seasonality.periods.items():
        arg = period.arg
        default_resolution = period.resolution
        if arg == "custom":
            continue
        elif arg == "auto":
            resolution = 0
            if auto_disable[name]:
                log.info(
                    f"Disabling {name} seasonality. Run NeuralProphet with "
                    f"{name}_seasonality=True to override this."
                )
            else:
                resolution = default_resolution
        elif arg is True:
            resolution = default_resolution
        elif arg is False:
            resolution = 0
        else:
            resolution = int(arg)
        config_seasonality.periods[name].resolution = resolution

    new_periods = OrderedDict({})
    for name, period in config_seasonality.periods.items():
        if period.resolution > 0:
            new_periods[name] = period
    config_seasonality.periods = new_periods
    config_seasonality = config_seasonality if len(config_seasonality.periods) > 0 else None
    log.debug(f"seasonality config: {config_seasonality}")
    return config_seasonality


def print_epoch_metrics(metrics, val_metrics=None, e=0):
    if val_metrics is not None and len(val_metrics) > 0:
        val = OrderedDict({f"{key}_val": value for key, value in val_metrics.items()})
        metrics = {**metrics, **val}
    metrics_df = pd.DataFrame(
        {
            **metrics,
        },
        index=[e + 1],
    )
    metrics_string = metrics_df.to_string(float_format=lambda x: f"{x:6.3f}")
    return metrics_string


def fcst_df_to_latest_forecast(fcst, quantiles, n_last=1):
    """Converts from line-per-lag to line-per-forecast.

    Parameters
    ----------
        fcst : pd.DataFrame
            Forecast df
        quantiles : list, default None
            A list of float values between (0, 1) which indicate the set of quantiles to be estimated.
        n_last : int
            Number of latest forecasts to include

    Returns
    -------
        pd.DataFrame
            Dataframe where origin-0 is latest forecast, origin-1 second to latest etc
    """
    cols = ["ds", "y"]  # cols to keep from df
    df = pd.concat((fcst[cols],), axis=1)
    df.reset_index(drop=True, inplace=True)

    yhat_col_names = [
        col_name for col_name in fcst.columns if "yhat" in col_name and "%" not in col_name and "qhat" not in col_name
    ]
    yhat_col_names_quants = [col_name for col_name in fcst.columns if "yhat" in col_name and "%" in col_name]
    n_forecast_steps = len(yhat_col_names)
    yhats = pd.concat((fcst[yhat_col_names],), axis=1)
    yhats_quants = pd.concat((fcst[yhat_col_names_quants],), axis=1)
    cols = list(range(n_forecast_steps))
    for i in range(n_last - 1, -1, -1):
        forecast_name = f"origin-{i}"
        df[forecast_name] = None
        rows = len(df) + np.arange(-n_forecast_steps - i, -i, 1)
        last = yhats.values[rows, cols]
        df.loc[rows, forecast_name] = last
        startcol = 0
        endcol = n_forecast_steps
        for quantile_idx in range(1, len(quantiles)):
            yhats_quants_split = yhats_quants.iloc[
                :, startcol:endcol
            ]  # split yhats_quants to consider one quantile at a time
            forecast_name_quants = "origin-{} {}%".format((i), quantiles[quantile_idx] * 100)
            df[forecast_name_quants] = None
            rows = len(df) + np.arange(-n_forecast_steps - i, -i, 1)
            last = yhats_quants_split.values[rows, cols]
            df.loc[rows, forecast_name_quants] = last
            startcol += n_forecast_steps
            endcol += n_forecast_steps
    return df


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def set_random_seed(seed: int = 0):
    """Sets the random number generator to a fixed seed.

    Parameters
    ----------

    seed : numeric
        Seed value for random number generator

    Note
    ----
    This needs to be set each time before fitting the model.

    Example
    -------
    >>> from neuralprophet import set_random_seed
    >>> set_random_seed(seed=42)
    """
    np.random.seed(seed)
    torch.manual_seed(seed)


def set_logger_level(logger, log_level, include_handlers=False):
    if log_level is None:
        logger.error("Failed to set log_level to None.")
    elif log_level not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", 10, 20, 30, 40, 50):
        logger.error(
            f"Failed to set log_level to {log_level}."
            "Please specify a valid log level from: "
            "'DEBUG', 'INFO', 'WARNING', 'ERROR' or 'CRITICAL'"
        )
    else:
        logger.setLevel(log_level)
        if include_handlers:
            for h in log.handlers:
                h.setLevel(log_level)
        logger.debug(f"Set log level to {log_level}")


def set_log_level(log_level: str = "INFO", include_handlers: bool = False):
    """Set the log level of all logger objects

    Parameters
    ----------
        log_level : str
            The log level of the logger objects used for printing procedure status
            updates for debugging/monitoring. Should be one of ``NOTSET``, ``DEBUG``, ``INFO``, ``WARNING``,
            ``ERROR`` or ``CRITICAL``
        include_handlers : bool
            Include any specified file/stream handlers

    Example
    -------
    >>> from neuralprophet import set_log_level
    >>> set_log_level("ERROR")
    """
    set_logger_level(logging.getLogger("NP"), log_level, include_handlers)


def smooth_loss_and_suggest(lr_finder_results, window=10):
    """
    Smooth loss using a Hamming filter.

    Parameters
    ----------
        loss : np.array
            Loss values

    Returns
    -------
        loss_smoothed : np.array
            Smoothed loss values
        lr: np.array
            Learning rate values
        suggested_lr: float
            Suggested learning rate based on gradient
    """
    lr = lr_finder_results["lr"]
    loss = lr_finder_results["loss"]
    # Derive window size from num lr searches, ensure window is divisible by 2
    half_window = math.ceil(round(len(loss) * 0.1) / 2)
    # Pad sequence and initialialize hamming filter
    loss = np.pad(np.array(loss), pad_width=half_window, mode="edge")
    window = np.hamming(half_window * 2)
    # Convolve the over the loss distribution
    try:
        loss = np.convolve(
            window / window.sum(),
            loss,
            mode="valid",
        )[1:]
    except ValueError:
        log.warning(
            f"The number of loss values ({len(loss)}) is too small to apply smoothing with a the window size of "
            f"{window}."
        )
    # Suggest the lr with steepest negative gradient
    try:
        # Find the steepest gradient and the minimum loss after that
        suggestion = lr[np.argmin(np.gradient(loss))]
    except ValueError:
        log.error(
            f"The number of loss values ({len(loss)}) is too small to estimate a learning rate. Increase the number of "
            "samples or manually set the learning rate."
        )
        raise
    return (loss, lr, suggestion)


def _smooth_loss(loss, beta=0.9):
    smoothed_loss = np.zeros_like(loss)
    smoothed_loss[0] = loss[0]
    for i in range(1, len(loss)):
        smoothed_loss[i] = smoothed_loss[i - 1] * beta + (1 - beta) * loss[i]
    return smoothed_loss


def configure_trainer(
    config_train: Train,
    config: dict,
    metrics_logger,
    early_stopping: bool = False,
    early_stopping_target: str = "Loss",
    accelerator: Optional[str] = None,
    progress_bar_enabled: bool = True,
    metrics_enabled: bool = False,
    checkpointing_enabled: bool = False,
    num_batches_per_epoch: int = 100,
):
    """
    Configures the PyTorch Lightning trainer.

    Parameters
    ----------
        config_train : Dict
            dictionary containing the overall training configuration.
        config : dict
            dictionary containing the custom PyTorch Lightning trainer configuration.
        metrics_logger : MetricsLogger
            MetricsLogger object to log metrics to.
        early_stopping: bool
            If True, early stopping is enabled.
        early_stopping_target : str
            Target metric to use for early stopping.
        accelerator : str
            Accelerator to use for training.
        progress_bar_enabled : bool
            If False, no progress bar is shown.
        metrics_enabled : bool
            If False, no metrics are logged. Calculating metrics is computationally expensive and reduces the training
            speed.
        checkpointing_enabled : bool
            If False, no checkpointing is performed. Checkpointing reduces the training speed.
        num_batches_per_epoch : int
            Number of batches per epoch.

    Returns
    -------
        pl.Trainer
            PyTorch Lightning trainer
        checkpoint_callback
            PyTorch Lightning checkpoint callback to load the best model
    """
    config = config.copy()

    # Enable Learning rate finder if not learning rate provided
    if config_train.learning_rate is None:
        config["auto_lr_find"] = True

    # Set max number of epochs
    if hasattr(config_train, "epochs"):
        if config_train.epochs is not None:
            config["max_epochs"] = config_train.epochs

    # Configure the Ligthing-logs directory
    if "default_root_dir" not in config.keys():
        config["default_root_dir"] = os.getcwd()

    # Accelerator
    if isinstance(accelerator, str):
        if (accelerator == "auto" and torch.cuda.is_available()) or accelerator == "gpu":
            config["accelerator"] = "gpu"
            config["devices"] = -1
        elif (accelerator == "auto" and hasattr(torch.backends, "mps")) or accelerator == "mps":
            if torch.backends.mps.is_available():
                config["accelerator"] = "mps"
                config["devices"] = 1
        elif accelerator != "auto":
            config["accelerator"] = accelerator
            config["devices"] = 1

        if "accelerator" in config:
            log.info(f"Using accelerator {config['accelerator']} with {config['devices']} device(s).")
        else:
            log.info("No accelerator available. Using CPU for training.")

    # Configure metrics
    if metrics_enabled:
        config["logger"] = metrics_logger
    else:
        config["logger"] = False

    # Configure callbacks
    callbacks = []
    has_custom_callbacks = True if "callbacks" in config else False

    # Configure checkpointing
    has_modelcheckpoint_callback = (
        True
        if has_custom_callbacks
        and any(isinstance(callback, pl.callbacks.ModelCheckpoint) for callback in config["callbacks"])
        else False
    )
    if has_modelcheckpoint_callback and not checkpointing_enabled:
        raise ValueError(
            "Checkpointing is disabled but a ModelCheckpoint callback is provided. Please enable checkpointing or "
            "remove the callback."
        )
    if checkpointing_enabled:
        if not has_modelcheckpoint_callback:
            # Callback to access both the last and best model
            checkpoint_callback = pl.callbacks.ModelCheckpoint(
                monitor=early_stopping_target, mode="min", save_top_k=1, save_last=True
            )
            callbacks.append(checkpoint_callback)
        else:
            checkpoint_callback = next(
                callback for callback in config["callbacks"] if isinstance(callback, pl.callbacks.ModelCheckpoint)
            )
    else:
        config["enable_checkpointing"] = False
        checkpoint_callback = None

    # Configure the progress bar, refresh every epoch
    has_progressbar_callback = (
        True
        if has_custom_callbacks
        and any(isinstance(callback, pl.callbacks.ProgressBarBase) for callback in config["callbacks"])
        else False
    )
    if has_progressbar_callback and not progress_bar_enabled:
        raise ValueError(
            "Progress bar is disabled but a ProgressBar callback is provided. Please enable the progress bar or remove"
            " the callback."
        )
    if progress_bar_enabled:
        if not has_progressbar_callback:
            prog_bar_callback = ProgressBar(refresh_rate=num_batches_per_epoch, epochs=config_train.epochs)
            callbacks.append(prog_bar_callback)
    else:
        config["enable_progress_bar"] = False

    # Early stopping monitor
    has_earlystopping_callback = (
        True
        if has_custom_callbacks
        and any(isinstance(callback, pl.callbacks.EarlyStopping) for callback in config["callbacks"])
        else False
    )
    if has_earlystopping_callback and not early_stopping:
        raise ValueError(
            "Early stopping is disabled but an EarlyStopping callback is provided. Please enable early stopping or "
            "remove the callback."
        )
    if early_stopping:
        if not metrics_enabled:
            raise ValueError("Early stopping requires metrics to be enabled.")
        if not has_earlystopping_callback:
            early_stop_callback = pl.callbacks.EarlyStopping(
                monitor=early_stopping_target, mode="min", patience=20, divergence_threshold=5.0
            )
            callbacks.append(early_stop_callback)

    if has_custom_callbacks:
        config["callbacks"].extend(callbacks)
    else:
        config["callbacks"] = callbacks
    config["num_sanity_val_steps"] = 0
    config["enable_model_summary"] = False
    # TODO: Disabling sampler_ddp brings a good speedup in performance, however, check whether this is a good idea
    # https://pytorch-lightning.readthedocs.io/en/stable/common/trainer.html#replace-sampler-ddp
    # config["replace_sampler_ddp"] = False

    return pl.Trainer(**config), checkpoint_callback
