Here is the raw text for your root **`README.md`**. You can copy everything below this line directly into your `README.md` file:

# ArisLogic Harness (`com.arislogic.harness`)

A multi-module Android reference architecture and diagnostic suite for benchmarking **Gradle ABI invalidation cascades** and **Jetpack Compose parameter instability** across module boundaries.

---

## Overview

`ArisLogic Harness` was built to demonstrate and prevent two common performance bottlenecks that emerge when scaling Android codebases past 20+ feature modules:

1. **ABI Invalidation Cascades:** Preventing single-line UI edits from triggering multi-module recompilation loops.
2. **Cross-Module Compose Instability:** Enforcing parameter stability rules for models passing between separate Gradle modules.

Whether you are refactoring a legacy monolith or setting up standards for a growing engineering team, this repository provides both the structural patterns (`:feature:api` vs `:feature:impl`) and diagnostic scripts to keep incremental build times under control.

---

## Module Hierarchy

* `:app`
    * `:feature:profile-impl` (Android Library - UI & ViewModels)
        * `:feature:profile-api` (Pure Kotlin - Contract Interfaces)
        * `:core:model` (Pure Kotlin - Domain Entities)

### Boundary Encapsulation Rules:
* Feature modules **never** depend on another feature's `-impl` module.
* All inter-module communication is routed strictly through pure interface contracts (`-api`).
* `:core:model` contains zero Android framework dependencies (`android.*`).

---

## Diagnostic Tooling (`/scripts`)

### 1. Synthetic Module Generator
Generate a 40-module synthetic dependency tree with `api` leaks and unstable models to test your local Gradle configuration cache and build metrics:

```bash
python3 scripts/generate_synthetic_modules.py --modules 40 --dir synthetic_modules
```

### 2. Compose Compiler Metrics Analyzer
Parse raw Compose compiler metric outputs (`*-classes.txt`) across all modules and generate an instant stability audit report:

```bash
python3 scripts/analyze_compose_metrics.py --build-dir app/build
```

---

## Centralized Compose Stability Config

To prevent Compose from marking cross-module primitives as `Unstable`, this harness applies a root `compose_compiler_config.conf`:

```conf
// compose_compiler_config.conf
java.time.Instant
java.time.LocalDate
java.time.LocalDateTime
java.util.UUID

// Treat core data models as stable across module boundaries
com.arislogic.harness.core.model.**
```

Wire it into your root `build.gradle.kts`:

```kotlin
subprojects {
    tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
        compilerOptions {
            freeCompilerArgs.addAll(
                "-P",
                "plugin:androidx.compose.compiler.plugins.kotlin:stabilityConfigurationPath=${rootDir}/compose_compiler_config.conf"
            )
        }
    }
}
```


## License

Copyright 2026 ArisLogic LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0