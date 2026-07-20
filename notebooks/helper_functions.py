"""Wiederverwendbare Hilfsfunktionen fuer PyTorch-Regressionsmodelle."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import torch
from torch import nn
from torch.utils.data import DataLoader


def get_torch_device() -> torch.device:
    """Waehlt MPS, CUDA oder CPU in dieser Reihenfolge aus."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def load_model_from_checkpoint(
    model_class: type[nn.Module],
    checkpoint_path: str | Path,
    *,
    device: torch.device | str | None = None,
    model_kwargs: Mapping[str, Any] | None = None,
) -> tuple[nn.Module, dict[str, Any]]:
    """Laedt einen Checkpoint und rekonstruiert das zugehoerige Modell.

    Falls ``model_kwargs`` nicht angegeben wird, erkennt die Funktion zwei
    Checkpoint-Formate automatisch:

    - Embedding-Modell: ``numeric_input_dim``, ``num_communities`` und
      ``embedding_dim``
    - Legacy-Modell ohne Embedding: ``input_dim``

    ``model_class`` muss jeweils zu der gespeicherten Architektur passen.
    """
    device = torch.device(device) if device is not None else get_torch_device()
    checkpoint_path = Path(checkpoint_path)

    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint nicht gefunden: {checkpoint_path}")

    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
        weights_only=False,
    )

    if "model_state_dict" not in checkpoint:
        raise KeyError("Der Checkpoint enthaelt keinen 'model_state_dict'.")

    if model_kwargs is None and "model_kwargs" in checkpoint:
        model_kwargs = checkpoint["model_kwargs"]

    if model_kwargs is None:
        embedding_keys = (
            "numeric_input_dim",
            "num_communities",
            "embedding_dim",
        )

        if all(key in checkpoint for key in embedding_keys):
            model_kwargs = {key: checkpoint[key] for key in embedding_keys}
        elif "input_dim" in checkpoint:
            model_kwargs = {"input_dim": checkpoint["input_dim"]}
        else:
            raise KeyError(
                "Der Checkpoint enthaelt weder die Parameter eines "
                "Embedding-Modells (numeric_input_dim, num_communities, "
                "embedding_dim) noch den Legacy-Parameter input_dim. "
                "Uebergib die Konstruktorargumente explizit ueber model_kwargs."
            )

    model = model_class(**dict(model_kwargs))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()

    return model, checkpoint


def collect_predictions(
    model: nn.Module,
    data_loader: DataLoader,
    *,
    device: torch.device | str | None = None,
    embedding_input: bool = True,
    inverse_target: Callable[[np.ndarray], np.ndarray] = np.expm1,
    clip_negative_predictions: bool = True,
) -> pl.DataFrame:
    """Erzeugt Predictions und eine Tabelle mit Regressionsfehlern.

    Bei ``embedding_input=True`` muss ein Batch als
    ``(X, community_idx, y, ...)`` aufgebaut sein. Andernfalls wird
    ``(X, y, ...)`` erwartet. Zusaetzliche Batch-Elemente, beispielsweise
    Sample-Gewichte, werden ignoriert.
    """
    device = torch.device(device) if device is not None else get_torch_device()
    model.to(device)
    model.eval()

    y_true_parts: list[np.ndarray] = []
    y_pred_parts: list[np.ndarray] = []

    with torch.inference_mode():
        for batch in data_loader:
            if embedding_input:
                if len(batch) < 3:
                    raise ValueError(
                        "Embedding-Batches muessen mindestens (X, ID, y) enthalten."
                    )
                x_batch, category_batch, y_batch = batch[:3]
                y_pred = model(
                    x_batch.to(device),
                    category_batch.to(device),
                )
            else:
                if len(batch) < 2:
                    raise ValueError("Batches muessen mindestens (X, y) enthalten.")
                x_batch, y_batch = batch[:2]
                y_pred = model(x_batch.to(device))

            y_true_parts.append(y_batch.detach().cpu().numpy().reshape(-1))
            y_pred_parts.append(y_pred.detach().cpu().numpy().reshape(-1))

    if not y_true_parts:
        raise ValueError("Der DataLoader enthaelt keine Batches.")

    y_true = inverse_target(np.concatenate(y_true_parts))
    y_pred = inverse_target(np.concatenate(y_pred_parts))

    if clip_negative_predictions:
        y_pred = np.clip(y_pred, a_min=0, a_max=None)

    return pl.DataFrame({"y_true": y_true, "y_pred": y_pred}).with_columns(
        (pl.col("y_true") - pl.col("y_pred")).alias("residual"),
        (pl.col("y_true") - pl.col("y_pred")).abs().alias("abs_error"),
        ((pl.col("y_true") - pl.col("y_pred")) ** 2).alias("squared_error"),
    )


