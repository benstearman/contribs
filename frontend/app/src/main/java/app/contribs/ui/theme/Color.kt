package app.contribs.ui.theme

import androidx.compose.ui.graphics.Color

val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFF507CEA)
val Pink80 = Color(0xFFEFB8C8)

val Purple40 = Color(0xFF6650a4)
val PurpleGrey40 = Color(0xFFB9098D)
val Pink40 = Color(0xFF7D5260)

// Used on candidate detail screen background and badges

fun partyColor(party: String?): Color {
    return when (party) {
        "DEM" -> Color(0xFF1141B9)
        "REP" -> Color(0xFFAF0E0E)
        "GRE", "IGR", "DGR", "DCG", "PG" -> Color(0xFF5BAF47)
        else -> Color(0xFFD3D3D3)
    }
}