package app.contribs.ui.contributions

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import app.contribs.data.model.getFullCommitteeType
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ContributionDetail(
    contributionId: Int,
    viewModel: ContributionViewModel,
    onNavigateBack: () -> Unit,
    onCandidateClick: (String) -> Unit
) {
    val contribution by viewModel.selectedContribution.collectAsState()
    LaunchedEffect(contributionId) {
        viewModel.fetchContributionDetail(contributionId)
    }
    val currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US)

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Contribution Detail") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        if (contribution == null) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            val contribution = contribution!!
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .verticalScroll(rememberScrollState())
            ) {

                // contribution stuff / card
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Contribution",
                            style = MaterialTheme.typography.titleMedium
                        )
                        HorizontalDivider()
                        Spacer(modifier = Modifier.height(10.dp))

                        DetailRow(
                            label = "From",
                            value = contribution.contributorDetail?.formattedName ?: "Unknown"
                        )
                        DetailRow(
                            label = "Amount",
                            value = currencyFormatter.format(contribution.amount ?: 0.0),
                            valueColor = MaterialTheme.colorScheme.primary,
                            valueBold = true
                        )
                        DetailRow(
                            label = "Date",
                            value = contribution.receiptDate ?: "Unknown"
                        )
                        DetailRow(
                            label = "Employer",
                            value = contribution.contributorDetail?.employerName ?: "Unknown"
                        )
                        DetailRow(
                            label = "Zip Code",
                            value = contribution.contributorDetail?.zipCode ?: "Unknown"
                        )
                    }
                }

                // the committee card
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Committee",
                            style = MaterialTheme.typography.titleMedium
                        )
                        HorizontalDivider()
                        Spacer(modifier = Modifier.height(10.dp))

                        DetailRow(
                            label = "Name",
                            value = contribution.committeeDetail?.name ?: "Unknown"
                        )
                        DetailRow(
                            label = "Type",
                            value = getFullCommitteeType(contribution.committeeDetail?.type)
                        )
                        DetailRow(
                            label = "Total Raised",
                            value = currencyFormatter.format(
                                contribution.committeeDetail?.totalContributions ?: 0.0
                            ),
                            valueColor = MaterialTheme.colorScheme.primary,
                            valueBold = true
                        )
                    }
                }

                // candidate card and info if any
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Candidate",
                            style = MaterialTheme.typography.titleMedium
                        )
                        HorizontalDivider()
                        Spacer(modifier = Modifier.height(10.dp))

                        val candidateId = contribution.committeeDetail?.candidateId
                        val candidateName = contribution.committeeDetail?.candidateName

                        if (candidateId != null && candidateName != null) {
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable { onCandidateClick(candidateId) },
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween
                            ) {
                                Text(
                                    text = candidateName,
                                    fontWeight = FontWeight.Medium,
                                    color = MaterialTheme.colorScheme.primary
                                )
                                Icon(
                                    imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                                    contentDescription = "Go to candidate",
                                    tint = Color.Gray
                                )
                            }
                        } else {
                            Text(
                                text = "No candidate associated with this committee.",
                                color = Color.Gray
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun DetailRow(
    label: String,
    value: String,
    valueColor: Color = Color.Unspecified,
    valueBold: Boolean = false
) {
    Column(modifier = Modifier.padding(vertical = 6.dp)) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyLarge,
            color = Color.DarkGray
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyLarge,
            color = valueColor,
            fontWeight = if (valueBold) FontWeight.Bold else FontWeight.Normal
        )
    }
    HorizontalDivider(thickness = 0.5.dp, color = Color.LightGray)
}