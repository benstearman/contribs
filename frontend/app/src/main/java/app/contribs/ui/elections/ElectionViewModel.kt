package app.contribs.ui.elections

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Election
import app.contribs.data.model.ElectionSummary
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ElectionViewModel : ViewModel() {
    private val _summary = MutableStateFlow<ElectionSummary?>(null)
    val summary: StateFlow<ElectionSummary?> = _summary.asStateFlow()

    private val _elections = MutableStateFlow<List<Election>>(emptyList())
    val elections: StateFlow<List<Election>> = _elections.asStateFlow()

    private val _selectedState = MutableStateFlow("")
    val selectedState: StateFlow<String> = _selectedState.asStateFlow()

    private val _selectedOffice = MutableStateFlow("")
    val selectedOffice: StateFlow<String> = _selectedOffice.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    init {
        fetchSummary()
    }

    fun onStateChange(state: String) {
        _selectedState.value = state
        fetchElections()
    }

    fun onOfficeChange(office: String) {
        _selectedOffice.value = office
        fetchElections()
    }

    private fun fetchSummary() {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                _summary.value = RetrofitClient.instance.getElectionSummary()
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                _isLoading.value = false
            }
        }
    }

    private fun fetchElections() {
        if (_selectedState.value.isEmpty() && _selectedOffice.value.isEmpty()) {
            _elections.value = emptyList()
            return
        }

        viewModelScope.launch {
            try {
                _isLoading.value = true
                _elections.value = RetrofitClient.instance.getElections(
                    state = _selectedState.value.ifEmpty { null },
                    office = _selectedOffice.value.ifEmpty { null }
                )
            } catch (e: Exception) {
                e.printStackTrace()
            } finally {
                _isLoading.value = false
            }
        }
    }
}