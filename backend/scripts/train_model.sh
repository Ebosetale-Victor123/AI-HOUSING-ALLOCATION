#!/bin/bash

# ML Model Training Script for SmartAlloc

set -e

echo "Training SmartAlloc ML Model..."

# Default values
SAMPLES=5000
VERSION="v1.0.0"
OUTPUT_DIR="apps/allocation/ml_models/artifacts"

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        --samples)
            SAMPLES="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Parameters:"
echo "  Samples: $SAMPLES"
echo "  Version: $VERSION"
echo "  Output: $OUTPUT_DIR"
echo ""

# Run training pipeline
python apps/allocation/ml_models/training_pipeline.py \
    --samples "$SAMPLES" \
    --version "$VERSION" \
    --output "$OUTPUT_DIR"

echo ""
echo "Model training complete!"
echo "Model saved to: $OUTPUT_DIR"
