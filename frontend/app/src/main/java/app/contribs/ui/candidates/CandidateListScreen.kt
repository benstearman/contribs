package app.contribs.ui.candidates

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed // IMPORT THIS
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect // IMPORT THIS
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateListScreen(
    viewModel: CandidateViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onCandidateClick: (String) -> Unit
) {
    val candidates by viewModel.candidates.collectAsState()

    Scaffold(
        topBar = { TopAppBar(title = { Text("Candidates") }) }
    ) { innerPadding: PaddingValues ->
        LazyColumn(modifier = Modifier.padding(innerPadding)) {

            // Use itemsIndexed to know exactly what row we are rendering
            itemsIndexed(candidates) { index, candidate ->

                // If we are rendering the very last item in the list, fetch more!
                if (index == candidates.lastIndex && !viewModel.isLoading) {
                    LaunchedEffect(key1 = index) {
                        viewModel.loadNextPage()
                    }
                }

                ListItem(
                    headlineContent = { Text(candidate.name) },
                    supportingContent = { Text("${candidate.party ?: "Unknown"} - ${candidate.state ?: "N/A"} ${candidate.office ?: ""}") },
                    leadingContent = { Icon(Icons.Default.Person, contentDescription = null) },
                    modifier = Modifier.clickable { onCandidateClick(candidate.id) }
                )
                HorizontalDivider()
            }
        }
    }
}