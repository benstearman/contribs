package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Committee(
    @SerializedName("CMTE_ID") val id: String,
    @SerializedName("CMTE_NM") val name: String,
    @SerializedName("CMTE_ST") val state: String?,
    @SerializedName("CMTE_TP") val type: String?,
    @SerializedName("CMTE_PTY_AFFILIATION") val party: String?,
    @SerializedName("TRES_NM") val treasurer: String?,
    @SerializedName("total_contributions") val totalContributions: Double? = 0.0

)

//converts FEC data to an actual readable name for a user versus having an ambiguous letter
fun getFullCommitteeType(code: String?): String {
    val typeName = mapOf(
        "C" to "Communication Cost",
        "D" to "Delegate Committee",
        "E" to "Electioneering Communication",
        "H" to "House",
        "I" to "Independent Expenditor",
        "N" to "PAC (Nonqualified)",
        "O" to "Super PAC",
        "P" to "Presidential",
        "Q" to "PAC (Qualified)",
        "S" to "Senate",
        "U" to "Single-Candidate Independent Expenditure",
        "V" to "Hybrid PAC (Nonqualified)",
        "W" to "Hybrid PAC (Qualified)",
        "X" to "Party (Nonqualified)",
        "Y" to "Party (Qualified)",
        "Z" to "National Party Nonfederal Account"
    )

    return typeName[code?.uppercase()] ?: "Unknown"
}