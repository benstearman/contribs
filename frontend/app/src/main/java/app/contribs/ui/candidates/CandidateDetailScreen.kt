package app.contribs.ui.candidates

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateDetailScreen(
    candidateId: String,
    viewModel: CandidateViewModel,
    onNavigateBack: () -> Unit
) {
    // Fetch the specific candidate from the dummy data
    val candidate = viewModel.getCandidateById(candidateId)

    Scaffold(
        topBar = {
            TopAppBar(title = { Text(candidate?.name ?: "Candidate Details") })
        }
    ) { innerPadding ->
        Column(modifier = Modifier.padding(innerPadding).padding(16.dp)) {
            if (candidate != null) {
                Text(text = "ID: ${candidate.id}", style = MaterialTheme.typography.bodyLarge)
                Text(text = "Party: ${candidate.party}", style = MaterialTheme.typography.bodyLarge)
                Text(text = "State: ${candidate.state}", style = MaterialTheme.typography.bodyLarge)
                Text(text = "Office: ${candidate.office}", style = MaterialTheme.typography.bodyLarge)

                Spacer(modifier = Modifier.height(32.dp))
                Text("UI for Financial Charts & Graphs goes here", style = MaterialTheme.typography.labelLarge)
            } else {
                Text("Candidate not found.")
            }

            Spacer(modifier = Modifier.height(16.dp))
            Button(onClick = onNavigateBack) {
                Text("Back to List")
            }
        }
    }
}