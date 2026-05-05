package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class CandidateFilters(
    @SerializedName("states") val states: List<String>,
    @SerializedName("offices") val offices: List<OfficeOption>
)

data class OfficeOption(
    @SerializedName("id") val id: String,
    @SerializedName("name") val name: String
)
