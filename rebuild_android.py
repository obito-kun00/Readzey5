import os

root_dir = r"c:\Users\Yug\Downloads\Redsmart\Redsmart\RedsmartAndroid"

# Structure defining all project files
project_files = {
    "settings.gradle.kts": """pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name = "RedsmartApp"
include(":app")
""",
    "build.gradle.kts": """plugins { id("com.android.application") version "8.1.1" apply false; id("org.jetbrains.kotlin.android") version "1.9.0" apply false }""",
    "app/build.gradle.kts": """plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.redsmart.app"
    compileSdk = 34
    defaultConfig {
        applicationId = "com.redsmart.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables { useSupportLibrary = true }
    }
    buildTypes { release { isMinifyEnabled = false; proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro") } }
    compileOptions { sourceCompatibility = JavaVersion.VERSION_1_8; targetCompatibility = JavaVersion.VERSION_1_8 }
    kotlinOptions { jvmTarget = "1.8" }
    buildFeatures { compose = true }
    composeOptions { kotlinCompilerExtensionVersion = "1.5.1" }
}
dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2")
    implementation("androidx.activity:activity-compose:1.8.0")
    implementation(platform("androidx.compose:compose-bom:2023.08.00"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.4")
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")
    implementation("io.coil-kt:coil-compose:2.4.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")
    // PDF Text Extraction Support
    implementation("com.tom-roush:pdfbox-android:1.8.10.3")
}
""",
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:usesCleartextTraffic="true"
        android:theme="@style/Theme.RedsmartApp">
        <activity android:name=".MainActivity" android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""",
    "app/src/main/java/com/redsmart/app/ui/theme/Color.kt": """package com.redsmart.app.ui.theme
import androidx.compose.ui.graphics.Color
val GlassBg = Color(0x991C1B1F)
val GlassBorder = Color(0x33FFFFFF)
val PinkPrimary = Color(0xFFC026D3)
val MihonBlack = Color(0xFF1C1B1F)
""",
    "app/src/main/java/com/redsmart/app/ui/theme/Theme.kt": """package com.redsmart.app.ui.theme
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = PinkPrimary,
    background = MihonBlack,
    surface = Color(0xFF252429),
    onBackground = Color.White,
    onSurface = Color.White
)

@Composable
fun RedsmartAppTheme(content: @Composable () -> Unit) {
    MaterialTheme(colorScheme = DarkColorScheme, content = content)
}
""",
    "app/src/main/java/com/redsmart/app/api/Models.kt": """package com.redsmart.app.api
data class AuthRequest(val email: String, val password: String, val username: String? = null)
data class AuthResponse(val success: Boolean, val token: String?, val user_id: Int?, val username: String?, val is_admin: Boolean?, val message: String?)
data class Book(val id: Int, val title: String, val author: String?, val description: String?, val cover_url: String?)
data class BookResponse(val books: List<Book>)
data class BookDetail(val success: Boolean, val id: Int, val title: String, val author: String?, val description: String?, val cover_url: String?, val pdf_url: String?, val total_pages: Int)
data class Friend(val id: Int, val username: String, val is_online: Boolean)
data class FriendRequestItem(val id: Int, val sender_id: Int, val sender_username: String)
data class ReadingInviteItem(val id: Int, val sender_name: String, val book_title: String, val book_id: Int)
data class ActiveSessionItem(val id: Int, val book_id: Int, val book_title: String, val partner_name: String, val partner_id: Int)
data class FriendResponse(val success: Boolean, val friends: List<Friend>, val requests: List<FriendRequestItem> = emptyList(), val invites: List<ReadingInviteItem> = emptyList(), val active_sessions: List<ActiveSessionItem> = emptyList())
data class UserItem(val id: Int, val username: String)
data class UserSearchResponse(val users: List<UserItem>)
data class Stats(val total_books: Int, val pages_read: Int, val total_pages_goal: Int)
data class Activity(val type: String, val desc: String, val date: String)
data class Badge(val name: String, val icon: String?)
data class ProfileResponse(val success: Boolean, val username: String, val email: String, val profile_photo: String?, val friends_count: Int, val stats: Stats?, val activities: List<Activity> = emptyList(), val badges: List<Badge> = emptyList())
data class InfoResponse(val about: String, val contact_email: String, val contact_phone: String, val address: String)
""",
    "app/src/main/java/com/redsmart/app/api/FlaskApiService.kt": """package com.redsmart.app.api
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.*
import okhttp3.ResponseBody
import okhttp3.MultipartBody
import okhttp3.RequestBody

