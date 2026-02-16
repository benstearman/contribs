package app.contribs.data.model

data class Candidate(
    val id: String,
    val name: String,
    val party: String?,
    val state: String?,
    val office: String?
)