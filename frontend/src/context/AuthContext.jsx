import {createContext, useContext, useState} from "react";
import {useAuth} from "../hooks/auth.js";

const AuthContext = createContext(null)

export function AuthProvider({ children }) {

    const {login, accessToken} = useAuth()

    const authValue = {
        login,
        accessToken
    }

    return (
        <AuthContext.Provider value={authValue}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuthContext = () => {
    const ctx = useContext(AuthContext)
    if(!ctx) throw new Error("useAuth must be used inside AuthProvider")
    return ctx
}