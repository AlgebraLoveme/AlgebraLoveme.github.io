#!/usr/bin/env python3
"""Approximate maximin point configurations on a Euclidean unit sphere.

For K points on S^(N-1), the objective is the smallest pairwise Euclidean
distance. Exact Rankin values are used when K <= 2N (and for every K when
N == 2). Remaining cases are reproducible heuristic lower bounds obtained by
projected gradient optimization of a smooth maximum pairwise inner product.

The script writes a CSV table and a publication-ready PNG summary.
"""

from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class Result:
    dimension: int
    points: int
    distance: float
    median_restart_distance: float
    restart_spread: float
    method: str
    seed: int


def parse_int_list(value: str) -> list[int]:
    values = sorted({int(item.strip()) for item in value.split(",") if item.strip()})
    if not values:
        raise argparse.ArgumentTypeError("expected a comma-separated integer list")
    return values


def exact_rankin_distance(dimension: int, points: int) -> tuple[float, str] | None:
    """Return the exact spherical-code distance in the elementary Rankin regimes."""
    if dimension < 2:
        raise ValueError("dimension must be at least 2")
    if points < 2:
        raise ValueError("point count must be at least 2")

    if dimension == 2:
        return 2.0 * math.sin(math.pi / points), "exact: regular polygon"
    if points <= dimension + 1:
        return math.sqrt(2.0 * points / (points - 1)), "exact: regular simplex"
    if points <= 2 * dimension:
        return math.sqrt(2.0), "exact: cross-polytope subset"
    return None


def optimize_spherical_code(
    dimension: int,
    points: int,
    *,
    restarts: int,
    steps: int,
    learning_rate: float,
    temperature_start: float,
    temperature_end: float,
    seed: int,
    device: str,
) -> tuple[float, float, float]:
    """Return best, median, and spread across projected-gradient restarts."""
    import torch
    import torch.nn.functional as functional

    if restarts < 1 or steps < 1:
        raise ValueError("restarts and steps must be positive")
    if not 0 < temperature_end <= temperature_start:
        raise ValueError("temperatures must satisfy 0 < end <= start")

    torch.manual_seed(seed)
    if device.startswith("cuda"):
        torch.cuda.manual_seed_all(seed)

    raw = torch.randn(
        restarts,
        points,
        dimension,
        dtype=torch.float32,
        device=device,
    )
    raw = torch.nn.Parameter(functional.normalize(raw, dim=-1))
    optimizer = torch.optim.Adam([raw], lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=steps,
        eta_min=learning_rate * 0.05,
    )
    pair_i, pair_j = torch.triu_indices(points, points, offset=1, device=device)
    best_by_restart = torch.zeros(restarts, dtype=torch.float32, device=device)

    for step in range(steps):
        fraction = step / max(steps - 1, 1)
        temperature = temperature_start * (
            temperature_end / temperature_start
        ) ** fraction

        vectors = functional.normalize(raw, dim=-1)
        gram = vectors @ vectors.transpose(-1, -2)
        pair_inner_products = gram[:, pair_i, pair_j]
        smooth_max = temperature * torch.logsumexp(
            pair_inner_products / temperature,
            dim=1,
        )
        loss = smooth_max.mean()
        if not torch.isfinite(loss):
            raise RuntimeError(
                f"non-finite loss for N={dimension}, K={points}, step={step}"
            )

        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        scheduler.step()

        with torch.no_grad():
            raw.copy_(functional.normalize(raw, dim=-1))
            max_inner_product = pair_inner_products.max(dim=1).values
            distances = torch.sqrt(
                torch.clamp(2.0 - 2.0 * max_inner_product, min=0.0)
            )
            best_by_restart = torch.maximum(best_by_restart, distances)

    values = best_by_restart.detach().cpu().numpy()
    return float(values.max()), float(np.median(values)), float(values.max() - values.min())


