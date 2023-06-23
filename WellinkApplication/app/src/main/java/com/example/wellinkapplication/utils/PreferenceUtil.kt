package com.example.wellinkapplication.utils

import android.content.Context
import android.content.SharedPreferences

class PreferenceUtil(context: Context) {
    private val PREFERENCE_NAME = "prefs_name"
    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREFERENCE_NAME, Context.MODE_PRIVATE)
    private val editor: SharedPreferences.Editor =
        prefs.edit()

    fun setPref(key: String, value: String) {
        editor.putString(key, value).apply()
    }

    fun getPref(key:String): String? {
        return prefs.getString(key, null)
    }
}