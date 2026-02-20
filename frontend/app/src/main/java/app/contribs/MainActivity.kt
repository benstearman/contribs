package app.contribs

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import app.contribs.ui.candidates.CandidateListScreen
import app.contribs.ui.navigation.ContribsScreen
import app.contribs.ui.navigation.bottomNavItems
import app.contribs.ui.theme.ContribsTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            ContribsTheme {
                ContribsApp()
            }
        }
    }
}

@Composable
fun ContribsApp() {
    val navController = rememberNavController()
    Scaffold(
        bottomBar = { ContribsBottomNavigation(navController) }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = ContribsScreen.Candidates.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(ContribsScreen.Candidates.route) { CandidateListScreen() }
            composable(ContribsScreen.Committees.route) { CommitteeListScreen() }
            composable(ContribsScreen.Contributions.route) { ContributionListScreen() }
            composable(ContribsScreen.Profile.route) { ProfileScreen() }
        }
    }
}

@Composable
fun ContribsBottomNavigation(navController: NavHostController) {
    NavigationBar {
        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentDestination = navBackStackEntry?.destination

        bottomNavItems.forEach { screen ->
            NavigationBarItem(
                icon = { Icon(screen.icon, contentDescription = null) },
                label = { Text(screen.label) },
                selected = currentDestination?.hierarchy?.any { it.route == screen.route } == true,
                onClick = {
                    navController.navigate(screen.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}

// Placeholder Screens to stop "Unresolved reference" errors
@Composable fun CommitteeListScreen() { Text("Committees") }
@Composable fun ContributionListScreen() { Text("Contributions") }
@Composable fun ProfileScreen() { Text("Profile") }