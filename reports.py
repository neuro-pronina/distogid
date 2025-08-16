"""Report generation utilities."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(patient_id: str, df: pd.DataFrame, output_path: Path) -> None:
    """Create a simple PDF report with summary statistics."""
    c = canvas.Canvas(str(output_path), pagesize=A4)
    c.setTitle("Distogid Report")
    c.drawString(50, 800, "Отчёт Distogid")
    c.drawString(50, 780, f"ID пациента: {patient_id}")
    c.drawString(50, 760, f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.drawString(50, 730, "Результаты анализа (средние значения):")
    stats = df[["yaw", "pitch", "roll"]].mean()
    for i, (col, value) in enumerate(stats.items()):
        c.drawString(70, 710 - i * 20, f"{col}: {value:.2f}")

    c.showPage()
    c.save()


__all__ = ["generate_pdf"]
