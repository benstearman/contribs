package app.contribs.ui.candidates
import app.contribs.R

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
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.text.style.TextAlign
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateDetailScreen(
    candidateId: String,
    viewModel: CandidateViewModel,
    onNavigateBack: () -> Unit
) {
    // Fetch the specific candidate from the dummy data
    val candidate by viewModel.selectedCandidate.collectAsState()
    val committees by viewModel.candidateCommittees.collectAsState()

    LaunchedEffect(candidateId) {
        viewModel.fetchCandidateDetail(candidateId)
        viewModel.fetchCommitteesForCandidate(candidateId)
    }

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
                val candidateVal = candidate!!

                //party color for background if rep or dem
                val bgColor = partyColor(candidateVal.party)


                //below is a photo placeholder, circle shaped and centered for portrait photo of candidate
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(bgColor)
                        .padding(vertical = 32.dp),
                    contentAlignment = Alignment.Center
                ) {
                    AsyncImage(
                        model = candidateVal.photoURL,
                        contentDescription = "Portrait of ${candidateVal.name}",
                        fallback = painterResource(R.drawable.default_portrait),
                        modifier = Modifier
                            .size(120.dp)
                            .clip(CircleShape)
                            .background(Color.White),
                        contentScale = ContentScale.Crop
                    )

                }

                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {


                    //name of the candidate with state and party badges underneath
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            text = candidateVal.name,
                            style = MaterialTheme.typography.headlineLarge,
                            textAlign = TextAlign.Center
                        )

                        Spacer(modifier = Modifier.height(8.dp))

                        //party badge
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.Center
                        ) {
                            Surface(
                                color = partyColor(candidateVal.party),
                                shape = CircleShape
                            ) {
                                Text(
                                    text = candidateVal.party ?: "N/A",
                                    color = Color.White,
                                    style = MaterialTheme.typography.labelLarge,
                                    modifier = Modifier.padding(
                                        horizontal = 14.dp,
                                        vertical = 6.dp
                                    )


                                )
                            }

                            Spacer(modifier = Modifier.width(8.dp))

                            //state badge
                            Surface(
                                color = Color(0xFF1C1C1C),
                                shape = CircleShape
                            ) {
                                Text(
                                    text = candidateVal.state ?: "N/A",
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

                        Text("Office: ${candidateVal.office ?: "N/A"}")
                        Text("Election Cycle(s): ${candidateVal.electionYear ?: "N/A"}")
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
                            Text("$${candidateVal.totalContributions ?: 0.00}")
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

                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Committees",
                            style = MaterialTheme.typography.titleMedium
                        )
                        HorizontalDivider()
                        Spacer(modifier = Modifier.height(10.dp))

                        if (committees.isNotEmpty()) {
                            for (committee in committees) {
                                Text(committee.name ?: "Unnamed Committee")
                            }
                        } else {
                            Text("No committees found.")
                        }
                    }
                }
            } else {
                Text("Candidate not found.")
            }
        }
    }
}

//function for making the candidate detail page bg color change according to party
private fun partyColor(party: String?): Color {
    return when (party) {
        "DEM" -> Color(0xFF1141B9)
        "REP" -> Color(0xFFAF0E0E)
        "GRE", "IGR", "DGR", "DCG", "PG" -> Color(0xFF5BAF47) //"green" parties
        else -> Color(0xFFD3D3D3)
    }
}
