package app.contribs.ui.elections

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
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
    val filters by viewModel.filters.collectAsState()
    val selectedState by viewModel.selectedState.collectAsState()
    val selectedOffice by viewModel.selectedOffice.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US)

    var stateExpanded by remember { mutableStateOf(false) }
    var officeExpanded by remember { mutableStateOf(false) }

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
                // State Dropdown
                ExposedDropdownMenuBox(
                    expanded = stateExpanded,
                    onExpandedChange = { stateExpanded = !stateExpanded },
                    modifier = Modifier.weight(1f)
                ) {
                    OutlinedTextField(
                        value = selectedState.ifEmpty { "All States" },
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("State") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = stateExpanded) },
                        modifier = Modifier.menuAnchor()
                    )
                    ExposedDropdownMenu(
                        expanded = stateExpanded,
                        onDismissRequest = { stateExpanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("All States") },
                            onClick = {
                                viewModel.onStateChange("")
                                stateExpanded = false
                            }
                        )
                        filters?.states?.forEach { state ->
                            DropdownMenuItem(
                                text = { Text(state) },
                                onClick = {
                                    viewModel.onStateChange(state)
                                    stateExpanded = false
                                }
                            )
                        }
                    }
                }

                // Office Dropdown
                ExposedDropdownMenuBox(
                    expanded = officeExpanded,
                    onExpandedChange = { officeExpanded = !officeExpanded },
                    modifier = Modifier.weight(1f)
                ) {
                    val officeName = filters?.offices?.find { it.id == selectedOffice }?.name ?: "All Offices"
                    OutlinedTextField(
                        value = officeName,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Office") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = officeExpanded) },
                        modifier = Modifier.menuAnchor()
                    )
                    ExposedDropdownMenu(
                        expanded = officeExpanded,
                        onDismissRequest = { officeExpanded = false }
                    ) {
                        DropdownMenuItem(
                            text = { Text("All Offices") },
                            onClick = {
                                viewModel.onOfficeChange("")
                                officeExpanded = false
                            }
                        )
                        filters?.offices?.forEach { office ->
                            DropdownMenuItem(
                                text = { Text(office.name) },
                                onClick = {
                                    viewModel.onOfficeChange(office.id)
                                    officeExpanded = false
                                }
                            )
                        }
                    }
                }
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
                            trailingContent = {
                                Text(
                                    text = currencyFormatter.format(election.totalAmount ?: 0.0),
                                    style = MaterialTheme.typography.bodyMedium,
                                    fontWeight = FontWeight.SemiBold
                                )
                            },
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