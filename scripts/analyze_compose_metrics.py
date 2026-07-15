#!/usr/bin/env python3
"""
ArisLogic Harness: Compose Compiler Metrics Boundary Analyzer
Parses Compose compiler output files (*-classes.txt) and outputs a Markdown audit report.
"""

import os
import glob
import argparse

def parse_compose_metrics(build_dir):
    pattern = os.path.join(build_dir, "**", "*-classes.txt")
    files = glob.glob(pattern, recursive=True)

    if not files:
        print(f"[ArisLogic Harness] No Compose metric files found in '{build_dir}'.")
        print("Ensure you passed '-Pplugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=...' to Gradle.")
        return

    unstable_classes = []
    stable_classes = []

    for filepath in files:
        with open(filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("unstable class "):
                    unstable_classes.append(line.strip().replace("unstable class ", ""))
                elif line.startswith("stable class "):
                    stable_classes.append(line.strip().replace("stable class ", ""))

    total = len(unstable_classes) + len(stable_classes)
    stability_rate = (len(stable_classes) / total * 100) if total > 0 else 100.0

    print("\n==================================================")
    print("      ARISLOGIC HARNESS: COMPOSE STABILITY REPORT   ")
    print("==================================================")
    print(f"Total Classes Analyzed: {total}")
    print(f"Stable Classes:         {len(stable_classes)}")
    print(f"Unstable Classes:       {len(unstable_classes)}")
    print(f"Overall Stability Rate: {stability_rate:.1f}%\n")

    if unstable_classes:
        print("⚠️  UNSTABLE BOUNDARY MODELS DETECTED:")
        for cls in unstable_classes[:10]:
            print(f"  - {cls}")
        if len(unstable_classes) > 10:
            print(f"  ... and {len(unstable_classes) - 10} more.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Compose Compiler Metrics.")
    parser.add_argument("--build-dir", type=str, default="build", help="Path to build output directory")
    args = parser.parse_args()
    parse_compose_metrics(args.build_dir)