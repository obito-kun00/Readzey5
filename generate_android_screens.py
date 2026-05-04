import os

root_dir = r"c:\Users\Yug\Downloads\Redsmart\Redsmart\RedsmartAndroid"

screens_dir = os.path.join(root_dir, "app/src/main/java/com/redsmart/app/ui/screens")
api_dir = os.path.join(root_dir, "app/src/main/java/com/redsmart/app/api")

# Ensure directories exist
os.makedirs(screens_dir, exist_ok=True)
os.makedirs(api_dir, exist_ok=True)

# 1. Provide the complete API Client
api_content = """package com.redsmart.app.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Body
import retrofit2.http.Multipart
import retrofit2.http.Part
import okhttp3.MultipartBody
import okhttp3.RequestBody

data class AuthRequest(val email: String, val password: String, val username: String? = null)
data class AuthResponse(val success: Boolean, val token: String?, val message: String?)

data class Book(val id: Int, val title: String, val author: String, val description: String, val cover_url: String?)
data class BookResponse(val books: List<Book>)

interface FlaskApiService {
    @POST("api/login")
    suspend fun login(@Body req: AuthRequest): AuthResponse

    @POST("api/register")
    suspend fun register(@Body req: AuthRequest): AuthResponse

    @GET("api/books")
    suspend fun getBooks(): BookResponse
    
    @Multipart
    @POST("api/admin/upload")
    suspend fun uploadBook(
        @Part("title") title: RequestBody,
        @Part("author") author: RequestBody,
        @Part cover: MultipartBody.Part,
        @Part pdf: MultipartBody.Part
    ): AuthResponse
}

object RetrofitClient {
    private const val BASE_URL = "http://10.0.2.2:8000/"
    val instance: FlaskApiService by lazy {
        Retrofit.Builder().baseUrl(BASE_URL).addConverterFactory(GsonConverterFactory.create()).build().create(FlaskApiService::class.java)
    }
}
"""

# 2. Auth Screens
auth_content = """package com.redsmart.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.redsmart.app.api.AuthRequest
import com.redsmart.app.api.RetrofitClient
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(navController: NavController) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()

    Column(modifier = Modifier.fillMaxSize().padding(16.dp), verticalArrangement = Arrangement.Center) {
        Text("Login to Redsmart", style = MaterialTheme.typography.headlineMedium, color = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = email, onValueChange = { email = it }, label = { Text("Email") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(value = password, onValueChange = { password = it }, label = { Text("Password") }, visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = {
            scope.launch {
                try {
                    val res = RetrofitClient.instance.login(AuthRequest(email, password))
                    if (res.success) { navController.navigate("home") } else { message = res.message ?: "Failed" }
                } catch(e: Exception) { message = "Network Error" }
            }
        }, modifier = Modifier.fillMaxWidth()) { Text("Login") }
        if (message.isNotEmpty()) { Text(message, color = MaterialTheme.colorScheme.error) }
    }
}
"""

# 3. Admin Screens
admin_content = """package com.redsmart.app.ui.screens

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import com.redsmart.app.api.RetrofitClient
import kotlinx.coroutines.launch

@Composable
fun AdminScreen() {
    var title by remember { mutableStateOf("") }
    var author by remember { mutableStateOf("") }
    var coverUri by remember { mutableStateOf<Uri?>(null) }
    var pdfUri by remember { mutableStateOf<Uri?>(null) }
    val scope = rememberCoroutineScope()

    val coverLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? -> coverUri = uri }
    val pdfLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? -> pdfUri = uri }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Admin Dashboard", style = MaterialTheme.typography.headlineMedium, color = MaterialTheme.colorScheme.secondary)
        Spacer(modifier = Modifier.height(16.dp))
        OutlinedTextField(value = title, onValueChange = { title = it }, label = { Text("Book Title") }, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(value = author, onValueChange = { author = it }, label = { Text("Author Name") }, modifier = Modifier.fillMaxWidth())
        Spacer(modifier = Modifier.height(8.dp))
        
        Button(onClick = { coverLauncher.launch("image/*") }) { Text("Select Cover Image = ${if (coverUri!=null) "Selected" else "None"}") }
        Button(onClick = { pdfLauncher.launch("application/pdf") }) { Text("Select PDF File = ${if (pdfUri!=null) "Selected" else "None"}") }
        
        Spacer(modifier = Modifier.height(16.dp))
        Button(onClick = { /* In production: Convert local URI to MultipartBody and send via RetrofitClient */ }, modifier = Modifier.fillMaxWidth()) {
            Text("Upload New Book to Flask DataBase")
        }
    }
}
"""

with open(os.path.join(api_dir, "FlaskApiService.kt"), "w") as f:
    f.write(api_content)
with open(os.path.join(screens_dir, "AuthScreens.kt"), "w") as f:
    f.write(auth_content)
with open(os.path.join(screens_dir, "AdminScreens.kt"), "w") as f:
    f.write(admin_content)

print("SUCCESS: Full suite of compose screens dynamically generated!")
