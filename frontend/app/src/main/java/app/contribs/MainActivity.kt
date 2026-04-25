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
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import app.contribs.data.model.ElectionSummary

// Feature Screen Imports
import app.contribs.ui.candidates.CandidateDetailScreen
import app.contribs.ui.candidates.CandidateListScreen
import app.contribs.ui.candidates.CandidateViewModel
import app.contribs.ui.committees.CommitteeListScreen
import app.contribs.ui.contributions.ContributionListScreen
import app.contribs.ui.elections.ElectionScreen
import app.contribs.ui.profile.ProfileScreen

// Navigation & Theme Imports
import app.contribs.ui.navigation.ContribsScreen
import app.contribs.ui.navigation.bottomNavItems
import app.contribs.ui.theme.ContribsTheme

import app.contribs.ui.contributions.ContributionViewModel
import app.contribs.ui.contributions.ContributionDetail

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
            startDestination = ContribsScreen.Elections.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(ContribsScreen.Elections.route) {
                ElectionScreen(
                    onElectionClick = { state, office, year ->
                        navController.navigate(ContribsScreen.Candidates.createRoute(state, office, year))
                    }
                )
            }
            // --- Candidates Flow ---
            composable(
                route = ContribsScreen.Candidates.routePattern,
                arguments = listOf(
                    navArgument("state") { type = NavType.StringType; nullable = true; defaultValue = null },
                    navArgument("office") { type = NavType.StringType; nullable = true; defaultValue = null },
                    navArgument("year") { type = NavType.IntType; defaultValue = 0 }
                )
            ) { backStackEntry ->
                val state = backStackEntry.arguments?.getString("state")
                val office = backStackEntry.arguments?.getString("office")
                val year = backStackEntry.arguments?.getInt("year")?.takeIf { it != 0 }
                
                // Scoped ViewModel so the list and detail screen share the same data
                val sharedViewModel: CandidateViewModel = viewModel()

                CandidateListScreen(
                    viewModel = sharedViewModel,
                    initialState = state,
                    initialOffice = office,
                    initialYear = year,
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

            composable(ContribsScreen.Contributions.route) {
                val sharedViewModel: ContributionViewModel = viewModel()
                ContributionListScreen(
                    viewModel = sharedViewModel,
                    onContributionClick = { contributionId ->
                        navController.navigate("contribution_detail/$contributionId")
                    }
                )
            }
            composable("contribution_detail/{contributionId}") { backStackEntry ->
                val sharedViewModel: ContributionViewModel = viewModel()
                val contributionId =
                    backStackEntry.arguments?.getString("contributionId")?.toIntOrNull() ?: 0
                ContributionDetail(
                    contributionId = contributionId,
                    viewModel = sharedViewModel,
                    onNavigateBack = { navController.popBackStack() },
                    onCandidateClick = { candidateId ->
                        navController.navigate("candidate_detail/$candidateId")
                    }
                )
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
                    val route = if (screen == ContribsScreen.Candidates) "candidates" else screen.route
                    navController.navigate(route) {
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