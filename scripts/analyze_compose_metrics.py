#!/usr/bin/env python3
"""
ArisLogic Harness: Compose Compiler Metrics Boundary Analyzer
Parses Compose compiler output files (*-classes.txt) and outputs a Markdown audit report.
"""

import os
import argparse

def parse_compose_metrics(search_dir):
    files = []
    for root, _, filenames in os.walk(search_dir):
        for f in filenames:
            if f.endswith("-classes.txt"):
                files.append(os.path.join(root, f))

    if not files:
        print(f"[ArisLogic Harness] No Compose metric files found under '{search_dir}'.")
        print("Searching for any files in build directories...")
        return

    unstable_classes = []
    stable_classes = []

    for filepath in files:
        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("unstable class "):
                    unstable_classes.append(line.strip().replace("unstable class ", ""))
                elif line.startswith("stable class "):
                    stable_classes.append(line.strip().replace("stable class ", ""))

    total = len(unstable_classes) + len(stable_classes)
    stability_rate = (len(stable_classes) / total * 100) if total > 0 else 100.0

    print("\n==================================================")
    print("      ARISLOGIC HARNESS: COMPOSE STABILITY REPORT   ")
    print("==================================================")
    print(f"Metrics Files Processed: {len(files)}")
    print(f"Total Classes Analyzed:  {total}")
    print(f"Stable Classes:          {len(stable_classes)}")
    print(f"Unstable Classes:        {len(unstable_classes)}")
    print(f"Overall Stability Rate:  {stability_rate:.1f}%\n")

    if unstable_classes:
        print("⚠️  UNSTABLE BOUNDARY MODELS DETECTED:")
        for cls in unstable_classes[:10]:
            print(f"  - {cls}")
        if len(unstable_classes) > 10:
            print(f"  ... and {len(unstable_classes) - 10} more.")
    else:
        print("✅ ALL ANALYZED CLASSES ARE STABLE!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Compose Compiler Metrics.")
    parser.add_argument("--build-dir", type=str, default=".", help="Path to search directory")
    args = parser.parse_args()
    parse_compose_metrics(args.build_dir)