package app.contribs.ui.contributions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Contribution
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ContributionViewModel : ViewModel() {

    private val api = RetrofitClient.instance

    // Full list from API
    private val _contributions = MutableStateFlow<List<Contribution>>(emptyList())

    // What actually gets displayed (filtered)
    private val _filteredContributions = MutableStateFlow<List<Contribution>>(emptyList())
    val filteredContributions: StateFlow<List<Contribution>> = _filteredContributions

    // Loading/error state
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    // Pagination
    private var currentPage = 1
    private var hasNextPage = true

    // Filter state
    private val _selectedParty = MutableStateFlow<String?>(null)
    val selectedParty: StateFlow<String?> = _selectedParty

    private val _selectedOffice = MutableStateFlow<String?>(null)
    val selectedOffice: StateFlow<String?> = _selectedOffice
    private val _selectedContribution = MutableStateFlow<Contribution?>(null)
    val selectedContribution: StateFlow<Contribution?> = _selectedContribution

    fun fetchContributionDetail(id: Int) {
        viewModelScope.launch {
            try {
                val contribution = api.getContributionDetail(id.toString())
                _selectedContribution.value = contribution
            } catch (e: Exception) {
                _error.value = "Failed to load contribution detail"
                e.printStackTrace()
            }
        }
    }

    init {
        fetchContributions()
    }

    fun fetchContributions(loadMore: Boolean = false) {
        if (_isLoading.value || !hasNextPage) return

        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            try {
                if (!loadMore) {
                    currentPage = 1
                    hasNextPage = true
                }

                val response = api.getContributions(page = currentPage)

                val updated = if (loadMore) {
                    _contributions.value + response.results
                } else {
                    response.results
                }

                _contributions.value = updated
                hasNextPage = response.next != null
                if (hasNextPage) currentPage++

                applyFilters()

            } catch (e: Exception) {
                _error.value = "Failed to load contributions"
                e.printStackTrace()
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun setPartyFilter(party: String?) {
        _selectedParty.value = if (_selectedParty.value == party) null else party
        applyFilters()
    }

    fun setOfficeFilter(office: String?) {
        _selectedOffice.value = if (_selectedOffice.value == office) null else office
        applyFilters()
    }

    fun clearFilters() {
        _selectedParty.value = null
        _selectedOffice.value = null
        applyFilters()
    }

    fun getContributionById(id: Int): Contribution? {
        return _contributions.value.find { it.id == id }
    }

    private fun applyFilters() {
        // Placeholder until we confirm party/office fields at runtime
        _filteredContributions.value = _contributions.value
    }
}