package app.contribs.ui.committees

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Committee
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class CommitteeViewModel : ViewModel() {
    private val _committees = MutableStateFlow<List<Committee>>(emptyList())
    val committees: StateFlow<List<Committee>> = _committees

    init {
        fetchCommittees()
    }

    private fun fetchCommittees() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.instance.getCommittees()
                _committees.value = response.results
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Add this function to find a specific committee for the detail screen
    fun getCommitteeById(id: String): Committee? {
        return _committees.value.find { it.id == id }
    }
}
