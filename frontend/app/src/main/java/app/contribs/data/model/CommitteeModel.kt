package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class Committee(
    @SerializedName("CMTE_ID") val id: String,
    @SerializedName("CMTE_NM") val name: String,
    @SerializedName("CMTE_ST") val state: String?,
    @SerializedName("CMTE_TYPE") val type: String?,
    @SerializedName("CMTE_PTY_AFFILIATION") val party: String?
)