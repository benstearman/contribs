package app.contribs.ui.candidates

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Candidate
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class CandidateViewModel : ViewModel() {

    private val _candidates = MutableStateFlow<List<Candidate>>(emptyList())
    val candidates: StateFlow<List<Candidate>> = _candidates

    // Pagination state variables
    private var currentPage = 1
    private var isLastPage = false
    var isLoading = false // Prevents duplicate API calls while loading

    private val _selectedCandidate = MutableStateFlow<Candidate?>(null)
    val selectedCandidate: StateFlow<Candidate?> = _selectedCandidate
    init {
        fetchCandidates()
        loadNextPage() // Fetch the first page when the screen opens
    }

    fun loadNextPage() {
        // Stop if we are already fetching data, or if there is no more data to fetch
        if (isLoading || isLastPage) return

        isLoading = true
        viewModelScope.launch {
            try {
                // Fetch the specific page
                val response = RetrofitClient.instance.getCandidates(currentPage)

                // Append the new results to the existing list
                _candidates.value = _candidates.value + response.results

                // Check if Django says there is another page
                if (response.next == null) {
                    isLastPage = true
                } else {
                    currentPage++
                }
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                isLoading = false // Done loading, unlock for the next scroll
            }
        }
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