package com.example.wellinkapplication.utils

import android.annotation.SuppressLint
import android.app.Activity
import android.util.Log
import com.example.wellinkapplication.retrofit.RetrofitManager
import com.example.wellinkapplication.utils.Constants.TAG
import com.example.wellinkapplication.utils.Loading.Companion.loadingEnd
import com.healthall.phrbluetoothlibrary.BLEDeviceHelper.*
import com.healthall.phrbluetoothlibrary.PillCalendarProtocols
import org.json.JSONArray
import java.util.*


class BleConnector {
    companion object {
        val instance = BleConnector()

        @SuppressLint("StaticFieldLeak")
        val mBleDeviceHelper = getInstance()
        lateinit var mBleDeviceConnectionCallback: BLEDeviceConnectionCallback
        lateinit var mBleDeviceCallback: BLEDeviceCallback
        lateinit var mBleDeviceSendDataCallback: BLEDeviceSendDataCallback
        var rawStringList = mutableListOf<String>()

        fun BLEsendData(sendData: String) {
            mBleDeviceHelper.sendData(sendData, object : BLEDeviceSendDataCallback {
                override fun isSucceeded() {
                    Log.d(TAG, "복약 캘린더와 통신 성공")
                }
                override fun isFailed() {
                    Log.d(TAG, "복약 캘린더와 통신 실패")
                }
            })
        }

    }


    fun init(mActivity:Activity) {
        mBleDeviceSendDataCallback = object : BLEDeviceSendDataCallback {
            override fun isSucceeded() {
            }

            override fun isFailed() {
            }
        }

        mBleDeviceConnectionCallback =
            object : BLEDeviceConnectionCallback {
                override fun isSucceeded() {
                    //연결성공
                    Log.d(TAG, "mBleDeviceConnectionCallback is succeeded")
                }

                override fun isFailed() {
                    //연결실패
                    Log.d(TAG, "mBleDeviceConnectionCallback is failed")
                }
            }

        mBleDeviceCallback = object : BLEDeviceCallback {
            override fun gattConnected() {
                //gatt 연결됨
                Log.d(TAG, "gattConnected")
                val pillCalendarProtocols = PillCalendarProtocols()
                val calendar: Calendar = Calendar.getInstance()
                val sendData = pillCalendarProtocols.setCurrentTime(calendar)
                Log.d(TAG, "PillCalendar value : $sendData")
                mBleDeviceHelper.sendData(sendData, object : BLEDeviceSendDataCallback {
                    override fun isSucceeded() {
                        //전송성공
                        Log.d(TAG, "isSucceeded")
                    }

                    override fun isFailed() {
                        //전송실패
                        Log.d(TAG, "isFailed")
                    }
                })
            }

            override fun gattDisconnected() {
                //gatt 연결 끊김
                Log.d(TAG, "gattDisconnected")
            }

            override fun gattServicesDiscovered() {
                //Service 발견
                Log.d(TAG, "gattServicesDiscovered")
            }

            override fun dataAvailable(result: String) {
                //통신성공 - 데이터수신
                Log.d(TAG, "callback result $result")
                if(result.get(0) == '[') {
                    Log.d(TAG, "복약 정보 데이터 수신")
                    val rawStringSet = mutableSetOf<String>()
                    val jsonArray = JSONArray(result)
                    for (i in 0 until jsonArray.length()) {
                        val jsonObject = jsonArray.getJSONObject(i)
                        rawStringSet.add(jsonObject.getString("rawString").substring(5))
                    }
                    rawStringList.clear()
                    rawStringList = rawStringSet.toMutableList()
                    rawStringList.removeLast()
                    Log.d(TAG, "dataAvailable: set 객수 ${rawStringSet.size}")
                    for (i in 0 until rawStringList.size) {
                        Log.d(TAG, "$i       ${rawStringList[i]}")
                    }
                    RetrofitManager.instance.modifyInfoCalendar(LoginedUserData.uid, rawStringList, completion = {
                            completionResponse, s ->
                        when(completionResponse) {
                            CompletionResponse.OK -> {
                                Log.d(TAG, "dataAvailable:캘린더 데이터 전송 성공")
                            }
                            CompletionResponse.FAIL -> {
                                Log.d(TAG, "dataAvailable:캘린더 데이터 전송 실패")
                            }
                        }
                    })
                }
            }
        }
        mBleDeviceHelper.initBluetooth(mActivity);
        mBleDeviceHelper.setBleDeviceCallback(mBleDeviceCallback);
        mBleDeviceHelper.connectWithDevice(BLEDevice.PILLCALENDAR_HANA, true, mBleDeviceConnectionCallback)
    }
}