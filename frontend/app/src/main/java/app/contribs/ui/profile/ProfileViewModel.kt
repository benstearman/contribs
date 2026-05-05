package app.contribs.ui.profile

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import app.contribs.data.FavoritesManager
import app.contribs.data.api.RetrofitClient
import app.contribs.data.model.Candidate
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ProfileViewModel(application: Application) : AndroidViewModel(application) {
    private val favoritesManager = FavoritesManager(application)
    private val apiService = RetrofitClient.instance

    private val _favoriteCandidates = MutableStateFlow<List<Candidate>>(emptyList())
    /** List of candidates favorited by the user */
    val favoriteCandidates: StateFlow<List<Candidate>> = _favoriteCandidates

    private val _isLoading = MutableStateFlow(false)
    /** Loading state for the favorites list */
    val isLoading: StateFlow<Boolean> = _isLoading

    /**
     * Fetches details for all candidate IDs stored in the favorites manager.
     */
    fun loadFavorites() {
        viewModelScope.launch {
            _isLoading.value = true
            try {
                val favoriteIds = favoritesManager.getFavorites()
                val candidates = mutableListOf<Candidate>()
                
                // Fetch details for each favorite candidate in parallel or sequence
                // Sequencing here to avoid overwhelming the API if many favorites exist
                favoriteIds.forEach { id ->
                    try {
                        val candidate = apiService.getCandidateDetail(id)
                        candidates.add(candidate)
                    } catch (_: Exception) {
                        // If one fails, we still want to show the others
                    }
                }
                
                _favoriteCandidates.value = candidates
            } finally {
                _isLoading.value = false
            }
        }
    }
}
