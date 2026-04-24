package app.contribs.ui.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MonetizationOn
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.AccountCircle
import androidx.compose.material.icons.filled.HowToVote
import androidx.compose.ui.graphics.vector.ImageVector

sealed class ContribsScreen(val route: String, val label: String, val icon: ImageVector) {
    object Elections : ContribsScreen("elections", "Elections", Icons.Filled.HowToVote)
    object Candidates : ContribsScreen("candidates", "Candidates", Icons.Filled.Person)
    object Contributions : ContribsScreen("contributions", "Contributions", Icons.Filled.MonetizationOn)
    object Profile : ContribsScreen("profile", "Profile", Icons.Filled.AccountCircle)
}

val bottomNavItems = listOf(
    ContribsScreen.Elections,
    ContribsScreen.Candidates,
    ContribsScreen.Contributions,
    ContribsScreen.Profile
)