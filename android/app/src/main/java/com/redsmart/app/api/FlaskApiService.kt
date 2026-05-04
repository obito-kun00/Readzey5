package com.redsmart.app.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*

interface FlaskApiService {
    @GET("api/books")
    suspend fun getBooks(): BookResponse

    @GET("api/book/{id}")
    suspend fun getBookDetails(@Path("id") id: Int): Book

    @POST("api/login")
    suspend fun login(@Body credentials: Map<String, String>): LoginResponse

    @POST("api/register")
    suspend fun register(@Body data: Map<String, String>): LoginResponse

    @GET("api/profile/{user_id}")
    suspend fun getProfile(@Path("user_id") userId: Int): ProfileResponse

    @GET("api/friends/{user_id}")
    suspend fun getFriends(@Path("user_id") userId: Int): FriendsResponse

    @GET("api/search_users")
    suspend fun searchUsers(@Query("q") query: String): Map<String, List<Friend>>

    @POST("api/send_friend_request")
    suspend fun sendFriendRequest(@Body data: Map<String, Int>): Map<String, Any>

    @POST("api/accept_friend_request/{request_id}")
    suspend fun acceptFriendRequest(@Path("request_id") requestId: Int): Map<String, Any>

    @POST("api/invite_to_read")
    suspend fun inviteToRead(@Body data: Map<String, Int>): Map<String, Any>

    @POST("api/accept_invite/{invite_id}")
    suspend fun acceptInvite(@Path("invite_id") invite_id: Int): Map<String, Any>

    @GET("api/get_info")
    suspend fun getAppInfo(): Map<String, String>
}

object RetrofitClient {
    private const val BASE_URL = "http://10.0.2.2:8000/"

    val instance: FlaskApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(FlaskApiService::class.java)
    }
}
