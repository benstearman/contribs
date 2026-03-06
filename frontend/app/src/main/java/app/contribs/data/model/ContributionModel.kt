package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Contribution(
    @SerializedName("id") val id: Int,
    @SerializedName("amount") val amount: Int?,
    @SerializedName("receipt_date") val receiptDate: String?
)