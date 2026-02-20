package app.contribs.data.api

import app.contribs.data.model.Candidate
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

// 1. Define the endpoints that match your Django urls.py
interface ContribsApiService {
    @GET("api/candidates/")
    suspend fun getCandidates(): List<Candidate>

    @GET("api/candidates/{id}/")
    suspend fun getCandidateDetail(@Path("id") id: String): Candidate
}

// 2. Build the Retrofit instance
object RetrofitClient {
    // 10.0.2.2 is the magic IP that tells the Android Emulator
    // to connect to the computer's localhost (where Django is running)
    private const val BASE_URL = "http://10.0.2.2:8000/"

    val instance: ContribsApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ContribsApiService::class.java)
    }
}