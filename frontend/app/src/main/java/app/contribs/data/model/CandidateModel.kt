package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Candidate(
    @SerializedName("CAND_ID") val id: String,
    @SerializedName("CAND_NAME") val name: String,
    @SerializedName("party_name") val party: String?,
    @SerializedName("CAND_ELECTION_YR") val electionYear: Int?,
    @SerializedName("CAND_OFFICE_ST") val state: String?,
    @SerializedName("office_display") val office: String?,
    @SerializedName("total_contributions") val totalContributions: Double?,
    @SerializedName("photo_url") val photoURL: String? = null
)

{

    //use this where you want the candidate name to be first THEN last
    val formattedName: String
        get() {
            if (!name.contains(",")) return name

            val parts = name.split(",")
            val lastName = parts[0].trim()
            val firstName = parts[1].trim()

            val fullName = "$firstName $lastName".lowercase()

            return fullName.split(" ").joinToString(" ") { word ->
                word.replaceFirstChar { it.uppercase() }
            }
        }
}