def compute_regression_metrics(
    evaluation: pl.DataFrame,
    *,
    zero_threshold: float = 0.0,
    peak_quantile: float = 0.90,
) -> pl.DataFrame:
    """Berechnet globale sowie Zero-, Non-Zero- und Peak-Metriken."""
    required_columns = {"y_true", "y_pred"}
    missing = required_columns.difference(evaluation.columns)
    if missing:
        raise ValueError(f"Fehlende Spalten: {', '.join(sorted(missing))}")
    if not 0 < peak_quantile < 1:
        raise ValueError("peak_quantile muss zwischen 0 und 1 liegen.")

    y_true = evaluation["y_true"].to_numpy()
    y_pred = evaluation["y_pred"].to_numpy()
    finite = np.isfinite(y_true) & np.isfinite(y_pred)
    y_true, y_pred = y_true[finite], y_pred[finite]

    if y_true.size == 0:
        raise ValueError("Keine endlichen Beobachtungen fuer die Auswertung vorhanden.")

    errors = y_true - y_pred
    absolute_errors = np.abs(errors)
    squared_errors = errors**2
    zero_mask = y_true <= zero_threshold
    nonzero_mask = ~zero_mask

    def masked_mean(values: np.ndarray, mask: np.ndarray) -> float:
        return float(values[mask].mean()) if mask.any() else float("nan")

    def masked_rmse(values: np.ndarray, mask: np.ndarray) -> float:
        return float(np.sqrt(values[mask].mean())) if mask.any() else float("nan")

    ss_res = squared_errors.sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    if nonzero_mask.any():
        peak_threshold = float(np.quantile(y_true[nonzero_mask], peak_quantile))
        peak_mask = y_true >= peak_threshold
    else:
        peak_threshold = float("nan")
        peak_mask = np.zeros_like(nonzero_mask)

    metrics = {
        "n_samples": float(y_true.size),
        "mae": float(absolute_errors.mean()),
        "mse": float(squared_errors.mean()),
        "rmse": float(np.sqrt(squared_errors.mean())),
        "r2": float(r_squared),
        "mean_residual_true_minus_pred": float(errors.mean()),
        "zero_share": float(zero_mask.mean()),
        "nonzero_share": float(nonzero_mask.mean()),
        "zero_mae": masked_mean(absolute_errors, zero_mask),
        "nonzero_mae": masked_mean(absolute_errors, nonzero_mask),
        "zero_rmse": masked_rmse(squared_errors, zero_mask),
        "nonzero_rmse": masked_rmse(squared_errors, nonzero_mask),
        "peak_threshold": peak_threshold,
        "peak_share": float(peak_mask.mean()),
        "peak_mae": masked_mean(absolute_errors, peak_mask),
        "peak_rmse": masked_rmse(squared_errors, peak_mask),
    }

    return pl.DataFrame({"metric": metrics.keys(), "value": metrics.values()})


