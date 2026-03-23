package app.contribs.ui.elections

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.ElectionSummary
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class ElectionViewModel : ViewModel() {
    private val _summary = MutableStateFlow<ElectionSummary?>(null)
    val summary: StateFlow<ElectionSummary?> = _summary.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    init {
        fetchSummary()
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
}