package app.contribs.ui.candidates

import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateListScreen(viewModel: CandidateViewModel = viewModel()) {
    val candidates by viewModel.candidates.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Candidates") })
        }
    ) { innerPadding: PaddingValues -> // Explicitly typed to help compiler
        LazyColumn(modifier = Modifier.padding(innerPadding)) {
            items(candidates) { candidate ->
                ListItem(
                    headlineContent = { Text(candidate.name) },
                    supportingContent = { Text("${candidate.party ?: "Unknown"} - ${candidate.state ?: "N/A"}") },
                    leadingContent = {
                        Icon(Icons.Default.Person, contentDescription = null)
                    }
                )
                HorizontalDivider()
            }
        }
    }
}