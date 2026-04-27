package app.contribs.ui.candidates

import app.contribs.R

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.*
import androidx.compose.material3.IconButton
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.ui.Alignment
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.ui.text.style.TextAlign
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.filled.StarBorder
import androidx.compose.ui.platform.LocalContext
import app.contribs.data.model.getFullCommitteeType
import androidx.compose.material.icons.filled.AccountBalance
import app.contribs.ui.theme.partyColor

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateDetailScreen(
    candidateId: String,
    viewModel: CandidateViewModel,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    //committee dialog box details
    var showDialog by remember { mutableStateOf(false) }
    var selectedCommitteeName by remember { mutableStateOf("") }
    var selectedCommitteeTres by remember { mutableStateOf("") }
    var selectedCommitteeType by remember { mutableStateOf("") }
    var selectedCommitteeTotal by remember { mutableStateOf(0.0) }

    val candidate by viewModel.selectedCandidate.collectAsState()
    val committees by viewModel.candidateCommittees.collectAsState()
    val isFavorite by viewModel.isFavorite.collectAsState()

    val currencyFormatter = java.text.NumberFormat.getCurrencyInstance(java.util.Locale.US)

    LaunchedEffect(candidateId) {
        viewModel.fetchCandidateDetail(candidateId)
        viewModel.fetchCommitteesForCandidate(candidateId)
        viewModel.checkFavoriteStatus(candidateId, context)
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
                },
                actions = {
                    IconButton(onClick = { viewModel.toggleFavorite(candidateId, context) }) {
                        Icon(
                            imageVector = if (isFavorite) Icons.Default.Star else Icons.Default.StarBorder,
                            contentDescription = "Favorite",
                            tint = if (isFavorite) Color(0xFFFFD700) else LocalContentColor.current
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


                //below is candidate portrait if there is one if not then a silly default photo
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
                            text = candidateVal.formattedName,
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
                        .padding(horizontal = 16.dp, vertical = 8.dp)
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
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {

                        Text(
                            text = "Financial Summary",
                            style = MaterialTheme.typography.titleMedium
                        )

                        HorizontalDivider()

                        Spacer(modifier = Modifier.height(10.dp))

                        // total money received
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text("Total Received This Cycle")
                            Text(currencyFormatter.format(candidateVal.totalContributions ?: 0.00))
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
                        .padding(horizontal = 16.dp, vertical = 8.dp)
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
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "Committees",
                            style = MaterialTheme.typography.titleMedium
                        )
                        HorizontalDivider()
                        Spacer(modifier = Modifier.height(10.dp))

                        //starting here is the arrow/ability to click on the committee name for a box to pop up
                        if (committees.isNotEmpty()) {
                            for (committee in committees) {

                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            selectedCommitteeName =
                                                committee.name ?: "Unnamed Committee"
                                            selectedCommitteeType = committee.type ?: "Unknown"
                                            selectedCommitteeTres = committee.treasurer ?: "Unknown"
                                            selectedCommitteeTotal = committee.totalContributions ?: 0.0

                                            showDialog = true
                                        }
                                        .padding(vertical = 12.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        committee.name ?: "Unnamed Committee"
                                    )
                                    Icon(
                                        imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                                        contentDescription = null,
                                        tint = Color.Gray
                                    )
                                }
                                HorizontalDivider(thickness = 0.5.dp, color = Color.LightGray)
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
        //the dialog box and information it shows starts here
        if (showDialog) {
            AlertDialog(
                onDismissRequest = { showDialog = false },

                icon = {
                    Icon(
                        imageVector = Icons.Default.AccountBalance,
                        contentDescription = "Institution",
                        tint = MaterialTheme.colorScheme.primary
                    )
                },

                title = {
                    Text(
                        text = selectedCommitteeName,
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        textAlign = TextAlign.Center
                    )
                },

                text = {
                    Column(modifier = Modifier.fillMaxWidth()) {


                        Text(
                            "COMMITTEE TYPE:",
                            style = MaterialTheme.typography.labelMedium,
                            color = Color.Gray
                        )
                        Text(
                            text = getFullCommitteeType(selectedCommitteeType),
                            style = MaterialTheme.typography.bodyLarge
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Text(
                            "TREASURER:",
                            style = MaterialTheme.typography.labelMedium,
                            color = Color.Gray
                        )
                        Text(
                            text = selectedCommitteeTres,
                            style = MaterialTheme.typography.bodyLarge
                        )

                        Spacer(modifier = Modifier.height(16.dp))

                        Text( 
                            "TOTAL MONEY RAISED:",
                            style = MaterialTheme.typography.labelMedium,
                            color = Color.Gray
                        )
                        Text(
                            text = currencyFormatter.format(selectedCommitteeTotal),
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                },
                confirmButton = {
                    TextButton(onClick = { showDialog = false }) {
                        Text("Close")
                    }
                }
            )
        }
    }
}


