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
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController

// Feature Screen Imports
import app.contribs.ui.candidates.CandidateDetailScreen
import app.contribs.ui.candidates.CandidateListScreen
import app.contribs.ui.candidates.CandidateViewModel
import app.contribs.ui.committees.CommitteeListScreen
import app.contribs.ui.contributions.ContributionListScreen
import app.contribs.ui.profile.ProfileScreen

// Navigation & Theme Imports
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
            // --- Candidates Flow ---
            composable(ContribsScreen.Candidates.route) {
                // Scoped ViewModel so the list and detail screen share the same data
                val sharedViewModel: CandidateViewModel = viewModel()

                CandidateListScreen(
                    viewModel = sharedViewModel,
                    onCandidateClick = { candidateId ->
                        navController.navigate("candidate_detail/$candidateId")
                    }
                )
            }

            composable("candidate_detail/{candidateId}") { backStackEntry ->
                val sharedViewModel: CandidateViewModel = viewModel()
                val candidateId = backStackEntry.arguments?.getString("candidateId") ?: ""

                CandidateDetailScreen(
                    candidateId = candidateId,
                    viewModel = sharedViewModel,
                    onNavigateBack = { navController.popBackStack() }
                )
            }

            // --- Other Tabs ---
            composable(ContribsScreen.Committees.route) {
                CommitteeListScreen()
            }
            composable(ContribsScreen.Contributions.route) {
                ContributionListScreen()
            }
            composable(ContribsScreen.Profile.route) {
                ProfileScreen()
            }
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
                        // Pop up to the start destination of the graph to
                        // avoid building up a large stack of destinations
                        // on the back stack as users select items
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        // Avoid multiple copies of the same destination when
                        // reselecting the same item
                        launchSingleTop = true
                        // Restore state when reselecting a previously selected item
                        restoreState = true
                    }
                }
            )
        }
    }
}