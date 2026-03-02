package app.contribs.ui.candidates

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.background //added -d
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.ui.Alignment //added -d
import androidx.compose.ui.draw.clip //added -d
import androidx.compose.ui.graphics.Color //added -d


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
            TopAppBar(
                title = { Text("Candidate Detail Page") },
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
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
        ) {
            if (candidate != null) {

                //party color for background if rep or dem
                val bgColor = partyColor(candidate.party)


                //below is a photo placeholder, circle shaped and centered for portrait photo of candidate
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(bgColor)
                        .padding(vertical = 32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Box(
                        modifier = Modifier
                            .size(140.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.secondaryContainer)
                    )
                }

                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {


                    //name of the candidate with a badge next to it with party and state
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.Center,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = candidate.name,
                            style = MaterialTheme.typography.headlineLarge
                        )

                        Spacer(modifier = Modifier.width(12.dp))

                        //party badge
                        Surface(
                            color = partyColor(candidate.party),
                            shape = CircleShape
                        ) {
                            Text(
                                text = candidate.party ?: "N/A",
                                color = Color.White,
                                style = MaterialTheme.typography.labelLarge,
                                modifier = Modifier.padding(
                                    horizontal = 14.dp,
                                    vertical = 6.dp
                                )


                            )
                        }

                        Spacer(modifier = Modifier.width(6.dp))

                        //state badge
                        Surface(
                            color = Color(0xFF1C1C1C),
                            shape = CircleShape
                        ) {
                            Text(
                                text = candidate.state ?: "N/A",
                                color = Color.White,
                                style = MaterialTheme.typography.labelLarge,
                                modifier = Modifier.padding(
                                    horizontal = 14.dp,
                                    vertical = 6.dp
                                )


                            )
                        }
                    }

                }

            } else {
                Text("Candidate not found.")
            }
            //about section with candidate info, election cycle, primary office
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            )
            {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "About",
                        style = MaterialTheme.typography.titleMedium
                    )

                    HorizontalDivider()

                    Spacer(modifier = Modifier.height(10.dp))

                    Text("Office: ${candidate?.office ?: "N/A"}")
                    Text("Election Cycle(s): ${candidate?.electionYear ?: "N/A"}")
                }


            }

            //summary of total money raised current cycle, leading donor/contributor this cycle
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {

                    Text(
                        text = "Financial Summary",
                        style = MaterialTheme.typography.titleMedium
                    )

                    HorizontalDivider()

                    Spacer(modifier = Modifier.height(10.dp))

                    // ttal money received
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Total Received This Cycle")
                        Text("$ —")
                    }

                    Spacer(modifier = Modifier.height(8.dp))

                    // the leading donor or contributor to candidate
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Text("Leading Donor")
                        Text("coming soon...")
                    }
                }
            }

            //top contributors / donors to candidate for current campaign
            Card(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
            )
            {
                Column(modifier = Modifier.padding(10.dp)) {
                    Text(
                        text = "Candidate's Top Contributors",
                        style = MaterialTheme.typography.titleMedium
                    )

                    HorizontalDivider()

                    Spacer(modifier = Modifier.height(10.dp))

                    Text("coming soon...")

                }


            }

//function for making the candidate detail page bg color change according to party
private fun partyColor(party: String?): Color {
    return when (party) {
        "DEM" -> Color(0xFF1141B9)
        "REP" -> Color(0xFFAF0E0E)
        else -> Color(0xFF9F9E9E)
    }
}
