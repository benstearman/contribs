package app.contribs.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.List
import androidx.compose.material.icons.filled.AccountBalance
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.graphics.vector.ImageVector

sealed class ContribsScreen(val route: String, val label: String, val icon: ImageVector) {
    object Candidates : ContribsScreen("candidates", "Candidates", Icons.Filled.Person)
    object Committees : ContribsScreen("committees", "Committees", Icons.Filled.AccountBalance)
    object Contributions : ContribsScreen(
        route = "contributions",
        label = "Contributions",
        icon = Icons.AutoMirrored.Filled.List // Updated this line
    )
    object Profile : ContribsScreen("profile", "Profile", Icons.Filled.Settings)
}

val bottomNavItems = listOf(
    ContribsScreen.Candidates,
    ContribsScreen.Committees,
    ContribsScreen.Contributions,
    ContribsScreen.Profile
)