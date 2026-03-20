package app.contribs.ui.candidates

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Candidate
import app.contribs.data.model.Committee
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class CandidateViewModel : ViewModel() {

    private val _candidates = MutableStateFlow<List<Candidate>>(emptyList())
    val candidates: StateFlow<List<Candidate>> = _candidates

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery

    // Pagination state variables
    private var currentPage = 1
    private var isLastPage = false
    var isLoading = false // Prevents duplicate API calls while loading

    private val _selectedCandidate = MutableStateFlow<Candidate?>(null)
    val selectedCandidate: StateFlow<Candidate?> = _selectedCandidate

    private val _candidateCommittees = MutableStateFlow<List<Committee>>(emptyList())
    val candidateCommittees: StateFlow<List<Committee>> = _candidateCommittees

    private var searchJob: Job? = null

    init {
        loadNextPage() // Fetch the first page when the screen opens
    }

    fun onSearchQueryChange(newQuery: String) {
        _searchQuery.value = newQuery
        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(500) // Debounce search to avoid too many API calls
            currentPage = 1
            isLastPage = false
            loadNextPage()
        }
    }

    fun loadNextPage() {
        // Stop if we are already fetching data, or if there is no more data to fetch
        if (isLoading || isLastPage) return

        isLoading = true
        viewModelScope.launch {
            try {
                // Fetch the specific page with search query
                val response = RetrofitClient.instance.getCandidates(
                    page = currentPage,
                    search = _searchQuery.value.ifBlank { null }
                )

                // If it's the first page, replace results. Otherwise, append.
                if (currentPage == 1) {
                    _candidates.value = response.results
                } else {
                    _candidates.value = _candidates.value + response.results
                }

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

    fun fetchCommitteesForCandidate(candidateId: String) {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.instance.getCandidateCommittees(candidateId)
                _candidateCommittees.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
