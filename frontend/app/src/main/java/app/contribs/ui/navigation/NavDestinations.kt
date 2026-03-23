package app.contribs.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.HowToVote
import androidx.compose.ui.graphics.vector.ImageVector

sealed class ContribsScreen(val route: String, val label: String, val icon: ImageVector) {
    object Elections : ContribsScreen("elections", "Elections", Icons.Filled.HowToVote)
    object Candidates : ContribsScreen("candidates", "Candidates", Icons.Filled.Person)
    // Use the explicit import for AutoMirrored.Filled.List if needed,
    // or just Icons.AutoMirrored.Filled.List depending on your compose version
    object Contributions : ContribsScreen("contributions", "Contributions", Icons.AutoMirrored.Filled.List)
    object Profile : ContribsScreen("profile", "Profile", Icons.Filled.Settings)
}

val bottomNavItems = listOf(
    ContribsScreen.Elections,
    ContribsScreen.Candidates,
    ContribsScreen.Contributions,
    ContribsScreen.Profile
)