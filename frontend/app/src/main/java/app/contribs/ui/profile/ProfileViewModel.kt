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
    val favoriteCandidates: StateFlow<List<Candidate>> = _favoriteCandidates

    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading

    fun loadFavorites() {
        viewModelScope.launch {
            _isLoading.value = true
            val favoriteIds = favoritesManager.getFavorites()
            val candidates = mutableListOf<Candidate>()
            
            favoriteIds.forEach { id ->
                try {
                    val candidate = apiService.getCandidateDetail(id)
                    candidates.add(candidate)
                } catch (_: Exception) {
                    // Handle or log error
                }
            }
            
            _favoriteCandidates.value = candidates
            _isLoading.value = false
        }
    }
}
