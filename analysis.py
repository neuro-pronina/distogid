"""Video analysis utilities for Distogid."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def _demo_analysis(video_path: Path) -> pd.DataFrame:
    """Generate synthetic head pose data for demo mode."""
    timestamps = np.linspace(0, 10, 100)
    rng = np.random.default_rng(seed=42)
    yaw = rng.normal(0, 5, size=100)
    pitch = rng.normal(0, 5, size=100)
    roll = rng.normal(0, 5, size=100)
    return pd.DataFrame({"time": timestamps, "yaw": yaw, "pitch": pitch, "roll": roll})


def _openface_analysis(video_path: Path, openface_cmd: str) -> pd.DataFrame:
    """Run OpenFace FeatureExtraction and return pose data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = Path(tmpdir) / "out.csv"
        cmd = [openface_cmd, "-f", str(video_path), "-of", str(csv_path)]
        subprocess.run(cmd, check=True, capture_output=True)
        df = pd.read_csv(csv_path)
    # Ensure expected columns exist
    if {"pose_Rx", "pose_Ry", "pose_Rz"}.issubset(df.columns):
        df = df.rename(columns={"pose_Rx": "roll", "pose_Ry": "yaw", "pose_Rz": "pitch"})
        df.insert(0, "time", df.index / 30.0)
        df = df[["time", "yaw", "pitch", "roll"]]
    return df


def analyze_video(video_path: Path, demo: Optional[bool] = None) -> pd.DataFrame:
    """Analyze the video at ``video_path`` and return a DataFrame.

    Parameters
    ----------
    video_path: Path
        Path to the video file to analyze.
    demo: Optional[bool]
        Whether to run in demo mode. If ``None`` (default), the value of
        environment variable ``DISTOGID_DEMO`` is used. ``1`` means demo.
    """

    if demo is None:
        demo = os.getenv("DISTOGID_DEMO", "1") != "0"

    if demo:
        return _demo_analysis(video_path)

    openface_cmd = os.getenv("OPENFACE_CMD", "/opt/OpenFace/build/bin/FeatureExtraction")
    return _openface_analysis(video_path, openface_cmd)


__all__ = ["analyze_video"]
