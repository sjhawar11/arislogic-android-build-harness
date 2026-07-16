package com.arislogic.harness.core.model

// ❌ UNSTABLE CLASS
// 1. 'var' allows mutation
// 2. Standard 'List<String>' is an interface
data class UserProfile(
    val id: String,
    var name: String,
    val interests: List<String>
)