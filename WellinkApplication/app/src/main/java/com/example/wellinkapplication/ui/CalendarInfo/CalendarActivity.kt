package com.example.wellinkapplication.ui.CalendarInfo

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.util.Log
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.core.content.ContextCompat
import com.afollestad.materialdialogs.MaterialDialog
import com.applandeo.materialcalendarview.EventDay
import com.applandeo.materialcalendarview.listeners.OnDayClickListener
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.utils.BleConnector
import com.example.wellinkapplication.utils.CompletionResponse
import com.example.wellinkapplication.utils.Loading
import com.example.wellinkapplication.utils.LoginedUserData
import com.healthall.phrbluetoothlibrary.PillCalendarProtocols
import kotlinx.android.synthetic.main.activity_calendar.*
import java.util.*

class CalendarActivity : AppCompatActivity(), OnDayClickListener, View.OnClickListener {

    private val TAG = "로그"
    private val mCalendar = Calendar.getInstance()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_calendar)

        mCalendar.set(Calendar.MONTH, mCalendar.get(Calendar.MONTH) + 1)
        calendarView.setOnDayClickListener(this)


        calendarView.setOnPreviousPageChangeListener {
            mCalendar.set(Calendar.MONTH, mCalendar.get(Calendar.MONTH) - 1)
            initCalendar()
        }
        calendarView.setOnForwardPageChangeListener {
            mCalendar.set(Calendar.MONTH, mCalendar.get(Calendar.MONTH) + 1)
            initCalendar()
        }

        getCalendarInfo()
        initView()
    }

    private fun getCalendarInfo() {
        RetrofitManager.instance.infoCalendar(LoginedUserData.uid, completion = {
                completionResponse, s ->
            when(completionResponse) {
                CompletionResponse.FAIL -> {
                    Log.d(TAG, "getAlarmInfo: 가져오기 실패")
                }
                CompletionResponse.OK -> {
                    val list = s.asJsonObject["rawStringList"].toString().replace(" ","").replace("[", "").replace("]", "").replace("\"","").replace("\\", "").split(',')
                    BleConnector.rawStringList = list.toMutableList()
                    initCalendar()
                }
            }
        })
    }


    private fun initView() {
        this.let { BleConnector.instance.init(it) }
        fab_reload.setOnClickListener(this)
    }

    @SuppressLint("SetTextI18n")
    override fun onDayClick(eventDay: EventDay?) {
        Log.d(TAG, "${eventDay?.calendar?.get(Calendar.YEAR)}   ${eventDay?.calendar?.get(Calendar.MONTH)?.plus(1)}   ${eventDay?.calendar?.get(
            Calendar.DATE
        )}")
        detail_calendar_title.visibility = View.GONE
        detail_calendar.visibility = View.VISIBLE
        val year = eventDay?.calendar?.get(Calendar.YEAR)
        val month = eventDay?.calendar?.get(Calendar.MONTH)?.plus(1)
        val day = eventDay?.calendar?.get(Calendar.DATE)
        calendar_textView_detail_day.text = "${year}.${month}.${day} 복용 정보"
        val timeFormat = String.format("%d%02d%02d", year, month, day).substring(2)
        var cnt = 0
        for(i in 0 until BleConnector.rawStringList.size) {
            if(BleConnector.rawStringList[i].length < 6) return
            if(BleConnector.rawStringList[i].substring(0, 6) == timeFormat) {
                cnt++
                when(cnt) {
                    1 -> {
                        calendar_textView_morning_time.text = String.format("%s : %s", BleConnector.rawStringList[i].substring(6, 8), BleConnector.rawStringList[i].substring(8, 10))
                        calendar_textView_morning.text = checkTakeMedicine(calendar_textView_morning, BleConnector.rawStringList[i].get(10))
                    }
                    2 -> {
                        calendar_textView_afternoon_time.text = String.format("%s : %s", BleConnector.rawStringList[i].substring(6, 8), BleConnector.rawStringList[i].substring(8, 10))
                        calendar_textView_afternoon.text = checkTakeMedicine(calendar_textView_afternoon, BleConnector.rawStringList[i].get(10))
                    }
                    3 -> {
                        calendar_textView_evening_time.text = String.format("%s : %s", BleConnector.rawStringList[i].substring(6, 8), BleConnector.rawStringList[i].substring(8, 10))
                        calendar_textView_evening.text = checkTakeMedicine(calendar_textView_evening, BleConnector.rawStringList[i].get(10))
                    }
                }
            }
        }
    }

    private fun checkTakeMedicine(v: TextView, c:Char):String {
        when(c) {
            '0' -> {
                v.setTextColor(Color.parseColor("#424242"))
                return "-"
            }
            '1' -> {
                v.setTextColor(Color.parseColor("#424242"))
                return "복용예정"
            }
            '2' -> {
                v.setTextColor(Color.parseColor("#31B404"))
                return "정상복용"
            }
            '3' -> {
                v.setTextColor(Color.parseColor("#FF4000"))
                return "미복용"
            }
        }
        return "-"
    }

    //캘린더 색깔 표시 메서드
    private fun initCalendar() {
        val events = arrayListOf<EventDay>()
        var dayCnt = 1
        var monthTmp = mCalendar.get(Calendar.MONTH)
        var yearTmp = mCalendar.get(Calendar.YEAR)
        if(mCalendar.get(Calendar.MONTH) == 0) {
            yearTmp--
            monthTmp = 12
        }
        while (32 != dayCnt) {
            var twoCnt = 0
            var threeCnt = 0
            val timeFormat = String.format("%d%02d%02d", yearTmp, monthTmp, dayCnt).substring(2)
            for (i in 0 until BleConnector.rawStringList.size) {
                if (BleConnector.rawStringList[i].length < 6) return
                if ((BleConnector.rawStringList[i].substring(0, 6) == timeFormat) && (BleConnector.rawStringList[i].get(10) == '2')) {
                    twoCnt++
                    continue
                }
                if ((BleConnector.rawStringList[i].substring(0, 6) == timeFormat) && (BleConnector.rawStringList[i].get(10) == '3')) {
                    threeCnt++
                    continue
                }
            }
            dayCnt++
            if(threeCnt == 1 || threeCnt == 2) {
                val calendar = Calendar.getInstance()
                calendar.set(yearTmp, monthTmp - 1, dayCnt - 1)
                events.add(EventDay(calendar, R.drawable.orange_circle))
                continue
            }
            if(threeCnt == 3) {
                val calendar = Calendar.getInstance()
                calendar.set(yearTmp, monthTmp - 1, dayCnt -1 )
                events.add(EventDay(calendar, R.drawable.red_circle))
                continue
            }
            if((twoCnt + threeCnt) == 0) {
                continue
            }
            if(threeCnt == 0) {
                val calendar = Calendar.getInstance()
                calendar.set(yearTmp, monthTmp - 1, dayCnt - 1)
                events.add(EventDay(calendar, R.drawable.green_circle))
                continue
            }
        }
        calendarView.setEvents(events)
    }

    override fun onClick(v: View?) {
        when(v) {
            fab_reload -> {
                getBluetoothPermission()
                this.let { Loading.loadingCalendar(it) }
                val pillCalendarProtocols = PillCalendarProtocols()
                val sendData = pillCalendarProtocols.allInfo
                BleConnector.BLEsendData(sendData)
                Handler().postDelayed(
                    {
                        finish()
                        startActivity(intent)
                    }, 11000
                )
            }
        }
    }
    private fun getBluetoothPermission() {
        val permissionCheck1 = this.let { ContextCompat.checkSelfPermission(it, Manifest.permission.BLUETOOTH) }
        val permissionCheck2 = this.let { ContextCompat.checkSelfPermission(it, Manifest.permission.BLUETOOTH_ADMIN) }
        if(permissionCheck1 == PackageManager.PERMISSION_GRANTED && permissionCheck2 == PackageManager.PERMISSION_GRANTED) {
            //블루투스 켜져있는지 확인
            val bleManager: BluetoothManager = this.applicationContext?.getSystemService(
                Context.BLUETOOTH_SERVICE
            ) as BluetoothManager
            val bleAdapter = bleManager.adapter
            if(bleAdapter == null || !bleAdapter.isEnabled) {
                val dialog = MaterialDialog(this, MaterialDialog.DEFAULT_BEHAVIOR)
                dialog.title(null, "알림")
                dialog.message(null, "블루투스 사용 옵션이 꺼져있습니다.\n복약 캘린더를 이용하기 위해 블루투스 사용 옵션을 켜주세요.", null)
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
}