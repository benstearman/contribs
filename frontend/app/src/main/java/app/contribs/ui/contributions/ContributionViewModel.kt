package app.contribs.ui.contributions

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Contribution
import app.contribs.ui.navigation.ContribsScreen
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class CommitteeViewModel : ViewModel() {
    private val _comm = MutableStateFlow<List<Contribution>>(emptyList())
    val committees: StateFlow<List<ContribsScreen.Contributions>> = _contributions

    init {
        fetchContributions()
    }

    private fun fetchContributions() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.instance.getContributions()
                _contributions.value = response
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    // Add this function to find a specific committee for the detail screen
    fun getCommitteeById(id: String): Contribution? {
        return _contributions.value.find { it.id == id }
    }
}
