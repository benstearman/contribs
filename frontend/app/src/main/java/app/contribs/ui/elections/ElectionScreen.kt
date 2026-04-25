package app.contribs.ui.elections

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ElectionScreen(
    viewModel: ElectionViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    onElectionClick: (String?, String?, Int?) -> Unit
) {
    val summary by viewModel.summary.collectAsState()
    val elections by viewModel.elections.collectAsState()
    val selectedState by viewModel.selectedState.collectAsState()
    val selectedOffice by viewModel.selectedOffice.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US)

    Scaffold(
        topBar = { TopAppBar(title = { Text("2026 Elections") }) }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(horizontal = 16.dp)
        ) {
            Spacer(modifier = Modifier.height(16.dp))

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                OutlinedTextField(
                    value = selectedState,
                    onValueChange = { viewModel.onStateChange(it) },
                    label = { Text("State") },
                    modifier = Modifier.weight(1f),
                    placeholder = { Text("e.g. NY") }
                )
                OutlinedTextField(
                    value = selectedOffice,
                    onValueChange = { viewModel.onOfficeChange(it) },
                    label = { Text("Office") },
                    modifier = Modifier.weight(1f),
                    placeholder = { Text("H, S, P") }
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            if (isLoading) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (selectedState.isNotEmpty() || selectedOffice.isNotEmpty()) {
                // Election List
                Text(
                    text = "Matching Elections",
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.padding(vertical = 8.dp)
                )
                LazyColumn(modifier = Modifier.fillMaxSize()) {
                    items(elections) { election ->
                        ListItem(
                            headlineContent = { Text("${election.year ?: ""} ${election.state ?: ""} - ${when(election.office) {
                                "H" -> "House"
                                "S" -> "Senate"
                                "P" -> "President"
                                else -> election.office ?: ""
                            }}") },
                            modifier = Modifier.clickable { 
                                onElectionClick(election.state, election.office, election.year)
                            }
                        )
                        HorizontalDivider()
                    }
                }
            } else {
                // Summary View
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                ) {
                    // Top Employers Card
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "Top Employers for Donations",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )
                            HorizontalDivider(modifier = Modifier.padding(vertical = 10.dp))

                            summary?.topEmployers?.forEach { entity ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 4.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(
                                        text = entity.name,
                                        modifier = Modifier.weight(1f),
                                        maxLines = 1
                                    )
                                    Text(
                                        text = currencyFormatter.format(entity.total),
                                        fontWeight = FontWeight.SemiBold
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Top Contributors Card
                    Card(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "Top Individual Contributors",
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )
                            HorizontalDivider(modifier = Modifier.padding(vertical = 10.dp))

                            summary?.topContributors?.forEach { entity ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 4.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween
                                ) {
                                    Text(
                                        text = entity.name,
                                        modifier = Modifier.weight(1f),
                                        maxLines = 1
                                    )
                                    Text(
                                        text = currencyFormatter.format(entity.total),
                                        fontWeight = FontWeight.SemiBold
                                    )
                                }
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}