def plot_regression_diagnostics(
    evaluation: pl.DataFrame,
    *,
    sample_size: int = 100_000,
    n_bins: int = 50,
    random_seed: int = 42,
) -> tuple[plt.Figure, pl.DataFrame]:
    """Erstellt vier Diagnoseplots und gibt zusaetzlich Bucket-Metriken zurueck."""
    required_columns = {"y_true", "y_pred", "residual", "abs_error"}
    missing = required_columns.difference(evaluation.columns)
    if missing:
        raise ValueError(f"Fehlende Spalten: {', '.join(sorted(missing))}")

    arrays = [evaluation[column].to_numpy() for column in required_columns]
    finite = np.logical_and.reduce([np.isfinite(values) for values in arrays])
    if not finite.any():
        raise ValueError("Keine endlichen Beobachtungen fuer die Plots vorhanden.")

    y_true = evaluation["y_true"].to_numpy()[finite]
    y_pred = evaluation["y_pred"].to_numpy()[finite]
    residual = evaluation["residual"].to_numpy()[finite]
    absolute_error = evaluation["abs_error"].to_numpy()[finite]

    if y_true.size > sample_size:
        rng = np.random.default_rng(random_seed)
        sample = rng.choice(y_true.size, size=sample_size, replace=False)
    else:
        sample = np.arange(y_true.size)

    bucket_order = ["0", "1", "2-3", "4-5", "6-10", "11-20", ">20"]
    bucket_evaluation = (
        pl.DataFrame({"y_true": y_true, "abs_error": absolute_error})
        .with_columns(
            pl.when(pl.col("y_true") == 0).then(pl.lit("0"))
            .when(pl.col("y_true") <= 1).then(pl.lit("1"))
            .when(pl.col("y_true") <= 3).then(pl.lit("2-3"))
            .when(pl.col("y_true") <= 5).then(pl.lit("4-5"))
            .when(pl.col("y_true") <= 10).then(pl.lit("6-10"))
            .when(pl.col("y_true") <= 20).then(pl.lit("11-20"))
            .otherwise(pl.lit(">20"))
            .alias("demand_bucket")
        )
        .group_by("demand_bucket")
        .agg(
            pl.len().alias("n_rows"),
            pl.col("abs_error").mean().alias("mae"),
            pl.col("y_true").mean().alias("avg_y_true"),
        )
        .with_columns(
            pl.col("demand_bucket")
            .replace({label: index for index, label in enumerate(bucket_order)})
            .cast(pl.Int64)
            .alias("bucket_order")
        )
        .sort("bucket_order")
    )

    figure, axes = plt.subplots(2, 2, figsize=(14, 11))

    axes[0, 0].scatter(y_true[sample], y_pred[sample], alpha=0.2, s=8)
    maximum = max(y_true[sample].max(), y_pred[sample].max())
    axes[0, 0].plot([0, maximum], [0, maximum], linestyle="--")
    axes[0, 0].set(title="Actual vs. Predicted", xlabel="Actual", ylabel="Predicted")

    residual_range = np.quantile(residual, [0.01, 0.99])
    axes[0, 1].hist(residual, bins=n_bins, range=tuple(residual_range))
    axes[0, 1].axvline(0, linestyle="--")
    axes[0, 1].set(title="Residuals (1st-99th percentile)", xlabel="y_true - y_pred")

    upper = np.quantile(np.concatenate([y_true, y_pred]), 0.99)
    axes[1, 0].hist(y_true, bins=n_bins, range=(0, upper), alpha=0.5, label="Actual")
    axes[1, 0].hist(y_pred, bins=n_bins, range=(0, upper), alpha=0.5, label="Predicted")
    axes[1, 0].set(title="Target distributions (up to 99th percentile)", xlabel="trip_count")
    axes[1, 0].legend()

    axes[1, 1].bar(
        bucket_evaluation["demand_bucket"].to_list(),
        bucket_evaluation["mae"].to_numpy(),
    )
    axes[1, 1].set(title="MAE by demand bucket", xlabel="Demand bucket", ylabel="MAE")

    for axis in axes.flat:
        axis.grid(True)
    figure.tight_layout()

    return figure, bucket_evaluation


