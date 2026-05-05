package app.contribs.ui.candidates

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.ListItem
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import app.contribs.R
import app.contribs.data.model.Candidate
import coil.compose.AsyncImage
import java.text.NumberFormat
import java.util.Locale

@Composable
fun CandidateItem(
    candidate: Candidate,
    onCandidateClick: (String) -> Unit,
) {
    val currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US)
    
    ListItem(
        headlineContent = { Text(candidate.formattedName) },
        supportingContent = { Text("${candidate.party ?: "Unknown"} - ${candidate.state ?: "N/A"} ${candidate.office ?: ""}") },
        leadingContent = {
            AsyncImage(
                model = candidate.photoURL,
                contentDescription = "Portrait of ${candidate.name}",
                fallback = painterResource(R.drawable.default_portrait),
                modifier = Modifier
                    .size(40.dp)
                    .clip(CircleShape)
                    .background(Color.LightGray),
                contentScale = ContentScale.Crop
            )
        },
        trailingContent = {
            Text(
                text = currencyFormatter.format(candidate.totalContributions ?: 0.0),
                style = MaterialTheme.typography.bodyMedium,
                fontWeight = FontWeight.SemiBold
            )
        },
        modifier = Modifier.clickable { onCandidateClick(candidate.id) }
    )
    HorizontalDivider()
}
