package app.contribs.ui.contributions

import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ContributionListScreen(
    viewModel: ContributionViewModel,
    onContributionClick: (Int) -> Unit
) {
    val contributions by viewModel.filteredContributions.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val selectedAmount by viewModel.selectedAmount.collectAsState()
    val currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Contributions") }
            )
        }
    ) { innerPadding ->

        when {
            isLoading && contributions.isEmpty() -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            }

            error != null && contributions.isEmpty() -> {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding),
                    contentAlignment = Alignment.Center
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = error ?: "Something went wrong",
                            color = MaterialTheme.colorScheme.error
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Button(onClick = { viewModel.fetchContributions() }) {
                            Text("Retry")
                        }
                    }
                }
            }

            else -> {
                Column(modifier = Modifier.padding(innerPadding)) {

                    TextField(
                        value = searchQuery,
                        onValueChange = { viewModel.setSearchQuery(it) },
                        placeholder = { Text("Search contributors or committees...") },
                        modifier = Modifier.fillMaxWidth(),
                        colors = TextFieldDefaults.colors(
                            focusedContainerColor = Color.Transparent,
                            unfocusedContainerColor = Color.Transparent,
                            disabledContainerColor = Color.Transparent,
                            focusedIndicatorColor = Color.Transparent,
                            unfocusedIndicatorColor = Color.Transparent,
                        ),
                        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                        trailingIcon = {
                            if (searchQuery.isNotEmpty()) {
                                IconButton(onClick = { viewModel.setSearchQuery("") }) {
                                    Icon(Icons.Default.Close, contentDescription = "Clear search")
                                }
                            }
                        },
                        singleLine = true
                    )

                    // the filter chips for amounts
                    Row(
                        modifier = Modifier
                            .horizontalScroll(rememberScrollState())
                            .padding(horizontal = 16.dp, vertical = 8.dp),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        FilterChip(
                            selected = selectedAmount == AmountFilter.SMALL,
                            onClick = { viewModel.setAmountFilter(AmountFilter.SMALL) },
                            label = { Text("< $500") }
                        )
                        FilterChip(
                            selected = selectedAmount == AmountFilter.MEDIUM,
                            onClick = { viewModel.setAmountFilter(AmountFilter.MEDIUM) },
                            label = { Text("$500–$2000") }
                        )
                        FilterChip(
                            selected = selectedAmount == AmountFilter.LARGE,
                            onClick = { viewModel.setAmountFilter(AmountFilter.LARGE) },
                            label = { Text("$2000–$5000") }
                        )
                        FilterChip(
                            selected = selectedAmount == AmountFilter.XLARGE,
                            onClick = { viewModel.setAmountFilter(AmountFilter.XLARGE) },
                            label = { Text("> $10,000") }
                        )
                    }

                    HorizontalDivider()

                    LazyColumn {
                        itemsIndexed(contributions) { index, contribution ->

                            if (index == contributions.lastIndex && !isLoading) {
                                LaunchedEffect(key1 = index) {
                                    viewModel.fetchContributions(loadMore = true)
                                }
                            }

                            ListItem(
                                headlineContent = {
                                    Text(
                                        text = currencyFormatter.format(contribution.amount ?: 0.0),
                                        fontWeight = FontWeight.Bold
                                    )
                                },
                                supportingContent = {
                                    Column {
                                        Text(
                                            "From: ${contribution.contributorDetail?.formattedName ?: "Unknown"}",
                                            fontWeight = FontWeight.Bold
                                        )
                                        Text(
                                            "To: ${contribution.committeeDetail?.name ?: "Unknown Committee"}",
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                },
                                trailingContent = {
                                    Text(
                                        text = contribution.receiptDate ?: "",
                                        style = MaterialTheme.typography.labelSmall
                                    )
                                },
                                modifier = Modifier.clickable { onContributionClick(contribution.id) }
                            )
                            HorizontalDivider()
                        }

                        if (isLoading) {
                            item {
                                Box(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(16.dp),
                                    contentAlignment = Alignment.Center
                                ) {
                                    CircularProgressIndicator()
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}