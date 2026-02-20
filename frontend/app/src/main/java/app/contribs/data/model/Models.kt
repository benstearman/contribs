package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Candidate(
    @SerializedName("CAND_ID") val id: String,
    @SerializedName("CAND_NAME") val name: String,
    @SerializedName("CAND_PTY_AFFILIATION") val party: String?,
    @SerializedName("CAND_ELECTION_YR") val electionYear: Int?,
    @SerializedName("CAND_OFFICE_ST") val state: String?,
    @SerializedName("CAND_OFFICE") val office: String?
)

// You can add Committee and Contribution models here later!