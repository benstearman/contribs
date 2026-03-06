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

    // Add this function to find a specific candidate for the detail screen
    fun getCandidateById(id: String): Candidate? {
        return _candidates.value.find { it.id == id }
    }
}