package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class TopContributorsResponse(
    @SerializedName("top_individuals") val topIndividuals: List<ContributorSummary>,
    @SerializedName("top_employers") val topEmployers: List<EmployerSummary>
)

data class ContributorSummary(
    val name: String,
    val total: Double,
    @SerializedName("employer_name") val employerName: String?
)

data class EmployerSummary(
    val name: String,
    val total: Double
)
