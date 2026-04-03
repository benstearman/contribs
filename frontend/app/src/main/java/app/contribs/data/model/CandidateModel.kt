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
) {
    val formattedName: String
        get() {
            val prefixes = listOf("MR", "MR.", "MRS", "MRS.", "MS", "MS.", "DR", "DR.", "HON", "HON.", "REV", "REV.")
            val suffixes = listOf("JR", "JR.", "SR", "SR.", "II", "III", "MD", "M.D.", "PHD", "PHD.")

            val parts = name.split(",", limit = 2)
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
                    val formatted = cleanWord.lowercase().replaceFirstChar { it.uppercase() }
                    finalNames.add(formatted)
                }
            }

            if (foundSuffix.isNotEmpty()) {
                finalNames.add(foundSuffix)
            }


            return finalNames.joinToString(" ")
        }
}