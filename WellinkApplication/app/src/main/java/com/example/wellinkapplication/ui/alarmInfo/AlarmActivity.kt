package com.example.wellinkapplication.ui.alarmInfo

import android.Manifest
import android.annotation.SuppressLint
import android.app.AlarmManager
import android.app.PendingIntent
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.CompoundButton
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.afollestad.materialdialogs.MaterialDialog
import com.akexorcist.snaptimepicker.SnapTimePickerDialog
import com.akexorcist.snaptimepicker.TimeValue
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.Alarm
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.ui.alarm.AlarmReceiver
import com.example.wellinkapplication.utils.BleConnector
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.LoginedUserData
import com.healthall.phrbluetoothlibrary.PillCalendarProtocols
import kotlinx.android.synthetic.main.activity_alarm.*
import java.util.*

class AlarmActivity : AppCompatActivity(), View.OnClickListener, CompoundButton.OnCheckedChangeListener {

    private lateinit var dialog: SnapTimePickerDialog
    val TAG: String = "로그"
    private var c = Calendar.getInstance()
    private var morning: String = "00 : 00"
    private var afternoon: String = "00 : 00"
    private var evening: String = "00 : 00"
    private var morning_switch = false
    private var afternoon_switch = false
    private var evening_switch = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_alarm)
        initView()
        getAlarmInfo()
    }

    private fun getBluetoothPermission() {
        val permissionCheck1 = this.let { ContextCompat.checkSelfPermission(it, Manifest.permission.BLUETOOTH) }
        val permissionCheck2 = this.let { ContextCompat.checkSelfPermission(it, Manifest.permission.BLUETOOTH_ADMIN) }
        if(permissionCheck1 == PackageManager.PERMISSION_GRANTED && permissionCheck2 == PackageManager.PERMISSION_GRANTED) {
            //블루투스 켜져있는지 확인
            val bleManager: BluetoothManager = this.applicationContext?.getSystemService(
                BLUETOOTH_SERVICE
            ) as BluetoothManager
            val bleAdapter = bleManager.adapter
            if(bleAdapter == null || !bleAdapter.isEnabled) {
                val dialog = MaterialDialog(this, MaterialDialog.DEFAULT_BEHAVIOR)
                dialog.title(null, "알림")
                dialog.message(null, "블루투스 사용 옵션이 꺼져있습니다.\n복약 캘린더를 이용하기 위해 블루투스 사용 옵션을 켜주세요.", null)
//                dialog.positiveButton(null, "설정") {
//                    startActivity(Intent(Settings.ACTION_BLUETOOTH_SETTINGS))
//                }
                dialog.negativeButton(null, "뒤로가기") {
                    val intent = Intent(this, MenuActivity::class.java)
                    startActivity(intent)
                }
                dialog.show()
            }
        }else{
            Toast.makeText(this, "블루투스 권한이 없습니다.", Toast.LENGTH_SHORT).show()
        }
    }

    //처음에 알람 시간 받아오기
    private fun getAlarmInfo() {
        RetrofitManager.instance.infoAlarm(LoginedUserData.uid, completion = { completionResponse, alarm ->
            when(completionResponse) {
                CompletionResponse.FAIL -> {
                    Log.d(TAG, "getAlarmInfo: 가져오기 실패")
                }
                CompletionResponse.OK -> {
                    morning = alarm.morning
                    afternoon = alarm.afternoon
                    evening = alarm.evening
                    morning_switch = alarm.morning_switch
                    afternoon_switch = alarm.afternoon_switch
                    evening_switch = alarm.evening_switch
                    Log.d(TAG, "getAlarmInfo: %^%^%^%^%^%^%^%^%^%^%^%^")
                    Log.d(TAG, "getAlarmInfo: $morning_switch     $afternoon_switch      $evening_switch")
                    switch_evening?.isChecked = evening_switch
                    switch_morning?.isChecked = morning_switch
                    switch_afternoon?.isChecked = afternoon_switch
                    btn_morning?.text = morning
                    btn_afternoon?.text = afternoon
                    btn_evening?.text = evening
                }
            }
        })
    }

    @RequiresApi(Build.VERSION_CODES.N)
    override fun onClick(v: View?) {
        when(v){
            home_btn_morning_on -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.setMorningAlarms(setCalendarTime(morning))
                BleConnector.BLEsendData(sendData)
                switch_morning?.isChecked = true
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_morning, true)

            }
            home_btn_morning_off -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.deleteMorningAlarms()
                BleConnector.BLEsendData(sendData)
                switch_morning?.isChecked = false
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_morning, false)

            }
            home_btn_afternoon_on -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.setNoonAlarms(setCalendarTime(afternoon))
                BleConnector.BLEsendData(sendData)
                switch_afternoon?.isChecked = true
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_afternoon, true)

            }
            home_btn_afternoon_off -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.deleteNoonAlarms()
                BleConnector.BLEsendData(sendData)
                switch_afternoon?.isChecked = false
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_afternoon, false)

            }
            home_btn_evening_on -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.setNightAlarms(setCalendarTime(evening))
                BleConnector.BLEsendData(sendData)
                switch_evening?.isChecked = true
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_evening, true)

            }
            home_btn_evening_off -> {
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.deleteNightAlarms()
                BleConnector.BLEsendData(sendData)
                switch_evening?.isChecked = false
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_evening, false)

            }
            home_btn_sync -> {
                //알림 시간 전송
                getBluetoothPermission()
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.setAlarmTimes(setCalendarTime(morning), setCalendarTime(afternoon), setCalendarTime(evening))
                BleConnector.BLEsendData(sendData)
                switch_morning?.isChecked = true
                switch_afternoon?.isChecked = true
                switch_evening?.isChecked = true
                modifyInfoAlarmRetrofit()
                onCheckedChanged(switch_morning, true)
                onCheckedChanged(switch_afternoon, true)
                onCheckedChanged(switch_evening, true)

            }
            btn_morning -> {
                dialog = makeDialog(R.string.title_morning, btn_morning, morning)
                dialog.show(supportFragmentManager, "morning")
            }
            btn_afternoon -> {
                dialog = makeDialog(R.string.title_afternoon, btn_afternoon, afternoon)
                dialog.show(supportFragmentManager, "afternoon")
            }
            btn_evening -> {
                dialog = makeDialog(R.string.title_evening, btn_evening, evening)
                dialog.show(supportFragmentManager, "evening")
            }
        }
    }
    //캘린더 시간 설정
    private fun setCalendarTime(time:String):Calendar {
        val calendarTime = Calendar.getInstance()
        val timePair: Pair<Int, Int> = makeStringTimeToInt(time)
        calendarTime.set(Calendar.HOUR_OF_DAY,timePair.first)
        calendarTime.set(Calendar.MINUTE,timePair.second)
        return calendarTime
    }

    //timePicker 컨트롤러
    private fun makeDialog(title : Int, btn : Button, key: String): SnapTimePickerDialog {
        val timePair: Pair<Int, Int> = makeStringTimeToInt(key)
        return SnapTimePickerDialog.Builder()
            .apply {
                setTitle(title)
                setPreselectedTime(TimeValue(timePair.first, timePair.second))
            }.build().apply {
                setListener { hour, minute ->
                    val timeFormat = String.format("%02d : %02d", hour, minute)
                    //DB 저장
                    when(btn) {
                        this@AlarmActivity.btn_morning -> {
                            morning = timeFormat
                            this@AlarmActivity.switch_morning?.isChecked = false
                            modifyInfoAlarmRetrofit()
                            onCheckedChanged(switch_morning, false)
                        }
                        this@AlarmActivity.btn_afternoon -> {
                            afternoon = timeFormat
                            this@AlarmActivity.switch_afternoon.isChecked = false
                            modifyInfoAlarmRetrofit()
                            onCheckedChanged(switch_afternoon, false)
                        }
                        this@AlarmActivity.btn_evening -> {
                            evening = timeFormat
                            this@AlarmActivity.switch_evening.isChecked = false
                            modifyInfoAlarmRetrofit()
                            onCheckedChanged(switch_evening, false)
                        }
                    }
                    btn.text = timeFormat
                }
            }
    }

    private fun modifyInfoAlarmRetrofit() {
        RetrofitManager.instance.modifyInfoAlarm(LoginedUserData.uid, Alarm(morning, afternoon, evening, switch_morning.isChecked, switch_afternoon.isChecked, switch_evening.isChecked), completion = {
                completionResponse, _ ->
            when(completionResponse) {
                CompletionResponse.OK -> {
                    Log.d(TAG, "makeDialog: 저장 완료")
                }
                CompletionResponse.FAIL -> {
                    Log.d(TAG, "makeDialog: 저장 실패")
                }
            }
        })
    }

    //스위치 컨트롤
    @RequiresApi(Build.VERSION_CODES.N)
    override fun onCheckedChanged(buttonView: CompoundButton?, isChecked: Boolean) {
        lateinit var timePair: Pair<Int, Int>
        when(buttonView) {
            switch_morning -> timePair = makeStringTimeToInt(morning)
            switch_afternoon -> timePair = makeStringTimeToInt(afternoon)
            switch_evening -> timePair = makeStringTimeToInt(evening)
        }

        //알람매니저 컨트롤
        val alarmManager = getSystemService(Context.ALARM_SERVICE) as AlarmManager
        val intent = Intent(this, AlarmReceiver::class.java)
        val pendingIntent = PendingIntent.getBroadcast(
            this, AlarmReceiver.NOTIFICATION_ID, intent,
            PendingIntent.FLAG_UPDATE_CURRENT)

        if(isChecked) {
            Log.d(TAG, "onCheckedChanged: ${timePair.first}    ${timePair.second}")
            //시간 정규화 하기
            c.set(Calendar.HOUR_OF_DAY, timePair.first)
            c.set(Calendar.MINUTE, timePair.second)
            if(c.before((Calendar.getInstance()))){
                c.add(Calendar.DATE, 1)
            }
            alarmManager.setExact(
                AlarmManager.RTC_WAKEUP,
                c.timeInMillis,
//                AlarmManager.INTERVAL_DAY,
                pendingIntent
            )
        } else {
            alarmManager.cancel(pendingIntent)
        }
    }

    //시간 Int로 바꾸기
    private fun makeStringTimeToInt(key: String) : Pair<Int, Int> {
        val hourTmp = key.substring(0, 2).toInt()
        val minuteTmp = key.substring(5, 7).toInt()
        return Pair(hourTmp, minuteTmp)
    }

    //처음 버튼 숫자 스위치 체크 설정 및 리스너 설정
    private fun initView() {
        btn_morning.setOnClickListener(this)
        btn_afternoon.setOnClickListener(this)
        btn_evening.setOnClickListener(this)
        switch_morning.setOnCheckedChangeListener(this)
        switch_afternoon.setOnCheckedChangeListener(this)
        switch_evening.setOnCheckedChangeListener(this)

        home_btn_sync.setOnClickListener(this)

        home_btn_morning_on.setOnClickListener(this)
        home_btn_afternoon_on.setOnClickListener(this)
        home_btn_evening_on.setOnClickListener(this)
        home_btn_morning_off.setOnClickListener(this)
        home_btn_afternoon_off.setOnClickListener(this)
        home_btn_evening_off.setOnClickListener(this)

        BleConnector.instance.init(this)
    }
}