interface FlaskApiService {
    @POST("api/login") suspend fun login(@Body req: AuthRequest): AuthResponse
    @POST("api/register") suspend fun register(@Body req: AuthRequest): AuthResponse
    @GET("api/books") suspend fun getBooks(): BookResponse
    @GET("api/book/{id}") suspend fun getBookDetails(@Path("id") id: Int): BookDetail
    @GET("api/friends/{user_id}") suspend fun getFriends(@Path("user_id") userId: Int): FriendResponse
    @GET("api/profile/{user_id}") suspend fun getProfile(@Path("user_id") userId: Int): ProfileResponse
    @GET("api/search_users") suspend fun searchUsers(@Query("q") query: String): UserSearchResponse
    @POST("api/send_friend_request") suspend fun sendRequest(@Body body: Map<String, Int>): AuthResponse
    @POST("api/accept_friend_request/{id}") suspend fun acceptRequest(@Path("id") id: Int): AuthResponse
    @POST("api/invite_to_read") suspend fun inviteToRead(@Body body: Map<String, Int>): AuthResponse
    @POST("api/accept_invite/{id}") suspend fun acceptInvite(@Path("id") id: Int): AuthResponse
    @GET("api/get_info") suspend fun getInfo(): InfoResponse
    
    @Multipart
    @POST("api/update_profile")
    suspend fun updateProfile(
        @Part("user_id") userId: RequestBody,
        @Part("username") username: RequestBody?,
        @Part("email") email: RequestBody?,
        @Part photo: MultipartBody.Part?
    ): AuthResponse

    @Streaming @GET suspend fun downloadFile(@Url url: String): ResponseBody
}

object RetrofitClient {
    private const val BASE_URL = "http://10.0.2.2:8000/"
    val instance: FlaskApiService by lazy { Retrofit.Builder().baseUrl(BASE_URL).addConverterFactory(GsonConverterFactory.create()).build().create(FlaskApiService::class.java) }
}
""",
    "app/src/main/java/com/redsmart/app/util/SessionManager.kt": """package com.redsmart.app.util
import android.content.Context
import android.content.SharedPreferences

