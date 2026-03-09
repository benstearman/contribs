package app.contribs.ui.candidates

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import app.contribs.data.model.Candidate
import kotlinx.coroutines.launch

class CandidateViewModel : ViewModel() {
    private val _candidates = MutableStateFlow<List<Candidate>>(emptyList())
    val candidates: StateFlow<List<Candidate>> = _candidates

    private val _selectedCandidate = MutableStateFlow<Candidate?>(null)
    val selectedCandidate: StateFlow<Candidate?> = _selectedCandidate


    init {
        fetchCandidates()
    }

    private fun fetchCandidates() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.instance.getCandidates()
                _candidates.value = response.results
            } catch (e: Exception) {
                e.printStackTrace()
            }

        }

    }

    fun fetchCandidateDetail(id: String) {
        viewModelScope.launch {
            try {
                val candidate = RetrofitClient.instance.getCandidateDetail(id)
                _selectedCandidate.value = candidate
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
