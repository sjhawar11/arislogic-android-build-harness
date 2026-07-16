package com.arislogic.harness

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import com.arislogic.harness.core.model.UserProfile

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val user = UserProfile(
            id = "1",
            name = "Sarvesh",
            interests = listOf("Android Infrastructure", "Compose Compiler")
        )
        setContent {
            UserCard(user = user)
        }
    }
}

@Composable
fun UserCard(user: UserProfile) {
    Text(text = "User: ${user.name}\nInterests: ${user.interests.joinToString(", ")}")
}