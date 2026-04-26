package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Election(
    @SerializedName("year") val year: Int?,
    @SerializedName("state") val state: String?,
    @SerializedName("office") val office: String?,
    @SerializedName("total_amount") val totalAmount: Double?
)
