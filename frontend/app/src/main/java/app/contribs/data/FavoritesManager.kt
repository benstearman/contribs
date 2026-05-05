package app.contribs.data

import android.content.Context
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken

class FavoritesManager(context: Context) {
    private val prefs = context.getSharedPreferences("contribs_prefs", Context.MODE_PRIVATE)
    private val gson = Gson()
    private val KEY_FAVORITES = "favorite_candidate_ids"

    fun getFavorites(): List<String> {
        val json = prefs.getString(KEY_FAVORITES, null) ?: return emptyList()
        val type = object : TypeToken<List<String>>() {}.type
        return try {
            gson.fromJson(json, type)
        } catch (e: Exception) {
            emptyList()
        }
    }

    fun toggleFavorite(candidateId: String) {
        val current = getFavorites().toMutableList()
        if (current.contains(candidateId)) {
            current.remove(candidateId)
        } else {
            current.add(candidateId)
        }
        saveFavorites(current)
    }

    fun isFavorite(candidateId: String): Boolean {
        return getFavorites().contains(candidateId)
    }

    private fun saveFavorites(favorites: List<String>) {
        val json = gson.toJson(favorites)
        prefs.edit().putString(KEY_FAVORITES, json).apply()
    }
}