def choose_device(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import torch

        return "cuda" if torch.cuda.is_available() else "cpu"
    except ImportError:
        return "cpu"


def run_grid(args: argparse.Namespace) -> list[Result]:
    device = choose_device(args.device)
    print(f"device={device}")
    results: list[Result] = []

    for points in args.points:
        for dimension in args.dimensions:
            case_seed = args.seed + 1009 * dimension + 9176 * points
            exact = exact_rankin_distance(dimension, points)
            if exact is not None:
                distance, method = exact
                median = distance
                spread = 0.0
            else:
                distance, median, spread = optimize_spherical_code(
                    dimension,
                    points,
                    restarts=args.restarts,
                    steps=args.steps,
                    learning_rate=args.learning_rate,
                    temperature_start=args.temperature_start,
                    temperature_end=args.temperature_end,
                    seed=case_seed,
                    device=device,
                )
                method = "heuristic: smooth-max projected gradient"

            result = Result(
                dimension=dimension,
                points=points,
                distance=distance,
                median_restart_distance=median,
                restart_spread=spread,
                method=method,
                seed=case_seed,
            )
            results.append(result)
            print(
                f"N={dimension:3d} K={points:3d} "
                f"d={distance:.6f} spread={spread:.6f} {method}",
                flush=True,
            )
    return results


def write_csv(results: list[Result], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            lineterminator="\n",
            fieldnames=[
                "dimension",
                "points",
                "distance",
                "median_restart_distance",
                "restart_spread",
                "method",
                "seed",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(
                {
                    "dimension": result.dimension,
                    "points": result.points,
                    "distance": f"{result.distance:.9f}",
                    "median_restart_distance": (
                        f"{result.median_restart_distance:.9f}"
                    ),
                    "restart_spread": f"{result.restart_spread:.9f}",
                    "method": result.method,
                    "seed": result.seed,
                }
            )


def plot_results(
    results: list[Result],
    dimensions: list[int],
    point_counts: list[int],
    path: Path,
    *,
    restarts: int,
) -> None:
    lookup = {(r.dimension, r.points): r for r in results}
    distances = np.array(
        [[lookup[(dimension, points)].distance for dimension in dimensions]
         for points in point_counts]
    )
    exact = np.array(
        [[lookup[(dimension, points)].method.startswith("exact")
          for dimension in dimensions]
         for points in point_counts]
    )

    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "figure.facecolor": "#f8fafc",
            "axes.facecolor": "#ffffff",
        }
    )
    fig, (heatmap_ax, line_ax) = plt.subplots(
        1,
        2,
        figsize=(13.5, 5.4),
        gridspec_kw={"width_ratios": [1.08, 1.0]},
    )

    image = heatmap_ax.imshow(
        distances,
        origin="lower",
        aspect="auto",
        cmap="viridis",
        vmin=0.0,
        vmax=max(1.6, float(distances.max())),
    )
    heatmap_ax.set_title("Best minimum pairwise distance")
    heatmap_ax.set_xlabel("Ambient dimension N")
    heatmap_ax.set_ylabel("Number of points K")
    heatmap_ax.set_xticks(range(len(dimensions)), dimensions)
    heatmap_ax.set_yticks(range(len(point_counts)), point_counts)

    for row, points in enumerate(point_counts):
        for column, dimension in enumerate(dimensions):
            value = distances[row, column]
            suffix = "" if exact[row, column] else "*"
            color = "white" if value < 0.85 or value > 1.35 else "#0f172a"
            heatmap_ax.text(
                column,
                row,
                f"{value:.2f}{suffix}",
                ha="center",
                va="center",
                color=color,
                fontsize=8.5,
                fontweight=600,
            )
    colorbar = fig.colorbar(image, ax=heatmap_ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Euclidean distance on the unit sphere")

    colors = plt.cm.viridis(np.linspace(0.08, 0.92, len(dimensions)))
    for color, dimension in zip(colors, dimensions):
        dimension_results = [lookup[(dimension, points)] for points in point_counts]
        exact_x = [r.points for r in dimension_results if r.method.startswith("exact")]
        exact_y = [r.distance for r in dimension_results if r.method.startswith("exact")]
        heuristic_x = [
            r.points for r in dimension_results if not r.method.startswith("exact")
        ]
        heuristic_y = [
            r.distance for r in dimension_results if not r.method.startswith("exact")
        ]
        line_ax.plot(
            point_counts,
            [r.distance for r in dimension_results],
            color=color,
            linewidth=1.5,
            alpha=0.6,
        )
        if exact_x:
            line_ax.scatter(
                exact_x,
                exact_y,
                color=color,
                s=28,
                marker="o",
                edgecolor="white",
                linewidth=0.6,
            )
        if heuristic_x:
            line_ax.scatter(
                heuristic_x,
                heuristic_y,
                color=color,
                s=36,
                marker="^",
                edgecolor="white",
                linewidth=0.6,
            )
        line_ax.plot([], [], color=color, linewidth=2, label=f"N={dimension}")

    line_ax.set_xscale("log")
    line_ax.set_ylim(bottom=0.0)
    line_ax.set_title("More points force a smaller separation")
    line_ax.set_xlabel("Number of points K (log scale)")
    line_ax.set_ylabel("Minimum pairwise distance")
    line_ax.grid(True, alpha=0.22)
    line_ax.legend(ncol=2, fontsize=8.5, frameon=False)

    fig.suptitle(
        "Maximin point separation on the unit sphere",
        fontsize=16,
        fontweight=700,
        y=1.02,
    )
    fig.text(
        0.5,
        -0.015,
        (
            "Circles and unstarred cells are exact Rankin values; "
            f"triangles and * are heuristic lower bounds (best of {restarts} restarts)."
        ),
        ha="center",
        fontsize=9.5,
        color="#334155",
    )
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dimensions",
        type=parse_int_list,
        default=parse_int_list("2,5,10,20,40,60,80,100"),
        help="comma-separated ambient dimensions",
    )
    parser.add_argument(
        "--points",
        type=parse_int_list,
        default=parse_int_list("5,10,20,40,80,120,160,200"),
        help="comma-separated point counts",
    )
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--steps", type=int, default=1200)
    parser.add_argument("--learning-rate", type=float, default=0.05)
    parser.add_argument("--temperature-start", type=float, default=0.08)
    parser.add_argument("--temperature-end", type=float, default=0.003)
    parser.add_argument("--seed", type=int, default=20260821)
    parser.add_argument(
        "--device",
        default="auto",
        help="PyTorch device, for example auto, cpu, or cuda",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("spherical_code_results.csv"),
    )
    parser.add_argument(
        "--output-figure",
        type=Path,
        default=Path("spherical_code_results.png"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if min(args.dimensions) < 2:
        raise SystemExit("all dimensions must be at least 2")
    if min(args.points) < 2:
        raise SystemExit("all point counts must be at least 2")

    results = run_grid(args)
    write_csv(results, args.output_csv)
    plot_results(
        results,
        args.dimensions,
        args.points,
        args.output_figure,
        restarts=args.restarts,
    )
    print(f"wrote {args.output_csv}")
    print(f"wrote {args.output_figure}")


if __name__ == "__main__":
    main()
