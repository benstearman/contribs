package app.contribs.ui.candidates

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import app.contribs.data.model.Candidate

class CandidateViewModel : ViewModel() {
    private val _candidates = MutableStateFlow<List<Candidate>>(
        listOf(
            Candidate("P00000001", "Bernie Sanders", "DEM", "VT", "P"),
            Candidate("P00000002", "Donald Trump", "REP", "FL", "P"),
        )
    )
    val candidates: StateFlow<List<Candidate>> = _candidates
}