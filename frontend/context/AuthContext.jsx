import {createContext, useContext, useState} from "react";

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [accessToken, setAccessToken] = useState(null)

    return (
        <AuthContext.Provider value={{ accessToken, setAccessToken }}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => {
    const ctx = useContext(AuthContext)
    if(!ctx) throw new Error("useAuth must be used inside AuthProvider")
    return ctx
}