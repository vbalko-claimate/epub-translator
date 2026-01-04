#!/usr/bin/env python3
"""
PDF Multi-Column Layout Detection

Detects and reorders text blocks for proper reading order in multi-column PDFs.
Uses K-means clustering on x-coordinates to identify columns.

Fixes reading order for:
- Academic papers (2-column)
- Newsletters (2-3 column)
- Technical books (mixed layouts)

Without column detection, text reads jumbled: A → C → B → D
With column detection, text reads correctly: A → B → C → D

Usage:
    from scripts.pdf.layout_detection import detect_columns, reorder_blocks_by_reading_order

    layout = detect_columns(blocks, page_width)
    blocks = reorder_blocks_by_reading_order(blocks, layout)
"""

import sys
from typing import Dict, List


def detect_columns(blocks: List[Dict], page_width: float) -> Dict:
    """
    Detect column layout using K-means clustering on x-coordinates.

    Tries k=1, 2, 3 columns and picks best based on silhouette score.
    Falls back to single column if confidence < 0.7.

    Args:
        blocks: List of text blocks with bbox coordinates
        page_width: Page width in points

    Returns:
        Dictionary with layout metadata:
        {
            "type": "single" | "two_column" | "three_column",
            "columns": [{"x_start": 72, "x_end": 280}, ...],
            "confidence": 0.92,
            "num_columns": 2
        }
    """
    if not blocks:
        return {
            "type": "single",
            "columns": [{"x_start": 0, "x_end": page_width}],
            "confidence": 1.0,
            "num_columns": 1
        }

    try:
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        import numpy as np
    except ImportError:
        # Fallback to single column if sklearn not available
        return {
            "type": "single",
            "columns": [{"x_start": 0, "x_end": page_width}],
            "confidence": 1.0,
            "num_columns": 1
        }

    # Extract x-coordinates (left edge of bboxes)
    x_coords = []
    for block in blocks:
        if "bbox" in block:
            x_coords.append(block["bbox"][0])  # Left edge (x0)

    if not x_coords:
        return {
            "type": "single",
            "columns": [{"x_start": 0, "x_end": page_width}],
            "confidence": 1.0,
            "num_columns": 1
        }

    # Convert to numpy array for sklearn
    X = np.array(x_coords).reshape(-1, 1)

    # Try k=1, 2, 3 and pick best silhouette score
    best_k = 1
    best_score = -1
    best_kmeans = None

    for k in [1, 2, 3]:
        if k > len(x_coords):
            continue  # Can't have more clusters than data points

        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X)

        if k == 1:
            score = 1.0  # Perfect score for single cluster
        else:
            try:
                score = silhouette_score(X, kmeans.labels_)
            except:
                score = -1

        if score > best_score:
            best_score = score
            best_k = k
            best_kmeans = kmeans

    # If confidence too low, fallback to single column
    if best_score < 0.7 and best_k > 1:
        return {
            "type": "single",
            "columns": [{"x_start": 0, "x_end": page_width}],
            "confidence": best_score,
            "num_columns": 1
        }

    # Determine column boundaries
    if best_k == 1:
        columns = [{"x_start": 0, "x_end": page_width}]
    else:
        # Get cluster centers and sort by x-coordinate
        centers = best_kmeans.cluster_centers_.flatten()
        sorted_centers = sorted(enumerate(centers), key=lambda x: x[1])

        columns = []
        for i, (cluster_idx, x_center) in enumerate(sorted_centers):
            # Find min/max x for blocks in this cluster
            cluster_blocks = [x_coords[j] for j, label in enumerate(best_kmeans.labels_) if label == cluster_idx]

            if cluster_blocks:
                x_start = min(cluster_blocks) - 10  # Small margin
                x_end = max(cluster_blocks) + 100   # Larger right margin

                # Clamp to page bounds
                x_start = max(0, x_start)
                x_end = min(page_width, x_end)

                columns.append({
                    "x_start": x_start,
                    "x_end": x_end
                })

        # Sort columns left to right
        columns = sorted(columns, key=lambda c: c["x_start"])

    # Classify layout type
    layout_type = classify_layout_type(best_k, best_score)

    return {
        "type": layout_type,
        "columns": columns,
        "confidence": best_score,
        "num_columns": best_k
    }


def classify_layout_type(num_columns: int, confidence: float) -> str:
    """
    Map cluster count to layout type.

    Args:
        num_columns: Number of detected columns
        confidence: Detection confidence (0-1)

    Returns:
        Layout type string
    """
    if num_columns == 1:
        return "single"
    elif num_columns == 2:
        return "two_column"
    elif num_columns == 3:
        return "three_column"
    else:
        return "complex"


def reorder_blocks_by_reading_order(
    blocks: List[Dict],
    layout: Dict
) -> List[Dict]:
    """
    Sort blocks by proper reading order within columns.

    For single column: Sort by Y-position (top to bottom)
    For multi-column: Sort by Y within each column, then merge columns left-to-right

    Args:
        blocks: List of text blocks with bbox coordinates
        layout: Layout metadata from detect_columns()

    Returns:
        Sorted blocks with added fields:
        - "column": 0-indexed column number
        - "reading_order": Global reading order index
    """
    if not blocks or not layout.get("columns"):
        return blocks

    num_columns = layout.get("num_columns", 1)

    if num_columns == 1:
        # Single column: just sort by y-coordinate (top to bottom)
        sorted_blocks = sorted(blocks, key=lambda b: b["bbox"][1] if "bbox" in b else 0)

        # Add reading_order field
        for i, block in enumerate(sorted_blocks):
            block["column"] = 0
            block["reading_order"] = i

        return sorted_blocks

    # Multi-column: assign blocks to columns, sort within columns, then merge
    columns = layout["columns"]
    column_blocks = [[] for _ in range(len(columns))]

    # Assign each block to a column based on x-coordinate
    for block in blocks:
        if "bbox" not in block:
            continue

        x_center = (block["bbox"][0] + block["bbox"][2]) / 2  # Center x

        # Find which column this block belongs to
        assigned = False
        for col_idx, col in enumerate(columns):
            if col["x_start"] <= x_center <= col["x_end"]:
                column_blocks[col_idx].append(block)
                block["column"] = col_idx
                assigned = True
                break

        # If not assigned, put in closest column
        if not assigned:
            closest_col = min(range(len(columns)), key=lambda i: abs(x_center - columns[i]["x_start"]))
            column_blocks[closest_col].append(block)
            block["column"] = closest_col

    # Sort blocks within each column by y-coordinate (top to bottom)
    for col_blocks in column_blocks:
        col_blocks.sort(key=lambda b: b["bbox"][1] if "bbox" in b else 0)

    # Merge columns in left-to-right order
    sorted_blocks = []
    for col_blocks in column_blocks:
        sorted_blocks.extend(col_blocks)

    # Assign global reading_order indices
    for i, block in enumerate(sorted_blocks):
        block["reading_order"] = i

    return sorted_blocks


if __name__ == "__main__":
    print(__doc__)
