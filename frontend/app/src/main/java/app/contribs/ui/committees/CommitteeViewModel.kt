package app.contribs.ui.committees

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import app.contribs.data.model.Committees
import app.contribs.ui.navigation.ContribsScreen
import kotlinx.coroutines.launch

class CommitteeViewModel : ViewModel() {
    private val _committees = MutableStateFlow<List<ContribsScreen.Committees>>(emptyList())
    val committees: StateFlow<List<ContribsScreen.Committees>> = _committees

    init {
        fetchCommittees()
    }

    private fun fetchCommittees() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.instance.getCommittees()
                _committees.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }

        }

    }

    // Add this function to find a specific candidate for the detail screen
    fun getCommitteesById(id: String): ContribsScreen.Committees? {
        return _committees.value.find { it.id == id }
    }
}