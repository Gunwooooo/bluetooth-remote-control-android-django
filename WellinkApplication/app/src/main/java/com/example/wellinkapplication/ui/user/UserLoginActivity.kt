package com.example.wellinkapplication.ui.user

import android.app.AlarmManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.ui.alarm.AlarmReceiver
import com.example.wellinkapplication.utils.BleConnector
import com.example.wellinkapplication.utils.CompletionResponse
import com.healthall.phrbluetoothlibrary.BLEDeviceHelper
import com.healthall.phrbluetoothlibrary.PillCalendarProtocols
import com.shashank.sony.fancytoastlib.FancyToast
import kotlinx.android.synthetic.main.activity_user_login.*

class UserLoginActivity : AppCompatActivity(), View.OnClickListener {
    private val TAG = "토큰"
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_user_login)

        userlogin_btn_loginUser.setOnClickListener(this)
        userlogin_btn_joinUser.setOnClickListener(this)
    }

    override fun onClick(v: View?) {
        when(v) {
            userlogin_btn_loginUser -> {
                val uid: String = editText_userID.text.toString()
                val password: String = editText_userPassword.text.toString()
                Log.d(TAG, "onClick:  $uid    $password")
                RetrofitManager.instance.loginUser(uid, password, getIntent().extras!!.getInt("protectorCheck"), completion = {
                    completionResponse, response ->
                    when(completionResponse) {
                        CompletionResponse.FAIL -> {
                            Log.d("태그", "로그인 실패")
                            FancyToast.makeText(this, "잘못된 회원정보입니다.", Toast.LENGTH_LONG, FancyToast.WARNING,true).show()
                        }
                        CompletionResponse.OK -> {
                            Log.d("태그", "로그인 성공")
                            //알람 초기화
                            val alarmManager = getSystemService(Context.ALARM_SERVICE) as AlarmManager
                            val pendingIntent = PendingIntent.getBroadcast(this, AlarmReceiver.NOTIFICATION_ID, intent, PendingIntent.FLAG_UPDATE_CURRENT)
                            alarmManager.cancel(pendingIntent)

                            val intent = Intent(this, MenuActivity::class.java)
                            startActivity(intent)
                        }
                    }
                })
            }
            userlogin_btn_joinUser -> {
                val intent = Intent(this, UserJoinActivity::class.java)
                val flag:Int = getIntent().extras!!.getInt("protectorCheck")
                intent.putExtra("protectorCheck", flag)
                startActivity(intent)
            }
        }
    }
}