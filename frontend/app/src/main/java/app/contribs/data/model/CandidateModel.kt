package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Candidate(
    @SerializedName("CAND_ID") val id: String,
    @SerializedName("CAND_NAME") val name: String,
    @SerializedName("party_name") val party: String?,
    @SerializedName("CAND_ELECTION_YR") val electionYear: Int?,
    @SerializedName("CAND_OFFICE_ST") val state: String?,
    @SerializedName("office_display") val office: String?,
    @SerializedName("total_contributions") val totalContributions: Double?
)