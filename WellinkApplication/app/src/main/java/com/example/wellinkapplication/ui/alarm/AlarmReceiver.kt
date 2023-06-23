package com.example.wellinkapplication.ui.alarm

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.os.Build.*
import android.util.Log
import androidx.core.app.NotificationCompat
import com.example.wellinkapplication.MenuActivity
import com.example.wellinkapplication.R

class AlarmReceiver: BroadcastReceiver() {
    companion object {
        const val TAG = "AlarmReceiver"
        const val NOTIFICATION_ID = 0
        const val PRIMARY_CHANNEL_ID = "primary_notification_channel"
    }

    lateinit var notificationManager: NotificationManager
    override fun onReceive(context: Context?, intent: Intent?) {
        Log.d(TAG, "알람 리시버 콜됨 -> 알람이 울립니다.")

        //////////////////
        //        val c = Calendar.getInstance()
        //        val q = c.get(Calendar.YEAR)
        //        val w = c.get(Calendar.MONTH) + 1
        //        val e = c.get(Calendar.DATE)
        //        val fm = String.format("%d%02d%02d", q, w, e)
        //블루투스 연결 확인 및 캘린더 스위치 이벤트 리스너 필요
        //리스너에 db에 같은 날짜 데이터 있으면 update 없으면 insert
        ////////////////
        notificationManager = context?.getSystemService(
            Context.NOTIFICATION_SERVICE) as NotificationManager

        createNotificationChannel()
        deliverNotification(context)
    }


    private fun createNotificationChannel() {
        if (VERSION.SDK_INT >= VERSION_CODES.O) {
            val notificationChannel = NotificationChannel(
                PRIMARY_CHANNEL_ID,
                "Stand up notification",
                NotificationManager.IMPORTANCE_HIGH
            )
            notificationChannel.enableLights(true)
            notificationChannel.lightColor = Color.RED
            notificationChannel.enableVibration(true)
            notificationChannel.description = "AlarmManager Tests"
            notificationManager.createNotificationChannel(
                notificationChannel)
        }
    }

    private fun deliverNotification(context: Context) {
        val contentIntent = Intent(context, MenuActivity::class.java)
        val contentPendingIntent = PendingIntent.getActivity(
            context,
            NOTIFICATION_ID,
            contentIntent,
            PendingIntent.FLAG_UPDATE_CURRENT
        )
        val builder =
            NotificationCompat.Builder(context, PRIMARY_CHANNEL_ID)
                .setSmallIcon(R.drawable.simple_icon)
                .setContentTitle("복약 캘린더")
                .setContentText("약 복용하실 시간입니다.")
                .setContentIntent(contentPendingIntent)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setAutoCancel(true)
                .setDefaults(NotificationCompat.DEFAULT_ALL)

        notificationManager.notify(NOTIFICATION_ID, builder.build())
    }


}