def plot_learning_curves(
    history: pl.DataFrame | Mapping[str, Any] | list[Mapping[str, Any]],
    *,
    best_epoch: int | None = None,
    title: str = "Learning curves",
) -> plt.Figure:
    """Visualisiert Lernkurven eines trainierten Modells.

    Erwartete Spalten sind ``epoch`` und mindestens eine der folgenden:
    ``train_loss``, ``val_loss``, ``val_log_loss``, ``val_mae``,
    ``val_rmse``, ``high_demand_mae`` oder ``selection_score``.

    ``history`` kann eine Polars-Tabelle, ein Dictionary aus Listen oder eine
    Liste von Dictionaries sein. Falls ``best_epoch`` nicht gesetzt ist und
    ein ``selection_score`` existiert, wird dessen Minimum markiert.
    """
    if isinstance(history, pl.DataFrame):
        frame = history
    elif isinstance(history, Mapping):
        frame = pl.DataFrame(history)
    else:
        frame = pl.DataFrame(history)

    if frame.is_empty():
        raise ValueError("Die Trainingshistorie ist leer.")

    if "epoch" not in frame.columns:
        frame = frame.with_row_index("epoch", offset=1)

    loss_columns = [
        column
        for column in ("train_loss", "val_loss", "val_log_loss")
        if column in frame.columns
    ]
    metric_columns = [
        column
        for column in (
            "val_mae",
            "val_rmse",
            "high_demand_mae",
            "selection_score",
        )
        if column in frame.columns
    ]

    if not loss_columns and not metric_columns:
        raise ValueError(
            "Keine unterstuetzte Loss- oder Metrikspalte in der Historie gefunden."
        )

    if best_epoch is None and "selection_score" in frame.columns:
        best_row = frame.drop_nulls("selection_score").sort("selection_score")
        if not best_row.is_empty():
            best_epoch = int(best_row[0, "epoch"])

    figure, axes = plt.subplots(1, 2, figsize=(14, 5))
    epochs = frame["epoch"].to_numpy()

    for column in loss_columns:
        axes[0].plot(epochs, frame[column].to_numpy(), label=column)
    axes[0].set(title="Training and validation loss", xlabel="Epoch", ylabel="Loss")

    for column in metric_columns:
        axes[1].plot(epochs, frame[column].to_numpy(), label=column)
    axes[1].set(title="Validation metrics", xlabel="Epoch", ylabel="Metric value")

    for axis, columns in zip(axes, (loss_columns, metric_columns)):
        if best_epoch is not None:
            axis.axvline(
                best_epoch,
                color="black",
                linestyle="--",
                alpha=0.7,
                label=f"best epoch ({best_epoch})",
            )
        axis.grid(True, alpha=0.3)
        if columns or best_epoch is not None:
            axis.legend()

    figure.suptitle(title)
    figure.tight_layout()
    return figure


