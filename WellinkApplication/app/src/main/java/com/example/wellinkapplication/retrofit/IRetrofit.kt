package com.example.wellinkapplication.retrofit


import com.example.wellinkapplication.utils.API
import com.google.gson.JsonElement
import okhttp3.Response
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.http.*

interface IRetrofit {

    @FormUrlEncoded
    @POST(API.JOIN_USER)
    fun joinUser(
        @Field("uid") uid:String,
        @Field("password") password:String,
        @Field("name") name:String,
        @Field("protector_check") protector_check:Boolean,
        @Field("protector_id") protector_id:String,
    ): Call<JsonElement>

    @FormUrlEncoded
    @POST(API.LOGIN_USER)
    fun loginUser(
        @Field("uid") uid:String,
        @Field("password") password:String,
    ): Call<TokenUser>

    @GET(API.INFO_USER)
    fun infoUser(
        @Header("token") token:String,
        @Query("uid") uid:String,
    ): Call<User>

    @GET(API.DUPLICATE_CHECK_USER)
    fun duplicateCheckUser(
        @Query("uid") uid:String,
    ): Call<JsonElement>

    @GET(API.PROTECTOR_INQUIRE_USER)
    fun protectorInquireUser(
        @Query("uid") uid:String,
    ): Call<JsonElement>

    @FormUrlEncoded
    @PUT(API.MODIFY_INFO_USER)
    fun modifyInfoUser(
        @Field("uid") uid:String,
        @Field("name") name:String,
        @Field("protector") protector:String,
    ): Call<JsonElement>

    /////////////////////////////////////////////////////////////////
    @GET(API.LOCAL_HOSPITAL)
    fun localHospital(
        @Query("x") x:Double,
        @Query("y") y:Double,
    ): Call<JsonElement>

    @GET(API.LOCAL_PHARMACY)
    fun localPharmacy(
        @Query("x") x:Double,
        @Query("y") y:Double,
    ): Call<JsonElement>
    //////////////////////////////////////////////////////////////////
    @FormUrlEncoded
    @PUT(API.MODIFY_INFO_ALARM)
    fun modifyInfoAlarm(
        @Field("uid") uid:String,
        @Field("morning") morning:String,
        @Field("afternoon") afternoon:String,
        @Field("evening") evening:String,
        @Field("morning_switch") morning_switch:Boolean,
        @Field("afternoon_switch") afternoon_switch:Boolean,
        @Field("evening_switch") evening_switch:Boolean,
    ): Call<JsonElement>

    @GET(API.INFO_ALARM)
    fun infoAlarm(
        @Query("uid") uid:String,
    ): Call<Alarm>
    ////////////////////////////////////////////////////////////////////
    @FormUrlEncoded
    @PUT(API.MODIFY_INFO_CALENDAR)
    fun modifyInfoCalendar(
        @Field("uid") uid:String,
        @Field("rawStringList") rawStringList: List<String>,
    ): Call<JsonElement>

    @GET(API.INFO_CALENDAR)
    fun infoCalendar(
        @Query("uid") uid:String,
    ): Call<JsonElement>
}