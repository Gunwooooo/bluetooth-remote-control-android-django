package com.example.wellinkapplication.utils

import android.app.Activity
import android.app.ProgressDialog
import android.os.Handler
import kotlinx.android.synthetic.main.activity_calendar.*


class Loading {
    companion object {
        private lateinit var progressDialog: ProgressDialog

        fun loading(activity: Activity) {
            //로딩
            run {
                progressDialog = ProgressDialog(activity)
                progressDialog.setIndeterminate(true)
                progressDialog.setMessage("잠시만 기다려 주세요")
                progressDialog.show()
            }
            Handler().postDelayed(
                {
                    progressDialog.dismiss()
                }, 500
            )
        }

        fun loadingCalendar(activity: Activity) {
            //로딩
            run {
                progressDialog = ProgressDialog(activity)
                progressDialog.setIndeterminate(true)
                progressDialog.setMessage("잠시만 기다려 주세요")
                progressDialog.show()
            }
            Handler().postDelayed(
                {
                    progressDialog.dismiss()
                }, 11000
            )
        }

        fun loadingEnd() {
            progressDialog.dismiss()
        }
    }
}