def analyze_training_history(
    history_path: str | Path,
    *,
    best_metric: str | None = None,
    title: str | None = None,
    show: bool = True,
    print_summary: bool = True,
) -> dict[str, Any]:
    """Laedt und analysiert eine als Parquet gespeicherte Trainingshistorie.

    Die Funktion bestimmt die beste Epoche, erstellt eine kompakte Summary und
    visualisiert die vorhandenen Loss- und Validierungsmetriken mit
    :func:`plot_learning_curves`.

    Falls ``best_metric`` nicht angegeben wird, wird die erste vorhandene
    Metrik aus dieser Reihenfolge verwendet: ``selection_score``, ``val_mae``,
    ``val_loss``, ``val_log_loss``, ``val_rmse`` und ``train_loss``. Für diese
    Metriken gilt jeweils: kleiner ist besser.

    Parameters
    ----------
    history_path:
        Pfad zur Parquet-Datei der Trainingshistorie.
    best_metric:
        Optionale Spalte, anhand derer die beste Epoche bestimmt wird.
    title:
        Optionale Überschrift der Lernkurven. Standardmäßig wird der Dateiname
        verwendet.
    show:
        Zeigt die Abbildung direkt mit ``plt.show()`` an.
    print_summary:
        Gibt Pfad, Auswahlmetrik und Summary-Tabelle aus.

    Returns
    -------
    dict
        Enthält ``history_df``, ``summary_df``, ``figure``, ``best_epoch``,
        ``best_metric`` und ``best_value``.

    Examples
    --------
    >>> analysis = analyze_training_history(
    ...     MODEL_PATH / "advanced_v7_community_areas_4h_training_history.parquet"
    ... )
    >>> analysis["summary_df"]
    """
    history_path = Path(history_path)
    if not history_path.exists():
        raise FileNotFoundError(f"Trainingshistorie nicht gefunden: {history_path}")
    if history_path.suffix.lower() != ".parquet":
        raise ValueError(
            "Die Trainingshistorie muss als Parquet-Datei vorliegen: "
            f"{history_path}"
        )

    history_df = pl.read_parquet(history_path)
    if history_df.is_empty():
        raise ValueError(f"Die Trainingshistorie ist leer: {history_path}")
    if "epoch" not in history_df.columns:
        history_df = history_df.with_row_index("epoch", offset=1)
    history_df = history_df.sort("epoch")

    metric_priority = (
        "selection_score",
        "val_mae",
        "val_loss",
        "val_log_loss",
        "val_rmse",
        "train_loss",
    )
    if best_metric is None:
        best_metric = next(
            (metric for metric in metric_priority if metric in history_df.columns),
            None,
        )
    elif best_metric not in history_df.columns:
        raise ValueError(
            f"Auswahlmetrik '{best_metric}' fehlt. "
            f"Verfügbare Spalten: {', '.join(history_df.columns)}"
        )
    if best_metric is None:
        raise ValueError(
            "Keine unterstützte Metrik zur Bestimmung der besten Epoche gefunden."
        )

    valid_metric_rows = history_df.filter(
        pl.col(best_metric).is_not_null() & pl.col(best_metric).is_finite()
    )
    if valid_metric_rows.is_empty():
        raise ValueError(f"Auswahlmetrik '{best_metric}' enthält keine endlichen Werte.")

    best_row = valid_metric_rows.sort(best_metric).row(0, named=True)
    final_row = history_df.row(-1, named=True)
    best_epoch = int(best_row["epoch"])
    best_value = float(best_row[best_metric])

    summary_rows: list[dict[str, Any]] = [
        {"metric": "epochs_trained", "value": float(history_df.height)},
        {"metric": "best_epoch", "value": float(best_epoch)},
        {"metric": f"best_{best_metric}", "value": best_value},
    ]
    summary_columns = (
        "train_loss",
        "val_loss",
        "val_log_loss",
        "val_mae",
        "val_rmse",
        "high_demand_mae",
        "selection_score",
        "learning_rate",
    )
    for metric in summary_columns:
        if metric not in history_df.columns:
            continue
        best_row_value = best_row.get(metric)
        final_row_value = final_row.get(metric)
        if best_row_value is not None:
            summary_rows.append(
                {"metric": f"{metric}_at_best_epoch", "value": float(best_row_value)}
            )
        if final_row_value is not None:
            summary_rows.append(
                {"metric": f"final_{metric}", "value": float(final_row_value)}
            )

    summary_df = pl.DataFrame(summary_rows)
    figure = plot_learning_curves(
        history_df,
        best_epoch=best_epoch,
        title=title or history_path.stem,
    )

    if print_summary:
        print(f"Training history: {history_path}")
        print(f"Best metric: {best_metric} (minimum)")
        print(summary_df)
    if show:
        plt.show()

    return {
        "history_df": history_df,
        "summary_df": summary_df,
        "figure": figure,
        "best_epoch": best_epoch,
        "best_metric": best_metric,
        "best_value": best_value,
    }
