package app.contribs.data.api

import app.contribs.data.model.Candidate
import app.contribs.data.model.CandidateFilters
import app.contribs.data.model.Committee
import app.contribs.data.model.Contribution
import app.contribs.data.model.Election
import app.contribs.data.model.ElectionSummary
import app.contribs.data.model.PaginatedResponse
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

// 1. Define the endpoints that match your Django urls.py
interface ContribsApiService {
    @GET("candidates/")
    suspend fun getCandidates(
        @Query("page") page: Int = 1,
        @Query("search") search: String? = null,
        @Query("state") state: String? = null,
        @Query("office") office: String? = null,
        @Query("year") year: Int? = null
    ): PaginatedResponse<Candidate>

    @GET("candidates/filters/")
    suspend fun getCandidateFilters(): CandidateFilters

    @GET("candidates/{id}/")
    suspend fun getCandidateDetail(@Path("id") id: String): Candidate

    @GET("candidates/{id}/committees/")
    suspend fun getCandidateCommittees(@Path("id") id: String): List<Committee>

    @GET("committees/")
    suspend fun getCommittees(@Query("page") page: Int = 1): PaginatedResponse<Committee>

    @GET("committees/{id}/")
    suspend fun getCommitteeDetail(@Path("id") id: String): Committee

    @GET("contributions/")
    suspend fun getContributions(
        @Query("page") page: Int = 1,
        @Query("search") search: String? = null
    ): PaginatedResponse<Contribution>

    @GET("contributions/{id}/")
    suspend fun getContributionDetail(@Path("id") id: String): Contribution

    @GET("elections/summary/")
    suspend fun getElectionSummary(): ElectionSummary

    @GET("elections/list/")
    suspend fun getElections(
        @Query("state") state: String? = null,
        @Query("office") office: String? = null
    ): List<Election>
}

// 2. Build the Retrofit instance
object RetrofitClient {
    // 10.0.2.2 is the magic IP that tells the Android Emulator
    // to connect to the computer's localhost (where Django is running)
    private const val BASE_URL = "https://contribs.app/api/"

    private val okHttpClient = OkHttpClient.Builder()
        .connectTimeout(60, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .writeTimeout(60, TimeUnit.SECONDS)
        .build()

    val instance: ContribsApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttpClient)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ContribsApiService::class.java)
    }
}