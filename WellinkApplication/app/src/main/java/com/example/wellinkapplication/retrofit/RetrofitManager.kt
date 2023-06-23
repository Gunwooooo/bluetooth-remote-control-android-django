package com.example.wellinkapplication.retrofit

import android.app.Activity
import android.util.Log
import com.example.wellinkapplication.utils.API.BASE_URL
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.Constants.TAG
import com.example.wellinkapplication.utils.LoginedUserData
import com.google.gson.JsonElement
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class RetrofitManager {

    companion object{
        val instance = RetrofitManager()
    }

    private val iRetrofit: IRetrofit? = RetrofitClient.getClient(BASE_URL)?.create(IRetrofit::class.java)

    fun joinUser(user: User, completion: (CompletionResponse, String) -> Unit){
        val call = iRetrofit?.joinUser(user.uid, user.password, user.name, user.protector_check, user.protector_id) ?: return

        call.enqueue(object: Callback<JsonElement>{
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "RetrofitManager - onFailure: ");
                completion(CompletionResponse.FAIL, t.toString())
            }

            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                Log.d(TAG, "RetrofitManager - onResponse: ${response.body()} ");
                Log.d(TAG, "RetrofitManager - onResponse: status code is ${response.code()}");
                if(response.code() != 201){
                    completion(CompletionResponse.FAIL, response.body().toString())
                }else{
                    completion(CompletionResponse.OK, response.body().toString())
                }
            }
        })
    }

    fun loginUser(uid:String, password:String, loginProtectorCheck:Int, completion: (CompletionResponse, String) -> Unit){
        val call = iRetrofit?.loginUser(uid, password) ?: return
        call.enqueue(object: Callback<TokenUser>{
            override fun onFailure(call: Call<TokenUser>, t: Throwable) {
                Log.d(TAG, "RetrofitManager - onFailure: ");
                completion(CompletionResponse.FAIL, t.toString())
            }
            override fun onResponse(call: Call<TokenUser>, response: Response<TokenUser>) {
                Log.d(TAG, "RetrofitManager - onResponse: ${response.body()} ");
                Log.d(TAG, "RetrofitManager - onResponse: status code is ${response.code()}");
                if((response.code() != 200) ||
                    (loginProtectorCheck == 1 && response.body()?.protector_check == false) ||
                    (loginProtectorCheck == 0 && response.body()?.protector_check == true)){
                    completion(CompletionResponse.FAIL, response.body().toString())
                }else{
                    LoginedUserData.token = response.body()?.token!!
                    LoginedUserData.uid = response.body()?.uid!!
                    completion(CompletionResponse.OK, response.body().toString())
                }
            }
        })
    }

    fun infoUser(completion: (CompletionResponse, String) -> Unit){
        val token = LoginedUserData.token
        val uid = LoginedUserData.uid
        if(token.isBlank() || uid.isBlank()) {
            return
        }
        val call = iRetrofit?.infoUser(token, uid) ?: return
        call.enqueue(object: Callback<User>{
            override fun onFailure(call: Call<User>, t: Throwable) {
                Log.d(TAG, "RetrofitManager - onFailure: ");
                completion(CompletionResponse.FAIL, t.toString())
            }

            override fun onResponse(call: Call<User>, response: Response<User>) {
                Log.d(TAG, "RetrofitManager - onResponse: ${response.body()} ");
                Log.d(TAG, "RetrofitManager - onResponse: status code is ${response.code()}");
                if(response.code() != 200){
                    completion(CompletionResponse.FAIL, response.body().toString())
                }else{
                    LoginedUserData.name = response.body()?.name!!
                    LoginedUserData.protector_check = response.body()?.protector_check!!
                    LoginedUserData.protector_id = response.body()?.protector_id!!
                    completion(CompletionResponse.OK, response.body().toString())
                }
            }
        })
    }

    fun duplicateCheckUser(uid:String, completion: (CompletionResponse, String) -> Unit){
        val call = iRetrofit?.duplicateCheckUser(uid) ?: return

        call.enqueue(object: Callback<JsonElement>{
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "RetrofitManager - onFailure: ");
                completion(CompletionResponse.FAIL, t.toString())
            }

            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                Log.d(TAG, "RetrofitManager - onResponse: ${response.body()} ");
                Log.d(TAG, "RetrofitManager - onResponse: status code is ${response.code()}");
                if(response.code() != 200) {
                    completion(CompletionResponse.FAIL, response.body()!!.asJsonObject["duplicate"].toString())
                }else {
                    completion(CompletionResponse.OK, response.body()!!.asJsonObject["duplicate"].toString())
                }
            }
        })
    }

    fun protectorInquireUser(uid:String, completion: (CompletionResponse, String) -> Unit){
        val call = iRetrofit?.protectorInquireUser(uid) ?: return

        call.enqueue(object: Callback<JsonElement>{
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "RetrofitManager - onFailure: ");
                completion(CompletionResponse.FAIL, t.toString())
            }

            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                Log.d(TAG, "RetrofitManager - onResponse: ${response.body()} ");
                Log.d(TAG, "RetrofitManager - onResponse: status code is ${response.code()}");
                if(response.code() != 201) {
                    completion(CompletionResponse.FAIL, response.body().toString())
                }else {
                    completion(CompletionResponse.OK, response.body()!!.asJsonObject["protector_name"].toString())
                }
            }
        })
    }

    fun modifyInfoUser(uid: String, name: String, protector: String, completion: (CompletionResponse, String) -> Unit) {
        val call = iRetrofit?.modifyInfoUser(uid, name, protector) ?: return
        call.enqueue(object: Callback<JsonElement> {
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.FAIL, response.body().toString())
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                completion(CompletionResponse.OK, t.toString())
            }
        })
    }
    /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    fun localHospital(x:Double, y:Double, completion: (CompletionResponse, JsonElement) -> Unit) {
        val call = iRetrofit?.localHospital(x, y) ?: return
        call.enqueue(object: Callback<JsonElement>{
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.OK, response.body()!!)
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "onResponse: $t")
            }
        })
    }
    fun localPharmacy(x:Double, y:Double, completion: (CompletionResponse, JsonElement) -> Unit) {
        val call = iRetrofit?.localPharmacy(x, y) ?: return
        call.enqueue(object: Callback<JsonElement>{
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.OK, response.body()!!)
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "onResponse: $t")
            }
        })
    }
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    fun modifyInfoAlarm(uid: String, alarm: Alarm, completion: (CompletionResponse, String) -> Unit) {
        val call = iRetrofit?.modifyInfoAlarm(uid, alarm.morning, alarm.afternoon, alarm.evening, alarm.morning_switch, alarm.afternoon_switch, alarm.evening_switch) ?: return
        call.enqueue(object: Callback<JsonElement> {
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.FAIL, response.body().toString())
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                completion(CompletionResponse.OK, t.toString())
            }
        })
    }
    fun infoAlarm(uid: String, completion: (CompletionResponse, Alarm) -> Unit) {
        val call = iRetrofit?.infoAlarm(uid) ?: return
        call.enqueue(object: Callback<Alarm> {
            override fun onResponse(call: Call<Alarm>, response: Response<Alarm>) {
                Log.d(TAG, "onResponse: @@@@@@@@@@@@")
                Log.d(TAG, "onResponse: ${response.body()}")
                if(response.code() == 200) {
                    completion(CompletionResponse.OK, response.body()!!)
                } else
                    completion(CompletionResponse.OK, Alarm("00 : 00", "00 : 00", "00 : 00", false, false, false))
            }
            override fun onFailure(call: Call<Alarm>, t: Throwable) {
                Log.d(TAG, "onFailure: ")
            }
        })
    }
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    fun modifyInfoCalendar(uid: String, rawStringList: List<String>, completion: (CompletionResponse, String) -> Unit) {
        Log.d(TAG, "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&    ${rawStringList.size}")
        val call = iRetrofit?.modifyInfoCalendar(uid, rawStringList) ?: return
        call.enqueue(object: Callback<JsonElement> {
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.FAIL, response.body().toString())
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                completion(CompletionResponse.OK, t.toString())
            }
        })
    }
    fun infoCalendar(uid: String, completion: (CompletionResponse, JsonElement) -> Unit) {
        val call = iRetrofit?.infoCalendar(uid) ?: return
        call.enqueue(object: Callback<JsonElement> {
            override fun onResponse(call: Call<JsonElement>, response: Response<JsonElement>) {
                completion(CompletionResponse.OK, response.body()!!)
            }
            override fun onFailure(call: Call<JsonElement>, t: Throwable) {
                Log.d(TAG, "onResponse: $t")
            }
        })

    }
}

data class User(var uid: String, var password: String, var name: String, var protector_check: Boolean, var protector_id: String)
data class Alarm(var morning: String, var afternoon: String, var evening: String, var morning_switch: Boolean, var afternoon_switch: Boolean, var evening_switch: Boolean)
data class TokenUser(var token:String, var message:String, var uid:String, var protector_check: Boolean)