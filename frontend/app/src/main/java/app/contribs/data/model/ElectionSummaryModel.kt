package app.contribs.data.model
import com.google.gson.annotations.SerializedName

data class TopEntity(
    @SerializedName("name") val name: String,
    @SerializedName("total") val total: Double
)

data class ElectionSummary(
    @SerializedName("top_employers") val topEmployers: List<TopEntity>,
    @SerializedName("top_contributors") val topContributors: List<TopEntity>
)