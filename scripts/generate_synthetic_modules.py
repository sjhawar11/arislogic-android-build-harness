#!/usr/bin/env python3
"""
ArisLogic Harness: Synthetic Module Graph Generator
Generates synthetic multi-module dependency trees with configurable ABI leaks and unstable Compose parameters.
"""

import argparse
import os

def generate_modules(num_modules, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    print(f"[ArisLogic Harness] Generating {num_modules} synthetic modules in '{output_dir}'...")

    # Generate settings.gradle.kts inclusions snippet
    includes = []
    for i in range(1, num_modules + 1):
        mod_name = f"synthetic-feature-{i}"
        mod_dir = os.path.join(output_dir, mod_name)
        os.makedirs(os.path.join(mod_dir, "src/main/java/com/arislogic/harness/synthetic"), exist_ok=True)

        # Create dummy build.gradle.kts
        with open(os.path.join(mod_dir, "build.gradle.kts"), "w") as f:
            f.write(f"""plugins {{
    id("java-library")
    id("org.jetbrains.kotlin.jvm")
}}

dependencies {{
    // Demonstrate api vs implementation leakage
    {"api" if i % 3 == 0 else "implementation"}(project(":core:model"))
}}
""")

        # Create dummy Unstable model to simulate Compose metrics flags
        with open(os.path.join(mod_dir, f"src/main/java/com/arislogic/harness/synthetic/SyntheticModel{i}.kt"), "w") as f:
            f.write(f"""package com.arislogic.harness.synthetic

// Synthetic Unstable Model (var property causes Compose instability)
data class SyntheticModel{i}(
    var id: String = "{i}",
    var rawData: Any = Object()
)
""")
        includes.append(f'include(":synthetic:{mod_name}")\nproject(":synthetic:{mod_name}").projectDir = file("{output_dir}/{mod_name}")')

    print(f"[ArisLogic Harness] Successfully generated {num_modules} modules.")
    print("Add the following to your settings.gradle.kts to link them:")
    print("\n".join(includes[:5]) + f"\n... and {num_modules - 5} more.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic multi-module build harness.")
    parser.add_argument("--modules", type=int, default=20, help="Number of synthetic modules to generate")
    parser.add_argument("--dir", type=str, default="synthetic_modules", help="Output directory")
    args = parser.parse_args()
    generate_modules(args.modules, args.dir)