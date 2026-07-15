// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.android.library) apply false
}



tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    compilerOptions {
        freeCompilerArgs.addAll(
            "-P",
            "plugin:androidx.compose.compiler.plugins.kotlin:reportsDestination=${layout.buildDirectory.get().asFile}/compose_metrics",
            "-P",
            "plugin:androidx.compose.compiler.plugins.kotlin:metricsDestination=${layout.buildDirectory.get().asFile}/compose_metrics",
            "-P",
            "plugin:org.jetbrains.kotlin.plugin.compose:reportsDestination=${layout.buildDirectory.get().asFile}/compose_metrics",
            "-P",
            "plugin:org.jetbrains.kotlin.plugin.compose:metricsDestination=${layout.buildDirectory.get().asFile}/compose_metrics"
        )
    }
}