package app.contribs.data.api

import app.contribs.data.model.Candidate
import app.contribs.data.model.Committee
import app.contribs.data.model.Contribution
import app.contribs.data.model.PaginatedResponse
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path

// 1. Define the endpoints that match your Django urls.py
interface ContribsApiService {
    @GET("candidates/")
    suspend fun getCandidates(): PaginatedResponse<Candidate>

    @GET("candidates/{id}/")
    suspend fun getCandidateDetail(@Path("id") id: String): Candidate

    @GET("committees/")
    suspend fun getCommittees(): PaginatedResponse<Committee>

    @GET("committees/{id}/")
    suspend fun getCommitteeDetail(@Path("id") id: String): Committee

    @GET("contributions/")
    suspend fun getContributions(): PaginatedResponse<Contribution>

    @GET("contributions/{id}/")
    suspend fun getContributionDetail(@Path("id") id: String): Contribution
}

// 2. Build the Retrofit instance
object RetrofitClient {
    // 10.0.2.2 is the magic IP that tells the Android Emulator
    // to connect to the computer's localhost (where Django is running)
    private const val BASE_URL = "https://contribs.app/api/"

    val instance: ContribsApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ContribsApiService::class.java)
    }
}