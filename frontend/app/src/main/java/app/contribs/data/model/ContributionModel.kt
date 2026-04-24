package app.contribs.data.model

import com.google.gson.annotations.SerializedName

data class ContributorDetail(
    @SerializedName("id") val id: Int,
    @SerializedName("full_name") val fullName: String?,
    @SerializedName("zip_code") val zipCode: String?,
    @SerializedName("employer_name") val employerName: String?
) {
val formattedName: String
    get() {
        val prefixes = listOf("MR", "MR.", "MRS", "MRS.", "MS", "MS.", "DR", "DR.", "HON", "HON.", "REV", "REV.")
        val suffixes = listOf("JR", "JR.", "SR", "SR.", "II", "III", "MD", "M.D.", "PHD", "PHD.")

        val parts = (fullName ?: return "Unknown").split(",", limit = 2)
        val lastNameString = parts[0]
        val restOfTheName = if (parts.size > 1) parts[1].replace(",", " ") else ""
        val allWords = (restOfTheName + " " + lastNameString).split(" ")

        val finalNames = mutableListOf<String>()
        var foundSuffix = ""

        for (word in allWords) {
            val cleanWord = word.trim()
            if (cleanWord.isEmpty()) continue
            val upperWord = cleanWord.uppercase()

            if (prefixes.contains(upperWord)) {
            } else if (suffixes.contains(upperWord)) {
                foundSuffix = upperWord
            } else {
                finalNames.add(cleanWord.lowercase().replaceFirstChar { it.uppercase() })
            }
        }

        if (foundSuffix.isNotEmpty()) finalNames.add(foundSuffix)

        return finalNames.joinToString(" ")
    }
}

data class CommitteeDetail(
    @SerializedName("CMTE_ID") val cmteId: String?,
    @SerializedName("CMTE_NM") val name: String?,
    @SerializedName("CMTE_TP") val type: String?,
    @SerializedName("CAND_ID") val candidateId: String?,
    @SerializedName("candidate_name") val candidateName: String?,
    @SerializedName("TRES_NM") val treasurerName: String?,
    @SerializedName("total_contributions") val totalContributions: Double?
)

data class Contribution(
    @SerializedName("id") val id: Int,
    @SerializedName("amount") val amount: Double?,
    @SerializedName("receipt_date") val receiptDate: String?,
    @SerializedName("contributor") val contributorId: Int?,
    @SerializedName("committee") val committeeId: String?,
    @SerializedName("contributor_detail") val contributorDetail: ContributorDetail?,
    @SerializedName("committee_detail") val committeeDetail: CommitteeDetail?,
    @SerializedName("fec_sub_id") val fecSubId: String?
)