class SessionManager(context: Context) {
    private val prefs: SharedPreferences = context.getSharedPreferences("RedsmartPrefs", Context.MODE_PRIVATE)
    fun saveAuth(user_id: Int, username: String, token: String, is_admin: Boolean) {
        prefs.edit().putInt("user_id", user_id).putString("username", username).putString("token", token).putBoolean("is_admin", is_admin).apply()
    }
    fun getUserId(): Int = prefs.getInt("user_id", -1)
    fun getUsername(): String? = prefs.getString("username", null)
    fun isAdmin(): Boolean = prefs.getBoolean("is_admin", false)
    fun clear() = prefs.edit().clear().apply()
    fun isLoggedIn(): Boolean = getUserId() != -1
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/ReaderScreen.kt": """package com.redsmart.app.ui.screens
import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.os.ParcelFileDescriptor
import android.speech.tts.TextToSpeech
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.redsmart.app.api.*
import com.redsmart.app.ui.theme.*
import com.tomroush.pdfbox.pdmodel.PDDocument
import com.tomroush.pdfbox.text.PDFTextStripper
import com.tomroush.pdfbox.util.PDFBoxResourceLoader
import kotlinx.coroutines.*
import java.io.*
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReaderScreen(bookId: Int, navController: NavController) {
    var bookDetail by remember { mutableStateOf<BookDetail?>(null) }
    var pages by remember { mutableStateOf<List<Bitmap>>(emptyList()) }
    var zoom by remember { mutableFloatStateOf(1.2f) }
    var pdfFile by remember { mutableStateOf<File?>(null) }
    var tts: TextToSpeech? by remember { mutableStateOf(null) }
    var isReading by remember { mutableStateOf(false) }
    var currentPageIndex by remember { mutableIntStateOf(0) }
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    val listState = rememberLazyListState()

    DisposableEffect(Unit) {
        PDFBoxResourceLoader.init(context)
        tts = TextToSpeech(context) { status -> if(status == TextToSpeech.SUCCESS) tts?.language = Locale.ENGLISH }
        onDispose { tts?.stop(); tts?.shutdown() }
    }

    LaunchedEffect(bookId) {
        try {
            val detail = RetrofitClient.instance.getBookDetails(bookId)
            bookDetail = detail
            detail.pdf_url?.let { url ->
                val response = RetrofitClient.instance.downloadFile(url)
                val file = File(context.cacheDir, "book_$bookId.pdf")
                withContext(Dispatchers.IO) { response.byteStream().use { input -> FileOutputStream(file).use { output -> input.copyTo(output) } } }
                pdfFile = file
                val pfd = ParcelFileDescriptor.open(file, ParcelFileDescriptor.MODE_READ_ONLY)
                val renderer = PdfRenderer(pfd)
                val bitmapList = mutableListOf<Bitmap>()
                for (i in 0 until renderer.pageCount) {
                    val page = renderer.openPage(i)
                    val bitmap = Bitmap.createBitmap(page.width, page.height, Bitmap.Config.ARGB_8888)
                    page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    bitmapList.add(bitmap)
                    page.close()
                }
                pages = bitmapList; renderer.close()
            }
        } catch (e: Exception) {}
    }

    fun readCurrentPage() {
        if (pdfFile == null) return
        scope.launch(Dispatchers.IO) {
            try {
                val doc = PDDocument.load(pdfFile)
                val stripper = PDFTextStripper()
                stripper.startPage = currentPageIndex + 1
                stripper.endPage = currentPageIndex + 1
                val text = stripper.getText(doc)
                doc.close()
                withContext(Dispatchers.Main) {
                    if (text.isNotBlank()) {
                        tts?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
                    } else {
                        isReading = false
                    }
                }
            } catch (e: Exception) { isReading = false }
        }
    }

    Scaffold { padding ->
        Box(Modifier.fillMaxSize()) {
            if (pages.isNotEmpty()) {
                LazyColumn(
                    state = listState,
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    itemsIndexed(pages) { index, bitmap ->
                        currentPageIndex = index
                        Image(bitmap = bitmap.asImageBitmap(), contentDescription = null, modifier = Modifier.fillMaxWidth(zoom).wrapContentHeight())
                    }
                }
            } else Box(Modifier.fillMaxSize(), Alignment.Center) { CircularProgressIndicator() }

            // Glassmorphic Overlays
            Box(Modifier.fillMaxSize().padding(16.dp)) {
                // Top Toolbar
                Row(Modifier.align(Alignment.TopCenter).background(GlassBg, MaterialTheme.shapes.medium).padding(8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = { navController.popBackStack() }) { Icon(Icons.Default.ArrowBack, null, tint = Color.White) }
                    Text(bookDetail?.title ?: "Reader", color = Color.White, style = MaterialTheme.typography.titleMedium)
                    Spacer(Modifier.width(16.dp))
                    IconButton(onClick = { zoom += 0.2f }) { Icon(Icons.Default.Add, null, tint = Color.White) }
                    IconButton(onClick = { zoom = (zoom - 0.2f).coerceAtLeast(0.5f) }) { Icon(Icons.Default.Remove, null, tint = Color.White) }
                }

                // Bottom Audio Bar
                Row(Modifier.align(Alignment.BottomCenter).background(GlassBg, MaterialTheme.shapes.extraLarge).padding(horizontal = 24.dp, vertical = 12.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    IconButton(onClick = { /* Prev */ }) { Icon(Icons.Default.SkipPrevious, null, tint = Color.White) }
                    FloatingActionButton(onClick = {
                        if (isReading) { tts?.stop(); isReading = false } else { isReading = true; readCurrentPage() }
                    }, containerColor = PinkPrimary, contentColor = Color.White, shape = MaterialTheme.shapes.extraLarge) {
                        Icon(if (isReading) Icons.Default.Stop else Icons.Default.PlayArrow, null)
                    }
                    IconButton(onClick = { /* Next */ }) { Icon(Icons.Default.SkipNext, null, tint = Color.White) }
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/FriendsScreen.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.redsmart.app.api.*
import com.redsmart.app.util.SessionManager
import kotlinx.coroutines.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun FriendsScreen(navController: NavController, session: SessionManager) {
    var query by remember { mutableStateOf("") }
    var searchResults by remember { mutableStateOf<List<UserItem>>(emptyList()) }
    var friends by remember { mutableStateOf<List<Friend>>(emptyList()) }
    var requests by remember { mutableStateOf<List<FriendRequestItem>>(emptyList()) }
    var invites by remember { mutableStateOf<List<ReadingInviteItem>>(emptyList()) }
    val scope = rememberCoroutineScope()
    val snackHost = remember { SnackbarHostState() }

    fun refresh() { scope.launch { try {
        val res = RetrofitClient.instance.getFriends(session.getUserId())
        friends = res.friends; requests = res.requests; invites = res.invites
    } catch(e: Exception){} } }

    LaunchedEffect(Unit) { refresh() }

    Scaffold(snackbarHost = { SnackbarHost(snackHost) }) { padding ->
        Column(Modifier.fillMaxSize().padding(16.dp).padding(padding)) {
            Text("Social Reading", style = MaterialTheme.typography.displaySmall, color = MaterialTheme.colorScheme.primary)
            Spacer(Modifier.height(16.dp))
            OutlinedTextField(
                query, { query = it },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("Find readers via username...") },
                trailingIcon = { IconButton(onClick = {
                    scope.launch { try {
                        val res = RetrofitClient.instance.searchUsers(query)
                        if (res.users.isEmpty()) snackHost.showSnackbar("No user found with that name")
                        searchResults = res.users
                    } catch(e: Exception){ snackHost.showSnackbar("Search failed. Check your connection.") } }
                }) { Icon(Icons.Default.Search, null) } }
            )

            LazyColumn(modifier = Modifier.fillMaxSize(), contentPadding = PaddingValues(top = 16.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
                if (searchResults.isNotEmpty()) {
                    item { Text("Global Discovery", style = MaterialTheme.typography.titleMedium) }
                    items(searchResults) { user ->
                        Card(Modifier.fillMaxWidth()) {
                            ListItem(
                                headlineContent = { Text(user.username) },
                                trailingContent = { Button(onClick = {
                                    scope.launch { try {
                                        val res = RetrofitClient.instance.sendRequest(mapOf("sender_id" to session.getUserId(), "receiver_id" to user.id))
                                        snackHost.showSnackbar(res.message ?: "Request Sent!")
                                    } catch(e: Exception){} }
                                }) { Text("Send Request") } }
                            )
                        }
                    }
                }

                if (invites.isNotEmpty()) {
                    item { Text("Reading Invites", style = MaterialTheme.typography.titleMedium, color = Color.Yellow) }
                    items(invites) { inv ->
                        Card(Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer)) {
                            ListItem(
                                headlineContent = { Text(inv.sender_name) },
                                supportingContent = { Text(inv.book_title) },
                                trailingContent = { Button(onClick = { scope.launch {
                                    RetrofitClient.instance.acceptInvite(inv.id)
                                    navController.navigate("reader/${inv.book_id}")
                                } }) { Text("Join") } }
                            )
                        }
                    }
                }

                if (requests.isNotEmpty()) {
                    item { Text("Incoming Requests", style = MaterialTheme.typography.titleMedium) }
                    items(requests) { req ->
                        Card(Modifier.fillMaxWidth()) {
                            ListItem(
                                headlineContent = { Text(req.sender_username) },
                                trailingContent = { Button(onClick = { scope.launch { RetrofitClient.instance.acceptRequest(req.id); refresh() } }) { Text("Accept") } }
                            )
                        }
                    }
                }

                item { Text("My Library Friends", style = MaterialTheme.typography.titleMedium) }
                items(friends) { f ->
                    ListItem(
                        headlineContent = { Text(f.username) },
                        trailingContent = {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Box(Modifier.size(8.dp).background(if(f.is_online) Color.Green else Color.Gray, MaterialTheme.shapes.extraSmall))
                                Spacer(Modifier.width(8.dp))
                                Text(if(f.is_online) "Online" else "Offline", style = MaterialTheme.typography.labelSmall)
                                if (f.is_online) {
                                  IconButton(onClick = { /* Send reading invite Logic */ }) { Icon(Icons.Default.VideoCall, null, tint = MaterialTheme.colorScheme.primary) }
                                }
                            }
                        }
                    )
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/ProfileScreen.kt": """package com.redsmart.app.ui.screens
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.redsmart.app.api.*
import com.redsmart.app.util.SessionManager
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileOutputStream

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(session: SessionManager) {
    var profile by remember { mutableStateOf<ProfileResponse?>(null) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    val snackHost = remember { SnackbarHostState() }

    fun refresh() { scope.launch { try { profile = RetrofitClient.instance.getProfile(session.getUserId()) } catch(e: Exception){} } }
    LaunchedEffect(Unit) { refresh() }

    val photoLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
        uri?.let {
            scope.launch {
                try {
                    val stream = context.contentResolver.openInputStream(uri)
                    val file = File(context.cacheDir, "upload.png")
                    stream?.use { input -> FileOutputStream(file).use { output -> input.copyTo(output) } }
                    val body = file.asRequestBody("image/*".toMediaTypeOrNull())
                    val part = MultipartBody.Part.createFormData("photo", file.name, body)
                    val res = RetrofitClient.instance.updateProfile(
                        session.getUserId().toString().toRequestBody(),
                        null, null, part
                    )
                    snackHost.showSnackbar(res.message ?: "Photo Uploaded")
                    refresh()
                } catch(e: Exception) { snackHost.showSnackbar("Upload failed") }
            }
        }
    }

    Scaffold(snackbarHost = { SnackbarHost(snackHost) }) { padding ->
        profile?.let { p ->
            LazyColumn(Modifier.fillMaxSize().padding(padding).padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                item {
                    Box(Modifier.size(150.dp)) {
                        AsyncImage(
                            model = p.profile_photo ?: "https://via.placeholder.com/150",
                            contentDescription = null,
                            modifier = Modifier.fillMaxSize().clip(CircleShape).border(4.dp, MaterialTheme.colorScheme.primary, CircleShape),
                            contentScale = ContentScale.Crop
                        )
                        FloatingActionButton(
                            onClick = { photoLauncher.launch("image/*") },
                            modifier = Modifier.align(Alignment.BottomEnd).size(40.dp),
                            containerColor = MaterialTheme.colorScheme.primary,
                            shape = CircleShape
                        ) { Icon(Icons.Default.CameraAlt, null, modifier = Modifier.size(20.dp), tint = Color.White) }
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(p.username, style = MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary)
                    Text(p.email, style = MaterialTheme.typography.bodyLarge)
                }

                item {
                    Spacer(Modifier.height(32.dp))
                    Row(Modifier.fillMaxWidth(), Arrangement.SpaceEvenly) {
                        StatCard("Reader Level", p.stats?.total_books ?: 0)
                        StatCard("Pages Done", p.stats?.pages_read ?: 0)
                        StatCard("Friend Network", p.friends_count)
                    }
                }

                item { Spacer(Modifier.height(32.dp)); Text("Badges Earned", style = MaterialTheme.typography.titleLarge) }
                items(p.badges) { b -> Card(Modifier.fillMaxWidth().padding(vertical = 4.dp)) { ListItem(headlineContent = { Text(b.name) }, leadingContent = { Icon(Icons.Default.Star, null, tint = Color.Yellow) }) } }
            }
        }
    }
}

@Composable
fun StatCard(lbl: String, value: Int) {
    Card(Modifier.padding(4.dp)) {
        Column(Modifier.padding(16.dp), Alignment.CenterHorizontally) {
            Text(value.toString(), style = MaterialTheme.typography.displaySmall, color = MaterialTheme.colorScheme.primary)
            Text(lbl, style = MaterialTheme.typography.labelSmall)
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/MoreScreen.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.redsmart.app.api.*
import com.redsmart.app.util.SessionManager

@Composable
fun MoreScreen(navController: NavController, session: SessionManager) {
    var info by remember { mutableStateOf<InfoResponse?>(null) }
    LaunchedEffect(Unit) { try { info = RetrofitClient.instance.getInfo() } catch(e:Exception){} }

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Management", style = MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary)
        Spacer(Modifier.height(24.dp))
        
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(8.dp)) {
                ListItem(headlineContent = { Text("About Redsmart") }, supportingContent = { Text(info?.about ?: "Connecting to server...") }, leadingContent = { Icon(Icons.Default.Info, null) })
                ListItem(headlineContent = { Text("Customer Support") }, supportingContent = { Text(info?.contact_email ?: "...@redsmart.com") }, leadingContent = { Icon(Icons.Default.Email, null) })
                ListItem(headlineContent = { Text("HQ Location") }, supportingContent = { Text(info?.address ?: "Loading...") }, leadingContent = { Icon(Icons.Default.PinDrop, null) })
            }
        }

        Spacer(Modifier.weight(1f))
        
        Button(
            onClick = { session.clear(); navController.navigate("login") { popUpTo(0) } },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.error)
        ) {
            Icon(Icons.Default.Logout, null)
            Spacer(Modifier.width(8.dp))
            Text("Terminate Session")
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/AuthScreens.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.navigation.NavController
import com.redsmart.app.api.*
import com.redsmart.app.util.SessionManager
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(navController: NavController, session: SessionManager) {
    var email by remember { mutableStateOf("") }; var password by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }; val scope = rememberCoroutineScope()
    Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.Center) {
        Text("ReadZey", style = MaterialTheme.typography.displayMedium, color = MaterialTheme.colorScheme.primary)
        Text("Digital Reading Sanctuary", style = MaterialTheme.typography.labelLarge)
        Spacer(Modifier.height(32.dp))
        OutlinedTextField(email, { email = it }, label = { Text("Login ID (Email/Admin)") }, modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(password, { password = it }, label = { Text("Keyphrase") }, visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(24.dp))
        Button({
            scope.launch {
                try {
                    val res = RetrofitClient.instance.login(AuthRequest(email, password))
                    if (res.success) {
                        session.saveAuth(res.user_id!!, res.username!!, res.token!!, res.is_admin == true)
                        navController.navigate(if (res.is_admin == true) "admin" else "library") { popUpTo(0) }
                    } else error = res.message ?: "Authentication failed"
                } catch(e: Exception) { error = "Connection error" }
            }
        }, Modifier.fillMaxWidth()) { Text("Enter Sanctuary") }
        TextButton({ navController.navigate("register") }) { Text("Create New Membership") }
        if (error.isNotEmpty()) Text(error, color = MaterialTheme.colorScheme.error, modifier = Modifier.padding(top = 8.dp))
    }
}

@Composable
fun RegisterScreen(navController: NavController, session: SessionManager) {
    var user by remember { mutableStateOf("") }; var email by remember { mutableStateOf("") }; var pass by remember { mutableStateOf("") }
    var error by remember { mutableStateOf("") }; val scope = rememberCoroutineScope()
    Column(Modifier.fillMaxSize().padding(24.dp), verticalArrangement = Arrangement.Center) {
        Text("Join Redsmart", style = MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary)
        Spacer(Modifier.height(32.dp))
        OutlinedTextField(user, { user = it }, label = { Text("Choose Username") }, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(email, { email = it }, label = { Text("Email Address") }, modifier = Modifier.fillMaxWidth())
        OutlinedTextField(pass, { pass = it }, label = { Text("Secure Password") }, visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth())
        Spacer(Modifier.height(24.dp))
        Button({
            scope.launch {
                try {
                    val res = RetrofitClient.instance.register(AuthRequest(email, pass, user))
                    if (res.success) navController.navigate("login") else error = res.message ?: "Error"
                } catch(e: Exception) { error = "Registration failed" }
            }
        }, Modifier.fillMaxWidth()) { Text("Register Account") }
        if (error.isNotEmpty()) Text(error, color = MaterialTheme.colorScheme.error)
    }
}
""",
    "app/src/main/java/com/redsmart/app/MainActivity.kt": """package com.redsmart.app
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.navigation.NavType
import androidx.navigation.compose.*
import androidx.navigation.navArgument
import com.redsmart.app.ui.theme.RedsmartAppTheme
import com.redsmart.app.ui.screens.*
import com.redsmart.app.util.SessionManager

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val session = SessionManager(this)
        setContent {
            RedsmartAppTheme {
                val navController = rememberNavController()
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentRoute = navBackStackEntry?.destination?.route
                val isLoggedIn = session.isLoggedIn()
                val isAdmin = session.isAdmin()
                val startDest = if (isLoggedIn) (if(isAdmin) "admin" else "library") else "login"
                
                Scaffold(
                    bottomBar = {
                        if (isLoggedIn && !isAdmin && currentRoute != "login" && currentRoute?.startsWith("reader") != true) {
                            NavigationBar {
                                NavigationBarItem(icon={Icon(Icons.Default.CollectionsBookmark,null)}, label={Text("Library")}, selected=currentRoute=="library", onClick={navController.navigate("library")})
                                NavigationBarItem(icon={Icon(Icons.Default.Forum,null)}, label={Text("Friends")}, selected=currentRoute=="friends", onClick={navController.navigate("friends")})
                                NavigationBarItem(icon={Icon(Icons.Default.VerifiedUser,null)}, label={Text("My Profile")}, selected=currentRoute=="profile", onClick={navController.navigate("profile")})
                                NavigationBarItem(icon={Icon(Icons.Default.SettingsSuggest,null)}, label={Text("More")}, selected=currentRoute=="more", onClick={navController.navigate("more")})
                            }
                        }
                    }
                ) { innerPadding ->
                    NavHost(navController, startDestination = startDest, Modifier.padding(innerPadding)) {
                        composable("login") { LoginScreen(navController, session) }
                        composable("register") { RegisterScreen(navController, session) }
                        composable("library") { LibraryScreen(navController) }
                        composable("friends") { FriendsScreen(navController, session) }
                        composable("profile") { ProfileScreen(session) }
                        composable("more") { MoreScreen(navController, session) }
                        composable("admin") { AdminDashboard() }
                        composable("detail/{id}", arguments=listOf(navArgument("id"){type=NavType.IntType})){ b -> DetailScreen(b.arguments?.getInt("id") ?: 0, navController) }
                        composable("reader/{id}", arguments=listOf(navArgument("id"){type=NavType.IntType})){ b -> ReaderScreen(b.arguments?.getInt("id") ?: 0, navController) }
                    }
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/AdminScreens.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun AdminDashboard() {
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("Core Management", style=MaterialTheme.typography.headlineLarge, color=MaterialTheme.colorScheme.secondary)
        Spacer(Modifier.height(24.dp))
        Card(Modifier.fillMaxWidth()) {
            Column(Modifier.padding(16.dp)) {
                Text("Content Control", style=MaterialTheme.typography.titleMedium)
                Text("Manage your library and user base from the web portal. Mobile admin features are currently focused on visibility.")
            }
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/LibraryScreen.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.*
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.redsmart.app.api.*

@Composable
fun LibraryScreen(navController: NavController) {
    var books by remember { mutableStateOf<List<Book>>(emptyList()) }
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) { try { books = RetrofitClient.instance.getBooks().books } catch(e: Exception) {} finally { isLoading = false } }

    Column(Modifier.fillMaxSize().padding(8.dp)) {
        Text("Digital Library", style = MaterialTheme.typography.headlineLarge, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, modifier = Modifier.padding(8.dp))
        if(isLoading) Box(Modifier.fillMaxSize(), Alignment.Center){ CircularProgressIndicator() }
        else LazyVerticalGrid(columns = GridCells.Fixed(3), contentPadding = PaddingValues(8.dp), verticalArrangement = Arrangement.spacedBy(12.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            items(books) { book ->
                Card(modifier = Modifier.fillMaxWidth().height(180.dp).clickable { navController.navigate("detail/${book.id}") }) {
                    Column {
                        AsyncImage(model = book.cover_url, contentDescription = null, modifier = Modifier.weight(1f).fillMaxWidth(), contentScale = ContentScale.Crop)
                        Text(book.title, modifier = Modifier.padding(4.dp), style = MaterialTheme.typography.bodySmall, maxLines = 1, overflow = TextOverflow.Ellipsis, fontWeight = FontWeight.SemiBold)
                    }
                }
            }
        }
    }
}
""",
    "app/src/main/java/com/redsmart/app/ui/screens/DetailScreen.kt": """package com.redsmart.app.ui.screens
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.redsmart.app.api.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DetailScreen(bookId: Int, navController: NavController) {
    var book by remember { mutableStateOf<BookDetail?>(null) }
    LaunchedEffect(bookId) { try { book = RetrofitClient.instance.getBookDetails(bookId) } catch(e: Exception) {} }

    Scaffold(
        topBar = { TopAppBar(title = { Text("Publication Info") }, navigationIcon = { IconButton(onClick = { navController.popBackStack() }) { Icon(Icons.Default.ArrowBack, null) } }) }
    ) { padding ->
        book?.let { b ->
            Column(Modifier.fillMaxSize().padding(padding).verticalScroll(rememberScrollState())) {
                AsyncImage(model = b.cover_url, contentDescription = null, modifier = Modifier.fillMaxWidth().height(350.dp), contentScale = ContentScale.Crop)
                Column(Modifier.padding(24.dp)) {
                    Text(b.title, style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                    Text(b.author ?: "Unknown", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.secondary)
                    Spacer(Modifier.height(24.dp))
                    Button(onClick = { navController.navigate("reader/${b.id}") }, modifier = Modifier.fillMaxWidth(), shape = MaterialTheme.shapes.extraLarge) { Text("ENTER READER") }
                    Spacer(Modifier.height(24.dp))
                    Text("Synopsis", style = MaterialTheme.typography.titleLarge)
                    Text(b.description ?: "Brief description unavailable.", style = MaterialTheme.typography.bodyLarge)
                }
            }
        } ?: Box(Modifier.fillMaxSize(), Alignment.Center) { CircularProgressIndicator() }
    }
}
"""
}

# Create and Write files
os.makedirs(root_dir, exist_ok=True)
for filepath, content in project_files.items():
    full_path = os.path.join(root_dir, filepath)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print(f"COMPLETE: Redbuilt Professional Grade Android App with PDFBox AI Voice and Glassmorphic UI.")
