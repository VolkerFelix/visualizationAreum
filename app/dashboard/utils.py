import pandas as pd
import numpy as np
from datetime import datetime


def process_acceleration_data(dataset):
    """Process acceleration data for visualization and metrics"""
    # Extract samples
    samples = dataset.get("data", {}).get("samples", [])

    if not samples:
        # Return empty dataframe if no samples
        return pd.DataFrame(columns=["index", "timestamp", "x", "y", "z", "magnitude"])

    # Convert to DataFrame
    df = pd.DataFrame(samples)

    # Convert timestamps to datetime objects
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Sort by timestamp
    df = df.sort_values("timestamp")

    # Add index for x-axis
    df["index"] = range(len(df))

    # Calculate magnitude
    df["magnitude"] = np.sqrt(df["x"] ** 2 + df["y"] ** 2 + df["z"] ** 2)

    return df


def calculate_metrics(df):
    """Calculate activity metrics from processed dataframe"""
    if df.empty:
        return {
            "avg_intensity": 0,
            "duration": 0,
            "active_samples": 0,
            "peak_magnitude": 0,
        }

    # Calculate metrics
    gravity_offset = 1.0  # Earth's gravity is approximately 1.0g

    avg_magnitude = df["magnitude"].mean()
    peak_magnitude = df["magnitude"].max()

    # Calculate intensity as percentage
    avg_intensity = min(max(0, (avg_magnitude - gravity_offset) / 0.5), 1.0) * 100

    # Calculate duration in minutes
    duration_ms = (df["timestamp"].max() - df["timestamp"].min()).total_seconds() * 1000
    duration_min = duration_ms / (1000 * 60)

    # Calculate active samples (movement above threshold)
    active_threshold = 0.2
    active_samples = df[abs(df["magnitude"] - gravity_offset) > active_threshold].shape[
        0
    ]

    return {
        "avg_intensity": avg_intensity,
        "duration": round(duration_min, 1),
        "active_samples": active_samples,
        "peak_magnitude": round(peak_magnitude, 2),
    }
