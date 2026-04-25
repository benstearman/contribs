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
import kotlinx.coroutines.flow.asStateFlow
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

    private var filterState: String? = null
    private var filterOffice: String? = null
    private var filterYear: Int? = null
    private var isFirstLoad = true

    // Expose whether any filters are active
    private val _isFiltered = MutableStateFlow(false)
    val isFiltered: StateFlow<Boolean> = _isFiltered.asStateFlow()

    init {
        // First load is now handled by setInitialFilters to coordinate with navigation args
    }

    private fun sanitize(value: String?): String? {
        return value?.takeIf { it.isNotEmpty() && !it.startsWith("{") }
    }

    fun setInitialFilters(state: String?, office: String?, year: Int?) {
        val sState = sanitize(state)
        val sOffice = sanitize(office)
        val sYear = year?.takeIf { it != 0 }

        if (isFirstLoad || filterState != sState || filterOffice != sOffice || filterYear != sYear) {
            isFirstLoad = false
            filterState = sState
            filterOffice = sOffice
            filterYear = sYear
            _isFiltered.value = filterState != null || filterOffice != null || filterYear != null
            currentPage = 1
            isLastPage = false
            _candidates.value = emptyList()
            loadNextPage()
        }
    }
    fun clearFilters() {
        filterState = null
        filterOffice = null
        filterYear = null
        _searchQuery.value = ""
        _isFiltered.value = false
        currentPage = 1
        isLastPage = false
        _candidates.value = emptyList()
        loadNextPage()
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
                // Fetch the specific page with search query and filters
                val response = RetrofitClient.instance.getCandidates(
                    page = currentPage,
                    search = _searchQuery.value.ifBlank { null },
                    state = filterState,
                    office = filterOffice,
                    year = filterYear
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
