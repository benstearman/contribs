package app.contribs.ui.contributions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Contribution
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

enum class AmountFilter { ALL, SMALL, MEDIUM, LARGE, XLARGE }

class ContributionViewModel : ViewModel() {

    private val api = RetrofitClient.instance

    private val _contributions = MutableStateFlow<List<Contribution>>(emptyList())

    private val _filteredContributions = MutableStateFlow<List<Contribution>>(emptyList())
    val filteredContributions: StateFlow<List<Contribution>> = _filteredContributions

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error

    private var currentPage = 1
    private var hasNextPage = true

    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery

    private val _selectedParty = MutableStateFlow<String?>(null)
    val selectedParty: StateFlow<String?> = _selectedParty

    private val _selectedOffice = MutableStateFlow<String?>(null)
    val selectedOffice: StateFlow<String?> = _selectedOffice

    private val _selectedContribution = MutableStateFlow<Contribution?>(null)
    val selectedContribution: StateFlow<Contribution?> = _selectedContribution

    private val _selectedAmount = MutableStateFlow(AmountFilter.ALL)
    val selectedAmount: StateFlow<AmountFilter> = _selectedAmount

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
        if (_isLoading.value || (!hasNextPage && loadMore)) return

        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null

            try {
                if (!loadMore) {
                    currentPage = 1
                    hasNextPage = true
                    _contributions.value = emptyList() // Clear for fresh search
                }

                val response = api.getContributions(
                    page = currentPage,
                    search = _searchQuery.value.takeIf { it.isNotEmpty() }
                )

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

    fun setAmountFilter(filter: AmountFilter) {
        _selectedAmount.value = if (_selectedAmount.value == filter) AmountFilter.ALL else filter
        applyFilters()
    }

    fun setPartyFilter(party: String?) {
        _selectedParty.value = if (_selectedParty.value == party) null else party
        applyFilters()
    }

    fun setOfficeFilter(office: String?) {
        _selectedOffice.value = if (_selectedOffice.value == office) null else office
        applyFilters()
    }

    fun setSearchQuery(query: String) {
        _searchQuery.value = query
        fetchContributions(loadMore = false)
    }

    fun clearFilters() {
        _selectedParty.value = null
        _selectedOffice.value = null
        _searchQuery.value = ""
        _selectedAmount.value = AmountFilter.ALL
        applyFilters()
    }

    fun getContributionById(id: Int): Contribution? {
        return _contributions.value.find { it.id == id }
    }

    private fun applyFilters() {
        var result = _contributions.value

        val query = _searchQuery.value.lowercase()
        if (query.isNotEmpty()) {
            result = result.filter {
                it.contributorDetail?.formattedName?.lowercase()?.contains(query) == true ||
                        it.committeeDetail?.name?.lowercase()?.contains(query) == true
            }
        }

        result = when (_selectedAmount.value) {
            AmountFilter.SMALL -> result.filter { (it.amount ?: 0.0) < 500.0 }
            AmountFilter.MEDIUM -> result.filter { (it.amount ?: 0.0) in 500.0..2000.0 }
            AmountFilter.LARGE -> result.filter { (it.amount ?: 0.0) in 2000.0..5000.0 }
            AmountFilter.XLARGE -> result.filter { (it.amount ?: 0.0) > 10000.0 }
            AmountFilter.ALL -> result
        }

       _filteredContributions.value = _contributions.value
    }
}