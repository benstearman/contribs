package app.contribs.ui.candidates

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.FilterListOff
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import app.contribs.R
import app.contribs.ui.candidates.CandidateItem
import java.text.NumberFormat
import java.util.Locale

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CandidateListScreen(
    viewModel: CandidateViewModel = androidx.lifecycle.viewmodel.compose.viewModel(),
    initialState: String? = null,
    initialOffice: String? = null,
    initialYear: Int? = null,
    onCandidateClick: (String) -> Unit
) {
    val candidates by viewModel.candidates.collectAsState()
    val searchQuery by viewModel.searchQuery.collectAsState()
    val isFiltered by viewModel.isFiltered.collectAsState()

    LaunchedEffect(initialState, initialOffice, initialYear) {
        viewModel.setInitialFilters(initialState, initialOffice, initialYear)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Candidates") },
                actions = {
                    if (isFiltered || searchQuery.isNotEmpty()) {
                        IconButton(onClick = { viewModel.clearFilters() }) {
                            Icon(
                                imageVector = Icons.Default.FilterListOff,
                                contentDescription = "Clear Filters"
                            )
                        }
                    }
                }
            )
        }
    ) { innerPadding: PaddingValues ->
        Column(modifier = Modifier.padding(innerPadding)) {
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { viewModel.onSearchQueryChange(it) },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                placeholder = { Text("Search") },
                leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { viewModel.onSearchQueryChange("") }) {
                            Icon(Icons.Default.Close, contentDescription = "Clear search")
                        }
                    }
                },
                singleLine = true
            )

            LazyColumn {
                // Use itemsIndexed to know exactly what row we are rendering
                itemsIndexed(candidates) { index, candidate ->

                    // If we are rendering the very last item in the list, fetch more!
                    if (index == candidates.lastIndex && !viewModel.isLoading) {
                        LaunchedEffect(key1 = index) {
                            viewModel.loadNextPage()
                        }
                    }

                    CandidateItem(
                        candidate = candidate,
                        onCandidateClick = onCandidateClick
                    )
                }
            }
        }
    }
}
